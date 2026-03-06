#!/usr/bin/env python3
"""
Gera imagens sintéticas em formato de fluxograma/arquitetura (camadas + setas)
a partir dos ícones em data/icon_dataset/, com anotações YOLO já geradas.

Formato de saída: data/labeled/images/train/flow_XXXX.png e labels/train/flow_XXXX.txt
Similar ao generate_synthetic_dataset.py (syn_), mas com layout em fluxo (setas entre camadas).

Uso (na raiz do projeto):
  python scripts/generate_flowchart_dataset.py
  python scripts/generate_flowchart_dataset.py --count 50 --out-size 1280 720
"""

from __future__ import annotations

import argparse
import math
import random
from pathlib import Path

try:
    from PIL import Image, ImageDraw
except ImportError:
    raise SystemExit("Instale Pillow: pip install Pillow")

ROOT = Path(__file__).resolve().parent.parent
ICON_DATASET = ROOT / "data" / "icon_dataset"
OUT_IMAGES = ROOT / "data" / "labeled" / "images" / "train"
OUT_LABELS = ROOT / "data" / "labeled" / "labels" / "train"

# Ordem das classes (índice 0..10) = data/architectures.yaml
CLASS_ORDER = [
    "user",
    "api_gateway",
    "app_service",
    "database",
    "storage",
    "waf_firewall",
    "cdn",
    "load_balancer",
    "cache",
    "monitoring_logging",
    "identity_auth",
]
CLASS_TO_ID = {name: i for i, name in enumerate(CLASS_ORDER)}


def find_icon_dirs() -> dict[str, list[Path]]:
    """Retorna {class_name: [path/to/icon.png, ...]} para pastas que existem e têm .png."""
    out: dict[str, list[Path]] = {}
    if not ICON_DATASET.is_dir():
        return out
    for d in sorted(ICON_DATASET.iterdir()):
        if not d.is_dir():
            continue
        name = d.name
        if name not in CLASS_TO_ID:
            continue
        pngs = sorted(d.glob("*.png")) + sorted(d.glob("*.PNG"))
        if pngs:
            out[name] = pngs
    return out


def random_icon(icon_dirs: dict[str, list[Path]], class_name: str) -> Image.Image | None:
    paths = icon_dirs.get(class_name)
    if not paths:
        return None
    p = random.choice(paths)
    try:
        img = Image.open(p).convert("RGBA")
        return img
    except Exception:
        return None


def resize_icon(img: Image.Image, max_side: int) -> Image.Image:
    w, h = img.size
    if w <= 0 or h <= 0:
        return img
    scale = max_side / max(w, h)
    nw, nh = max(1, int(w * scale)), max(1, int(h * scale))
    return img.resize((nw, nh), Image.Resampling.LANCZOS)


def to_yolo_line(class_id: int, x1: float, y1: float, x2: float, y2: float, img_w: int, img_h: int) -> str:
    cx = ((x1 + x2) / 2) / img_w
    cy = ((y1 + y2) / 2) / img_h
    w = (x2 - x1) / img_w
    h = (y2 - y1) / img_h
    w = max(0.001, min(1.0, w))
    h = max(0.001, min(1.0, h))
    cx = max(0.0, min(1.0, cx))
    cy = max(0.0, min(1.0, cy))
    return f"{class_id} {cx:.6f} {cy:.6f} {w:.6f} {h:.6f}"


def draw_arrow(draw: ImageDraw.ImageDraw, x1: int, y1: int, x2: int, y2: int, width: int = 2, color: str = "#333333") -> None:
    """Desenha uma seta simples (linha + ponta triangular)."""
    draw.line([(x1, y1), (x2, y2)], fill=color, width=width)
    angle = math.atan2(y2 - y1, x2 - x1)
    head = 10
    left = (x2 - head * math.cos(angle - 2.5), y2 - head * math.sin(angle - 2.5))
    right = (x2 - head * math.cos(angle + 2.5), y2 - head * math.sin(angle + 2.5))
    draw.polygon([(x2, y2), left, right], fill=color)


