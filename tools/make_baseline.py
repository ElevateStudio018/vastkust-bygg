"""Bygger content/baseline.json – hemsidans ursprungliga innehåll – från tools/innehall.py.

Kör efter tools/bilder.py:  python3 tools/make_baseline.py
Baseline är det sajten byggs från innan Supabase är inkopplat, och det som läggs in som första publicerade version
(supabase/migrations/20261002120400_baseline.sql, som skriptet också uppdaterar). Därefter ändras innehållet i
adminpanelen, inte här.
"""
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import innehall as C  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
SIZES = json.loads((ROOT / "lib/photo-sizes.json").read_text())
QUOTE = {"label": "Begär offert", "href": "#offert"}
NO_LINK = {"label": "", "href": "/"}


def img(name, alt="", focus=None):
    widths = SIZES[name]
    variants = [{"width": w, "src": f"/photos/{name}-{w}.webp"} for w in widths[:-1]]
    variants.append({"width": widths[-1], "src": f"/photos/{name}.webp"})
    out = {"src": f"/photos/{name}.webp", "variants": variants, "alt": alt or alt_for(name)}
    if focus:
        out["focus"] = focus
    return out


def badge(name, alt):
    return {"src": f"/photos/{name}.png", "variants": [], "alt": alt}


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


def coll(items, prefix="i"):
    """A collection (order + items) with ids made from the given keys, or numbered."""
    order, out = [], {}
    for i, item in enumerate(items):
        key = item.pop("_id", None) or f"{prefix}{i + 1}"
        order.append(key)
        out[key] = item
    return {"order": order, "items": out}


def labels(texts):
    return coll([{"label": t} for t in texts])


def section(type_, eyebrow="", anchor="", **fields):
    return {"type": type_, "hidden": False, "anchor": anchor, "label": "", "eyebrow": eyebrow, **fields}


def page_hero(eyebrow, heading, text, photo, focus=None, button=QUOTE, size="medium"):
    return sid(section("pageHero", eyebrow, heading=heading, text=text, button=button, image=img(photo, focus=focus), size=size), "bild")


def cta():
    return section("cta", heading="Har du ett projekt på gång?",
                   text="Berätta vad du vill göra så återkommer vi med en skräddarsydd offert. Måndag–fredag 08.00–17.00.",
                   button=QUOTE)


def strip_html(text):
    return re.sub(r"<[^>]+>", "", text)


def page(slug, title, seo_title, seo_desc, sections):
    return {"_id": slug or "hem", "slug": slug, "title": title, "seo": {"title": seo_title, "description": seo_desc},
            "sections": coll([dict(s, _id=s.pop("_id", None)) for s in sections], "s")}


def sid(s, key):
    s["_id"] = key
    return s


# --- Delar som återkommer ---------------------------------------------------------------------------------------
name, role = C.CONTACT_PERSON
FACTS = [(role, name), ("Område", C.AREA), ("Våtrum", "Behörig enligt BBV"), ("Försäkring", "Länsförsäkringar"),
         ("Arbetsplats", "ID06 och personalliggare"), ("Öppettider", "Måndag–fredag 08.00–17.00")]
REVIEWS = [{"_id": f"r{i + 1}", "title": r["job"], "quote": r["text"].replace(" 😃", " 😃"), "name": r["name"],
            "detail": ", ".join(x for x in (r["place"], r["date"]) if x), "rating": 5, "image": None}
           for i, r in enumerate(C.REVIEWS)]
STEP_ICONS = ["Phone", "MapPin", "FileText", "Wrench"]
VALUE_ICONS = ["HardHat", "Wrench", "Users"]


def about(photo, focus, link=True):
    return section(
        "about", "Om Västkust Bygg", heading="Ett byggföretag med kompetens", subheading=C.ABOUT[0],
        text=C.ABOUT[1] if link else C.ABOUT[1] + "\n\n" + C.TEAM_TEXT,
        facts=coll([{"label": a, "value": b} for a, b in FACTS]),
        link={"label": "Läs mer om oss", "href": "/om-oss"} if link else dict(NO_LINK),
        image=img(photo, "Badrum med upplyst nisch och tvättställ på trä" if photo == "bad1-2" else "", focus),
        badgeValue="5/5", badgeLabel="i omdömen")


