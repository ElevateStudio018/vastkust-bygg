# Västkust Bygg & Montage AB – hemsida med adminpanel

Ny hemsida för [Västkust Bygg & Montage AB](https://www.vastkustbygg.se/) (bygg och renovering i Göteborg och
Kungsbacka), med adminpanelen från Elevate Studios Bugg-test: ägaren ändrar texter, bilder, färger och sidor själv,
får offertförfrågningarna i panelen och kan be AI-assistenten om ändringar.

**Kom igång: läs [SETUP.md](SETUP.md)** – GitHub Pages, Supabase och inloggningen.

## Så hänger det ihop

- **Next.js** (statisk export till GitHub Pages, basePath `/vastkust-bygg`). Hela innehållet är ett dokument
  (`lib/site/schema.ts`); varje sida är en lista sektioner som ritas av `components/sections/`.
- **Utseendet** är den godkända designen (en mix av Elevate Studios hantverkarsajter): `app/site.css`, avgränsad till
  `.vk` så att adminpanelen inte påverkas. Färger och typsnitt kommer från temat i adminpanelen (Plus Jakarta Sans,
  loggans svart och blått).
- **Adminpanelen** (`app/admin`, `components/admin`) och **Supabase** (`supabase/`: databas, Edge Functions för
  publicering, offertförfrågningar, förslag, inbjudningar och AI) är desamma som i Bugg-test.
- **Omdömena** hämtas från ServiceFinder (och Google, med nyckel) före varje bygge av `scripts/fetch-reviews.ts`
  till `content/reviews.json`. Workflowet bygger var sjätte timme och checkar in filen när det kommit nya, så listan
  växer. Finns det hämtade omdömen visas de i stället för dem i adminpanelen.
- Utan Supabase byggs sajten från `content/baseline.json` och offertformuläret mejlar via FormSubmit till Elevate
  Studio; adminpanelen visar då att den inte är ansluten.

## Sidor

Start (hero i helskärm, tjänsterutor, om oss med faktatabell, våtrum, kök före/efter, utförda jobb, varför oss,
arbetsgång, omdömen att bläddra i, kontakt med formulär, frågor), fyra tjänstesidor under `/tjanster/…`, `/projekt`
med tre projektsidor (`/projekt-badrum`, `/projekt-kok`, `/projekt-kontor`), `/certifikat`, `/om-oss`, `/kontakt` och
`/admin`.

Sektionstyper som lagts till för den här designen: *Bild med mörk ruta* (`overlay`), *Före och efter*
(`beforeAfter`), *Mörkt band med kort* (`values`) och *Område och karta* (`area`). Alla sektioner har dessutom en
liten text ovanför rubriken (`eyebrow`), och tjänsterna har ingress, ”Det här kan ingå” och egna bilder.

## Utveckla

```bash
npm ci
npm run dev                       # http://localhost:3000
GITHUB_PAGES=true npm run build   # som på GitHub Pages, till out/
npx tsx supabase/tests/changeset.test.ts
node scripts/sync-shared.mjs      # efter ändringar i lib/site eller content/baseline.json
```

## Ursprungligt innehåll

All text och alla bilder är skrapade från nuvarande vastkustbygg.se. Verktygen ligger i `tools/` (Python, Pillow):

```bash
python3 tools/skrapa.py          # text och originalbilder till skrapat/ (inte incheckat)
python3 tools/bilder.py          # webp i flera storlekar till public/photos, loggorna och ikonen till public/
python3 tools/make_baseline.py   # content/baseline.json och baseline-migrationen, från tools/innehall.py
node scripts/sync-shared.mjs
```

När sajten är kopplad till Supabase ändras innehållet i adminpanelen, inte i baseline.

## Fakta och förslag – gå igenom före lansering

**Från vastkustbygg.se:** namn, telefon 076-882 03 33, info@vastkustbygg.se, öppettider (mån–fre 08–17),
arbetsledare Emanuel Ström, tjänsterna och deras korttexter, ”Om oss”-texterna, ”Vad gör oss unika?”, alla fem
kundomdömen, texterna om ID06, våtrumsbehörighet (BBV), BAS P/U, Länsförsäkringar och FORA, loggan, certifikatloggorna
och alla projektbilder.

**Förslag som Västkust Bygg bör bekräfta eller ändra** (märkta FÖRSLAG i `tools/innehall.py`):

- Området *Göteborg och Kungsbacka* och ortlistan – bygger på orterna i omdömena.
- Tjänstesidornas längre texter och ”Det här kan ingå”, arbetsgången, frågorna och svaren och projektbeskrivningarna.
- Gatuadress, org.nr och grundår saknas på gamla sajten och visas inte (grundåret 2023 i företagsuppgifterna är en
  platshållare som inte syns någonstans).
- Omdömena från gamla sajten (i adminpanelen) visas bara om inga kunde hämtas från ServiceFinder eller Google.
