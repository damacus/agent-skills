#!/usr/bin/env python3
"""Resolve a model family from current, caller-supplied runtime metadata only."""
import argparse
import json
import re
import sys

MODEL = re.compile(r"^gpt-((?:0|[1-9]\d*)(?:\.(?:0|[1-9]\d*))*)-(luna|sol|astra|terra)$")
OLD = re.compile(r"\b(retired|deprecated|legacy|older|previous(?:[- ]generation)?)\b", re.I)
PREVIEW = re.compile(r"\b(preview|experimental|beta)\b", re.I)


class RoutingError(ValueError):
    pass


def identity(identifier):
    if not isinstance(identifier, str):
        raise RoutingError("Model ID must be a string")
    match = MODEL.fullmatch(identifier)
    if not match:
        raise RoutingError("No verified canonical numeric family ID")
    version = tuple(int(part) for part in match[1].split('.'))
    family = match[2]
    if family == 'terra':
        raise RoutingError("Terra is excluded")
    if family == 'sol' and (version + (0,))[0:2] == (6, 0):
        raise RoutingError("Sol 6.0 is excluded")
    return family, version


def resolve(inventory, family):
    if family not in ('luna', 'sol', 'astra'):
        raise RoutingError("Family must be Luna, Sol or Astra")
    if not isinstance(inventory, dict) or not isinstance(inventory.get('models'), list):
        raise RoutingError("An advertised models inventory is required")
    candidates = {}
    for entry in inventory['models']:
        if not isinstance(entry, dict):
            raise RoutingError("Invalid model inventory entry")
        try:
            actual_family, version = identity(entry.get('id'))
        except RoutingError:
            # Unknown IDs and aliases cannot be mistaken for permitted models.
            continue
        if actual_family != family or entry.get('available') is False:
            continue
        status = entry.get('status', 'stable')
        description = entry.get('description', '')
        if not isinstance(description, str) or status != 'stable':
            continue
        if OLD.search(description) or PREVIEW.search(description):
            continue
        if entry.get('is_latest') is False:
            continue
        previous = candidates.get(entry['id'])
        if previous is not None and previous['metadata'] != entry:
            raise RoutingError("Conflicting metadata for the same model")
        candidates[entry['id']] = {'metadata': entry, 'version': version}
    if not candidates:
        raise RoutingError("No permitted advertised model in the requested family")
    width = max(len(candidate['version']) for candidate in candidates.values())
    key = lambda candidate: candidate['version'] + (0,) * (width - len(candidate['version']))
    newest = max(key(candidate) for candidate in candidates.values())
    winners = [candidate for candidate in candidates.values() if key(candidate) == newest]
    if any(candidate['metadata'].get('is_latest') is True and key(candidate) != newest
           for candidate in candidates.values()):
        raise RoutingError("Conflicting latest/version metadata")
    if len(winners) != 1:
        raise RoutingError("Ambiguous newest model; verify runtime metadata")
    selected = winners[0]['metadata']
    return {
        'family': family,
        'model': selected['id'],
        'default_reasoning_effort': selected.get('default_reasoning_effort'),
        'supported_reasoning_efforts': selected.get('supported_reasoning_efforts'),
    }


def check(inventory, model):
    family, _ = identity(model)
    result = resolve(inventory, family)
    if result['model'] != model:
        raise RoutingError("Model is superseded; use the resolved latest permitted ID")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--family', choices=['luna', 'sol', 'astra'])
    group.add_argument('--check-model')
    args = parser.parse_args()
    try:
        inventory = json.load(sys.stdin)
        result = check(inventory, args.check_model) if args.check_model else resolve(inventory, args.family)
    except (RoutingError, json.JSONDecodeError) as error:
        print(json.dumps({'status': 'blocked', 'reason': str(error)}))
        return 2
    print(json.dumps(result))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