def values(heading="Vad gör oss unika?"):
    return section("values", "Varför arbeta med oss", heading=heading, text=C.TEAM_TEXT,
                   items=coll([{"heading": t, "text": d, "icon": VALUE_ICONS[i]} for i, (t, d) in enumerate(C.VALUES)]))


def process():
    return section("process", "Så går det till", anchor="sa-gar-det-till", heading="Från idé till färdigt projekt", text="",
                   steps=coll([{"title": t, "description": d, "icon": STEP_ICONS[i]} for i, (t, d) in enumerate(C.STEPS)]))


def testimonials(first=(0, 2, 3)):
    order = list(first) + [i for i in range(len(REVIEWS)) if i not in first]
    return section("testimonials", "Omdömen", anchor="omdomen", heading="Vad kunderna säger", text="i alla omdömen",
                   items=coll([dict(REVIEWS[i]) for i in order]))


def contact():
    return section("contact", "Kontakt", anchor="kontakt", heading="Kontakta oss",
                   text="Få en skräddarsydd offert för ditt byggprojekt. Hör av dig så återkommer vi – vill du hellre ringa går det lika bra.",
                   phoneLabel="Telefon", emailLabel="E-post", addressLabel="Område", openingHoursLabel="Öppettider",
                   orgLabel="Org.nr", formHeading="Begär offert")


def faq():
    return section("faq", "Vanliga frågor", anchor="fragor", heading="Frågor och svar", phonePrompt="Hittar du inte svaret? Ring",
                   items=coll([{"question": q, "answer": strip_html(a)} for q, a in C.FAQ]))


def gallery(eyebrow, heading, text, photos, captions=None, link=NO_LINK, group=""):
    captions = captions or {}
    return section("gallery", eyebrow, heading=heading, text=text, link=dict(link),
                   images=coll([{"image": img(n), "caption": captions.get(n, "")} for n in photos]))


# --- Startsidan -------------------------------------------------------------------------------------------------
JOBS = ["bad1-1", "kok-efter-1", "kontor-glas", "bad2-1", "bastu", "kok-detalj", "bad3-1", "kontor-3"]
JOB_CAPS = {"bad1-1": "Badrum med nisch", "kok-efter-1": "Kök från golv till tak", "kontor-glas": "Glasvägg på kontor",
            "bad2-1": "Badrum under snedtak", "bastu": "Bastu", "kok-detalj": "Bänkskiva och stänkskydd",
            "bad3-1": "Duschrum", "kontor-3": "Lokalanpassning"}

home = page("", "Hem", "Byggföretag i Göteborg och Kungsbacka – badrum, kök, renovering",
            f"{C.NAME} bygger och renoverar badrum, kök, bostäder och lokaler i {C.AREA}. Behörig våtrum, ID06 och BAS P/U. Ring {C.PHONE}.", [
    sid(section("hero", f"Bygg och renovering · {C.AREA}", heading="Kompetens, noggrannhet och tydlighet",
                text="Badrum, kök, renoveringar och nybyggnation – vi är med er hela vägen, från idé till färdigt projekt.",
                image=img("kok-efter-1", focus="50% 62%"), button=QUOTE), "hero"),
    sid(section("services", "Våra tjänster", anchor="tjanster", heading="Erfaret byggföretag för alla dina behov",
                link={"label": "Alla projekt", "href": "/projekt"}, cardLinkPrefix="",
                moreHeading="Även mindre uppdrag", moreItems=labels(C.SMALL_JOBS),
                ctaHeading="Hittar du inte det du söker?", ctaText="Vi tar uppdrag i alla storlekar. Berätta vad du behöver hjälp med.",
                ctaButton=QUOTE), "tjanster"),
    sid(about("bad1-2", "50% 55%"), "om-oss"),
    sid(section("overlay", "Badrum", heading="Behörig våtrumsbyggare",
                text="Vi har gått utbildning hos Byggkeramikrådet och arbetar efter branschreglerna BBV. Efter avslutad entreprenad lämnar vi ett Kvalitetsdokument till dig som beställare.",
                chips=labels(["Tätskikt enligt BBV", "Kvalitetsdokument", "Plattsättning", "Helrenovering"]),
                link={"label": "Läs om badrumsrenovering", "href": "/tjanster/badrumsrenovering"},
                image=img("bad1-5", "Renoverat badrum med grå plattor och glasvägg", "50% 62%")), "vatrum"),
    sid(section("beforeAfter", "Före och efter", heading="Samma kök – helt nytt rum",
                link={"label": "Se köksprojektet", "href": "/projekt-kok"},
                beforeLabel="Före", before=img("kok-fore"), afterLabel="Efter", after=img("kok-efter-2")), "fore-efter"),
    sid(gallery("Utförda jobb", "Ett urval av våra projekt", "", JOBS, JOB_CAPS, {"label": "Se alla projekt", "href": "/projekt"}), "jobb"),
    sid(values(), "varfor"),
    sid(process(), "process"),
    sid(testimonials(), "omdomen"),
    sid(contact(), "kontakt"),
    sid(faq(), "fragor"),
])

