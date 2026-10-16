# Västkust Bygg & Montage AB – ny webbplats

Ny webbplats för [Västkust Bygg & Montage AB](https://www.vastkustbygg.se/) (bygg och renovering i Göteborg och
Kungsbacka). All text och alla bilder är skrapade från nuvarande vastkustbygg.se.

Designen är en mix av Elevate Studios hantverkarsajter:

| Från | Vad |
| --- | --- |
| S-Bygg, Ohan, Antonsson | Python-generatorn (`scripts/` → `docs/`), Plus Jakarta Sans, piller-knappar, FAQ, offertformulär via FormSubmit med `?typ=` |
| JJ El | Inforad med betyg, ”Begär offert”-knapp med pil i cirkel, tjänsterutor med pil och färgad ”Hittar du inte det du söker?”-ruta, om oss-bild med rund betygsbricka, galleri med utförda jobb |
| Kungsbacka Mark & Trädgård | Hero i full bredd med tjänsterad längst ner |
| Appelgrens Elektriska | Faktatabell i om oss, skrapskriptet |
| Antonsson | Mörk ruta som ligger över en bred bild, arbetsgång med ikon och stora nummer, kontakt med formulär i ruta |
| GBG Mosaik | Förtroenderaden under heron, före/efter |

Färgerna kommer från loggan: svart och blått.

## Sidor

Allt ligger i [`docs/`](docs/) – öppna `docs/index.html` i en webbläsare.

- `index.html` – startsidan: hero med tjänsterad, förtroenderad, tjänsterutor, om oss med faktatabell, våtrum,
  kök före/efter, utförda jobb, varför oss, arbetsgång, omdömen, kontakt med formulär, frågor
- `tjanst-badrum.html`, `tjanst-kok.html`, `tjanst-renovering.html`, `tjanst-nybyggnation.html`
- `projekt.html` + `projekt-badrum.html`, `projekt-kok.html`, `projekt-kontor.html` (alla bilder från gamla
  sajtens projektportfölj, med bildvisning)
- `trygghet.html` – certifikat och försäkringar: våtrumsbehörighet, ID06, BAS P/U, Länsförsäkringar och FORA
- `om-oss.html`, `kontakt.html` (offertformulär), `404.html`, `sitemap.xml`, `robots.txt`

## Ändra text eller bygga om

```bash
python3 scripts/skrapa.py      # hämtar text (skrapat/text.txt) och originalbilder (skrapat/original/, inte incheckad)
python3 scripts/bilder.py      # gör webbversioner till docs/img/ och loggan i ljus/mörk version (kräver Pillow)
python3 scripts/build.py docs  # bygger sidorna
```

All text och alla uppgifter finns i `scripts/innehall.py`; layouten i `scripts/build.py`, `docs/assets/site.css` och
`docs/assets/site.js`. Ändra aldrig HTML-filerna i `docs/` direkt – de skrivs över.

## Fakta och förslag – gå igenom före lansering

**Från vastkustbygg.se:** namn, telefon 076-882 03 33, info@vastkustbygg.se, öppettider (mån–fre 08–17),
arbetsledare Emanuel Ström, tjänsterna och deras korttexter, ”Om oss”-texterna, de tre punkterna under ”Vad gör oss
unika?”, alla fem kundomdömen, texterna om ID06, våtrumsbehörighet (BBV), BAS P/U, Länsförsäkringar och FORA,
loggan, certifikatloggorna och alla projektbilder.

**Förslag som Västkust Bygg bör bekräfta eller ändra** (märkta FÖRSLAG i `scripts/innehall.py`):

- Området *Göteborg och Kungsbacka* och ortlistan – bygger på orterna i omdömena (Malevik, Lindome, Västra
  Frölunda, Hovås).
- Tjänstesidornas längre texter och listorna ”Det här kan ingå” (särskilt Nybyggnation: tillbyggnader,
  attefallshus m.m.), arbetsgången, frågorna och svaren, och beskrivningarna av projekten.
- Gatuadress och org.nr saknas på gamla sajten (där står bara en mallrad) och visas inte.
- Omdömet från Ingvar Nore kommer från Google; de övriga fyra har ort och datum men ingen källa på gamla sajten.

Inga priser, årtal eller antal anställda anges.

## Offertformuläret

Formuläret skickar e-post via [FormSubmit](https://formsubmit.co). Under förhandsvisningen går förfrågningarna till
Elevate Studio; byt `FORM_EMAIL` i `scripts/innehall.py` till info@vastkustbygg.se vid lansering (första förfrågan
skickar ett aktiveringsmejl). ”Få offert” från en tjänstesida fyller i projekttypen (`kontakt.html?typ=…#offert`).

## Publicera

Sidan publiceras av `.github/workflows/deploy-pages.yml` vid varje push till `main` eller
`claude/happy-wright-lhp01u` (GitHub Pages, källa *GitHub Actions*). Byt `SITE_URL` i `scripts/innehall.py` om sajten
flyttas till vastkustbygg.se.
