from __future__ import annotations

import argparse
from pathlib import Path


def find_candidates(venv_path: Path) -> list[Path]:
    candidates: list[Path] = []

    for init_file in venv_path.rglob("__init__.py"):
        if not init_file.is_file():
            continue

        # Skip non-empty files; touched files are typically 0-byte stubs.
        if init_file.stat().st_size != 0:
            continue

        parent = init_file.parent
        other_py_files = [
            p for p in parent.glob("*.py") if p.name != "__init__.py"
        ]

        # Keep __init__.py in real Python package directories.
        if other_py_files:
            continue

        candidates.append(init_file)

    return sorted(candidates)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Remove likely accidental empty __init__.py files under .venv"
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Delete the detected files. Without this flag, runs in dry-run mode.",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    venv_path = repo_root / ".venv"

    if not venv_path.exists():
        print(f"No .venv found at: {venv_path}")
        return 1

    candidates = find_candidates(venv_path)

    if not candidates:
        print("No accidental empty __init__.py files found.")
        return 0

    print(f"Found {len(candidates)} candidate file(s):")
    for file_path in candidates:
        print(file_path)

    if not args.apply:
        print("Dry run complete. Re-run with --apply to delete these files.")
        return 0

    deleted = 0
    for file_path in candidates:
        file_path.unlink(missing_ok=True)
        deleted += 1

    print(f"Deleted {deleted} file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
