#!/usr/bin/env python3
"""Check end-of-life status for products using endoflife.date API."""

import argparse
import json
import sys
from urllib.request import urlopen
from urllib.error import HTTPError, URLError

API_BASE = "https://endoflife.date/api/v1"


def fetch_json(url: str) -> dict | list | None:
    """Fetch JSON from URL."""
    try:
        with urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
            # Handle API wrapper if present
            if isinstance(data, dict) and "result" in data:
                return data["result"]
            return data
    except HTTPError as e:
        if e.code == 404:
            return None
        raise
    except URLError as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return None


def list_products() -> list[str]:
    """List all available products."""
    data = fetch_json(f"{API_BASE}/products")
    if data:
        return [p["name"] for p in data]
    return []


def get_product(product: str) -> dict | None:
    """Get product details including all release cycles."""
    return fetch_json(f"{API_BASE}/products/{product}")


def get_latest_release(product: str) -> dict | None:
    """Get latest release cycle for a product."""
    return fetch_json(f"{API_BASE}/products/{product}/releases/latest")


def check_eol_status(product: str, version: str | None = None) -> dict:
    """Check EOL status for a product/version."""
    result = {"product": product, "found": False}

    product_data = get_product(product)
    if not product_data:
        result["error"] = f"Product '{product}' not found"
        return result

    result["found"] = True
    result["label"] = product_data.get("label", product)
    result["category"] = product_data.get("category")

    releases = product_data.get("releases", [])
    if not releases:
        result["error"] = "No release data available"
        return result

    if version:
        # Find matching release cycle
        matching = None
        for rel in releases:
            if rel["name"] == version or version.startswith(rel["name"]):
                matching = rel
                break

        if matching:
            result["version"] = matching["name"]
            result["is_eol"] = matching.get("isEol", False)
            result["eol_date"] = matching.get("eolFrom")
            result["is_lts"] = matching.get("isLts", False)
            result["latest_version"] = matching.get("latest", {}).get("name")
            result["release_date"] = matching.get("releaseDate")
        else:
            result["error"] = f"Version '{version}' not found for {product}"
    else:
        # Return latest release info
        latest = releases[0] if releases else None
        if latest:
            result["latest_cycle"] = latest["name"]
            result["latest_version"] = latest.get("latest", {}).get("name")
            result["is_lts"] = latest.get("isLts", False)

    # Find all supported versions
    supported = [r for r in releases if not r.get("isEol", True)]
    result["supported_versions"] = [r["name"] for r in supported[:5]]

    return result


def format_output(results: list[dict], output_format: str = "text") -> str:
    """Format results for output."""
    if output_format == "json":
        return json.dumps(results, indent=2, default=str)

    lines = []
    for r in results:
        if not r.get("found"):
            lines.append(f"❌ {r['product']}: {r.get('error', 'Not found')}")
            continue

        label = r.get("label", r["product"])
        if r.get("is_eol"):
            eol_date = r.get("eol_date", "unknown date")
            lines.append(
                f"⚠️  {label} {r.get('version', '')}: EOL since {eol_date}")
        elif r.get("version"):
            lines.append(f"✅ {label} {r['version']}: Supported")
        else:
            lines.append(
                f"ℹ️  {label}: Latest cycle {r.get('latest_cycle', 'N/A')}")

        if r.get("supported_versions"):
            lines.append(f"   Supported: {', '.join(r['supported_versions'])}")
        if r.get("latest_version"):
            lines.append(f"   Latest: {r['latest_version']}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Check EOL status via endoflife.date")
    parser.add_argument("products", nargs="*",
                        help="Products to check (format: product or product:version)")
    parser.add_argument("--list", action="store_true",
                        help="List all available products")
    parser.add_argument(
        "--search", help="Search for products matching pattern")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    if args.list:
        products = list_products()
        if args.search:
            products = [
                p for p in products
                if args.search.lower() in p.lower()
            ]
        for p in sorted(products):
            print(p)
        return

    if args.search:
        products = list_products()
        matches = [
            p for p in products
            if args.search.lower() in p.lower()
        ]
        for p in sorted(matches):
            print(p)
        return

    if not args.products:
        parser.print_help()
        return

    results = []
    for item in args.products:
        if ":" in item:
            product, version = item.split(":", 1)
        else:
            product, version = item, None
        results.append(check_eol_status(product, version))

    output_format = "json" if args.json else "text"
    print(format_output(results, output_format))


if __name__ == "__main__":
    main()
