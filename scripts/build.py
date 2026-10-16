"""Bygger docs/*.html för Västkust Bygg & Montage AB.

Kör:  python3 scripts/build.py docs

All text och alla uppgifter finns i scripts/innehall.py; layouten här, i docs/assets/site.css och docs/assets/site.js.
Ändra aldrig HTML-filerna i docs/ direkt – de skrivs över.
"""
import html
import json
import pathlib
import sys
from urllib.parse import quote_plus

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import innehall as C  # noqa: E402

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "docs")
E = html.escape
SVC = {s["slug"]: s for s in C.SERVICES}
PRJ = {p["slug"]: p for p in C.PROJECTS}
VERSION = "2"

# --- Ikoner -------------------------------------------------------------------------------------------------------
def icon(name, cls="ic"):
    paths = {
        "phone": '<path d="M21 16.5v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 1.1 3.8 2 2 0 0 1 3.1 1.6h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L7.1 9.5a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>',
        "mail": '<rect x="2.5" y="4.5" width="19" height="15" rx="2"/><path d="m3 6 9 7 9-7"/>',
        "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
        "pin": '<path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
        "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
        "drop": '<path d="M12 3s6 6.4 6 11a6 6 0 0 1-12 0c0-4.6 6-11 6-11z"/>',
        "id": '<rect x="3" y="5" width="18" height="14" rx="2"/><circle cx="9" cy="11" r="2.2"/><path d="M5.8 16c.6-1.5 1.8-2.3 3.2-2.3s2.6.8 3.2 2.3M14 10h4M14 13.5h3"/>',
        "helmet": '<path d="M4 16a8 8 0 0 1 16 0"/><path d="M2.5 16h19v2.5h-19z"/><path d="M10 8.3V6h4v2.3"/>',
        "shield": '<path d="M12 3 4.5 6v5.5c0 4.6 3.2 8.3 7.5 9.5 4.3-1.2 7.5-4.9 7.5-9.5V6z"/><path d="m8.8 12 2.2 2.2 4.3-4.4"/>',
        "users": '<circle cx="9" cy="8" r="3.2"/><path d="M3 20c.7-3.4 3-5.3 6-5.3s5.3 1.9 6 5.3"/><circle cx="17.2" cy="9" r="2.4"/><path d="M16.5 14.6c2.4.2 4 1.9 4.5 4.6"/>',
        "check": '<path d="m5 12.5 4.5 4.5L19 7.5"/>',
        "plus": '<path d="M12 5v14M5 12h14"/>',
        "star": '<path d="m12 2.8 2.8 5.8 6.3.9-4.6 4.4 1.1 6.3L12 17.2l-5.6 3 1.1-6.3-4.6-4.4 6.3-.9z"/>',
        "close": '<path d="M6 6l12 12M18 6 6 18"/>',
        "left": '<path d="M15 5l-7 7 7 7"/>',
        "right": '<path d="M9 5l7 7-7 7"/>',
        "chev": '<path d="m6 9 6 6 6-6"/>',
        "expand": '<path d="M9 3H3v6M15 3h6v6M9 21H3v-6M15 21h6v-6"/>',
    }
    fill = ' fill="currentColor" stroke="none"' if name == "star" else ' fill="none" stroke="currentColor"'
    return (f'<svg class="{cls}" viewBox="0 0 24 24"{fill} stroke-width="1.8" stroke-linecap="round" '
            f'stroke-linejoin="round" aria-hidden="true">{paths[name]}</svg>')


def stars():
    return f'<span class="stars" role="img" aria-label="5 av 5 stjärnor">{icon("star") * 5}</span>'


# --- Bilder -------------------------------------------------------------------------------------------------------
def img(name, alt, pos="50% 50%", sizes="(min-width: 960px) 50vw, 100vw", lazy=True, cls=""):
    c = f' class="{cls}"' if cls else ""
    load = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    return (f'<img{c} src="img/foto/{name}.jpg" srcset="img/foto/{name}-s.jpg 800w, img/foto/{name}.jpg 1800w" '
            f'sizes="{sizes}" alt="{E(alt)}"{load} decoding="async" style="object-position:{pos}">')


ALTS = {
    "kok-fore": "Köket före renoveringen med gamla luckor, kakel och korkmatta",
    "kok-efter-1": "Det nya köket med ljusa trästommar, massiv bänkskiva och inbyggda vitvaror",
    "kok-efter-2": "Det nya köket från andra hållet med fönster och spotlightskena",
    "kok-detalj": "Detalj av bänkskiva, häll och stänkskydd i marmormönster",
    "bad2-fore": "Badrummet före med badkar och plastmatta",
    "bad2-under": "Duschhörna med nya plattor och golvbrunn under arbetet",
    "bastu": "Bastu med lavar i trä",
    "kontor-glas": "Glasvägg mot mötesrum i en ombyggd kontorslokal",
    "kontor-klar": "Färdig vägg och glasdörr i kontoret",
}


def alt_for(name):
    if name in ALTS:
        return ALTS[name]
    if name.startswith("bad"):
        return "Badrum renoverat av Västkust Bygg"
    if name.startswith("kontor"):
        return "Kontorslokal under ombyggnad med nya väggar"
    return "Projekt av Västkust Bygg"


