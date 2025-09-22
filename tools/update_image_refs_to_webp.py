# tools/update_image_refs_to_webp.py
import re
from pathlib import Path

# ---- Config ----
ROOTS = [Path("templates"), Path("assets")]   # folders to scan
INCLUDE_EXTS = {".html", ".css", ".js"}       # file types to edit

# Skip jpg->webp rewrite if these appear in the URL path
SKIP_KEYWORDS = ["logo", "icon"]
SKIP_FOLDER = "favicon/"

# Match any 'images/...*.jpg|jpeg' inside quotes, url(), or Django {% static %} usage.
# Only capture the path up to the extension so we can swap it cleanly.
PATTERN = re.compile(r'(?i)(images/[^"\'\)]+?)\.(?:jpe?g)')

def should_skip(url_path: str) -> bool:
    p = url_path.lower()
    if SKIP_FOLDER in p:
        return True
    return any(k in p for k in SKIP_KEYWORDS)

def rewrite(content: str) -> tuple[str, int]:
    """Return (new_content, replacements_count)."""
    count = 0

    def _sub(m: re.Match) -> str:
        nonlocal count
        url_path = m.group(1)  # e.g., images/gallery/pic
        if should_skip(url_path):
            return m.group(0)   # leave unchanged
        count += 1
        return url_path + ".webp"

    new = PATTERN.sub(_sub, content)
    return new, count

def process_file(fp: Path) -> int:
    # Open with newline='' to preserve existing line endings; force UTF-8 to keep emojis
    text = fp.open("r", encoding="utf-8", newline="").read()
    new_text, n = rewrite(text)
    if n:
        fp.open("w", encoding="utf-8", newline="").write(new_text)
    return n

def main():
    total_files = 0
    total_changes = 0
    for root in ROOTS:
        if not root.exists():
            continue
        for fp in root.rglob("*"):
            if fp.is_file() and fp.suffix.lower() in INCLUDE_EXTS:
                changes = process_file(fp)
                if changes:
                    total_files += 1
                    total_changes += changes
                    print(f"Updated {fp}  (+{changes})")
    print(f"\nDone. Files changed: {total_files}, total replacements: {total_changes}")

if __name__ == "__main__":
    main()