def generate_one(
    icon_dirs: dict[str, list[Path]],
    out_w: int,
    out_h: int,
    icon_max_side: int = 72,
) -> tuple[Image.Image, list[tuple[int, float, float, float, float]]]:
    """
    Gera uma imagem de fluxograma e lista de (class_id, x1, y1, x2, y2) em pixels.
    Layout em camadas (de cima para baixo): user -> cdn/waf -> api_gateway -> load_balancer -> app_service(s) -> cache/database/storage; identity_auth e monitoring_logging à direita.
    """
    bg = Image.new("RGB", (out_w, out_h), (250, 250, 252))
    draw = ImageDraw.Draw(bg)
    bboxes: list[tuple[int, float, float, float, float]] = []

    # Camadas: (y_center_ratio, [lista de class_names para esta linha])
    # Algumas camadas podem ter vários ícones da mesma classe (ex.: 2x app_service).
    layers: list[tuple[float, list[str]]] = [
        (0.08, ["user"]),
        (0.22, ["cdn", "waf_firewall"]),
        (0.36, ["api_gateway"]),
        (0.50, ["load_balancer"]),
        (0.64, ["app_service", "app_service", "app_service"]),
        (0.78, ["cache", "database", "storage"]),
        (0.88, ["monitoring_logging", "identity_auth"]),
    ]

    layer_blocks: list[list[tuple[str, int, int, int, int]]] = []

    for y_ratio, class_names in layers:
        y_center = int(out_h * y_ratio)
        n = len(class_names)
        if n == 1:
            xs = [out_w // 2]
        else:
            margin = out_w * 0.12
            usable = out_w - 2 * margin
            xs = [int(margin + (i + 0.5) * usable / n) for i in range(n)]
        block: list[tuple[str, int, int, int, int]] = []
        for i, cls in enumerate(class_names):
            x_center = xs[i]
            icon = random_icon(icon_dirs, cls)
            if icon is None:
                continue
            icon = resize_icon(icon, icon_max_side)
            iw, ih = icon.size
            x1 = x_center - iw // 2
            y1 = y_center - ih // 2
            x2 = x1 + iw
            y2 = y1 + ih
            if icon.mode == "RGBA":
                bg.paste(icon, (x1, y1), icon)
            else:
                bg.paste(icon, (x1, y1))
            block.append((cls, x1, y1, x2, y2))
            cid = CLASS_TO_ID[cls]
            bboxes.append((cid, x1, y1, x2, y2))
        if block:
            layer_blocks.append(block)

    # Desenhar setas entre camadas consecutivas
    for i in range(len(layer_blocks) - 1):
        top = layer_blocks[i]
        bottom = layer_blocks[i + 1]
        for t in top:
            tx = (t[1] + t[3]) // 2
            ty2 = t[4]
            best = min(bottom, key=lambda b: abs((b[1] + b[3]) // 2 - tx))
            bx = (best[1] + best[3]) // 2
            by1 = best[2]
            draw_arrow(draw, tx, ty2, bx, by1, width=2, color="#555555")


    return bg, bboxes


def main() -> None:
    parser = argparse.ArgumentParser(description="Gera fluxogramas sintéticos com setas e labels YOLO")
    parser.add_argument("--count", type=int, default=30, help="Quantidade de imagens a gerar")
    parser.add_argument("--out-size", type=int, nargs=2, default=[1280, 720], metavar=("W", "H"), help="Largura e altura da imagem")
    parser.add_argument("--icon-size", type=int, default=72, help="Tamanho máximo do lado do ícone")
    parser.add_argument("--prefix", default="flow", help="Prefixo dos arquivos (flow_0000.png)")
    args = parser.parse_args()

    icon_dirs = find_icon_dirs()
    if not icon_dirs:
        print(f"Nenhuma pasta de ícones encontrada em {ICON_DATASET}", file=__import__("sys").stderr)
        return

    OUT_IMAGES.mkdir(parents=True, exist_ok=True)
    OUT_LABELS.mkdir(parents=True, exist_ok=True)

    # último número flow_ existente
    existing = list(OUT_IMAGES.glob(f"{args.prefix}_*.png"))
    start = 0
    for p in existing:
        try:
            stem = p.stem  # flow_0012
            num = int(stem.split("_")[-1])
            start = max(start, num + 1)
        except ValueError:
            pass

    out_w, out_h = args.out_size[0], args.out_size[1]
    for i in range(args.count):
        idx = start + i
        img, bboxes = generate_one(icon_dirs, out_w, out_h, icon_max_side=args.icon_size)
        name = f"{args.prefix}_{idx:04d}"
        img_path = OUT_IMAGES / f"{name}.png"
        lbl_path = OUT_LABELS / f"{name}.txt"
        img.save(img_path)
        lines = []
        for cid, x1, y1, x2, y2 in bboxes:
            lines.append(to_yolo_line(cid, x1, y1, x2, y2, out_w, out_h))
        lbl_path.write_text("\n".join(lines) + ("\n" if lines else ""))
        print(f"  {name}.png ({len(bboxes)} objetos)")

    print(f"Salvo em {OUT_IMAGES} e {OUT_LABELS}")


if __name__ == "__main__":
    main()
