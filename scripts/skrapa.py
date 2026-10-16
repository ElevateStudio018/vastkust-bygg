"""Skrapar text och bilder från nuvarande hemsida (www.vastkustbygg.se).

Kör från repots rot:  python3 scripts/skrapa.py
Texten hamnar i skrapat/text.txt (rubriker med #) och bilderna i originalstorlek i skrapat/original/
(mappen är inte incheckad). Kör sedan scripts/bilder.py för att göra webbversioner till docs/img/.
Kräver bara Pythons standardbibliotek.

vastkustbygg.se är en enda sida byggd i One.com Web Editor. Bilderna ligger på impro.usercontent.one; utan
parametrarna resize/quality hämtas originalfilen.
"""
import html
import os
import re
import urllib.parse
import urllib.request

URL = "https://www.vastkustbygg.se/"
MEDIA = re.compile(r"https://impro\.usercontent\.one/[^\"'\s)]+?/onewebmedia/([^?\"'\s)]+)")
OUT_TXT, OUT_ORIG = "skrapat/text.txt", "skrapat/original"
UA = {"User-Agent": "Mozilla/5.0 (vastkustbygg innehallsflytt)"}


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return r.read()


def text(src):
    s = re.sub(r"<head>.*?</head>|<(script|style|svg)[^>]*>.*?</\1>", "", src, flags=re.S)
    s = re.sub(r"<h([1-4])[^>]*>", lambda m: "\n\n" + "#" * int(m.group(1)) + " ", s)
    s = re.sub(r"<br\s*/?>|</(p|div|h\d|li)>", "\n", s)
    s = html.unescape(re.sub(r"<[^>]+>", "", s))
    lines = [ln.strip() for ln in s.splitlines()]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip() + "\n"


def main():
    src = get(URL).decode("utf-8")
    os.makedirs(OUT_ORIG, exist_ok=True)
    with open(OUT_TXT, "w", encoding="utf-8") as f:
        f.write(text(src))
    base = MEDIA.search(src).group(0).rsplit("/onewebmedia/", 1)[0] + "/onewebmedia/"
    names = sorted({m.group(1) for m in MEDIA.finditer(src)})
    for name in names:
        local = urllib.parse.unquote(name).replace(" ", "_")
        dest = os.path.join(OUT_ORIG, local)
        if not os.path.exists(dest):
            with open(dest, "wb") as f:
                f.write(get(base + name))
        print("  ", local)
    print(f"Text: {OUT_TXT}  Bilder: {len(names)} i {OUT_ORIG}/")


if __name__ == "__main__":
    main()
