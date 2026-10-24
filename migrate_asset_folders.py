#!/usr/bin/env python3
"""
One-time Italian Finds asset-folder migration.

Run this script from the website root (the directory containing cars.json,
script.js, and assets/). It first shows a plan. Re-run with --apply to rename
folders and update cars.json + script.js.

Example:
  python migrate_asset_folders.py
  python migrate_asset_folders.py --apply
"""
import argparse
import json
import shutil
import sys
from pathlib import Path

ROOT = Path.cwd()
CARS_JSON = ROOT / "cars.json"
SCRIPT_JS = ROOT / "script.js"
ASSETS = ROOT / "assets"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="perform the migration")
    args = parser.parse_args()

    for required in (CARS_JSON, SCRIPT_JS, ASSETS):
        if not required.exists():
            sys.exit(f"ERROR: Expected {required} in the current directory.")

    original_json = CARS_JSON.read_text(encoding="utf-8")
    cars = json.loads(original_json)

    plan = []
    seen_prefixes = set()
    for car in cars:
        old = str(car.get("folder", "")).strip()
        prefix = str(car.get("prefix", "")).strip()
        if not old or not prefix:
            sys.exit(f"ERROR: Every car needs both 'folder' and 'prefix': {car.get('name', '(unnamed)')}")
        if "/" in prefix or "\\" in prefix or prefix in {".", ".."}:
            sys.exit(f"ERROR: Unsafe prefix used as folder name: {prefix!r}")
        if prefix in seen_prefixes:
            sys.exit(f"ERROR: Duplicate prefix {prefix!r}; fix cars.json before migrating.")
        seen_prefixes.add(prefix)
        src, dst = ASSETS / old, ASSETS / prefix
        if not src.is_dir():
            sys.exit(f"ERROR: Source folder does not exist: {src}")
        if old != prefix and dst.exists():
            sys.exit(f"ERROR: Destination already exists: {dst}")
        plan.append((car, old, prefix, src, dst))

    # Avoid ambiguous cases where a destination is another source folder name.
    source_names = {old for _, old, _, _, _ in plan}
    for _, old, prefix, _, dst in plan:
        if old != prefix and prefix in source_names:
            sys.exit(
                f"ERROR: {prefix!r} is also an existing car folder name. "
                "Rename that folder manually to a temporary unique name, then rerun."
            )

    print("Folder migration plan:")
    for _, old, prefix, _, _ in plan:
        print(f"  assets/{old}/  ->  assets/{prefix}/" if old != prefix else f"  assets/{old}/  (unchanged)")

    if not args.apply:
        print("\nDry run only; nothing has changed.")
        print("Back up your website, then run: python migrate_asset_folders.py --apply")
        return

    # Rename folders first. If a rename fails, stop before editing JSON/JS.
    renamed = []
    try:
        for _, old, prefix, src, dst in plan:
            if old != prefix:
                src.rename(dst)
                renamed.append((dst, src))
    except Exception as exc:
        print(f"ERROR during folder rename: {exc}", file=sys.stderr)
        print("Attempting to roll back completed folder renames…", file=sys.stderr)
        for current, previous in reversed(renamed):
            if current.exists() and not previous.exists():
                current.rename(previous)
        sys.exit(1)

    # Prefix is now the canonical folder name; keep it explicit in JSON.
    for car, _, prefix, _, _ in plan:
        car["folder"] = prefix
    CARS_JSON.write_text(json.dumps(cars, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    js = SCRIPT_JS.read_text(encoding="utf-8")
    js = js.replace(
        "Folder numbers remain 01, 02, 03...",
        "Asset folders use each car's prefix (for example assets/AlfaGTJunior/)."
    )
    SCRIPT_JS.write_text(js, encoding="utf-8")

    print("\nMigration complete.")
    print("cars.json now sets each car's folder to its prefix.")
    print("script.js already builds asset paths from car.folder, so no path logic change was needed.")
    print("Check the website locally before publishing. Keep your backup until verified.")

if __name__ == "__main__":
    main()
