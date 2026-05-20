# EOL API Reference

Use this only for runtime, OS, platform, database, infrastructure tool, or application
lifecycle checks. Dependency ecosystems such as npm, Ruby gems, and Rust crates have
their own registries; use this API for their runtimes only.

## Commands

Prefer the bundled script when it covers the product:

```bash
python3 scripts/check_eol.py ubuntu:22.04 ruby:3.2 nodejs:20
python3 scripts/check_eol.py --search postgres
python3 scripts/check_eol.py --list
```

Direct API calls use v1 and responses are wrapped in `result`:

```bash
curl -s "https://endoflife.date/api/v1/products/ubuntu" | jq '.result.releases[] | {name, isEol, eolFrom, latest: .latest.name}'
curl -s "https://endoflife.date/api/v1/products/ubuntu/releases/22.04" | jq '.result | {name, isEol, eolFrom, isLts, latest: .latest.name}'
curl -s "https://endoflife.date/api/v1/products/ubuntu/releases/latest" | jq '.result | {name, isLts, latest: .latest.name}'
```

## Target Selection

- Prefer supported LTS releases when the product has LTS cycles.
- Keep compatibility constraints visible: CI images, Docker tags, distro package
  availability, language runtime requirements, and deployment platform support.
- For soon-EOL versions, document the EOL date and recommended target.
- Read `common-products.md` only when the product ID is not obvious.

Key release fields: `name`, `releaseDate`, `isEol`, `eolFrom`, `isLts`,
`isMaintained`, `latest.name`.

## Fallback Policy

Fall back when endoflife.date is unavailable, lacks the product, lacks the release
cycle, or conflicts with project/vendor evidence.

- Use primary upstream sources first: vendor lifecycle pages, official release
  notes, official support matrices, package registry metadata, or maintained
  container image tags.
- For ecosystem dependencies, use the ecosystem registry instead of EOL data:
  npm registry for npm packages, RubyGems for gems, crates.io for Rust crates,
  Supermarket/GitHub releases for Chef cookbooks.
- Cross-check with one independent source when lifecycle dates affect a risky
  migration or the primary source is ambiguous.
- Record the source URL and retrieval date in the work summary when making a
  lifecycle claim from fallback data.
- Do not guess. If no authoritative source is found, report "unknown from
  available sources" and recommend the newest compatible supported target only
  when that target can be verified.