# --- Delar --------------------------------------------------------------------------------------------------------
def btn(label, href, kind="blue", ic=None, arrow=False, extra=""):
    i = icon(ic) if ic else ""
    a = icon("arrow") if arrow else ""
    return f'<a class="btn btn-{kind}" href="{href}"{extra}>{i}<span>{label}</span>{a}</a>'


def quote_href(typ=None):
    return "kontakt.html" + (f"?typ={quote_plus(typ)}" if typ else "") + "#offert"


def label(text):
    return f'<p class="label">{text}</p>'


NAV = [("tjanster", "Tjänster"), ("projekt.html", "Projekt"), ("trygghet.html", "Trygghet"),
       ("om-oss.html", "Om oss"), ("kontakt.html", "Kontakt")]


def header(active):
    svc = "".join(f'<li><a href="tjanst-{s["slug"]}.html"{" aria-current=\"page\"" if active == "tjanst-" + s["slug"] + ".html" else ""}>{s["title"]}</a></li>'
                  for s in C.SERVICES)
    items = []
    for href, text in NAV:
        if href == "tjanster":
            on = " on" if active.startswith("tjanst-") else ""
            items.append(f'<li class="has-sub{on}"><a href="index.html#tjanster">{text}{icon("chev", "ic chev")}</a><ul class="sub">{svc}</ul></li>')
        else:
            cur = ' aria-current="page"' if active == href or (href == "projekt.html" and active.startswith("projekt")) else ""
            items.append(f'<li><a href="{href}"{cur}>{text}</a></li>')
    mob = "".join(f'<li><a href="{h if h != "tjanster" else "index.html#tjanster"}">{t}</a></li>' for h, t in NAV)
    return f'''<a class="skip" href="#main">Hoppa till innehållet</a>
<div class="topbar">
  <div class="wrap topbar-in">
    <span>{C.AREA} · {C.HOURS_SHORT}</span>
    <span class="topbar-r">
      <a href="tel:{C.TEL}">{icon("phone")}{C.PHONE}</a>
      <a href="mailto:{C.EMAIL}">{icon("mail")}{C.EMAIL}</a>
    </span>
  </div>
</div>
<header class="head">
  <div class="wrap bar">
    <a class="logo" href="index.html" aria-label="{C.NAME}, till startsidan"><img src="img/logo-mork.png" alt="{C.NAME}" width="900" height="320"></a>
    <nav class="nav" aria-label="Huvudmeny"><ul>{"".join(items)}</ul></nav>
    <a class="btn btn-blue btn-sm head-cta" href="{quote_href()}"><span>Få offert</span></a>
    <a class="round" href="tel:{C.TEL}" aria-label="Ring {C.PHONE}">{icon("phone")}</a>
    <button class="burger" id="menuBtn" type="button" aria-expanded="false" aria-controls="menu" aria-label="Meny"><span></span><span></span><span></span></button>
  </div>
  <nav class="menu" id="menu" aria-label="Meny" hidden>
    <div class="wrap">
      <ul>{mob}</ul>
      <p class="m-h">Tjänster</p>
      <ul>{svc}</ul>
      <div class="btns">{btn("Få offert", quote_href())}{btn("Ring " + C.PHONE, "tel:" + C.TEL, "ghost", "phone")}</div>
    </div>
  </nav>
</header>'''


def cta_band():
    return f'''<section class="cta">
  <div class="wrap cta-in">
    <div>
      <h2>Har du ett projekt på gång?</h2>
      <p>Berätta vad du vill göra så återkommer vi med en skräddarsydd offert.</p>
    </div>
    <div class="btns">{btn("Ring " + C.PHONE, "tel:" + C.TEL, "dark", "phone")}{btn("Få offert", quote_href(), "light", arrow=True)}</div>
  </div>
</section>'''


def footer():
    svc = "".join(f'<li><a href="tjanst-{s["slug"]}.html">{s["title"]}</a></li>' for s in C.SERVICES)
    prj = "".join(f'<li><a href="projekt-{p["slug"]}.html">{p["title"]}</a></li>' for p in C.PROJECTS)
    hours = "".join(f"<li>{d}: {t}</li>" for d, t in C.HOURS)
    return f'''<footer class="foot">
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-brand">
        <a class="logo" href="index.html" aria-label="{C.NAME}, till startsidan"><img src="img/logo-ljus.png" alt="{C.NAME}" width="900" height="320" loading="lazy"></a>
        <p>Bygg och renovering i {C.AREA}. Behörig våtrum, ID06 och BAS P/U.</p>
      </div>
      <div><p class="foot-h">Tjänster</p><ul>{svc}</ul></div>
      <div><p class="foot-h">Projekt</p><ul>{prj}</ul></div>
      <div><p class="foot-h">Västkust Bygg</p><ul><li><a href="trygghet.html">Trygghet och certifikat</a></li><li><a href="om-oss.html">Om oss</a></li><li><a href="kontakt.html">Kontakt</a></li></ul></div>
      <div>
        <p class="foot-h">Kontakt</p>
        <ul>
          <li><a href="tel:{C.TEL}">{C.PHONE}</a></li>
          <li><a href="mailto:{C.EMAIL}">{C.EMAIL}</a></li>
          {hours}
        </ul>
      </div>
    </div>
    <div class="foot-end">
      <span>© <span data-year>2026</span> {C.NAME}</span>
      <a href="https://elevatestudio.nu" target="_blank" rel="noopener">Byggd av Elevate Studio</a>
    </div>
  </div>
</footer>
<div class="lb" id="lb" hidden role="dialog" aria-modal="true" aria-label="Bildvisning">
  <button class="lb-x" type="button" aria-label="Stäng">{icon("close")}</button>
  <button class="lb-prev" type="button" aria-label="Föregående bild">{icon("left")}</button>
  <figure><img alt=""><figcaption></figcaption></figure>
  <button class="lb-next" type="button" aria-label="Nästa bild">{icon("right")}</button>
</div>
<script src="assets/site.js?v={VERSION}" defer></script>
</body>
</html>
'''


