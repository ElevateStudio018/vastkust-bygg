"""Gör webbversioner av bilderna från nuvarande hemsida (skrapat/original/) till docs/img/.

Kör efter scripts/skrapa.py:  python3 scripts/bilder.py
Kräver Pillow (pip install pillow).

- docs/img/foto/<namn>.jpg (högst 1800 px på längsta ledden) och <namn>-s.jpg (högst 800 px)
- docs/img/<märke>.png – certifikat- och försäkringsloggor, högst 480 px
- docs/img/logo-ljus.png (vit text, för mörk bakgrund), logo-mork.png (mörk text, för ljus bakgrund),
  favicon.png och apple-touch-icon.png (V:et) – loggan ligger på svart botten i originalet
"""
import pathlib
import sys

from PIL import Image, ImageOps

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import innehall as C  # noqa: E402

SRC = pathlib.Path("skrapat/original")
OUT = pathlib.Path("docs/img")
INK = (14, 17, 22)


def fit(im, size):
    im = im.copy()
    im.thumbnail((size, size), Image.LANCZOS)
    return im


def photos():
    d = OUT / "foto"
    d.mkdir(parents=True, exist_ok=True)
    for name, src in C.PHOTOS.items():
        im = ImageOps.exif_transpose(Image.open(SRC / src)).convert("RGB")
        fit(im, 1800).save(d / f"{name}.jpg", "JPEG", quality=80, optimize=True, progressive=True)
        fit(im, 800).save(d / f"{name}-s.jpg", "JPEG", quality=76, optimize=True, progressive=True)


def badges():
    for name, src in C.BADGES.items():
        im = ImageOps.exif_transpose(Image.open(SRC / src)).convert("RGBA")
        fit(im, 480).save(OUT / f"{name}.png", optimize=True)


def logo():
    """Svart botten blir genomskinlig. Blått behålls, vitt blir vitt eller mörkt beroende på version."""
    im = Image.open(SRC / C.LOGO_SRC).convert("RGB")
    px = im.load()
    w, h = im.size
    light = Image.new("RGBA", im.size, (0, 0, 0, 0))
    dark = Image.new("RGBA", im.size, (0, 0, 0, 0))
    lp, dp = light.load(), dark.load()
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            a = max(r, g, b)
            if a < 8:
                continue
            blue = b > r + 40
            col = (36, 151, 255) if blue else (255, 255, 255)
            lp[x, y] = col + (a,)
            dp[x, y] = ((36, 151, 255) if blue else INK) + (a,)
    box = light.getbbox()
    for img, name in ((light, "logo-ljus.png"), (dark, "logo-mork.png")):
        c = img.crop(box)
        c = c.resize((900, round(c.height * 900 / c.width)), Image.LANCZOS)
        c.save(OUT / name, optimize=True)
    # Favicon: bara det blå V:et ovanför linjen, på mörk ruta
    lc = light.crop(box)
    lpx = lc.load()
    line = next(y for y in range(lc.height)
                if sum(1 for x in range(0, lc.width, 4) if lpx[x, y][3] > 128 and lpx[x, y][2] > lpx[x, y][0] + 40)
                > lc.width / 4 * 0.6)
    v_only = lc.crop((0, 0, int(lc.width * 0.4), line - 2))
    v_only.putdata([c if c[2] > c[0] + 40 else (0, 0, 0, 0) for c in v_only.getdata()])
    v_only = v_only.crop(v_only.getbbox())
    for size, name in ((64, "favicon.png"), (180, "apple-touch-icon.png")):
        tile = Image.new("RGBA", (size, size), INK + (255,))
        v = v_only.copy()
        v.thumbnail((int(size * 0.62), int(size * 0.62)), Image.LANCZOS)
        tile.alpha_composite(v, ((size - v.width) // 2, (size - v.height) // 2))
        tile.save(OUT / name, optimize=True)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    photos()
    badges()
    logo()
    print("Klart:", len(list(OUT.rglob("*.*"))), "filer i", OUT)
