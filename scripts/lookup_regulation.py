#!/usr/bin/env python3
"""Registry-backed regulation lookup for NatPRD.

Usage:
    python3 scripts/lookup_regulation.py --signals payments,pii [--geo ID]
    python3 scripts/lookup_regulation.py --list-signals

Filters references/regulations.json by compliance signal and (optionally)
geography, and prints the matching candidates as JSON. This is the deterministic
entry point used by §0.3b of the interview: it returns only the matched subset so
the full registry never has to be loaded into the model's context.

The output is a STARTING POINT, not legal advice. The interview always confirms
the candidate list with the user and verifies any fetched regulation text before
writing it. This script performs NO network access — it only reads the bundled
registry. Fetching a regulation's official_url (when the user opts in) is done
separately via the WebFetch tool.

Exits 0 on success, 2 on registry-not-found, 3 on parse/crash.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

DEFAULT_REGISTRY = Path(__file__).resolve().parent.parent / "references" / "regulations.json"


def country_of(code: str) -> str:
    """Country part of a geography code: 'US-CA' -> 'US', 'ID' -> 'ID'."""
    return code.strip().upper().split("-", 1)[0]


def geo_matches(requested: str, geographies: List[str]) -> bool:
    """A regulation matches if it is GLOBAL or shares a country with the request."""
    geos = [g.strip().upper() for g in geographies]
    if "GLOBAL" in geos:
        return True
    req_country = country_of(requested)
    return any(country_of(g) == req_country for g in geos)


def lookup(
    registry: Dict[str, Any], signals: List[str], geo: str
) -> List[Dict[str, Any]]:
    wanted = {s.strip().lower() for s in signals if s.strip()}
    matches: List[Dict[str, Any]] = []
    for reg in registry.get("regulations", []):
        reg_signals = {s.lower() for s in reg.get("signals", [])}
        if not (wanted & reg_signals):
            continue
        if geo and not geo_matches(geo, reg.get("geographies", [])):
            continue
        matches.append(
            {
                "id": reg.get("id"),
                "name": reg.get("name"),
                "jurisdiction": reg.get("jurisdiction"),
                "official_url": reg.get("official_url"),
                "summary": reg.get("summary"),
                "matched_signals": sorted(wanted & reg_signals),
                "last_reviewed": reg.get("last_reviewed"),
            }
        )
    return matches


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Registry-backed regulation lookup for NatPRD (no network access).",
    )
    parser.add_argument(
        "--signals",
        help="Comma-separated compliance signals, e.g. 'payments,pii,ekyc'.",
    )
    parser.add_argument(
        "--geo",
        default="",
        help="Geography code, e.g. ID, SG, EU, US, US-CA. Optional; omit for all geographies.",
    )
    parser.add_argument(
        "--registry",
        default=str(DEFAULT_REGISTRY),
        help="Path to the regulation registry JSON (default: bundled references/regulations.json).",
    )
    parser.add_argument(
        "--list-signals",
        action="store_true",
        help="Print the supported signal vocabulary and exit.",
    )
    args = parser.parse_args()

    path = Path(args.registry)
    if not path.is_file():
        print(json.dumps({"error": f"Registry not found: {path}"}), file=sys.stderr)
        return 2

    try:
        registry = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001 - report any parse failure uniformly
        print(
            json.dumps({"error": f"Registry parse failed: {type(e).__name__}: {e}"}),
            file=sys.stderr,
        )
        return 3

    if args.list_signals:
        json.dump(
            {"signals_vocabulary": registry.get("signals_vocabulary", {})},
            sys.stdout,
            indent=2,
            ensure_ascii=False,
        )
        sys.stdout.write("\n")
        return 0

    if not args.signals:
        print(
            json.dumps({"error": "Provide --signals (or use --list-signals)."}),
            file=sys.stderr,
        )
        return 3

    try:
        candidates = lookup(registry, args.signals.split(","), args.geo)
    except Exception as e:  # noqa: BLE001
        print(
            json.dumps({"error": f"Lookup crashed: {type(e).__name__}: {e}"}),
            file=sys.stderr,
        )
        return 3

    result = {
        "registry_version": registry.get("version"),
        "registry_last_reviewed": registry.get("last_reviewed"),
        "query": {"signals": [s.strip() for s in args.signals.split(",") if s.strip()], "geo": args.geo or None},
        "disclaimer": "Starting point, not legal advice. Confirm with the user and verify official_url text before writing. When unsure, write '[TBD - legal/compliance to confirm]'.",
        "match_count": len(candidates),
        "candidates": candidates,
    }
    json.dump(result, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
