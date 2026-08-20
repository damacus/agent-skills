#!/usr/bin/env bash

set -euo pipefail

usage() {
  printf '%s\n' \
    'Usage: check_locale_sync.sh REFERENCE_FILE [LOCALE_FILE ...]' \
    '' \
    'Compare translation node paths and kinds with REFERENCE_FILE.' \
    'When no locale files are supplied, locale-named sibling files with the' \
    'same extension are discovered automatically.'
}

fail() {
  printf 'error: %s\n' "$*" >&2
  exit 2
}

if [[ ${1:-} == "-h" || ${1:-} == "--help" ]]; then
  usage
  exit 0
fi

[[ $# -ge 1 ]] || {
  usage >&2
  exit 2
}

command -v yq >/dev/null 2>&1 || fail 'mikefarah yq v4 is required'

yq_version=$(yq --version 2>/dev/null || true)
[[ $yq_version =~ version[[:space:]]v4\. ]] || \
  fail "mikefarah yq v4 is required (found: ${yq_version:-unknown})"

reference=$1
shift
[[ -f $reference ]] || fail "reference file not found: $reference"

files=("$reference")

if [[ $# -gt 0 ]]; then
  files+=("$@")
else
  reference_dir=$(dirname "$reference")
  reference_name=$(basename "$reference")
  extension=${reference_name##*.}

  while IFS= read -r candidate; do
    candidate_name=$(basename "$candidate")
    candidate_stem=${candidate_name%.*}
    if [[ $candidate != "$reference" && \
          $candidate_stem =~ ^[A-Za-z]{2,3}([_-][A-Za-z0-9]{2,8})*$ ]]; then
      files+=("$candidate")
    fi
  done < <(find "$reference_dir" -maxdepth 1 -type f -name "*.${extension}" -print | sort)
fi

[[ ${#files[@]} -gt 1 ]] || \
  fail 'no accompanying locale files found; pass them explicitly'

for file in "${files[@]}"; do
  [[ -f $file ]] || fail "locale file not found: $file"
done

tmp_dir=$(mktemp -d "${TMPDIR:-/tmp}/check-locale-sync.XXXXXX")
trap 'rm -rf "$tmp_dir"' EXIT

manifest() {
  local file=$1
  local output=$2
  local root_key
  local expression

  if ! root_key=$(yq eval -r \
    'select(kind == "map" and (keys | length) == 1) | keys[0]' \
    "$file" 2>"$tmp_dir/yq-error"); then
    printf 'error: could not parse %s\n' "$file" >&2
    sed 's/^/  /' "$tmp_dir/yq-error" >&2
    return 2
  fi

  expression='.. | {"document": document_index, "path": path, "kind": kind}'
  if [[ $root_key =~ ^[A-Za-z]{2,3}([_-][A-Za-z0-9]{2,8})*$ ]]; then
    expression='.[strenv(ROOT_KEY)] | .. | {"document": document_index, "path": (path | .[1:]), "kind": kind}'
  fi

  if ! ROOT_KEY=$root_key yq eval -o=json -I=0 "$expression" "$file" \
    2>"$tmp_dir/yq-error" | sort >"$output"; then
    printf 'error: could not inspect %s\n' "$file" >&2
    sed 's/^/  /' "$tmp_dir/yq-error" >&2
    return 2
  fi
}

reference_manifest="$tmp_dir/reference.manifest"
manifest "$reference" "$reference_manifest"

status=0
for index in "${!files[@]}"; do
  [[ $index -eq 0 ]] && continue

  locale_file=${files[$index]}
  locale_manifest="$tmp_dir/locale-${index}.manifest"
  manifest "$locale_file" "$locale_manifest" || exit $?

  if ! diff -u "$reference_manifest" "$locale_manifest" \
    >"$tmp_dir/diff-${index}"; then
    status=1
    printf 'locale tree drift: %s differs from %s\n' \
      "$locale_file" "$reference" >&2
    sed \
      -e "1s|$reference_manifest|$reference|" \
      -e "2s|$locale_manifest|$locale_file|" \
      "$tmp_dir/diff-${index}" >&2
  fi
done

if [[ $status -ne 0 ]]; then
  exit "$status"
fi

printf 'Locale trees are in sync across %d files.\n' "${#files[@]}"
