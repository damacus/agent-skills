import { spawn } from 'node:child_process';
import { createInterface } from 'node:readline';
import { readFileSync, writeFileSync, appendFileSync, existsSync, accessSync, constants } from 'node:fs';
import path from 'node:path';
const [role, family, effort, cwdArg, promptFile, outputPrefix, sandbox = 'read-only', timeoutArg = '240'] = process.argv.slice(2);
if (!outputPrefix) throw new Error('usage: role family effort cwd prompt-file output-prefix [sandbox] [timeout-seconds]');
const timeoutSeconds = Number(timeoutArg);
if (!Number.isInteger(timeoutSeconds) || timeoutSeconds < 10 || timeoutSeconds > 3600) throw new Error('timeout-seconds must be an integer from 10 through 3600');
if (!['sol', 'astra'].includes(family)) throw new Error('family must be sol or astra');
if (!['read-only', 'workspace-write'].includes(sandbox)) throw new Error('sandbox must be read-only or workspace-write');
const cwd = path.resolve(cwdArg);
accessSync(path.dirname(path.resolve(outputPrefix)), constants.W_OK);
for (const suffix of ['.settings.json', '.events.json', '.events.jsonl', '.md']) {
  if (existsSync(outputPrefix + suffix)) throw new Error('Use a fresh output prefix; existing evidence must not be overwritten');
}
const child = spawn('codex', ['app-server', '--stdio', '-c', 'service_tier="default"'], { stdio: ['pipe', 'pipe', 'pipe'] });
const pending = new Map();
let nextId = 0;
let notifications = [];
let completionResolve;
let completionReject;
const completion = new Promise((r, j) => { completionResolve = r; completionReject = j; });
completion.catch(() => {});
let stderr = '';
child.stderr.on('data', b => { stderr = (stderr + b).slice(-4000); });
const send = msg => child.stdin.write(JSON.stringify(msg) + '\n');
function request(method, params) {
  return new Promise((resolve, reject) => {
    const id = ++nextId;
    pending.set(id, { resolve, reject });
    send({ id, method, params });
  });
}
createInterface({ input: child.stdout }).on('line', line => {
  let msg;
  try { msg = JSON.parse(line); } catch { return; }
  if (!msg.method && pending.has(msg.id)) {
    const p = pending.get(msg.id); pending.delete(msg.id);
    msg.error ? p.reject(new Error(JSON.stringify(msg.error))) : p.resolve(msg.result);
  } else if (msg.method) {
    notifications.push(msg);
    appendFileSync(outputPrefix + '.events.jsonl', JSON.stringify(msg) + '\n');
    if (msg.id !== undefined) send({ id: msg.id, error: { code: -32601, message: 'Interactive requests are not supported by this validation client' } });
    if (msg.method === 'turn/completed') completionResolve(msg.params);
  }
});
child.on('error', e => { for (const p of pending.values()) p.reject(e); completionReject(e); });
child.on('exit', code => { const e = new Error(`app-server exited ${code}: ${stderr}`); for (const p of pending.values()) p.reject(e); completionReject(e); });
const timer = setTimeout(() => { completionReject(new Error('Review session timeout')); child.kill(); }, timeoutSeconds * 1000);
try {
  await request('initialize', { clientInfo: { name: 'code_quality_review_validation', version: '1.0.0' }, capabilities: { experimentalApi: true } });
  send({ method: 'initialized' });
  const models = [];
  let cursor;
  do {
    const page = await request('model/list', { limit: 100, ...(cursor ? { cursor } : {}) });
    models.push(...page.data); cursor = page.nextCursor;
  } while (cursor);
  const candidates = models.filter(m => new RegExp(`^gpt-(\\d+)(?:\\.(\\d+))?-${family}$`).test(m.model) && !/older|previous|deprecated|retired|legacy|preview|beta/i.test(m.description));
  candidates.sort((a, b) => { const av=a.model.match(/\d+/g).map(Number),bv=b.model.match(/\d+/g).map(Number);return (bv[0]-av[0])||((bv[1]??0)-(av[1]??0)); });
  const selected = candidates[0];
  if (candidates[1]?.model === selected?.model) throw new Error('Ambiguous model inventory');
  if (!selected || (family === 'sol' && /^gpt-6(?:\.0)?-sol$/.test(selected.model))) throw new Error('No permitted model');
  if (!selected.supportedReasoningEfforts.some(x => x.reasoningEffort === effort)) throw new Error('Unsupported effort');
  const started = await request('thread/start', { model: selected.model, serviceTier: 'default', cwd, ephemeral: true, approvalPolicy: 'never', sandbox, config: { model_reasoning_effort: effort, service_tier: 'default' }, developerInstructions: 'You are a bounded code-quality reviewer. Do not spawn agents. Follow the supplied role brief and repository instructions. Keep the original target checkout read-only; all generated artifacts belong in the supplied scratch workspace. Use fish or Node for helpers, not Python. Do not call external messaging tools or publish anything.' });
  writeFileSync(outputPrefix + '.settings.json', JSON.stringify({ role, observedAt: new Date().toISOString(), selectedCatalog: { id: selected.id, model: selected.model, supportedReasoningEfforts: selected.supportedReasoningEfforts }, applied: started }, null, 2));
  if (started.model !== selected.model || started.reasoningEffort !== effort || started.serviceTier !== 'default') throw new Error('Applied settings do not match requested route; no turn launched');
  const expectedSandbox = sandbox === 'read-only' ? 'readOnly' : 'workspaceWrite';
  if (started.sandbox.type !== expectedSandbox) throw new Error('Applied sandbox does not match requested policy; no turn launched');
  console.log(JSON.stringify({ role, threadId: started.thread.id, model: started.model, effort: started.reasoningEffort, tier: started.serviceTier, sandbox: started.sandbox }));
  await request('turn/start', { threadId: started.thread.id, model: selected.model, effort, serviceTierForTurn: 'default', input: [{ type: 'text', text: readFileSync(promptFile, 'utf8') }] });
  const result = await completion;
  writeFileSync(outputPrefix + '.events.json', JSON.stringify(notifications, null, 2));
  if (result.turn.status !== 'completed') throw new Error(`Turn ${result.turn.status}: ${JSON.stringify(result.turn.error)}`);
  const messages = notifications.filter(n => n.method === 'item/completed' && n.params.item.type === 'agentMessage' && n.params.item.phase === 'final_answer').map(n => n.params.item.text);
  if (!messages.length) throw new Error('Completed turn produced no final answer');
  writeFileSync(outputPrefix + '.md', messages.join('\n\n'));
  console.log(JSON.stringify({ role, status: result.turn.status, output: outputPrefix + '.md', messageCount: messages.length }));
} catch (error) {
  writeFileSync(outputPrefix + '.events.json', JSON.stringify(notifications, null, 2));
  console.error(error.message); process.exitCode = 1;
} finally { clearTimeout(timer); child.kill(); }
