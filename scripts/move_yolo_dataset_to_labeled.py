#!/usr/bin/env python3
"""
Move images and labels from data/yolo_dataset to data/labeled,
renaming all pairs to the same base name: yolo_0001.png / yolo_0001.txt, etc.

expects:
  data/yolo_dataset/images/<train|val>/*.png (or .jpg)
  data/yolo_dataset/labels/<train|val>/*.txt  (same stem as image)

writes:
  data/labeled/images/<train|val>/yolo_XXXX.png
  data/labeled/labels/<train|val>/yolo_XXXX.txt
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

# Project root = parent of scripts/
ROOT = Path(__file__).resolve().parent.parent
YOLO_DATASET = ROOT / "data" / "yolo_dataset"
LABELED = ROOT / "data" / "labeled"

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}


def find_splits(images_dir: Path) -> list[str]:
    """Return ['train', 'val'] if they exist, else [''] for flat layout."""
    if not images_dir.is_dir():
        return []
    subs = [p.name for p in images_dir.iterdir() if p.is_dir()]
    if "train" in subs or "val" in subs:
        return [s for s in ("train", "val") if s in subs]
    return [""]  # flat: images/*.png directly under images/ -> will go to train only


def collect_pairs(split: str) -> list[tuple[Path, Path]]:
    """List (image_path, label_path) for split; label must exist."""
    if split:
        img_dir = YOLO_DATASET / "images" / split
        lbl_dir = YOLO_DATASET / "labels" / split
    else:
        img_dir = YOLO_DATASET / "images"
        lbl_dir = YOLO_DATASET / "labels"

    if not img_dir.is_dir():
        return []
    pairs = []
    for img in sorted(img_dir.iterdir()):
        if img.suffix.lower() not in IMAGE_EXTS:
            continue
        stem = img.stem
        lbl = lbl_dir / f"{stem}.txt"
        if lbl.is_file():
            pairs.append((img, lbl))
        else:
            print(f"  [skip] no label for {img.name}", file=sys.stderr)
    return pairs


def main() -> None:
    if not YOLO_DATASET.is_dir():
        print(f"Not found: {YOLO_DATASET}", file=sys.stderr)
        sys.exit(1)

    splits = find_splits(YOLO_DATASET / "images")
    if not splits:
        print("No images under data/yolo_dataset/images/", file=sys.stderr)
        sys.exit(1)

    total_moved = 0
    for split in splits:
        pairs = collect_pairs(split)
        if not pairs:
            continue
        # Flat layout -> put everything under train (YOLO yaml expects train/val)
        out_split = split if split else "train"
        out_img_dir = LABELED / "images" / out_split
        out_lbl_dir = LABELED / "labels" / out_split
        out_img_dir.mkdir(parents=True, exist_ok=True)
        out_lbl_dir.mkdir(parents=True, exist_ok=True)

        for i, (img_path, lbl_path) in enumerate(pairs, start=1):
            name = f"yolo_{i:04d}"
            new_img = out_img_dir / f"{name}{img_path.suffix.lower()}"
            new_lbl = out_lbl_dir / f"{name}.txt"
            shutil.move(str(img_path), str(new_img))
            shutil.move(str(lbl_path), str(new_lbl))
            total_moved += 1
            print(f"  {out_split}: {img_path.name} -> {new_img.name}")

    if total_moved == 0:
        print("No image/label pairs found to move.", file=sys.stderr)
        sys.exit(1)
    print(f"Done. Moved {total_moved} pairs into {LABELED}")


if __name__ == "__main__":
    main()
