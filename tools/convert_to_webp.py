# tools/convert_to_webp.py
from pathlib import Path
from shutil import copy2

from PIL import Image, ImageOps

# ----- Paths -----
# Source of truth (originals, including any existing .webp already had):
SRC = Path("assets/images_original")
# Destination (the live, optimized set to actually serve):
DST = Path("assets/images")

# ----- Behaviour toggles -----
OVERWRITE_EXISTING = True  # always write fresh files into DST
RECOMPRESS_EXISTING_WEBP = (
    True  # re-save .webp using the rule (resize + quality/lossless)
)

# First matching rule wins (case-insensitive substring match on relative path)
RULES = [
    {"match": "hero/", "max_w": 1920, "quality": 80, "lossless": False},
    {"match": "carousel/", "max_w": 1600, "quality": 80, "lossless": False},
    {"match": "gallery/", "max_w": 1200, "quality": 82, "lossless": False},
    {"match": "region_cards/", "max_w": 900, "quality": 82, "lossless": False},
    {"match": "equipment/", "max_w": 1000, "quality": 82, "lossless": False},
    # filename-based helpers (optional):
    {"match": "_600pxw", "max_w": 600, "quality": 75, "lossless": False},
    {"match": "thumb", "max_w": 600, "quality": 75, "lossless": False},
    # crisp UI/branding
    {"match": "logo", "max_w": 800, "quality": 100, "lossless": True},
    {"match": "icon", "max_w": 800, "quality": 100, "lossless": True},
]

# Fallback for anything not matching above (incl. files in SRC root)
DEFAULT = {"max_w": 1600, "quality": 82, "lossless": False}

# Process these input types
EXTS = {".jpg", ".jpeg", ".png", ".webp"}


def pick_rule(rel_path: Path):
    p = str(rel_path).lower().replace("\\", "/")
    for r in RULES:
        if r["match"].lower() in p:
            return r
    return DEFAULT


def ensure_mode(im: Image.Image) -> Image.Image:
    # Preserve alpha if present; otherwise RGB
    if im.mode in ("RGB", "RGBA"):
        return im
    return im.convert("RGBA" if "A" in im.getbands() else "RGB")


def save_webp(im: Image.Image, out_path: Path, rule: dict):
    save_kwargs = {"method": 6}
    if rule["lossless"]:
        # lossless ignores quality, but we pass 100 for clarity
        save_kwargs.update({"lossless": True, "quality": 100})
    else:
        save_kwargs.update({"quality": rule["quality"], "optimize": True})
    im.save(out_path, "WEBP", **save_kwargs)


def process_one(src_path: Path):
    rel = src_path.relative_to(SRC)
    rule = pick_rule(rel)

    out_dir = DST / rel.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / (src_path.stem + ".webp")

    if (
        not OVERWRITE_EXISTING
        and out_path.exists()
        and out_path.stat().st_mtime >= src_path.stat().st_mtime
    ):
        return "skipped", out_path

    suffix = src_path.suffix.lower()
    is_webp_src = suffix == ".webp"

    # Open image (even webp) so we can optionally resize/recompress
    with Image.open(src_path) as im:
        im = ImageOps.exif_transpose(im)
        im = ensure_mode(im)

        w, h = im.size
        needs_resize = w > rule["max_w"]
        if needs_resize:
            new_h = int(h * (rule["max_w"] / w))
            im = im.resize((rule["max_w"], new_h), Image.LANCZOS)

        # Decide how to write:
        if is_webp_src:
            if needs_resize or RECOMPRESS_EXISTING_WEBP or rule["lossless"]:
                save_webp(im, out_path, rule)
                return "recompressed", out_path
            else:
                # pass-through copy if no resize and recompress disabled
                copy2(src_path, out_path)
                return "copied", out_path
        else:
            # JPG/PNG -> WebP according to rule
            save_webp(im, out_path, rule)
            return "converted", out_path


def main():
    stats = {"converted": 0, "recompressed": 0, "copied": 0, "skipped": 0}
    for p in SRC.rglob("*"):
        if p.is_file() and p.suffix.lower() in EXTS:
            status, _ = process_one(p)
            stats[status] += 1
    print(
        "Done.",
        f"Converted: {stats['converted']},",
        f"Recompressed: {stats['recompressed']},",
        f"Copied: {stats['copied']},",
        f"Skipped: {stats['skipped']}.",
        f"Output → {DST}",
    )


if __name__ == "__main__":
    main()
