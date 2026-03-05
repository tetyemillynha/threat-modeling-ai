from __future__ import annotations
import argparse
import json
from pathlib import Path

from src.detect import run_detection
from src.stride_engine import build_stride_report
from src.report import to_markdown

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", required=True, help="Caminho da imagem do diagrama")
    parser.add_argument("--model", required=True, help="Caminho do modelo YOLO (.pt)")
    parser.add_argument("--conf", type=float, default=0.25, help="Confidence threshold")
    parser.add_argument("--outdir", default="outputs", help="Pasta de saída")
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    detections = run_detection(args.image, args.model, conf=args.conf)
    stride_data = build_stride_report(detections)

    # salvar jsons
    (outdir / "detections.json").write_text(json.dumps(detections, ensure_ascii=False, indent=2), encoding="utf-8")
    (outdir / "stride_report.json").write_text(json.dumps(stride_data, ensure_ascii=False, indent=2), encoding="utf-8")

    # salvar markdown
    md = to_markdown(args.image, detections, stride_data)
    md_path = outdir / "report.md"
    md_path.write_text(md, encoding="utf-8")

if __name__ == "__main__":
    main()