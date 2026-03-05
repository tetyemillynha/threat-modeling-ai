import random
from pathlib import Path
from PIL import Image

# Nomes devem ser iguais às pastas em data/icon_dataset (ex.: waf_firewall, identity_auth)
ICONS_DIR = Path("data/icon_dataset")
if not ICONS_DIR.exists():
    ICONS_DIR = Path("assets/icons")

# Descobre classes que têm pelo menos um .png (evita erro se uma pasta estiver vazia)
def _discover_classes():
    if not ICONS_DIR.exists():
        return [], {}
    classes = []
    for d in sorted(ICONS_DIR.iterdir()):
        if d.is_dir() and list(d.glob("*.png")):
            classes.append(d.name)
    return classes, {c: i for i, c in enumerate(classes)}

CLASSES, CLASS_TO_ID = _discover_classes()
if not CLASSES:
    raise RuntimeError(f"Nenhuma pasta com ícones .png em {ICONS_DIR}")
OUT_IMAGES = Path("data/labeled/images/train")
OUT_LABELS = Path("data/labeled/labels/train")

OUT_IMAGES.mkdir(parents=True, exist_ok=True)
OUT_LABELS.mkdir(parents=True, exist_ok=True)

IMG_W, IMG_H = 1024, 768
CELL_COLS, CELL_ROWS = 3, 2
CELL_W, CELL_H = IMG_W // CELL_COLS, IMG_H // CELL_ROWS

def load_icon(cls):
    files = list((ICONS_DIR/cls).glob("*.png"))
    if not files:
        raise RuntimeError(f"Sem ícones em {ICONS_DIR/cls}")
    return Image.open(random.choice(files)).convert("RGBA")

def paste_icon(bg, icon, x, y, max_w, max_h):
    iw, ih = icon.size
    scale = min(max_w/iw, max_h/ih) * random.uniform(0.6, 0.9)
    new_size = (int(iw*scale), int(ih*scale))
    icon = icon.resize(new_size, Image.LANCZOS)
    ix = x + (max_w - new_size[0])//2
    iy = y + (max_h - new_size[1])//2
    bg.alpha_composite(icon, (ix, iy))
    return ix, iy, new_size[0], new_size[1]

def to_yolo_bbox(x, y, w, h):
    xc = (x + w/2) / IMG_W
    yc = (y + h/2) / IMG_H
    wn = w / IMG_W
    hn = h / IMG_H
    return xc, yc, wn, hn

def generate(n=200):
    print(f"Classes com ícones: {CLASSES}")
    for i in range(n):
        bg = Image.new("RGBA", (IMG_W, IMG_H), (255,255,255,255))
        labels = []
        grid = [(c,r) for r in range(CELL_ROWS) for c in range(CELL_COLS)]
        random.shuffle(grid)
        num_objs = random.randint(3, 6)

        for k in range(num_objs):
            cls = random.choice(CLASSES)
            icon = load_icon(cls)
            c,r = grid[k]
            x, y = c*CELL_W, r*CELL_H
            bx, by, bw, bh = paste_icon(bg, icon, x, y, CELL_W, CELL_H)
            xc, yc, wn, hn = to_yolo_bbox(bx, by, bw, bh)
            labels.append(f"{CLASS_TO_ID[cls]} {xc:.6f} {yc:.6f} {wn:.6f} {hn:.6f}")

        img_path = OUT_IMAGES / f"syn_{i:04d}.png"
        lbl_path = OUT_LABELS / f"syn_{i:04d}.txt"

        bg.convert("RGB").save(img_path)
        lbl_path.write_text("\n".join(labels))

    print(f"Geradas {n} imagens sintéticas em {OUT_IMAGES}")

if __name__ == "__main__":
    generate(200)