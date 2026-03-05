#!/usr/bin/env python3
"""
Renomeia todas as imagens em data/raw para o padrão arch_0.png, arch_1.png, ...
- Converte SVGs para PNG (requer cairosvg: pip install cairosvg).
- Converte JPG/etc. para PNG ao renomear (usa Pillow).

Uso:
  python scripts/rename_raw_images.py [--dir data/raw] [--dry-run]
"""
import argparse
import shutil
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    Image = None

# Extensões consideradas como imagem (após conversão SVG→PNG, só raster)
RASTER_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff", ".webp"}
SVG_EXTENSION = ".svg"


def convert_svg_to_png(svg_path: Path, png_path: Path) -> bool:
    """Converte um arquivo SVG para PNG. Retorna True se ok."""
    try:
        import cairosvg
    except ImportError:
        print("Aviso: instale cairosvg para converter SVG → PNG: pip install cairosvg")
        return False
    try:
        cairosvg.svg2png(url=str(svg_path), write_to=str(png_path))
        return True
    except Exception as e:
        print(f"Erro ao converter {svg_path.name}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Renomear imagens para arch_0.png, arch_1.png, ...")
    parser.add_argument("--dir", "-d", type=Path, default=Path("data/raw"), help="Pasta com as imagens")
    parser.add_argument("--dry-run", action="store_true", help="Apenas mostrar o que seria feito")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    raw_dir = args.dir if args.dir.is_absolute() else root / args.dir

    if not raw_dir.exists() or not raw_dir.is_dir():
        print(f"Pasta não encontrada: {raw_dir}")
        return 1

    # 1) Converter SVGs para PNG
    svg_files = [f for f in raw_dir.iterdir() if f.is_file() and f.suffix.lower() == SVG_EXTENSION]
    converted = 0
    for svg_path in svg_files:
        png_path = svg_path.with_suffix(".png")
        if png_path.exists() and png_path != svg_path:
            print(f"Já existe {png_path.name}, pulando conversão de {svg_path.name}")
            continue
        if args.dry_run:
            print(f"[dry-run] Converteria {svg_path.name} → {png_path.name}")
            converted += 1
            continue
        if convert_svg_to_png(svg_path, png_path):
            converted += 1
            print(f"Convertido: {svg_path.name} → {png_path.name}")
            # Remove o SVG após conversão para não contar duas vezes
            try:
                svg_path.unlink()
            except OSError as e:
                print(f"Aviso: não foi possível remover {svg_path.name}: {e}")

    if svg_files and converted == 0 and not args.dry_run:
        print("Nenhum SVG convertido (instale cairosvg ou verifique os arquivos).")

    # 2) Listar todas as imagens raster (ordenar por nome para resultado previsível)
    image_files = [
        f for f in raw_dir.iterdir()
        if f.is_file() and f.suffix.lower() in RASTER_EXTENSIONS
    ]
    image_files.sort(key=lambda p: p.name.lower())

    if not image_files:
        print("Nenhuma imagem (PNG, JPG, etc.) encontrada em", raw_dir)
        return 0

    # 3) Renomear para arch_0.png, arch_1.png, ... (em dois passos para não sobrescrever)
    temp_prefix = "__tmp_arch_"
    if args.dry_run:
        for i, f in enumerate(image_files):
            print(f"[dry-run] {f.name} → arch_{i}.png")
        return 0

    # Passo 1: renomear tudo para nomes temporários
    temp_paths = []
    for i, f in enumerate(image_files):
        temp_name = f"{temp_prefix}{i}{f.suffix}"
        temp_path = raw_dir / temp_name
        if f.resolve() != temp_path.resolve():
            shutil.move(str(f), str(temp_path))
            temp_paths.append(temp_path)

    # Passo 2: gravar como arch_0.png, arch_1.png, ... (convertendo para PNG se necessário)
    for i, temp_path in enumerate(temp_paths):
        final_path = raw_dir / f"arch_{i}.png"
        if temp_path.suffix.lower() == ".png" and temp_path.resolve() != final_path.resolve():
            shutil.move(str(temp_path), str(final_path))
        elif Image is not None:
            try:
                img = Image.open(temp_path).convert("RGB")
                img.save(final_path, "PNG")
                temp_path.unlink()
            except Exception as e:
                print(f"Erro ao converter {temp_path.name} para PNG: {e}")
                if temp_path.exists():
                    shutil.move(str(temp_path), str(final_path))
        else:
            shutil.move(str(temp_path), str(final_path))
        print(f"Renomeado: arch_{i}.png")

    print(f"Total: {len(image_files)} imagens → arch_0.png a arch_{len(image_files)-1}.png")
    return 0


if __name__ == "__main__":
    exit(main() or 0)
