// Read-only catalog/skill discovery. This does not launch a model turn.
import { spawn } from 'node:child_process';
import { createInterface } from 'node:readline';
const child = spawn('codex', ['app-server', '--stdio'], { stdio: ['pipe', 'pipe', 'pipe'] });
const pending = new Map();
let id = 0;
let stderr = '';
child.stderr.on('data', b => { stderr = (stderr + b).slice(-2000); });
createInterface({ input: child.stdout }).on('line', line => {
  let msg;
  try { msg = JSON.parse(line); } catch { return; }
  if (pending.has(msg.id)) {
    const { resolve, reject } = pending.get(msg.id);
    pending.delete(msg.id);
    msg.error ? reject(new Error(JSON.stringify(msg.error))) : resolve(msg.result);
  }
});
child.on('error', error => { for (const p of pending.values()) p.reject(error); });
child.on('exit', code => { for (const p of pending.values()) p.reject(new Error(`Codex exited ${code}: ${stderr}`)); });
function request(method, params) {
  return new Promise((resolve, reject) => {
    const requestId = ++id;
    pending.set(requestId, { resolve, reject });
    child.stdin.write(JSON.stringify({ id: requestId, method, params }) + '\n');
  });
}
const timeout = setTimeout(() => { child.kill(); }, 30000);
try {
  const init = await request('initialize', { clientInfo: { name: 'code_quality_review_probe', version: '1.0.0' }, capabilities: { experimentalApi: true } });
  child.stdin.write(JSON.stringify({ method: 'initialized' }) + '\n');
  const models = [];
  let cursor;
  do {
    const page = await request('model/list', { limit: 100, ...(cursor ? { cursor } : {}) });
    models.push(...page.data);
    cursor = page.nextCursor;
  } while (cursor);
  const skills = await request('skills/list', { cwds: [process.cwd()], forceReload: true });
  console.log(JSON.stringify({ observedAt: new Date().toISOString(), server: init, models: models.map(m => ({ id: m.id, model: m.model, description: m.description, supportedReasoningEfforts: m.supportedReasoningEfforts, defaultReasoningEffort: m.defaultReasoningEffort, serviceTiers: m.serviceTiers, defaultServiceTier: m.defaultServiceTier })), skill: skills.data?.flatMap(x => x.skills ?? []).filter(x => x.name === 'code-quality-review'), errors: skills.data?.flatMap(x => x.errors ?? []) }, null, 2));
} catch (error) {
  console.error(`Discovery failed: ${error.message}`);
  process.exitCode = 1;
} finally {
  clearTimeout(timeout);
  child.kill();
}