# --- Projekt ----------------------------------------------------------------------------------------------------
PROJECT_HREF = {"badrum": "/projekt-badrum", "kok": "/projekt-kok", "kontor": "/projekt-kontor"}
projects_page = page("projekt", "Projekt", "Projekt – badrum, kök och kontor",
                     "Bilder från Västkust Byggs projekt: badrumsrenoveringar, köksrenoveringar och lokalanpassningar för kontor.", [
    page_hero("Projektportfölj", "Våra projekt", "Badrum, kök och lokalanpassningar – bilder direkt från våra arbetsplatser.", "bad1-3", "50% 55%"),
    section("uppdragGrid", "Projektportfölj", heading="Välj ett projekt", text="", filterAllLabel="Se projektet"),
    section("beforeAfter", "Före och efter", heading="Badrum under snedtak", link={"label": "Se badrumsprojekten", "href": "/projekt-badrum"},
            beforeLabel="Före", before=img("bad2-fore"), afterLabel="Efter", after=img("bad2-1")),
    section("beforeAfter", "Före och efter", heading="Köket som byggdes om från golv till tak", link={"label": "Se köksprojektet", "href": "/projekt-kok"},
            beforeLabel="Före", before=img("kok-fore"), afterLabel="Efter", after=img("kok-efter-2")),
    cta(),
])

project_pages = []
for p in C.PROJECTS:
    svc = next((s for s in C.SERVICES if s["project"] == p["slug"]), None)
    button = QUOTE
    parts = [gallery(part["eyebrow"], part["h"], "\n\n".join(part["text"]), part["photos"], part.get("captions")) for part in p["parts"]]
    project_pages.append(page(f'projekt-{p["slug"]}', p["title"], f'{p["title"]} – projekt', f'{p["intro"]} {C.NAME}, {C.AREA}.', [
        page_hero("Projektportfölj", p["title"], p["intro"], p["cover"], "50% 55%", button),
        *parts,
        cta(),
    ]))

# --- Certifikat, om oss, kontakt --------------------------------------------------------------------------------
cert_page = page("certifikat", "Certifikat", "Certifikat och försäkringar – behörig våtrum, ID06, BAS P/U",
                 "Västkust Bygg är behörig våtrumsbyggare enligt BBV, använder ID06, har BAS P/U-utbildning, allrisk- och ansvarsförsäkring via Länsförsäkringar och kollektivavtalade försäkringar via FORA.", [
    page_hero("Certifikat och försäkringar", "Säkra byggarbeten", C.CERTS_INTRO, "bad2-under", "50% 60%"),
    section("certificates", "Certifikat och försäkringar", heading="Säkra byggarbeten med våra certifikat och försäkringar", text="",
            issuerPrefix="", validUntilPrefix="Giltigt till", emptyHeading="Certifikat", emptyText="Fråga oss gärna om våra behörigheter på"),
    section("overlay", "Våtrum", heading="Kvalitetsdokument efter varje badrum",
            text="Ett badrum ska hålla i många år. Därför arbetar vi efter Byggkeramikrådets branschregler och dokumenterar tätskiktet – när badrummet är klart får du ett Kvalitetsdokument.",
            chips=labels(["Byggkeramikrådet", "BBV", "Kvalitetsdokument"]), link={"label": "Läs om badrumsrenovering", "href": "/tjanster/badrumsrenovering"},
            image=img("bad2-1", "Badrum under snedtak med grå plattor", "50% 55%")),
    cta(),
])

