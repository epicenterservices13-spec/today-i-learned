#!/usr/bin/env python3
"""Build and maintain the Today I Learned (TIL) repository index in README.md."""

from pathlib import Path
import re
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent

EXCLUDED_DIRS = {".git", "scripts", ".github", ".venv"}
EXCLUDED_FILES = {"README.md", "template.md", "LICENSE"}

CATEGORY_TITLES = {
    "arch": "Architecture & Taxonomy",
    "bash": "Bash & Shell Scripting",
    "git": "Git Discipline & Version Control",
    "linux": "Linux Administration & Storage",
    "termux": "Termux & Android POSIX",
    "python": "Python & Data Processing",
}


def extract_title(file_path: Path) -> str:
    """Extract the first markdown H1 title from the file."""
    with file_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("# "):
                return line[2:].strip()
    return file_path.stem.replace("-", " ").title()


def collect_tils():
    categories = {}
    total_tils = 0

    for category_dir in sorted(REPO_ROOT.iterdir()):
        if not category_dir.is_dir() or category_dir.name in EXCLUDED_DIRS or category_dir.name.startswith("."):
            continue

        category_name = category_dir.name
        files = sorted(
            [
                p for p in category_dir.glob("*.md")
                if p.name not in EXCLUDED_FILES and not p.name.startswith(".")
            ],
            key=lambda p: p.stem,
        )

        if files:
            categories[category_name] = []
            for file_path in files:
                title = extract_title(file_path)
                relative_path = file_path.relative_to(REPO_ROOT).as_posix()
                categories[category_name].append((title, relative_path))
                total_tils += 1

    return categories, total_tils


def generate_readme(categories, total_count):
    lines = [
        "# Today I Learned",
        "",
        "> A collection of concise, battle-tested write-ups on commands, systems architecture, and engineering discipline.",
        "",
        f"**Total TILs documented:** `{total_count}`",
        "",
        "---",
        "",
        "## Categories",
        "",
    ]

    for cat_key in sorted(categories.keys()):
        display_name = CATEGORY_TITLES.get(cat_key, cat_key.replace("-", " ").title())
        count = len(categories[cat_key])
        lines.append(f"- [{display_name}](#{cat_key}) (`{count}`)")

    lines.append("")
    lines.append("---")
    lines.append("")

    for cat_key in sorted(categories.keys()):
        display_name = CATEGORY_TITLES.get(cat_key, cat_key.replace("-", " ").title())
        entries = categories[cat_key]
        lines.append(f"<a id=\"{cat_key}\"></a>")
        lines.append(f"### {display_name}")
        lines.append("")
        for title, rel_path in entries:
            lines.append(f"- [{title}]({rel_path})")
        lines.append("")

    lines.extend([
        "---",
        "",
        "## Adding a TIL",
        "",
        "1. Copy [`template.md`](template.md) into the appropriate category folder:",
        "   ```bash",
        "   cp template.md bash/my-topic.md",
        "   ```",
        "2. Populate your notes following the structured sections.",
        "3. Rebuild the index:",
        "   ```bash",
        "   python3 scripts/build_index.py",
        "   ```",
        "4. Enforce atomic commits:",
        "   ```bash",
        "   git add bash/my-topic.md && git commit -m \"bash/my-topic.md: add notes on my topic\"",
        "   git add README.md && git commit -m \"README.md: update index\"",
        "   ```",
        "",
        "## License",
        "",
        "MIT License. See [LICENSE](LICENSE).",
        "",
    ])

    return "\n".join(lines)


def main():
    categories, total_count = collect_tils()
    readme_content = generate_readme(categories, total_count)
    readme_path = REPO_ROOT / "README.md"
    readme_path.write_text(readme_content, encoding="utf-8")
    print(f"Index generated successfully: {total_count} TILs across {len(categories)} categories.")


if __name__ == "__main__":
    main()
