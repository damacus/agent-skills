---
name: structure-codebase
description: >-
  Design, audit, and evolve repository, source, module, and package structures so real ownership,
  runtime, dependency, and change boundaries are easy to see and enforce. Use when deciding where
  code belongs; reorganizing flat or layer-first trees; structuring by feature, route, screen,
  command, workflow, use case, bounded context, or capability; evaluating DDD or ports-and-adapters
  placement; planning safe folder migrations; or reviewing package and import direction. Do not
  activate for ordinary file moves whose destination is already established by the repository.
---

# Structure Codebase

Design the source tree as a truthful map of meaning, ownership, runtime boundaries, and change cohesion. Do not start from a universal template. Select the lightest structure that makes this project's real seams easy to see and proportionately difficult to violate.

Use this skill for physical placement, package shape, migration, and dependency enforcement. Domain modeling and port or adapter implementation are separate concerns. If the repository has dedicated guidance for DDD or hexagonal architecture, follow it alongside this skill; never infer that adopting one pattern requires the other.

## Operating Guardrails

- Read the repository's instructions, architecture decisions, and framework conventions before proposing a new taxonomy.
- Preserve a coherent existing structure unless the user asked for redesign or evidence shows a concrete navigation, ownership, runtime, or dependency problem.
- Separate observations from proposals. Label inferred boundaries and unverified change-cohesion claims as hypotheses.
- For an audit or proposal, do not move files. For an implementation, preserve unrelated work and migrate in reviewable slices.
- Prefer project-native enforcement and verification over introducing new tooling solely to defend a diagram.

Read the relevant reference before producing a target tree:

- Read [`references/visible-hexagon.md`](references/visible-hexagon.md) for a ports-and-adapters backend, DDD plus hexagonal architecture, or questions about ports, test actors, read models, and package isolation.
- Read [`references/backend-patterns.md`](references/backend-patterns.md) for a BFF, ordinary feature-first service, framework-constrained backend, operational tool, CLI, or small package.
- Read [`references/frontend-patterns.md`](references/frontend-patterns.md) for a frontend, design system, client-side feature architecture, meta-framework UI, or full-stack request.
- Read [`references/enforcement-and-migration.md`](references/enforcement-and-migration.md) before moving existing code, changing package depth, or designing import/package enforcement.
- Read [`references/research-notes.md`](references/research-notes.md) when explaining named approaches or source rationale.

## Core Model

Read a well-structured codebase from broadest meaning to narrowest detail:

1. **Product or capability** — why the code exists and who owns it.
2. **Architectural boundary** — inside versus outside, but only when that boundary is real.
3. **Feature, domain concept, use case, workflow, or endpoint** — what changes together.
4. **Implementation detail** — framework, persistence, SDK, protocol, and small helpers.

Treat “screaming architecture” as a fitness question, not a folder taxonomy: can a newcomer tell what the system does? Technical names such as `hexagon`, `adapters`, `driving`, `driven`, and `composition` are useful at real seams. They are harmful only when they replace product meaning or claim boundaries that do not exist.

Folder names make claims. Packages, exports, imports, tests, and automated boundary rules prove them.

## Keep the Axes Distinct

| Axis | It answers | Do not confuse it with |
| ------ | ------------ | ------------------------ |
| Capability | Why does this code exist and change? | A technical layer |
| Bounded context | Where does language and model authority change? | A noun, table, team label, or folder of convenience |
| Hexagon | What policy must remain independently testable from external technology? | DDD, a generic `core`, or every pure library |
| Feature/use case | What behavior changes together? | A required package or bounded context |
| Endpoint | Where does a BFF request enter? | The owner of shared workflow state |
| Package/module | What boundary can tooling enforce? | A business boundary by itself |
| Composition root | Where is the runtime object graph constructed and owned? | A mandatory folder in every library |

## Workflow

### 1. Preserve the Requested Scope

Determine whether the user asked for an audit, proposal, migration plan, or implementation. Do not move files for a suggestion-only request. Do not broaden a folder change into a domain redesign without authorization.

### 2. Inspect Before Naming

Read enough of the actual system to avoid designing from filenames alone:

- Project rules, architecture decisions, glossary, roadmap, and package index.
- Routes, screens, commands, jobs, components, state/data owners, tests, public exports, and user-facing language.
- Package manifests, source imports, runtime/deployment units, and provider dependencies.
- Framework-required locations, generated code, workspace globs, build/test configuration, and boundary tooling.
- Recent changes or ownership signals that reveal which files change together.

Record uncertainty. Candidate bounded contexts and package splits are hypotheses until language, invariants, ownership, or dependency direction justify them.

Summarize the evidence before drawing a target tree:

| Evidence | Record |
| ---------- | -------- |
| Current shape | The established organizing axes and framework-required paths |
| Friction | Concrete navigation, cohesion, ownership, runtime, or dependency failures |
| Constraints | Build, test, packaging, deployment, compatibility, and team ownership rules |
| Change signals | Files that repeatedly change together or require coordinated review |
| Uncertainty | Claims that still need validation before implementation |

### 3. Select the Smallest Honest Shape

| Project signal | Primary shape |
| ---------------- | --------------- |
| Tiny package or early prototype | Flat or nearly flat |
| Ordinary backend without ports/adapters | Feature or use-case first |
| DDD without hexagonal architecture | Bounded-context and domain-language first |
| Explicitly hexagonal backend | Capability, then visible inside/outside, then featureful interior |
| BFF or endpoint-heavy edge service | URL/resource-first endpoints plus sibling workflows and composition |
| Framework-constrained backend | Thin required entrypoints delegating to feature-oriented behavior |
| Small frontend | Framework-native routes and shallow colocation |
| Feature-rich frontend | Route/screen composition plus product-feature modules and named foundations |
| Meta-framework full-stack app | Framework route tree with explicit client/server module boundaries |
| Established coherent frontend | Preserve or evolve it according to the requested scope and evidence |
| Frontend monorepo or design system | App/product scope plus earned packages and enforced public APIs |
| Ops, migration, or automation package | Workflow or command first |
| Monorepo | Product/capability grouping plus real leaf package boundaries |

These shapes can combine. A monorepo is an enforcement overlay. A BFF is often a driving host for other hexagons without being a hexagon itself. DDD may exist with or without ports and adapters.

When two shapes fit, compare them explicitly on discovery, change cohesion, enforceability, framework fit, migration cost, and reversibility. Prefer the simpler option unless the more elaborate boundary solves an observed problem.

### 4. Test Whether a Hexagon Is Earned

Use a visible hexagon only when the project explicitly chooses ports and adapters and the proposed boundary has:

- Meaningful application policy that must run without real external systems.
- At least one purposeful conversation with a driving or driven actor.
- Ports expressed in application language rather than cloned SDK APIs.
- A credible way to exercise each important port independently, or a concrete plan to add one.
- Import, package, or architecture tests capable of enforcing inside versus outside.

Do not give adapter wrappers, provider integrations, simple CRUD, operational scripts, or vocabulary-only packages ceremonial hexagons.

### 5. Produce the Structure and Its Rules Together

Every proposal must include:

1. The selected shape and the evidence supporting it.
2. An annotated ASCII tree distinguishing grouping directories, real packages, and executable hosts. Show only evidence-backed target paths: every new directory displayed must own at least one named file, package, or concrete responsibility. Collapse unknown candidates into prose; use an ellipsis only for an existing unchanged subtree or an explicitly repeated established pattern.
3. Placement rules for new files.
4. Allowed and forbidden dependency directions.
5. Proportionate automated enforcement.
6. A staged migration when an existing tree must change.
7. Rejected alternatives and why they lost.
8. Assumptions, deliberately deferred decisions, and structures intentionally not introduced.

## Visible Hexagonal Backends

For an opted-in monorepo capability, prefer this grammar:

```text
<capability>/                       # grouping directory, not a package
├── hexagon/                        # unmistakable INSIDE
│   └── <inside-package>/           # real workspace package
│       └── src/
│           └── <feature-or-use-case>/
├── adapters/                       # unmistakable OUTSIDE
│   ├── driving/
│   │   └── <transport-adapter>/    # real workspace package
│   └── driven/
│       └── <provider-adapter>/     # real workspace package
└── testing/                        # outside test interactors
    └── <fake-or-contract-suite>/   # real workspace package when reusable
```

Apply these semantics:

- Put pure business rules in domain modules.
- Put provider-free application policy and orchestration in the hexagon even when it calls injected ports and is not referentially pure.
- Put driving and driven port contracts inside; the application owns the conversations.
- Put every concrete transport, database, filesystem, queue, clock, UUID generator, cloud service, and provider SDK outside.
- Put reusable fakes, test drivers, and behavioral adapter contracts under `testing/`, never inside the production hexagon. Keep ordinary behavior tests colocated with the code they verify.
- Put concrete construction, configuration, resource ownership, and shutdown in the executable host's composition root.
- Organize inside packages by feature, domain concept, or use case. Do not replace one flat god file with a flat layer folder.
- Keep domain and application as separate packages only when that dependency boundary earns its cost. One cohesive inside package is valid.
- In a single-package service, `src/hexagon` is acceptable only with path-based import or architecture tests. In a monorepo, prefer manifests and compiler/package boundaries over a cosmetic subfolder inside a provider-dependent package.

## DDD Placement

Let bounded contexts define language and model authority; let the hexagon define the technology test wall. One does not imply the other.