def jsonld():
    data = {
        "@context": "https://schema.org", "@type": "HomeAndConstructionBusiness", "name": C.NAME, "url": C.SITE_URL,
        "telephone": C.TEL, "email": C.EMAIL, "image": C.SITE_URL + "img/foto/kok-efter-1.jpg",
        "logo": C.SITE_URL + "img/logo-mork.png",
        "areaServed": [{"@type": "City", "name": n} for n in ("Göteborg", "Kungsbacka", "Mölndal")],
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
                                       "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                                       "opens": "08:00", "closes": "17:00"}],
    }
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'


def page(name, title, desc, main, image="kok-efter-1", home=False):
    url = C.SITE_URL + ("" if name == "index.html" else name)
    doc = f'''<!doctype html>
<html lang="sv">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:locale" content="sv_SE">
<meta property="og:site_name" content="{C.NAME}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:image" content="{C.SITE_URL}img/foto/{image}.jpg">
<meta name="theme-color" content="#1b1c1d">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="assets/site.css?v={VERSION}">
<link rel="icon" href="img/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="img/apple-touch-icon.png">
{jsonld() if home else ""}
</head>
<body>
{header(name)}
<main id="main">
{main}
</main>
{cta_band() if name not in ("kontakt.html", "404.html") else ""}
{footer()}'''
    (OUT / name).write_text(doc, encoding="utf-8")


# --- Byggstenar ---------------------------------------------------------------------------------------------------
def hero(title, lead, photos, crumbs=None, btns=None, home=False):
    """Syd-hero: bilden inom sidans marginaler, rubrik och en rad nere till vänster. Flera bilder = bildspel."""
    slides = "".join(f'<div class="slide{" on" if i == 0 else ""}">{img(n, a, pos, "100vw", lazy=i > 0)}</div>'
                     for i, (n, a, pos) in enumerate(photos))
    cr = ""
    if crumbs:
        parts = " / ".join(f'<a href="{h}">{t}</a>' for h, t in crumbs[:-1])
        cr = f'<nav class="crumbs" aria-label="Brödsmulor">{parts} / <span aria-current="page">{crumbs[-1][1]}</span></nav>'
    b = f'<div class="btns">{btns}</div>' if btns else ""
    return f'''<section class="hero{" hero-home" if home else ""}">
  <div class="hero-frame">
    <div class="hero-bg{" slides" if len(photos) > 1 else ""}">{slides}</div>
    <div class="hero-in">{cr}<h1>{title}</h1><p class="hero-lead">{lead}</p>{b}</div>
    <a class="hero-down" href="#main-start" aria-label="Till innehållet">{icon("chev")}</a>
  </div>
</section>
<span id="main-start"></span>'''


def intro(lab, title, paras, btns=None, narrow=True):
    b = f'<div class="btns">{btns}</div>' if btns else ""
    return f'''<section class="sec">
  <div class="wrap{" narrow" if narrow else ""} intro">
    {label(lab)}
    <h2>{title}</h2>
    {"".join(f"<p>{p}</p>" for p in paras)}
    {b}
  </div>
</section>'''


def trust_strip():
    items = [
        ("drop", "Behörig våtrum", "Byggkeramikrådets regler, BBV"),
        ("id", "ID06", "Personalliggare och ID-kort"),
        ("helmet", "BAS P och BAS U", "Byggarbetsmiljösamordning"),
        ("shield", "Försäkrade", "Länsförsäkringar och FORA"),
    ]
    li = "".join(f'<li>{icon(i)}<span><b>{t}</b><small>{s}</small></span></li>' for i, t, s in items)
    return f'<section class="trust" aria-label="Certifikat och försäkringar"><ul class="wrap trust-in">{li}</ul></section>'


def panel(text_html, media_html, flip=False, pid="", white=False):
    i = f' id="{pid}"' if pid else ""
    cls = "panel" + (" flip" if flip else "") + (" white" if white else "")
    return f'''<section class="pwrap"{i}>
  <div class="wrap">
    <div class="{cls}">
      <div class="panel-text"><div class="sticky">{text_html}</div></div>
      <div class="panel-media">{media_html}</div>
    </div>
  </div>
</section>'''


