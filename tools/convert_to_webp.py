from pathlib import Path
from PIL import Image, ImageOps

# ---- Adjust paths if needed ----
SRC = Path("assets/images")                 # current structure 
DST = Path("assets/images_optimized")       # output root

# First matching rule wins (case-insensitive substring match on relative path)
RULES = [
    {"match": "hero/",         "max_w": 1920, "quality": 80, "lossless": False},
    {"match": "carousel/",     "max_w": 1600, "quality": 80, "lossless": False},
    {"match": "gallery/",      "max_w": 1200, "quality": 82, "lossless": False},
    {"match": "region_cards/", "max_w":  900, "quality": 82, "lossless": False},
    {"match": "equipment/",    "max_w": 1000, "quality": 82, "lossless": False},
    # filename-based helpers (optional):
    {"match": "_600pxw",       "max_w":  600, "quality": 75, "lossless": False},
    {"match": "thumb",         "max_w":  600, "quality": 75, "lossless": False},
    # crisp UI/branding
    {"match": "logo",          "max_w":  800, "quality": 100, "lossless": True},
    {"match": "icon",          "max_w":  800, "quality": 100, "lossless": True},
]

# Fallback for files in the root of assets/images or anything not matching above
DEFAULT = {"max_w": 1600, "quality": 82, "lossless": False}

# Only convert these input types (add ".webp" if required)
EXTS = {".jpg", ".jpeg", ".png"}

SKIP_IF_UP_TO_DATE = True  # skip if output newer than source


def pick_rule(rel_path: Path):
    p = str(rel_path).lower().replace("\\", "/")
    for r in RULES:
        if r["match"].lower() in p:
            return r
    return DEFAULT

def ensure_mode(im: Image.Image) -> Image.Image:
    # Keep alpha if present; otherwise RGB
    if im.mode in ("RGB", "RGBA"):
        return im
    return im.convert("RGBA" if "A" in im.getbands() else "RGB")

def process_one(src_path: Path):
    rel = src_path.relative_to(SRC)
    rule = pick_rule(rel)

    out_dir = DST / rel.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / (src_path.stem + ".webp")

    if SKIP_IF_UP_TO_DATE and out_path.exists() and out_path.stat().st_mtime >= src_path.stat().st_mtime:
        return "skipped", out_path

    with Image.open(src_path) as im:
        im = ImageOps.exif_transpose(im)  # fix orientation
        im = ensure_mode(im)
        w, h = im.size
        if w > rule["max_w"]:
            new_h = int(h * (rule["max_w"] / w))
            im = im.resize((rule["max_w"], new_h), Image.LANCZOS)

        save_kwargs = {"method": 6}
        if rule["lossless"]:
            save_kwargs.update({"lossless": True, "quality": 100})
        else:
            save_kwargs.update({"quality": rule["quality"], "optimize": True})

        im.save(out_path, "WEBP", **save_kwargs)

    return "converted", out_path

def main():
    stats = {"converted": 0, "skipped": 0}
    for p in SRC.rglob("*"):
        if p.is_file() and p.suffix.lower() in EXTS:
            status, _ = process_one(p)
            stats[status] += 1
    print(f"Done. Converted {stats['converted']}, skipped {stats['skipped']}. Output → {DST}")

if __name__ == "__main__":
    main()
