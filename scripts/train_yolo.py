#!/usr/bin/env python3
"""
Treina o modelo YOLO para detecção de componentes em diagramas de arquitetura.
Usa data/architectures.yaml (dataset em data/labeled).

Uso (na raiz do projeto):
  python scripts/train_yolo.py
  python scripts/train_yolo.py --epochs 100
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

# Garante que o YOLO encontra o data yaml relativamente ao cwd = raiz do projeto
ROOT = Path(__file__).resolve().parent.parent
DATA_YAML = ROOT / "data" / "architectures.yaml"


def main() -> None:
    parser = argparse.ArgumentParser(description="Treino YOLO (detect) para componentes de diagramas")
    parser.add_argument("--epochs", type=int, default=50, help="Número de épocas")
    parser.add_argument("--model", default="yolov8n.pt", help="Modelo base (ex: yolov8n.pt)")
    parser.add_argument("--imgsz", type=int, default=640, help="Tamanho da imagem")
    args = parser.parse_args()

    if not DATA_YAML.is_file():
        print(f"Erro: não encontrado {DATA_YAML}", file=sys.stderr)
        sys.exit(1)

    # Ultralytics resolve paths do YAML em relação ao cwd; usar raiz do projeto
    os.chdir(ROOT)

    from ultralytics import YOLO

    model = YOLO(args.model)
    data_path = "data/architectures.yaml"
    model.train(
        data=data_path,
        epochs=args.epochs,
        imgsz=args.imgsz,
        project=str(ROOT / "runs" / "detect"),
        name="train",
        exist_ok=True,
    )
    print("Treino concluído. Pesos em runs/detect/train/weights/best.pt (ou train2, train3, ...)")


if __name__ == "__main__":
    main()