def mosaic(photos, tile=None, captions=None, group="g"):
    captions = captions or {}
    out = []
    for i, n in enumerate(photos):
        cap = captions.get(n, "")
        tag = f'<span class="tag">{E(cap)}</span>' if cap else ""
        wide = " wide" if i == 0 else ""
        out.append(f'<a class="m-item{wide}" href="img/foto/{n}.jpg" data-lb="{group}" data-cap="{E(cap or alt_for(n))}">'
                   f'{img(n, alt_for(n), sizes="(min-width: 960px) 30vw, 50vw")}{tag}</a>')
        if tile and (i == 2 or (len(photos) <= 2 and i == len(photos) - 1)):
            out.append(f'<div class="m-tile"><p>{E(tile)}</p></div>')
    return f'<div class="mosaic">{"".join(out)}</div>'


def before_after(before, after):
    return f'''<div class="ba">
  <a class="ba-fig" href="img/foto/{before}.jpg" data-lb="ba-{before}" data-cap="Före">{img(before, alt_for(before), sizes="(min-width: 960px) 30vw, 50vw")}<span class="tag">Före</span></a>
  <a class="ba-fig" href="img/foto/{after}.jpg" data-lb="ba-{before}" data-cap="Efter">{img(after, alt_for(after), sizes="(min-width: 960px) 30vw, 50vw")}<span class="tag tag-blue">Efter</span></a>
</div>'''


def svc_tile(s, big=False):
    """Syd-ruta: stor bild, text uppe till vänster, vit pill-knapp nere till vänster."""
    return (f'<li class="tile{" big" if big else ""}"><a href="tjanst-{s["slug"]}.html">'
            f'{img(s["photo"], s["alt"], s["pos"], "(min-width: 960px) 50vw, 100vw")}'
            f'<span class="tile-text"><span class="label">{s["nav"]}</span><b>{s["title"]}</b><span>{s["short"]}</span></span>'
            f'<span class="tile-btn">{s["title"]} {icon("arrow")}</span></a></li>')


def project_card(p):
    n = sum(len(x["photos"]) for x in p["parts"])
    return (f'<li class="card"><a href="projekt-{p["slug"]}.html"><span class="card-ph">{img(p["cover"], alt_for(p["cover"]), "50% 55%", "(min-width: 960px) 33vw, 100vw")}</span>'
            f'<span class="card-meta">{p["tag"]} · {n} bilder</span><b>{p["title"]}</b><span class="card-txt">{p["intro"]}</span>'
            f'<span class="btn btn-blue btn-xs">Se projektet {icon("arrow")}</span></a></li>')


def review_card(r):
    meta = ", ".join(x for x in (r["place"], r["date"]) if x)
    return (f'<figure class="rev">{stars()}<blockquote><p>{E(r["text"])}</p></blockquote>'
            f'<figcaption><b>{E(r["name"])}</b> · {E(meta)}<span>{E(r["job"])}</span></figcaption></figure>')


def badges_grid():
    cells = [("badge-vatrum", "Behörig våtrum"), ("badge-id06", "ID06"), ("badge-lf", "Länsförsäkringar"), ("badge-fora", "FORA")]
    out = "".join(f'<li><a href="trygghet.html#{a}"><img src="img/{b}.png" alt="{t}" loading="lazy"><span>{t}</span></a></li>'
                  for (b, t), a in zip(cells, ("vatrum", "id06", "forsakring", "forsakring")))
    out += '<li class="bas"><a href="trygghet.html#bas"><b>BAS P / BAS U</b><span>Byggarbetsmiljösamordning</span></a></li>'
    return f'<ul class="badges">{out}</ul>'


