#!/usr/bin/env python3
"""
Move ~10% dos pares (imagem + label) de data/labeled/images/train e labels/train
para data/labeled/images/val e labels/val.

Agora considera TODAS as imagens em train (syn_*, flow_*, yolo_*, etc.), não só syn_*.
Assim, após adicionar novas anotações, rode este script de novo para rebalancear.

Uso:
  python scripts/split_train_val.py
  python scripts/split_train_val.py --ratio 0.15   # 15% para val
"""
import argparse
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMAGES_TRAIN = ROOT / "data" / "labeled" / "images" / "train"
LABELS_TRAIN = ROOT / "data" / "labeled" / "labels" / "train"
IMAGES_VAL = ROOT / "data" / "labeled" / "images" / "val"
LABELS_VAL = ROOT / "data" / "labeled" / "labels" / "val"
VAL_RATIO = 0.10
SEED = 42

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}


def main():
    parser = argparse.ArgumentParser(description="Rebalanceia train/val movendo ~10% dos pares para val")
    parser.add_argument("--ratio", type=float, default=VAL_RATIO, help="Proporção para val (ex.: 0.10 = 10%%)")
    parser.add_argument("--seed", type=int, default=SEED, help="Semente para reprodutibilidade")
    args = parser.parse_args()

    IMAGES_VAL.mkdir(parents=True, exist_ok=True)
    LABELS_VAL.mkdir(parents=True, exist_ok=True)

    # Todos os pares em train que têm label
    pairs = []
    for p in IMAGES_TRAIN.iterdir():
        if not p.is_file() or p.suffix.lower() not in IMAGE_EXTS:
            continue
        stem = p.stem
        txt = LABELS_TRAIN / f"{stem}.txt"
        if txt.exists():
            pairs.append((p, txt))

    if not pairs:
        print("Nenhum par (imagem + .txt) encontrado em", IMAGES_TRAIN)
        return

    random.seed(args.seed)
    n_val = max(1, int(len(pairs) * args.ratio))
    to_val = random.sample(pairs, n_val)

    moved = 0
    for png, txt in to_val:
        try:
            png.rename(IMAGES_VAL / png.name)
            txt.rename(LABELS_VAL / txt.name)
            moved += 1
        except Exception as e:
            print(f"Aviso: não foi possível mover {png.name}: {e}")

    remaining = len(pairs) - moved
    val_total = moved + len([p for p in IMAGES_VAL.iterdir() if p.is_file() and p.suffix.lower() in IMAGE_EXTS])
    print(f"Movidos {moved} pares para val (~{args.ratio*100:.0f}%)")
    print(f"  Train: {remaining} | Val (total): {val_total}")


if __name__ == "__main__":
    main()
