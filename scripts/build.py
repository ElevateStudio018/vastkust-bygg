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
VERSION = "5"

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
        "doc": '<path d="M7 3h7l4 4v14H7z"/><path d="M14 3v4h4M10 12h5M10 16h5"/>',
        "tool": '<path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.6 2.6-2.4-.6-.6-2.4z"/>',
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
def btn(text, href, kind="blue", ic=None, arrow=False, extra=""):
    i = icon(ic) if ic else ""
    a = f'<span class="btn-arrow">{icon("arrow")}</span>' if arrow else ""
    return f'<a class="btn btn-{kind}{" has-arrow" if arrow else ""}" href="{href}"{extra}>{i}<span>{text}</span>{a}</a>'


def quote_href(typ=None):
    return "kontakt.html" + (f"?typ={quote_plus(typ)}" if typ else "") + "#offert"


def eyebrow(text):
    return f'<p class="eyebrow">{text}</p>'


NAV = [("tjanster", "Tjänster"), ("projekt.html", "Projekt"), ("trygghet.html", "Certifikat"),
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
<header class="head">
  <div class="wrap bar">
    <a class="logo" href="index.html" aria-label="{C.NAME}, till startsidan"><img src="img/logo-mork.png" alt="{C.NAME}" width="900" height="320"></a>
    <nav class="nav" aria-label="Huvudmeny"><ul>{"".join(items)}</ul></nav>
    <a class="head-tel" href="tel:{C.TEL}">{icon("phone")}{C.PHONE}</a>
    <a class="btn btn-dark btn-sm has-arrow head-cta" href="{quote_href()}"><span>Begär offert</span><span class="btn-arrow">{icon("arrow")}</span></a>
    <a class="round" href="tel:{C.TEL}" aria-label="Ring {C.PHONE}">{icon("phone")}</a>
    <button class="burger" id="menuBtn" type="button" aria-expanded="false" aria-controls="menu" aria-label="Meny"><span></span><span></span><span></span></button>
  </div>
  <nav class="menu" id="menu" aria-label="Meny" hidden>
    <div class="wrap">
      <ul>{mob}</ul>
      <p class="m-h">Tjänster</p>
      <ul>{svc}</ul>
      <div class="btns">{btn("Begär offert", quote_href(), "blue", arrow=True)}{btn("Ring " + C.PHONE, "tel:" + C.TEL, "ghost", "phone")}</div>
    </div>
  </nav>
</header>'''


def cta_band():
    return f'''<section class="cta">
  <div class="wrap cta-in">
    <div>
      <h2>Har du ett projekt på gång?</h2>
      <p>Berätta vad du vill göra så återkommer vi med en skräddarsydd offert. {C.HOURS[0][0]} {C.HOURS[0][1]}.</p>
    </div>
    <div class="btns">{btn("Begär offert", quote_href(), "light", arrow=True)}{btn(C.PHONE, "tel:" + C.TEL, "outline", "phone")}</div>
  </div>
</section>'''


def footer():
    svc = "".join(f'<li><a href="tjanst-{s["slug"]}.html">{s["title"]}</a></li>' for s in C.SERVICES)
    hours = "".join(f"<li>{d}: {t}</li>" for d, t in C.HOURS)
    return f'''<footer class="foot">
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-brand">
        <a class="logo" href="index.html" aria-label="{C.NAME}, till startsidan"><img src="img/logo-ljus.png" alt="{C.NAME}" width="900" height="320" loading="lazy"></a>
        <p>Med er hela vägen – från idé till färdigt projekt. Bygg och renovering i {C.AREA}.</p>
        <ul class="foot-certs"><li>Behörig våtrum</li><li>ID06</li><li>BAS P/U</li></ul>
      </div>
      <div><p class="foot-h">Tjänster</p><ul>{svc}</ul></div>
      <div><p class="foot-h">Västkust Bygg</p><ul><li><a href="projekt.html">Projekt</a></li><li><a href="trygghet.html">Certifikat och försäkringar</a></li><li><a href="om-oss.html">Om oss</a></li><li><a href="kontakt.html">Kontakt</a></li></ul></div>
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


def page(name, title, desc, main, image="kok-efter-1", home=False, cta=True):
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
<meta name="theme-color" content="#121418">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap">
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
{cta_band() if cta else ""}
{footer()}'''
    (OUT / name).write_text(doc, encoding="utf-8")


# --- Byggstenar ---------------------------------------------------------------------------------------------------
def hero(eb, title, lead, photo, alt, pos="50% 50%", crumbs=None, btns=None, home=False):
    cr = ""
    if crumbs:
        parts = " / ".join(f'<a href="{h}">{t}</a>' for h, t in crumbs[:-1])
        cr = f'<nav class="crumbs" aria-label="Brödsmulor">{parts} / <span aria-current="page">{crumbs[-1][1]}</span></nav>'
    b = f'<div class="btns">{btns}</div>' if btns else ""
    return f'''<section class="hero{" hero-home" if home else ""}">
  <div class="hero-bg">{img(photo, alt, pos, "100vw", lazy=False)}</div>
  <div class="wrap hero-in">{cr}{eyebrow(eb) if eb else ""}<h1>{title}</h1><p class="hero-lead">{lead}</p>{b}</div>
</section>'''


def sec_head(eb, title, right=""):
    return f'<div class="sec-head"><div>{eyebrow(eb)}<h2>{title}</h2></div>{right}</div>'


def more_link(text, href):
    return f'<a class="more" href="{href}">{text} {icon("arrow")}</a>'


def svc_tile(s):
    """JJ El-ruta: bild, rubrik nere till vänster, pil uppe till höger."""
    return (f'<li class="tile"><a href="tjanst-{s["slug"]}.html">{img(s["photo"], s["alt"], s["pos"], "(min-width: 960px) 33vw, 100vw")}'
            f'<span class="tile-go">{icon("arrow")}</span><span class="tile-text"><b>{s["title"]}</b><span>{s["short"]}</span></span></a></li>')


def services_grid(skip=None, extra=True):
    tiles = "".join(svc_tile(s) for s in C.SERVICES if s["slug"] != skip)
    if extra:
        small = "".join(f"<li>{icon('check')}{j}</li>" for j in C.SMALL_JOBS)
        tiles += (f'<li class="tile tile-list"><div><p class="tile-h">Även mindre uppdrag</p><ul>{small}</ul></div></li>'
                  f'<li class="tile tile-cta"><div><p class="tile-h">Hittar du inte det du söker?</p>'
                  f'<p>Vi tar uppdrag i alla storlekar. Berätta vad du behöver hjälp med.</p>'
                  f'{btn("Begär offert", quote_href(), "dark", arrow=True)}</div></li>')
    return f'<ul class="tiles">{tiles}</ul>'


def gallery(photos, group, captions=None, cols=4):
    captions = captions or {}
    items = "".join(
        f'<li><a href="img/foto/{n}.jpg" data-lb="{group}" data-cap="{E(captions.get(n) or alt_for(n))}">'
        f'{img(n, alt_for(n), sizes="(min-width: 960px) 25vw, 50vw")}'
        f'{f"<span class=\"g-cap\">{E(captions[n])}</span>" if n in captions else ""}</a></li>'
        for n in photos)
    return f'<ul class="gallery c{cols}">{items}</ul>'


def before_after(before, after, text=""):
    return f'''<div class="ba">
  <a class="ba-fig" href="img/foto/{before}.jpg" data-lb="ba-{before}" data-cap="Före">{img(before, alt_for(before), sizes="(min-width: 960px) 50vw, 100vw")}<span class="ba-tag">Före</span></a>
  <a class="ba-fig" href="img/foto/{after}.jpg" data-lb="ba-{before}" data-cap="Efter">{img(after, alt_for(after), sizes="(min-width: 960px) 50vw, 100vw")}<span class="ba-tag ba-after">Efter</span></a>
</div>'''


def facts():
    name, role = C.CONTACT_PERSON
    rows = [(role, name), ("Område", C.AREA), ("Våtrum", "Behörig enligt BBV"), ("Försäkring", "Länsförsäkringar"),
            ("Arbetsplats", "ID06 och personalliggare"), ("Öppettider", f"{C.HOURS[0][0]} {C.HOURS[0][1]}")]
    return '<dl class="facts">' + "".join(f"<div><dt>{a}</dt><dd>{b}</dd></div>" for a, b in rows) + "</dl>"


def about_split(heading, paras, photo="bad1-2", link=True):
    b = f'<div class="btns">{btn("Läs mer om oss", "om-oss.html", "ghost", arrow=True)}</div>' if link else ""
    return f'''<section class="sec">
  <div class="wrap split">
    <figure class="split-ph">{img(photo, "Badrum med upplyst nisch och tvättställ på trä", "50% 55%")}
      <span class="badge-round"><b>5/5</b><span>i omdömen</span></span></figure>
    <div>
      {eyebrow("Om Västkust Bygg")}
      <h2>{heading}</h2>
      {"".join(f'<p{" class=lead" if i == 0 else ""}>{p}</p>' for i, p in enumerate(paras))}
      {facts()}
      {b}
    </div>
  </div>
</section>'''


def feature(photo, alt, eb, title, text, chips, link_text, link_href, pos="50% 50%"):
    """Antonsson-blocket: bred bild med en mörk ruta som ligger över."""
    ch = "".join(f"<li>{c}</li>" for c in chips)
    return f'''<section class="sec sec-feature">
  <div class="wrap feature">
    <div class="feature-ph">{img(photo, alt, pos, "(min-width: 960px) 70vw, 100vw")}</div>
    <div class="feature-box">
      {eyebrow(eb)}
      <h2>{title}</h2>
      <p>{text}</p>
      <ul class="chips">{ch}</ul>
      <a class="btn btn-outline has-arrow" href="{link_href}"><span>{link_text}</span><span class="btn-arrow">{icon("arrow")}</span></a>
    </div>
  </div>
</section>'''


def values_band(title="Vad gör oss unika?"):
    ics = ["helmet", "tool", "users"]
    li = "".join(f'<li>{icon(ics[i])}<h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(C.VALUES))
    return f'''<section class="band">
  <div class="wrap">
    {sec_head("Varför arbeta med oss", title, f'<p class="band-lead">{C.TEAM_TEXT}</p>')}
    <ul class="values">{li}</ul>
  </div>
</section>'''


def steps():
    ics = ["phone", "pin", "doc", "tool"]
    li = "".join(f'<li><span class="step-top">{icon(ics[i])}<span class="step-no">0{i + 1}</span></span><h3>{t}</h3><p>{d}</p></li>'
                 for i, (t, d) in enumerate(C.STEPS))
    return f'<ol class="steps">{li}</ol>'


def review_card(r):
    meta = ", ".join(x for x in (r["place"], r["date"]) if x)
    return (f'<figure class="rev">{stars()}<p class="rev-job">{E(r["job"])}</p><blockquote><p>”{E(r["text"])}”</p></blockquote>'
            f'<figcaption><span class="av" aria-hidden="true">{E(r["name"][0])}</span><span><b>{E(r["name"])}</b><small>{E(meta)}</small></span></figcaption></figure>')


def reviews_sec(idx=(0, 2, 3), tint=True):
    """Alla omdömen i en rad man bläddrar i; idx styr vilket som visas först."""
    order = list(idx) + [i for i in range(len(C.REVIEWS)) if i not in idx]
    cards = "".join(f'<li>{review_card(C.REVIEWS[i])}</li>' for i in order)
    nav = (f'<div class="rev-nav"><p class="rating">{stars()}<span><b>5 av 5</b> i alla omdömen</span></p>'
           f'<span class="rev-btns"><button class="rev-prev" type="button" aria-label="Föregående omdöme" disabled>{icon("left")}</button>'
           f'<button class="rev-next" type="button" aria-label="Nästa omdöme">{icon("right")}</button></span></div>')
    return f'''<section class="sec{" tint" if tint else ""}">
  <div class="wrap">
    {sec_head("Omdömen", "Vad kunderna säger", nav)}
    <div class="rev-slider" data-slider><ul class="rev-track" tabindex="0" aria-label="Omdömen">{cards}</ul></div>
  </div>
</section>'''


def faq_sec(tint=False):
    items = "".join(f'<details><summary>{q}<span class="pm" aria-hidden="true">{icon("plus")}</span></summary><p>{a}</p></details>'
                    for q, a in C.FAQ)
    return f'''<section class="sec{" tint" if tint else ""}" id="fragor">
  <div class="wrap narrow">
    {eyebrow("Vanliga frågor")}<h2>Frågor och svar</h2>
    <div class="faq">{items}</div>
  </div>
</section>'''


def quote_form():
    opts = "".join(f"<option>{E(t)}</option>" for t in C.WORK_TYPES)
    req = '<span class="req" aria-hidden="true">*</span>'
    return f'''<form class="form" id="qform" novalidate data-endpoint="https://formsubmit.co/ajax/{C.FORM_EMAIL}">
  <p class="form-h">Begär offert</p>
  <p class="field"><label for="f-typ">Typ av projekt</label><select id="f-typ" name="Typ av projekt"><option value="">– Välj ett alternativ –</option>{opts}</select></p>
  <p class="field"><label for="f-namn">För- och efternamn{req}</label><input id="f-namn" name="Namn" autocomplete="name" required><span class="err" id="e-namn" hidden>Skriv ditt namn.</span></p>
  <div class="field-row">
    <p class="field"><label for="f-tel">Telefon{req}</label><input id="f-tel" name="Telefon" type="tel" autocomplete="tel"><span class="err" id="e-tel" hidden>Skriv telefonnummer eller e-post.</span></p>
    <p class="field"><label for="f-epost">E-post</label><input id="f-epost" name="E-post" type="email" autocomplete="email"><span class="err" id="e-epost" hidden>Kontrollera e-postadressen.</span></p>
  </div>
  <p class="field"><label for="f-ort">Ort</label><input id="f-ort" name="Ort" autocomplete="address-level2"></p>
  <p class="field"><label for="f-besk">Beskriv projektet</label><textarea id="f-besk" name="Beskrivning" rows="4" placeholder="Vad ska göras, ungefär hur stort och när?"></textarea></p>
  <p class="hp" aria-hidden="true"><label for="f-web">Lämna tomt</label><input id="f-web" name="_honey" tabindex="-1" autocomplete="off"></p>
  <p class="small">{req} Telefon eller e-post räcker.</p>
  <button class="btn btn-blue has-arrow" type="submit"><span>Skicka förfrågan</span><span class="btn-arrow">{icon("arrow")}</span></button>
  <p class="send-err" id="send-err" role="alert" hidden>Det gick inte att skicka just nu. Försök igen, mejla <a href="mailto:{C.EMAIL}">{C.EMAIL}</a> eller ring <a href="tel:{C.TEL}">{C.PHONE}</a>.</p>
</form>
<div class="done" id="qdone" tabindex="-1" hidden>
  <p class="form-h">Tack! Vi har fått din förfrågan.</p>
  <p>Vi återkommer så snart vi kan. Brådskar det, ring <a href="tel:{C.TEL}">{C.PHONE}</a>.</p>
  <p><button class="link" type="button" id="qagain">Skicka en ny förfrågan</button></p>
</div>'''


def contact_sec(tint=True):
    name, role = C.CONTACT_PERSON
    hours = "".join(f"<li><span>{d}</span><b>{t}</b></li>" for d, t in C.HOURS)
    return f'''<section class="sec{" tint" if tint else ""}" id="offert">
  <div class="wrap contact">
    <div class="contact-info">
      {eyebrow("Kontakt")}
      <h2>Kontakta oss</h2>
      <p class="lead">Få en skräddarsydd offert för ditt byggprojekt. Hör av dig så återkommer vi – vill du hellre ringa går det lika bra.</p>
      <ul class="clist">
        <li>{icon("phone")}<span><small>Telefon</small><a href="tel:{C.TEL}">{C.PHONE}</a></span></li>
        <li>{icon("mail")}<span><small>E-post</small><a href="mailto:{C.EMAIL}">{C.EMAIL}</a></span></li>
        <li>{icon("users")}<span><small>{role}</small>{name}</span></li>
        <li>{icon("pin")}<span><small>Område</small>{C.AREA} med omnejd</span></li>
      </ul>
      <p class="hours-h">Öppettider</p>
      <ul class="hours">{hours}</ul>
    </div>
    <div class="form-box">{quote_form()}</div>
  </div>
</section>'''


# --- Startsidan ---------------------------------------------------------------------------------------------------
def index():
    jobs = ["bad1-1", "kok-efter-1", "kontor-glas", "bad2-1", "bastu", "kok-detalj", "bad3-1", "kontor-3"]
    caps = {"bad1-1": "Badrum med nisch", "kok-efter-1": "Kök från golv till tak", "kontor-glas": "Glasvägg på kontor",
            "bad2-1": "Badrum under snedtak", "bastu": "Bastu", "kok-detalj": "Bänkskiva och stänkskydd",
            "bad3-1": "Duschrum", "kontor-3": "Lokalanpassning"}
    main = f'''{hero(f"Bygg och renovering · {C.AREA}", "Kompetens, noggrannhet och tydlighet",
                 "Badrum, kök, renoveringar och nybyggnation – vi är med er hela vägen, från idé till färdigt projekt.",
                 "kok-efter-1", ALTS["kok-efter-1"], "50% 62%",
                 btns=btn("Begär offert", quote_href(), "blue", arrow=True) + btn("Ring " + C.PHONE, "tel:" + C.TEL, "outline", "phone"),
                 home=True)}

<section class="sec" id="tjanster">
  <div class="wrap">
    {sec_head("Våra tjänster", "Erfaret byggföretag för alla dina behov", more_link("Alla projekt", "projekt.html"))}
    {services_grid()}
  </div>
</section>

{about_split("Ett byggföretag med kompetens", C.ABOUT)}

{feature("bad1-5", "Renoverat badrum med grå plattor och glasvägg", "Badrum", "Behörig våtrumsbyggare",
         "Vi har gått utbildning hos Byggkeramikrådet och arbetar efter branschreglerna BBV. Efter avslutad entreprenad lämnar vi ett Kvalitetsdokument till dig som beställare.",
         ["Tätskikt enligt BBV", "Kvalitetsdokument", "Plattsättning", "Helrenovering"], "Läs om badrumsrenovering", "tjanst-badrum.html", "50% 62%")}

<section class="sec tint">
  <div class="wrap">
    {sec_head("Före och efter", "Samma kök – helt nytt rum", more_link("Se köksprojektet", "projekt-kok.html"))}
    {before_after("kok-fore", "kok-efter-2")}
  </div>
</section>

<section class="sec">
  <div class="wrap">
    {sec_head("Utförda jobb", "Ett urval av våra projekt", more_link("Se alla projekt", "projekt.html"))}
    {gallery(jobs, "jobb", caps)}
  </div>
</section>

{values_band()}

<section class="sec">
  <div class="wrap">
    {sec_head("Så går det till", "Från idé till färdigt projekt")}
    {steps()}
  </div>
</section>

{reviews_sec()}
{contact_sec(tint=False)}
{faq_sec(tint=True)}'''
    page("index.html", f"Byggföretag i Göteborg och Kungsbacka – badrum, kök, renovering | {C.NAME}",
         f"{C.NAME} bygger och renoverar badrum, kök, bostäder och lokaler i {C.AREA}. Behörig våtrum, ID06 och BAS P/U. Ring {C.PHONE}.",
         main, home=True, cta=False)


# --- Tjänstesidor -------------------------------------------------------------------------------------------------
def service_page(s):
    items = "".join(f"<li>{icon('check')}{i}</li>" for i in s["items"])
    typ = s["title"]
    p = PRJ.get(s["project"]) if s["project"] else None
    if p:
        photos = [x for part in p["parts"] for x in part["photos"]][:8]
        gal = f'''<section class="sec tint">
  <div class="wrap">
    {sec_head("Från projektportföljen", p["title"], more_link("Se hela projektet", f"projekt-{p['slug']}.html"))}
    {gallery(photos, s["slug"], {k: v for part in p["parts"] for k, v in part.get("captions", {}).items()})}
  </div>
</section>'''
    else:
        gal = ""
    rel = {"badrum": (0, 1, 2), "kok": (2, 0, 4), "renovering": (3, 4, 1), "nybyggnation": (1, 2, 0)}[s["slug"]]
    main = f'''{hero(f"Tjänster · {C.AREA}", s["title"], s["short"], s["photo"], s["alt"], s["pos"],
                 [("index.html", "Start"), ("index.html#tjanster", "Tjänster"), ("", s["title"])],
                 btn("Begär offert", quote_href(typ), "blue", arrow=True) + btn("Ring " + C.PHONE, "tel:" + C.TEL, "outline", "phone"))}
<section class="sec">
  <div class="wrap svc-intro">
    <div class="prose">
      {eyebrow(s["title"])}
      <h2>{s["lead"]}</h2>
      {"".join(f"<p>{x}</p>" for x in s["body"])}
      <div class="btns">{btn("Begär offert", quote_href(typ), "blue", arrow=True)}{btn("Ring " + C.PHONE, "tel:" + C.TEL, "ghost", "phone")}</div>
    </div>
    <aside class="incl"><p class="incl-h">Det här kan ingå</p><ul>{items}</ul></aside>
  </div>
</section>
{gal}
{reviews_sec(rel, tint=not gal)}
<section class="sec{" tint" if not gal else ""}">
  <div class="wrap">
    {sec_head("Fler tjänster", "Det här gör vi också")}
    <ul class="tiles">{"".join(svc_tile(o) for o in C.SERVICES if o["slug"] != s["slug"])}</ul>
  </div>
</section>'''
    page(f'tjanst-{s["slug"]}.html', f'{s["title"]} i Göteborg och Kungsbacka | {C.NAME}',
         f'{s["title"]} i {C.AREA}. {s["short"]} Ring {C.PHONE}.', main, image=s["photo"])


# --- Projekt ------------------------------------------------------------------------------------------------------
def project_card(p):
    n = sum(len(x["photos"]) for x in p["parts"])
    return (f'<li class="card"><a href="projekt-{p["slug"]}.html"><span class="card-ph">{img(p["cover"], alt_for(p["cover"]), "50% 55%", "(min-width: 960px) 33vw, 100vw")}'
            f'<span class="card-tag">{n} bilder</span></span><span class="card-body"><b>{p["title"]}</b><span>{p["intro"]}</span>'
            f'<span class="card-more">Se projektet {icon("arrow")}</span></span></a></li>')


def projects_page():
    cards = "".join(project_card(p) for p in C.PROJECTS)
    main = f'''{hero("Projektportfölj", "Våra projekt", "Badrum, kök och lokalanpassningar – bilder direkt från våra arbetsplatser.",
                 "bad1-3", "Renoverat badrum med grå plattor", "50% 55%", [("index.html", "Start"), ("", "Projekt")])}
<section class="sec">
  <div class="wrap">
    {sec_head("Projektportfölj", "Välj ett projekt")}
    <ul class="cards">{cards}</ul>
  </div>
</section>
<section class="sec tint">
  <div class="wrap">
    {sec_head("Före och efter", "Badrum under snedtak", more_link("Se badrumsprojekten", "projekt-badrum.html"))}
    {before_after("bad2-fore", "bad2-1")}
  </div>
</section>
<section class="sec">
  <div class="wrap">
    {sec_head("Före och efter", "Köket som byggdes om från golv till tak", more_link("Se köksprojektet", "projekt-kok.html"))}
    {before_after("kok-fore", "kok-efter-2")}
  </div>
</section>'''
    page("projekt.html", f"Projekt – badrum, kök och kontor | {C.NAME}",
         "Bilder från Västkust Byggs projekt: badrumsrenoveringar, köksrenoveringar och lokalanpassningar för kontor.",
         main, image="bad1-1")


def project_page(p):
    parts = []
    for i, part in enumerate(p["parts"]):
        parts.append(f'''<section class="sec{" tint" if i % 2 == 1 else ""}">
  <div class="wrap">
    <div class="part-head">
      <div>{eyebrow(part["eyebrow"])}<h2>{part["h"]}</h2></div>
      <div>{"".join(f"<p>{t}</p>" for t in part["text"])}</div>
    </div>
    {gallery(part["photos"], f'{p["slug"]}{i}', part.get("captions"), 4 if len(part["photos"]) > 3 else 3)}
  </div>
</section>''')
    others = "".join(project_card(o) for o in C.PROJECTS if o["slug"] != p["slug"])
    svc = next((s for s in C.SERVICES if s["project"] == p["slug"]), None)
    b = btn("Begär offert", quote_href(svc["title"] if svc else None), "blue", arrow=True)
    if svc:
        b += btn(svc["title"], f'tjanst-{svc["slug"]}.html', "outline")
    main = f'''{hero("Projektportfölj", p["title"], p["intro"], p["cover"], alt_for(p["cover"]), "50% 55%",
                 [("index.html", "Start"), ("projekt.html", "Projekt"), ("", p["title"])], b)}
{"".join(parts)}
<section class="sec{" tint" if len(parts) % 2 == 1 else ""}">
  <div class="wrap">
    {sec_head("Fler projekt", "Se även")}
    <ul class="cards c2">{others}</ul>
  </div>
</section>'''
    page(f'projekt-{p["slug"]}.html', f'{p["title"]} – projekt | {C.NAME}', f'{p["intro"]} {C.NAME}, {C.AREA}.', main, image=p["cover"])


# --- Certifikat ---------------------------------------------------------------------------------------------------
def trust_page():
    cards = []
    for c in C.CERTS:
        logos = "".join(f'<img src="img/{b}.png" alt="" loading="lazy">' for b in (c.get("badge"), c.get("badge2")) if b)
        top = f'<div class="cert-logos">{logos}</div>' if logos else f'<div class="cert-logos cert-text">{icon("helmet")}<b>BAS P · BAS U</b></div>'
        cards.append(f'<li class="cert" id="{c["slug"]}">{top}<h3>{c["title"]}</h3>{"".join(f"<p>{t}</p>" for t in c["text"])}</li>')
    main = f'''{hero("Certifikat och försäkringar", "Säkra byggarbeten", C.CERTS_INTRO,
                 "bad2-under", ALTS["bad2-under"], "50% 60%", [("index.html", "Start"), ("", "Certifikat")])}
<section class="sec">
  <div class="wrap">
    {sec_head("Certifikat och försäkringar", "Säkra byggarbeten med våra certifikat och försäkringar")}
    <ul class="certs">{"".join(cards)}</ul>
  </div>
</section>
{feature("bad2-1", "Badrum under snedtak med grå plattor", "Våtrum", "Kvalitetsdokument efter varje badrum",
         "Ett badrum ska hålla i många år. Därför arbetar vi efter Byggkeramikrådets branschregler och dokumenterar tätskiktet – när badrummet är klart får du ett Kvalitetsdokument.",
         ["Byggkeramikrådet", "BBV", "Kvalitetsdokument"], "Läs om badrumsrenovering", "tjanst-badrum.html", "50% 55%")}'''
    page("trygghet.html", f"Certifikat och försäkringar – behörig våtrum, ID06, BAS P/U | {C.NAME}",
         "Västkust Bygg är behörig våtrumsbyggare enligt BBV, använder ID06, har BAS P/U-utbildning, allrisk- och ansvarsförsäkring via Länsförsäkringar och kollektivavtalade försäkringar via FORA.",
         main, image="bad2-under")


# --- Om oss -------------------------------------------------------------------------------------------------------
def about_page():
    main = f'''{hero("Om oss", "Med er hela vägen", "Kompetens, noggrannhet och tydlighet – i varje projekt, stort som litet.",
                 "kontor-glas", ALTS["kontor-glas"], "50% 45%", [("index.html", "Start"), ("", "Om oss")])}
{about_split("Ett byggföretag med kompetens", C.ABOUT + [C.TEAM_TEXT], "bad1-6", link=False)}
{values_band("Vår unika företagsidentitet")}
<section class="sec">
  <div class="wrap">
    {sec_head("Så går det till", "Från idé till färdigt projekt")}
    {steps()}
  </div>
</section>
{reviews_sec((1, 0, 4))}'''
    page("om-oss.html", f"Om oss | {C.NAME}",
         f"{C.NAME} är ett byggföretag i {C.AREA}. Kompetens, noggrannhet och tydlighet från idé till färdigt projekt.",
         main, image="kontor-glas")


# --- Kontakt ------------------------------------------------------------------------------------------------------
def contact_page():
    places = "".join(f"<li>{p}</li>" for p in C.AREA_PLACES)
    main = f'''{hero("Kontakt", "Begär offert", "Få en skräddarsydd offert för ditt byggprojekt. Vårt team är redo att hjälpa dig.",
                 "kok-efter-2", ALTS["kok-efter-2"], "50% 50%", [("index.html", "Start"), ("", "Kontakt")])}
{contact_sec(tint=False)}
<section class="sec tint">
  <div class="wrap split split-map">
    <div>
      {eyebrow("Område")}
      <h2>Vi bygger i {C.AREA}</h2>
      <p>Våra kunder finns bland annat här. Ligger ditt projekt utanför – hör av dig ändå.</p>
      <ul class="chips chips-light">{places}</ul>
      <div class="btns">{btn("Öppna i Google Maps", C.MAPS_LINK, "dark", "pin", extra=' target="_blank" rel="noopener"')}</div>
    </div>
    <div class="map"><iframe src="{C.MAP_EMBED}" title="Karta över Göteborg och Kungsbacka" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
  </div>
</section>
{faq_sec()}'''
    page("kontakt.html", f"Kontakt och offert | {C.NAME}",
         f"Begär offert från {C.NAME}. Ring {C.PHONE} eller mejla {C.EMAIL}. Måndag–fredag 08–17.", main, image="kok-efter-2", cta=False)


def not_found():
    main = f'''<section class="sec"><div class="wrap narrow">{eyebrow("404")}<h1>Sidan finns inte</h1>
<p class="lead">Länken kan vara gammal eller felstavad.</p><div class="btns">{btn("Till startsidan", "index.html", "blue", arrow=True)}{btn("Kontakt", "kontakt.html", "ghost")}</div></div></section>'''
    page("404.html", f"Sidan finns inte | {C.NAME}", "Sidan kunde inte hittas.", main, cta=False)


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