about_page = page("om-oss", "Om oss", "Om oss", f"{C.NAME} är ett byggföretag i {C.AREA}. Kompetens, noggrannhet och tydlighet från idé till färdigt projekt.", [
    page_hero("Om oss", "Med er hela vägen", "Kompetens, noggrannhet och tydlighet – i varje projekt, stort som litet.", "kontor-glas", "50% 45%", dict(NO_LINK, label="")),
    about("bad1-6", "50% 50%", link=False),
    values("Vår unika företagsidentitet"),
    process(),
    testimonials((1, 0, 4)),
    cta(),
])

contact_page = page("kontakt", "Kontakt", "Kontakt och offert", f"Begär offert från {C.NAME}. Ring {C.PHONE} eller mejla {C.EMAIL}. Måndag–fredag 08–17.", [
    page_hero("Kontakt", "Begär offert", "Få en skräddarsydd offert för ditt byggprojekt. Vårt team är redo att hjälpa dig.", "kok-efter-2", "50% 50%", dict(NO_LINK, label="")),
    contact(),
    section("area", "Område", heading=f"Vi bygger i {C.AREA}", text="Våra kunder finns bland annat här. Ligger ditt projekt utanför – hör av dig ändå.",
            places=labels(C.AREA_PLACES), link={"label": "Öppna i Google Maps", "href": C.MAPS_LINK}, mapQuery="Göteborg"),
    faq(),
])

# --- Tjänster, projekt och certifikat som listor ------------------------------------------------------------------
SLUGS = {"badrum": "badrumsrenovering", "kok": "koksrenovering", "renovering": "renovering-och-ombyggnation", "nybyggnation": "nybyggnation"}
ICONS = {"badrum": "Droplets", "kok": "Home", "renovering": "Hammer", "nybyggnation": "Building2"}
PRJ = {p["slug"]: p for p in C.PROJECTS}
services = []
for s in C.SERVICES:
    p = PRJ.get(s["project"])
    photos = [x for part in p["parts"] for x in part["photos"]][:8] if p else []
    caps = {k: v for part in p["parts"] for k, v in part.get("captions", {}).items()} if p else {}
    services.append({
        "_id": SLUGS[s["slug"]], "slug": SLUGS[s["slug"]], "name": s["title"], "shortDescription": s["short"], "lead": s["lead"],
        "description": s["body"], "includes": s["items"],
        "galleryHeading": p["title"] if p else "",
        "galleryLink": {"label": "Se hela projektet", "href": PROJECT_HREF[p["slug"]]} if p else dict(NO_LINK, label=""),
        "gallery": coll([{"image": img(n), "caption": caps.get(n, "")} for n in photos]),
        "icon": ICONS[s["slug"]], "image": img(s["photo"], s["alt"], s["pos"]),
        "seo": {"title": f'{s["title"]} i Göteborg och Kungsbacka', "description": f'{s["title"]} i {C.AREA}. {s["short"]} Ring {C.PHONE}.'},
    })

uppdrag = [{"_id": p["slug"], "tag": p["tag"], "title": p["title"], "text": p["intro"], "href": PROJECT_HREF[p["slug"]],
            "image": img(p["cover"], focus="50% 55%")} for p in C.PROJECTS]

certificates = [
    {"_id": "vatrum", "name": "Våtrumsbehörighet", "issuer": "Byggkeramikrådet", "validUntil": "",
     "description": C.CERTS[0]["text"][0], "image": badge("badge-vatrum", "Behörig våtrum – Byggkeramikrådet")},
    {"_id": "id06", "name": "ID06", "issuer": "ID06", "validUntil": "", "description": "\n\n".join(C.CERTS[1]["text"]),
     "image": badge("badge-id06", "ID06")},
    {"_id": "bas", "name": "BAS P och BAS U", "issuer": "", "validUntil": "", "description": C.CERTS[2]["text"][0], "image": None},
    {"_id": "forsakring", "name": "Allrisk- och ansvarsförsäkring", "issuer": "Länsförsäkringar", "validUntil": "",
     "description": C.CERTS[3]["text"][0], "image": badge("badge-lf", "Länsförsäkringar")},
    {"_id": "fora", "name": "Kollektivavtalade försäkringar", "issuer": "FORA", "validUntil": "",
     "description": C.CERTS[3]["text"][1], "image": badge("badge-fora", "FORA")},
]