def steps():
    li = "".join(f'<li><span class="step-no">{i + 1}</span><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(C.STEPS))
    return f'<ol class="steps">{li}</ol>'


def faq_block(head=True):
    items = "".join(f'<details><summary>{q}<span class="pm" aria-hidden="true"></span></summary><p>{a}</p></details>'
                    for q, a in C.FAQ)
    side = (f'<div>{label("Vanliga frågor")}<h2>Frågor och svar</h2><p>Hittar du inte svaret? Ring <a href="tel:{C.TEL}">{C.PHONE}</a> '
            f'eller mejla <a href="mailto:{C.EMAIL}">{C.EMAIL}</a>.</p></div>') if head else ""
    return f'<section class="sec"><div class="wrap faq-wrap">{side}<div class="faq">{items}</div></div></section>'


def quote_form():
    opts = "".join(f"<option>{E(t)}</option>" for t in C.WORK_TYPES)
    req = '<span class="req" aria-hidden="true">*</span>'
    return f'''<form class="form" id="qform" novalidate data-endpoint="https://formsubmit.co/ajax/{C.FORM_EMAIL}">
  <p class="field"><label for="f-typ">Typ av projekt</label><select id="f-typ" name="Typ av projekt"><option value="">– Välj –</option>{opts}</select></p>
  <div class="field-row">
    <p class="field"><label for="f-namn">Namn{req}</label><input id="f-namn" name="Namn" autocomplete="name" required><span class="err" id="e-namn" hidden>Skriv ditt namn.</span></p>
    <p class="field"><label for="f-ort">Ort</label><input id="f-ort" name="Ort" autocomplete="address-level2"></p>
  </div>
  <div class="field-row">
    <p class="field"><label for="f-tel">Telefon{req}</label><input id="f-tel" name="Telefon" type="tel" autocomplete="tel"><span class="err" id="e-tel" hidden>Skriv telefonnummer eller e-post.</span></p>
    <p class="field"><label for="f-epost">E-post</label><input id="f-epost" name="E-post" type="email" autocomplete="email"><span class="err" id="e-epost" hidden>Kontrollera e-postadressen.</span></p>
  </div>
  <p class="field"><label for="f-besk">Berätta om projektet</label><textarea id="f-besk" name="Beskrivning" rows="5" placeholder="Vad ska göras, ungefär hur stort och när?"></textarea></p>
  <p class="hp" aria-hidden="true"><label for="f-web">Lämna tomt</label><input id="f-web" name="_honey" tabindex="-1" autocomplete="off"></p>
  <p class="small">{req} Telefon eller e-post räcker. Uppgifterna används bara för att svara dig.</p>
  <p><button class="btn btn-blue" type="submit"><span>Skicka förfrågan</span></button></p>
  <p class="send-err" id="send-err" role="alert" hidden>Det gick inte att skicka just nu. Försök igen, mejla <a href="mailto:{C.EMAIL}">{C.EMAIL}</a> eller ring <a href="tel:{C.TEL}">{C.PHONE}</a>.</p>
</form>
<div class="done" id="qdone" tabindex="-1" hidden>
  <p class="done-h">Tack! Vi har fått din förfrågan.</p>
  <p>Vi återkommer så snart vi kan. Brådskar det, ring <a href="tel:{C.TEL}">{C.PHONE}</a>.</p>
  <p><button class="link" type="button" id="qagain">Skicka en ny förfrågan</button></p>
</div>'''


# --- Startsidan ---------------------------------------------------------------------------------------------------
def index():
    tiles = "".join(svc_tile(s, big=i == 0) for i, s in enumerate(C.SERVICES))
    small = "".join(f'<li class="pill">{j}</li>' for j in C.SMALL_JOBS)
    values = "".join(f'<li><h3>{t}</h3><p>{d}</p></li>' for t, d in C.VALUES)
    cards = "".join(project_card(p) for p in C.PROJECTS)
    reviews = "".join(review_card(r) for r in C.REVIEWS[:3])
    name, role = C.CONTACT_PERSON
    main = f'''{hero("Kompetens, noggrannhet och tydlighet",
                 f"Badrum, kök, renovering och nybyggnation i {C.AREA}. Med er hela vägen – från idé till färdigt projekt.",
                 [("kok-efter-1", ALTS["kok-efter-1"], "50% 60%"), ("bad1-5", "Renoverat badrum med grå plattor", "50% 62%"),
                  ("kontor-glas", ALTS["kontor-glas"], "50% 45%")],
                 btns=btn("Få offert", quote_href(), "blue") + btn("Se våra projekt", "projekt.html", "light"), home=True)}
{trust_strip()}
{intro(C.NAME, "Ett byggföretag med kompetens", C.ABOUT, btn("Om oss", "om-oss.html", "ghost") + btn("Ring " + C.PHONE, "tel:" + C.TEL, "ghost", "phone"))}

<section class="pwrap" id="tjanster">
  <div class="wrap">
    <ul class="tiles">{tiles}</ul>
    <div class="also"><p>Vi tar också mindre uppdrag:</p><ul>{small}</ul></div>
  </div>
</section>

{panel(f"""{label("Före och efter")}<h2>Samma kök, två helt olika rum</h2>
<p>Ut åkte de gamla luckorna, kaklet och korkmattan. In kom ljusa trästommar, massiv bänkskiva, stänkskydd i marmormönster och inbyggda vitvaror.</p>
<p>Väggarna rättades till innan något monterades och taket fick ny belysning.</p>
<div class="btns">{btn("Se köksprojektet", "projekt-kok.html", "blue", arrow=True)}</div>""", before_after("kok-fore", "kok-efter-2"))}

<section class="band">
  <div class="wrap band-in">
    <div class="band-head">
      {label("Varför arbeta med oss")}
      <h2>Vad gör oss unika?</h2>
      <p>{C.TEAM_TEXT}</p>
      <p class="sign"><b>{name}</b>, {role.lower()}</p>
    </div>
    <ul class="values">{values}</ul>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="box">
      <div class="box-head"><div>{label("Projektportfölj")}<h2>Senaste projekten</h2></div>{btn("Alla projekt", "projekt.html", "ghost", arrow=True)}</div>
      <ul class="cards">{cards}</ul>
    </div>
  </div>
</section>

<section class="sec sec-tight">
  <div class="wrap">
    <div class="sec-head"><div>{label("Omdömen")}<h2>Vad kunderna säger</h2></div><p class="rating">{stars()} 5 av 5 i alla omdömen</p></div>
    <div class="revs">{reviews}</div>
  </div>
</section>

{panel(f"""{label("Certifikat och försäkringar")}<h2>Säkra byggarbeten</h2>
<p>{C.CERTS_INTRO}</p>
<p>Vi är behöriga våtrumsbyggare, använder ID06 på arbetsplatsen och har utbildning i byggarbetsmiljösamordning. Bolaget har allrisk- och ansvarsförsäkring, och de anställda omfattas av kollektivavtalade försäkringar.</p>
<div class="btns">{btn("Vårt trygghetsarbete", "trygghet.html", "blue", arrow=True)}</div>""", badges_grid(), flip=True)}

<section class="sec">
  <div class="wrap">
    <div class="sec-head"><div>{label("Så går det till")}<h2>Från idé till färdigt projekt</h2></div>{btn("Få offert", quote_href(), "blue")}</div>
    {steps()}
  </div>
</section>
{faq_block()}'''
    page("index.html", f"Byggföretag i Göteborg och Kungsbacka – badrum, kök, renovering | {C.NAME}",
         f"{C.NAME} bygger och renoverar badrum, kök, bostäder och lokaler i {C.AREA}. Behörig våtrum, ID06 och BAS P/U. Ring {C.PHONE}.",
         main, home=True)


# --- Tjänstesidor -------------------------------------------------------------------------------------------------
def service_page(s):
    items = "".join(f"<li>{icon('check')}{i}</li>" for i in s["items"])
    typ = s["title"]
    p = PRJ.get(s["project"]) if s["project"] else None
    if p:
        photos = [x for part in p["parts"] for x in part["photos"]][:5]
        gallery = panel(f"""{label("Från projektportföljen")}<h2>{p["title"]}</h2><p>{p["intro"]}</p>
<div class="btns">{btn("Se hela projektet", f"projekt-{p['slug']}.html", "blue", arrow=True)}</div>""", mosaic(photos, group=s["slug"]), flip=True)
    else:
        gallery = ""
    rel = {"badrum": [0, 1, 2], "kok": [2, 0, 4], "renovering": [3, 4, 1], "nybyggnation": [1, 2, 0]}[s["slug"]]
    revs = "".join(review_card(C.REVIEWS[i]) for i in rel)
    others = "".join(svc_tile(o) for o in C.SERVICES if o["slug"] != s["slug"])
    main = f'''{hero(s["title"], s["short"], [(s["photo"], s["alt"], s["pos"])],
                 [("index.html", "Start"), ("index.html#tjanster", "Tjänster"), ("", s["title"])],
                 btn("Få offert", quote_href(typ), "blue") + btn("Ring " + C.PHONE, "tel:" + C.TEL, "light", "phone"))}
{trust_strip()}
{panel(f"""{label(s["title"])}<h2>{s["lead"]}</h2>{"".join(f"<p>{x}</p>" for x in s["body"])}
<div class="btns">{btn("Begär offert", quote_href(typ), "blue")}</div>""",
       f'<div class="incl"><p class="incl-h">Det här kan ingå</p><ul>{items}</ul></div>', white=False)}
{gallery}
<section class="sec sec-tight">
  <div class="wrap">
    <div class="sec-head"><div>{label("Omdömen")}<h2>Vad kunderna säger</h2></div><p class="rating">{stars()} 5 av 5</p></div>
    <div class="revs">{revs}</div>
  </div>
</section>
<section class="pwrap">
  <div class="wrap">
    <div class="sec-head"><div>{label("Fler tjänster")}<h2>Det här gör vi också</h2></div></div>
    <ul class="tiles n3">{others}</ul>
  </div>
</section>'''
    page(f'tjanst-{s["slug"]}.html', f'{s["title"]} i Göteborg och Kungsbacka | {C.NAME}',
         f'{s["title"]} i {C.AREA}. {s["short"]} Ring {C.PHONE}.', main, image=s["photo"])


# --- Projekt ------------------------------------------------------------------------------------------------------
def projects_page():
    cards = "".join(project_card(p) for p in C.PROJECTS)
    main = f'''{hero("Projekt", "Badrum, kök och lokalanpassningar – bilder från våra arbetsplatser.",
                 [("bad1-3", "Renoverat badrum med grå plattor", "50% 55%")], [("index.html", "Start"), ("", "Projekt")])}
<section class="sec">
  <div class="wrap">
    <div class="box"><ul class="cards">{cards}</ul></div>
  </div>
</section>
{panel(f"""{label("Före och efter")}<h2>Badrum under snedtak</h2>
<p>Ett äldre badrum med badkar och plastmatta blev ett ljust duschrum med grå plattor och böjd duschvägg.</p>
<div class="btns">{btn("Se badrumsprojekten", "projekt-badrum.html", "blue", arrow=True)}</div>""", before_after("bad2-fore", "bad2-1"))}
{panel(f"""{label("Före och efter")}<h2>Köket som byggdes om från golv till tak</h2>
<p>Gamla luckor, kakel och korkmatta ersattes med ljusa trästommar, massiv bänkskiva och inbyggda vitvaror.</p>
<div class="btns">{btn("Se köksprojektet", "projekt-kok.html", "blue", arrow=True)}</div>""", before_after("kok-fore", "kok-efter-2"), flip=True)}'''
    page("projekt.html", f"Projekt – badrum, kök och kontor | {C.NAME}",
         "Bilder från Västkust Byggs projekt: badrumsrenoveringar, köksrenoveringar och lokalanpassningar för kontor.",
         main, image="bad1-1")


def project_page(p):
    parts = []
    for i, part in enumerate(p["parts"]):
        text = f'''{label(part["eyebrow"])}<h2>{part["h"]}</h2>{"".join(f"<p>{t}</p>" for t in part["text"])}
<p class="small">{len(part["photos"])} bilder – klicka för att förstora.</p>'''
        parts.append(panel(text, mosaic(part["photos"], part.get("tile"), part.get("captions"), f'{p["slug"]}{i}'), flip=i % 2 == 1))
    others = "".join(project_card(o) for o in C.PROJECTS if o["slug"] != p["slug"])
    svc = next((s for s in C.SERVICES if s["project"] == p["slug"]), None)
    b = btn("Få offert", quote_href(svc["title"] if svc else None), "blue")
    if svc:
        b += btn(svc["title"], f'tjanst-{svc["slug"]}.html', "light")
    main = f'''{hero(p["title"], p["intro"], [(p["cover"], alt_for(p["cover"]), "50% 55%")],
                 [("index.html", "Start"), ("projekt.html", "Projekt"), ("", p["title"])], b)}
{"".join(parts)}
<section class="sec">
  <div class="wrap">
    <div class="box">
      <div class="box-head"><div>{label("Fler projekt")}<h2>Se även</h2></div></div>
      <ul class="cards n2">{others}</ul>
    </div>
  </div>
</section>'''
    page(f'projekt-{p["slug"]}.html', f'{p["title"]} – projekt | {C.NAME}', f'{p["intro"]} {C.NAME}, {C.AREA}.', main, image=p["cover"])


# --- Trygghet (efter Sydställningars säkerhetssida) ---------------------------------------------------------------
def trust_page():
    parts = []
    for i, c in enumerate(C.CERTS):
        logos = "".join(f'<span class="logo-box"><img src="img/{b}.png" alt="" loading="lazy"></span>'
                        for b in (c.get("badge"), c.get("badge2")) if b)
        text = f'''{label("Försäkringar" if c["slug"] == "forsakring" else "Certifikat")}<h2>{c["title"]}</h2>{"".join(f"<p>{t}</p>" for t in c["text"])}'''
        if c["slug"] == "bas":
            media = (f'<div class="mosaic"><div class="m-tile wide"><p><b>BAS P</b> – arbetsmiljön i projekterings- och planeringsfasen.</p>'
                     f'<p><b>BAS U</b> – arbetsmiljön i genomförandefasen.</p></div>'
                     + mosaic(c["photos"], group="bas")[len('<div class="mosaic">'):])
        elif c["photos"]:
            media = (f'<div class="logos">{logos}</div>' if logos else "") + mosaic(c["photos"], group=c["slug"])
        else:
            media = f'<div class="logos big">{logos}</div>'
        parts.append(panel(text, media, flip=i % 2 == 1, pid=c["slug"]))
    main = f'''{hero("Trygghet", "Vi bygger badrum och kök – men det vi levererar är trygghet.",
                 [("bad2-under", ALTS["bad2-under"], "50% 60%")], [("index.html", "Start"), ("", "Trygghet")])}
{intro("Certifikat och försäkringar", "Säkra byggarbeten med våra certifikat och försäkringar",
       [C.CERTS_INTRO, "Här kan du läsa om våra behörigheter, hur vi använder ID06 på arbetsplatsen, vår utbildning i arbetsmiljösamordning och försäkringarna som skyddar både dig och oss."])}
{"".join(parts)}'''
    page("trygghet.html", f"Trygghet – behörig våtrum, ID06, BAS P/U och försäkringar | {C.NAME}",
         "Västkust Bygg är behörig våtrumsbyggare enligt BBV, använder ID06, har BAS P/U-utbildning, allrisk- och ansvarsförsäkring via Länsförsäkringar och kollektivavtalade försäkringar via FORA.",
         main, image="bad2-under")


# --- Om oss -------------------------------------------------------------------------------------------------------
def about_page():
    values = "".join(f'<li><h3>{t}</h3><p>{d}</p></li>' for t, d in C.VALUES)
    name, role = C.CONTACT_PERSON
    main = f'''{hero("Om oss", "Kompetens, noggrannhet och tydlighet – i varje projekt, stort som litet.",
                 [("kontor-glas", ALTS["kontor-glas"], "50% 45%")], [("index.html", "Start"), ("", "Om oss")])}
{intro(C.NAME, "Med er hela vägen", C.ABOUT)}
{panel(f"""{label("Vårt team")}<h2>Professionellt byggande med erfarenhet</h2><p>{C.TEAM_TEXT}</p>
<div class="person"><p class="label">{role}</p><p class="person-name">{name}</p><p>Din kontaktperson genom hela projektet – från första samtalet till slutgenomgången.</p>
<div class="btns">{btn("Ring " + C.PHONE, "tel:" + C.TEL, "blue", "phone")}{btn("Mejla oss", "mailto:" + C.EMAIL, "ghost", "mail")}</div></div>""",
          mosaic(["bad1-6", "kontor-5", "kok-detalj"], "Vi är supernöjda med Västkust Bygg och Emanuel som totalrenoverat vårt badrum. – Lotta, Malevik", group="om"))}
<section class="band">
  <div class="wrap band-in">
    <div class="band-head">{label("Varför arbeta med oss")}<h2>Vår unika företagsidentitet</h2></div>
    <ul class="values">{values}</ul>
  </div>
</section>
<section class="sec">
  <div class="wrap">
    <div class="sec-head"><div>{label("Så går det till")}<h2>Från idé till färdigt projekt</h2></div></div>
    {steps()}
  </div>
</section>
<section class="sec sec-tight">
  <div class="wrap">
    <div class="sec-head"><div>{label("Omdömen")}<h2>Vad kunderna säger</h2></div></div>
    <div class="revs">{"".join(review_card(r) for r in C.REVIEWS[1:4])}</div>
  </div>
</section>'''
    page("om-oss.html", f"Om oss | {C.NAME}",
         f"{C.NAME} är ett byggföretag i {C.AREA}. Kompetens, noggrannhet och tydlighet från idé till färdigt projekt.",
         main, image="kontor-glas")


# --- Kontakt ------------------------------------------------------------------------------------------------------
def contact_page():
    places = "".join(f'<li class="pill">{p}</li>' for p in C.AREA_PLACES)
    hours = "".join(f"<li><span>{d}</span><b>{t}</b></li>" for d, t in C.HOURS)
    name, role = C.CONTACT_PERSON
    main = f'''{hero("Kontakt", "Få en skräddarsydd offert för ditt byggprojekt. Vårt team är redo att hjälpa dig.",
                 [("kok-efter-2", ALTS["kok-efter-2"], "50% 50%")], [("index.html", "Start"), ("", "Kontakt")])}
<section class="sec" id="offert">
  <div class="wrap contact">
    <div>
      {label("Offertförfrågan")}
      <h2>Berätta om ditt projekt</h2>
      <p>Fyll i formuläret så återkommer vi. Skicka gärna bilder i ett mejl efteråt – det gör offerten mer träffsäker.</p>
      {quote_form()}
    </div>
    <aside class="cbox">
      <p class="label">{role}</p>
      <p class="person-name">{name}</p>
      <ul class="clist">
        <li>{icon("phone")}<a href="tel:{C.TEL}">{C.PHONE}</a></li>
        <li>{icon("mail")}<a href="mailto:{C.EMAIL}">{C.EMAIL}</a></li>
        <li>{icon("pin")}<span>{C.AREA} med omnejd</span></li>
      </ul>
      <p class="cbox-h">Öppettider</p>
      <ul class="hours">{hours}</ul>
    </aside>
  </div>
</section>
{panel(f"""{label("Område")}<h2>Vi bygger i {C.AREA}</h2><p>Våra kunder finns bland annat här. Ligger ditt projekt utanför – hör av dig ändå.</p>
<ul class="pills">{places}</ul>
<div class="btns">{btn("Öppna i Google Maps", C.MAPS_LINK, "blue", "pin", extra=' target="_blank" rel="noopener"')}</div>""",
          f'<div class="map"><iframe src="{C.MAP_EMBED}" title="Karta över Göteborg och Kungsbacka" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>')}
{faq_block()}'''
    page("kontakt.html", f"Kontakt och offert | {C.NAME}",
         f"Begär offert från {C.NAME}. Ring {C.PHONE} eller mejla {C.EMAIL}. Måndag–fredag 08–17.", main, image="kok-efter-2")


def not_found():
    main = f'''<section class="sec"><div class="wrap narrow intro">{label("404")}<h1>Sidan finns inte</h1>
<p>Länken kan vara gammal eller felstavad.</p><div class="btns">{btn("Till startsidan", "index.html", "blue")}{btn("Kontakt", "kontakt.html", "ghost")}</div></div></section>'''
    page("404.html", f"Sidan finns inte | {C.NAME}", "Sidan kunde inte hittas.", main)


def seo_files():
    urls = (["index.html"] + [f'tjanst-{s["slug"]}.html' for s in C.SERVICES] + ["projekt.html"]
            + [f'projekt-{p["slug"]}.html' for p in C.PROJECTS] + ["trygghet.html", "om-oss.html", "kontakt.html"])
    locs = "".join(f"<url><loc>{C.SITE_URL}{'' if u == 'index.html' else u}</loc></url>" for u in urls)
    (OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{locs}</urlset>\n', encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {C.SITE_URL}sitemap.xml\n", encoding="utf-8")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    index()
    for s in C.SERVICES:
        service_page(s)
    projects_page()
    for p in C.PROJECTS:
        project_page(p)
    trust_page()
    about_page()
    contact_page()
    not_found()
    seo_files()
    print("Byggde", len(list(OUT.glob("*.html"))), "sidor i", OUT)
