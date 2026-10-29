---
name: grilling
description: >-
  Investigate a plan and question unresolved decisions until the affected scope
  is understood. Use for grill, grill me, or an explicit request to challenge
  assumptions. Require evidence of coverage before ending the interview.
---

# Grilling

Reach a shared understanding without making the owner reconstruct facts that
the agent can discover. A short interview is sufficient only when the evidence
is sufficient. Question count and a general "yes" do not establish completeness.

## Investigate first

Read the request, existing decisions and relevant implementation. For an existing
product, inspect the running behaviour and tests where available. Record facts,
contradictions and unknowns in the existing brief. Keep assumptions labelled.
Use authorised help only when it saves more than briefing and coordination cost.

For migration work, apply `migrate` to identify the areas that must be examined.
For other work, identify the affected users, outcomes, constraints, dependencies,
failure states and acceptance evidence. Mark irrelevant areas with a reason.
Do not declare a question answered merely because the implementation seems easy.

## Ask in rounds

Ask a small coherent group of questions whose prerequisites are known. Give each
question a stable number, the evidence, your recommendation and its consequence.
Explain the work or risk that the answer changes. Do not bundle independent
decisions into a single yes/no question or word alternatives to invite agreement.

Wait for answers to decisions that block implementation. A yes applies only to
the explicit question or listed agreement. Silence, a timeout or an unrelated
answer is not approval. Reuse earlier answers unless evidence changes.

After each round, trace consequences before asking again. For example, permitting
removal of the last carer also raises questions about creating a dependent with
no carer, warnings and existing permissions. Investigate those effects; ask only
where the existing application or an earlier answer does not settle them.

Do not invent a new product policy to fill an implementation gap. Do not ask
about ordinary layout or behaviour already demonstrated by the reference app.
Use plain language; the owner should not need to translate internal architecture.

## Completion requires evidence

Before ending, check each affected area:

- What was inspected, and what does that evidence establish?
- What must remain unchanged?
- Which specific differences did the owner approve?
- What contradictions or consequential unknowns remain?
- How will execution demonstrate that the result meets the agreement?

Summarise facts, approved decisions and unresolved items separately in the same
brief. Include concrete examples where edge cases could change the outcome.
Check the summary against the original objective, not just questions you asked.
Ask the owner to confirm shared understanding before dependent implementation;
existing explicit confirmation remains valid for unchanged scope.

A broad approval does not approve unstated assumptions. Unresolved material
decisions keep the affected work pending; independent work may continue.
Do not keep questioning once the affected scope is evidenced and agreed.

## Relationship to other skills

`migrate` owns preservation evidence. `slice` decomposes an agreed outcome.
`team-planning` assigns resources only when a team is needed.
`adaptive-model-routing` owns model choice. This skill creates no standing team,
recurring timer, extra report or permission to broaden the task.

## Provenance

This is the damacus revision of the previously installed `grilling` workflow.
It retains rounds of dependent questions and replaces the implicit
"all branches visited" judgement with an explicit evidence check.
