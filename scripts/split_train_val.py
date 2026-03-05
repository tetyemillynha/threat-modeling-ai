#!/usr/bin/env python3
"""
Move ~10% dos syn_*.png e syn_*.txt de data/labeled/images/train e labels/train
para data/labeled/images/val e labels/val.
"""
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMAGES_TRAIN = ROOT / "data" / "labeled" / "images" / "train"
LABELS_TRAIN = ROOT / "data" / "labeled" / "labels" / "train"
IMAGES_VAL = ROOT / "data" / "labeled" / "images" / "val"
LABELS_VAL = ROOT / "data" / "labeled" / "labels" / "val"
VAL_RATIO = 0.10
SEED = 42

def main():
    IMAGES_VAL.mkdir(parents=True, exist_ok=True)
    LABELS_VAL.mkdir(parents=True, exist_ok=True)

    pngs = sorted(IMAGES_TRAIN.glob("syn_*.png"))
    if not pngs:
        print("Nenhum syn_*.png em", IMAGES_TRAIN)
        return
    random.seed(SEED)
    n_val = max(1, int(len(pngs) * VAL_RATIO))
    to_val = set(random.sample(pngs, n_val))

    moved = 0
    for png in to_val:
        stem = png.stem
        txt = LABELS_TRAIN / f"{stem}.txt"
        if not txt.exists():
            print("Aviso: sem label", txt.name)
            continue
        png.rename(IMAGES_VAL / png.name)
        txt.rename(LABELS_VAL / txt.name)
        moved += 1
    print(f"Movidos {moved} pares (imagem + label) para val (~{VAL_RATIO*100:.0f}%)")
    print(f"  Train: {len(pngs) - moved} | Val: {moved}")

if __name__ == "__main__":
    main()