- Use a separate context only when terminology, invariants, lifecycle, ownership, or integration contracts diverge.
- Keep domain concepts as nouns and use cases/workflows as verbs.
- Communicate across contexts through explicit contracts, events, or anti-corruption layers.
- Keep a shared kernel minimal and stable.
- Keep a concept as a feature module inside an existing context when the context evidence is weak.

Do not use this placement skill as a substitute for aggregate, entity, value-object, event, or ubiquitous-language modeling guidance.

## Frontend Structure

Treat frontend architecture as a first-class mode. Read `references/frontend-patterns.md` and classify route ownership, product-feature cohesion, UI reuse level, state/data ownership, runtime boundaries, and package ownership before choosing a tree. Preserve an established frontend only when the requested scope or evidence supports preservation; redesign it when that is the task. Do not project backend `hexagon/`, ports, adapters, DDD entities, or composition-root vocabulary onto client code unless the frontend explicitly adopts those patterns for a real boundary. In a full-stack repository, classify client and server modules independently and enforce the framework's client/server graph.

## Composition Roots

Only executable applications have composition roots. Keep concrete selection near the entry point and nowhere else.

- Use `composition/` when a host has a nontrivial graph, configuration families, owned resources, or lifecycle/shutdown behavior.
- Let `main.ts`, a framework startup file, or a small factory serve the role inline when the graph is trivial.
- Do not make libraries, bounded contexts, or every feature contain an empty `composition/` folder.
- Do not let ordinary endpoints, use cases, or adapters construct their concrete collaborators. When a serverless framework makes a handler or consumer the executable deployment entrypoint, that entrypoint may also host trivial inline composition; keep wiring visibly separate from translation and extract it as soon as the graph is shared, stateful, or nontrivial.

## Cohesion and Sharing

- Keep files that change together close, including focused tests, schemas, fixtures, and mappers owned by one slice.
- Expose a small explicit public API from every package or cross-feature module.
- Prevent sibling features from importing one another's internals.
- Promote code only when more than one current owner needs it and the promoted capability has a stable, purpose-specific name.
- Prefer `shared/money`, `platform/clock`, or `contracts/order-events` over `shared/utils`, `common`, `helpers`, or `services`.
- Split a folder when navigation or change cohesion improves; split a package when a dependency, ownership, release, or trust boundary needs mechanical enforcement.

## Proportionate Enforcement

- For a small package, public exports and review may be sufficient.
- For a single application, use path aliases, restricted imports, architecture tests, and framework boundary rules.
- For a monorepo, validate manifests, project references, public exports, workspace discovery, and dependency direction.
- For a large/deep workspace, derive rules from physical roles or a small package-role registry instead of hand-maintained package allowlists.
- Test recursive discovery at the deepest proposed path before moving packages there.

Read `references/enforcement-and-migration.md` for the dependency matrix and migration gates.

## Anti-Patterns

Reject these structures:

- Cosmetic `src/hexagon` inside a package that mixes provider code or permits outward imports.
- Global `domain`, `application`, `controllers`, `services`, or `repositories` buckets spanning unrelated capabilities.
- A package, bounded context, port, or hexagon for every noun or tiny interface.
- Ports that reproduce SQL, HTTP, ORM, or SDK APIs.
- Test adapters and reusable fakes beneath `hexagon/`.
- Business behavior, provider construction, or shared runtime state hidden in endpoint handlers.
- HTTP route leaves or CLI command entries buried inside capability or hexagon folders instead of the public interface tree (`endpoints/`, `commands/`).
- Production code importing development-only routes or test packages.
- `shared`, `common`, `utils`, `helpers`, or `services` as unowned dumping grounds.
- Empty folder skeletons added for symmetry.
- Deep trees that workspace, build, test, coverage, and lint tooling cannot discover.
- A big-bang migration that combines behavior changes, dependency inversion, and mass file moves.
- Treating every pure formatter or utility as domain policy.
- Fighting required framework locations instead of keeping them thin.
- Global `components`, `hooks`, `stores`, or `api` buckets that obscure frontend product ownership.
- Client bundles that can reach server-only modules, secrets, or privileged provider code.

## Completion Check

- Can a newcomer identify the product capabilities before the framework?
- If hexagonal architecture is used, is inside versus outside unmistakable and mechanically true?
- Is the interior navigable by domain concept or behavior rather than flat files?
- Are endpoints and framework entrypoints thin?
- Is concrete construction owned by an application entry point?
- Are bounded contexts justified by language and model authority?
- Are small and non-hexagonal projects spared architecture they have not earned?
- In a frontend, are route, feature, UI-reuse, state/data, and runtime owners explicit without ceremonial layers?
- Do package discovery and boundary checks support the proposed depth?
- Does the proposal state where the next new file belongs and what it may import?
- Does every new directory shown have a real owner now rather than serving as an empty or speculative placeholder?
- Are rejected alternatives, assumptions, and migration risks explicit enough for a reviewer to challenge?
