import re
from pathlib import Path
from datetime import date, timedelta

# katalogi źródłowy i docelowy
SRC_DIR = Path("path")
DST_DIR = Path("path")

DST_DIR.mkdir(parents=True, exist_ok=True)

# schemat front matter
FRONT_MATTER = """---
title: "{title} - Writeup"
classes: single
ribbon: LightBlue
categories:
  - writeup
tags:
  - writeups
  - pentest
  - writeup
  - oscp
  - shell
  - exploit
  - htb
  - hackthebox
  - machine
{tags}
toc: true
hide_title: true
excerpt: ""
sidebar:
        nav: "menu_writeups"
---
"""

def process_tags(line: str) -> str:
    tags = re.findall(r"#(\w+)", line)
    return "\n".join([f"  - {t.lower()}" for t in tags])

def process_images(content: str) -> str:
    return re.sub(
        r"!\[\[(.*?)\]\]",
        lambda m: f"![](https://kar0nx.github.io/assets/images/writeup/{Path(m.group(1)).name})",
        content
    )

def convert_headers(content: str) -> str:
    """
    Zamienia wszystkie nagłówki H1 (# ) na H2 (## )
    """
    return re.sub(r"^# (.*)", r"## \1", content, flags=re.MULTILINE)

def convert_file(src_file: Path, current_date: date):
    with open(src_file, "r", encoding="utf-8") as f:
        raw_content = f.read()

    lines = raw_content.splitlines()

    title = None
    tags_yaml = ""
    body_lines = []

    for line in lines:
        if line.startswith("# ") and not title:
            title = line.strip("# \n")
            body_lines.append(line)  # ten pierwszy też zachowujemy
            continue
        if line.lower().startswith("tags:"):
            tags_yaml = process_tags(line)
            continue
        body_lines.append(line)

    body = "\n".join(body_lines)
    body = process_images(body)
    body = convert_headers(body)

    fm = FRONT_MATTER.format(title=title or "Untitled", tags=tags_yaml)
    final_content = fm + "\n" + body

    # przygotowanie nowej nazwy pliku: 2025-07-01-Access.md
    clean_title = (title or "Untitled").split()[0]
    new_filename = f"{current_date.isoformat()}-{clean_title}.md"
    dst_file = DST_DIR / new_filename

    with open(dst_file, "w", encoding="utf-8") as f:
        f.write(final_content)

    print(f"[+] {src_file.name} -> {dst_file.name}")

def main():
    start_date = date(2025, 7, 1)
    current_date = start_date

    for md_file in sorted(SRC_DIR.glob("*.md")):
        convert_file(md_file, current_date)
        current_date += timedelta(days=1)

if __name__ == "__main__":
    main()
