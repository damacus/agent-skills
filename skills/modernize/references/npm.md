# npm/Node Modernization

Use this for Node.js runtime and npm package modernization.

## Detect

- Runtime: `.nvmrc`, `.node-version`, `package.json` `engines.node`, CI matrices,
  Docker tags.
- Package manager: choose from the committed lockfile: `package-lock.json`,
  `npm-shrinkwrap.json`, `yarn.lock`, or `pnpm-lock.yaml`.
- Dependencies: `package.json` `dependencies`, `devDependencies`,
  `optionalDependencies`, `peerDependencies`.

## Inspect

```bash
npm outdated --json
npm view <package> version engines peerDependencies
npm audit --json
```

For Yarn or pnpm projects, use their native outdated/update/install commands instead
of converting the project to npm.

## Update

- Do not switch package managers or delete lockfiles.
- Respect existing semver ranges unless the user asked for broad upgrades.
- Update the Node.js runtime with `references/eol-api.md` when runtime files,
  Docker images, or CI versions are in scope.
- For package updates, prefer focused changes first: one package, one group, or one
  framework family.
- Regenerate the lockfile with the existing package manager.

## Validate

Run the project scripts that exist in `package.json`, usually tests, type checks,
linting, and build. If scripts are missing, run the package manager's install or
lockfile validation command and report the gap.
