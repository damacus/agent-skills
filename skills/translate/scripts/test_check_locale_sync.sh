#!/usr/bin/env bash

set -euo pipefail

script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
checker="$script_dir/check_locale_sync.sh"
fixtures="$script_dir/tests/fixtures"

"$checker" "$fixtures/synced/en.yml" >/dev/null
"$checker" \
  "$fixtures/synced-json/en.json" \
  "$fixtures/synced-json/es.json" >/dev/null

if "$checker" "$fixtures/drifted/en.yml" >/dev/null 2>&1; then
  printf '%s\n' 'expected drifted fixtures to fail' >&2
  exit 1
fi

printf '%s\n' 'check_locale_sync tests passed'