# --- Allt ihop --------------------------------------------------------------------------------------------------
link = lambda label, href: {"label": label, "href": href}  # noqa: E731
site = {
    "schemaVersion": 1,
    "theme": {
        "colors": {
            "primary": "#1572D3", "secondary": "#121418", "accent": "#2497FF", "background": "#FFFFFF", "surface": "#F1F3F6",
            "text": "#3B4048", "heading": "#121418", "muted": "#646B75", "subtle": "#C5CCD5", "border": "#E2E6EB",
            "input": "#FFFFFF", "link": "#1572D3", "button": "#1572D3", "buttonHover": "#0F5FB3", "buttonText": "#FFFFFF",
            "navigation": "#FFFFFF", "navigationText": "#121418", "footer": "#121418", "footerText": "#A9B0BA",
            "onPrimary": "#FFFFFF", "success": "#1E7B3A", "warning": "#B45309", "error": "#B91C1C",
        },
        "fonts": {role: {"family": "Plus Jakarta Sans", "category": "sans-serif"} for role in ("heading", "body", "button")},
    },
    "settings": {
        "siteName": C.NAME, "siteUrl": C.SITE_URL.rstrip("/"), "language": "sv",
        "favicon": {"src": "/icon.png", "variants": [], "alt": ""}, "logo": {"kind": "wordmark"}, "analyticsId": "",
        "maintenance": {"enabled": False, "heading": "Vi uppdaterar hemsidan",
                        "text": "Sidan är snart tillbaka. Under tiden når du oss på telefon eller e-post."},
    },
    "company": {
        "legalName": C.NAME, "shortName": C.SHORT, "foundedYear": 2023, "employees": 0, "city": "Göteborg",
        "serviceArea": C.AREA,
        "address": {"street": "", "postalCode": "", "city": "Göteborg", "country": "SE", "geo": {"lat": 57.70887, "lng": 11.97456}},
        "phone": C.PHONE, "email": C.EMAIL, "orgNumber": "", "vatNumber": "",
        "openingHours": "; ".join(f"{d}: {t}" for d, t in C.HOURS),
        "social": {"facebook": "", "instagram": "", "linkedin": ""},
    },
    "navigation": {
        "barLinks": coll([dict(link("Projekt", "/projekt"), _id="projekt"), dict(link("Certifikat", "/certifikat"), _id="certifikat"),
                          dict(link("Om oss", "/om-oss"), _id="om-oss"), dict(link("Kontakt", "/kontakt"), _id="kontakt")]),
        "menu": coll([{"_id": "hem", "label": "Hem", "href": "/", "kind": "link"},
                      {"_id": "tjanster", "label": "Tjänster", "href": "/#tjanster", "kind": "services"},
                      {"_id": "projekt", "label": "Projekt", "href": "/projekt", "kind": "link"},
                      {"_id": "certifikat", "label": "Certifikat", "href": "/certifikat", "kind": "link"},
                      {"_id": "om-oss", "label": "Om oss", "href": "/om-oss", "kind": "link"},
                      {"_id": "kontakt", "label": "Kontakt", "href": "/kontakt", "kind": "link"}]),
        "menuButton": "Begär offert",
    },
    "footer": {
        "contactHeading": "Kontakt", "servicesHeading": "Tjänster", "companyHeading": C.SHORT,
        "companyLinks": coll([dict(link("Projekt", "/projekt"), _id="projekt"), dict(link("Certifikat och försäkringar", "/certifikat"), _id="certifikat"),
                              dict(link("Om oss", "/om-oss"), _id="om-oss"), dict(link("Kontakt", "/kontakt"), _id="kontakt")]),
        "button": QUOTE, "copyrightName": C.NAME, "orgLabel": "Org.nr", "vatLabel": "Momsreg.nr",
    },
    "form": {
        "modalHeading": "Begär offert",
        "labels": {"name": "Namn", "phone": "Telefon", "email": "E-post", "workType": "Typ av projekt", "description": "Beskriv projektet"},
        "workTypePlaceholder": "Välj typ av projekt", "descriptionPlaceholder": "Vad ska göras, ungefär hur stort och när?",
        "workTypes": coll([{"label": t} for t in C.WORK_TYPES], "t"),
        "contactHint": "Det räcker med telefon eller e-post.",
        "errors": {"name": "Ange ditt namn.", "contact": "Ange telefonnummer eller e-postadress, så att vi kan nå dig.",
                   "phone": "Ange ett giltigt telefonnummer.", "email": "Ange en giltig e-postadress.", "workType": "Välj typ av projekt."},
        "submit": "Skicka förfrågan", "sending": "Skickar…", "sendFailed": "Förfrågan kunde inte skickas. Försök igen eller ring oss på",
        "closeHint": "Du kan stänga rutan när som helst genom att klicka utanför eller på", "closeHintButton": "X",
        "confirmation": "Tack! Vi återkommer så snart vi kan.", "emailSubject": "Offertförfrågan från {namn}",
    },
    "ui": {
        "skipLink": "Hoppa till innehållet", "openMenu": "Öppna meny", "closeMenu": "Stäng meny", "menuLabel": "Meny",
        "mainMenuLabel": "Huvudmeny", "quickLinksLabel": "Snabblänkar", "callPrefix": "Ring", "homeLinkLabel": f"{C.NAME} – startsida",
        "breadcrumbsLabel": "Brödsmulor", "breadcrumbHome": "Start", "carouselPrevious": "Föregående", "carouselNext": "Nästa",
        "carouselGoTo": "Gå till position {n} av {total}", "uppdragFilterLabel": "Filtrera projekt", "stepPrefix": "Steg",
        "mapTitlePrefix": "Karta:", "closeLabel": "Stäng", "ratingLabel": "{n} av 5 stjärnor",
        "cookieText": "Vi vill använda kakor för att se hur besökare använder sidan, så att vi kan göra den bättre. Godkänner du det?",
        "cookieAccept": "Godkänn", "cookieDecline": "Nej tack", "cookieSettings": "Kakinställningar",
    },
    "servicePage": {
        "badge": "", "eyebrow": f"Tjänster · {C.AREA}", "includesHeading": "Det här kan ingå", "galleryEyebrow": "Från projektportföljen",
        "reviewsEyebrow": "Omdömen", "reviewsHeading": "Vad kunderna säger", "moreEyebrow": "Fler tjänster",
        "cta": {"heading": "Har du ett projekt på gång?",
                "text": "Berätta vad du vill göra så återkommer vi med en skräddarsydd offert. Måndag–fredag 08.00–17.00.", "button": QUOTE},
        "factsTitle": "Fakta om tjänsten",
        "factLabels": {"service": "Tjänst", "performedBy": "Utförs av", "seat": "Säte", "area": "Område", "org": "Org.nr"},
        "contactTagline": "Bygg och renovering i Göteborg och Kungsbacka", "contactButton": QUOTE,
        "backLink": {"label": "Tillbaka till tjänster", "href": "/#tjanster"}, "moreHeading": "Det här gör vi också",
        "breadcrumbLabel": "Tjänster", "breadcrumbHref": "/#tjanster",
    },
    "notFound": {"eyebrow": "404", "heading": "Sidan finns inte", "text": "Länken kan vara gammal eller felstavad.",
                 "button": {"label": "Till startsidan", "href": "/"}, "seoTitle": "Sidan finns inte"},
    "services": coll(services),
    "uppdrag": coll(uppdrag),
    "certificates": coll(certificates),
    "pages": coll([home, projects_page, *project_pages, cert_page, about_page, contact_page]),
}

text = json.dumps(site, ensure_ascii=False, indent=2) + "\n"
(ROOT / "content/baseline.json").write_text(text)

# The first published version in the database is the same content.
sql_path = ROOT / "supabase/migrations/20261002120400_baseline.sql"
sql = sql_path.read_text()
sql = re.sub(r"\$baseline\$.*?\$baseline\$", lambda _: "$baseline$" + json.dumps(site, ensure_ascii=False) + "$baseline$", sql, count=1, flags=re.S)
sql = re.sub(r"values \('admin', 'primary', '#[0-9A-Fa-f]{6}'\)", "values ('admin', 'primary', '#1572D3')", sql)
sql_path.write_text(sql)
print("content/baseline.json:", len(site["pages"]["order"]), "sidor,", len(services), "tjänster")
