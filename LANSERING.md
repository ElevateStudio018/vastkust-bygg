# Lansering på vastkustbygg.se

Hemsidan ligger i dag på förhandsadressen https://elevatestudio018.github.io/vastkust-bygg/. Allt i koden är förberett
för https://vastkustbygg.se/. Själva bytet styrs av **en** inställning (repo-variabeln `SITE_DOMAIN`) plus DNS hos
one.com, och görs först när vi bestämt oss. Domänen och mejlen ligger kvar hos one.com.

## Så fungerar bytet i koden

- Utan `SITE_DOMAIN` byggs sidan som i dag, under `/vastkust-bygg/`.
- Med `SITE_DOMAIN=vastkustbygg.se` byggs den från roten: alla länkar, bilder, videor, CSS, JS, adminpanelen,
  sitemap, robots.txt och kanoniska länkar pekar på https://vastkustbygg.se, och bygget lägger en `CNAME`-fil i
  publiceringen.
- GitHub Pages publiceras med GitHub Actions (`.github/workflows/deploy-pages.yml`) vid varje push, var sjätte timme
  och vid publicering från adminpanelen.

## DNS hos one.com (läggs in vid lanseringen)

Rör inte MX, SPF, DKIM, DMARC eller andra mejlposter. Mejlen påverkas inte av ändringarna nedan.

| Typ | Namn (värd) | Värde | Ersätter i dag |
| --- | --- | --- | --- |
| A | `@` (vastkustbygg.se) | `185.199.108.153` | A `46.30.215.57` |
| A | `@` | `185.199.109.153` | |
| A | `@` | `185.199.110.153` | |
| A | `@` | `185.199.111.153` | |
| AAAA | `@` | `2606:50c0:8000::153` | AAAA `2a02:2350:5:10e:80ce:cb12:8141:e82c` |
| AAAA | `@` | `2606:50c0:8001::153` | |
| AAAA | `@` | `2606:50c0:8002::153` | |
| AAAA | `@` | `2606:50c0:8003::153` | |
| CNAME | `www` | `elevatestudio018.github.io` | A `46.30.215.57` för www |

- Den gamla A-posten och AAAA-posten för `@` och A-posten för `www` **ska bort**. Ligger den gamla AAAA-posten kvar
  hamnar besökare med IPv6 på den gamla sidan.
- Stäng av **Vidarebefordring** (one.com → DNS → Vidarebefordring) om den är på.
- one.com har en jokerpost (`*` → `46.30.215.57`). Den kan ligga kvar.
- Det finns ingen CAA-post, så GitHub får utfärda certifikat.

### Gamla värden (för återställning)

```
A     @    46.30.215.57
AAAA  @    2a02:2350:5:10e:80ce:cb12:8141:e82c
A     www  46.30.215.57
MX    @    mx1.pub.mailpod11-cph3.one.com (10), mx2…, mx3…, mx4… (ändras aldrig)
NS         ns01.one.com, ns02.one.com (ändras aldrig)
```

## Ordning vid lanseringen

1. **Före (valfritt men rekommenderat):** verifiera domänen i GitHub så att ingen annan kan ta den: GitHub →
   profilbild → Settings → Pages → Add a domain → `vastkustbygg.se`. GitHub ger en TXT-post
   (`_github-pages-challenge-ElevateStudio018`) som läggs in hos one.com; tryck Verify. Påverkar inte sidan.
2. **DNS:** lägg in posterna ovan hos one.com och ta bort de gamla. Ändringen syns oftast inom en timme (högst ett
   dygn).
3. **GitHub Pages:** repot → Settings → Pages → Custom domain: `vastkustbygg.se` → Save. (Inte tidigare: då skickar
   förhandsadressen besökare till den gamla sidan.)
4. **Bygg för domänen:** repot → Settings → Secrets and variables → Actions → Variables → New variable:
   `SITE_DOMAIN` = `vastkustbygg.se`. Kör sedan Actions → *Deploy preview to GitHub Pages* → Run workflow.
5. **HTTPS:** när GitHub visar att certifikatet är klart (Settings → Pages, oftast inom 15–60 minuter efter att DNS
   slagit igenom) bockar du i **Enforce HTTPS**.
6. **Supabase:** Edge Function-hemligheter `SITE_URL=https://vastkustbygg.se` och
   `ADMIN_URL=https://vastkustbygg.se/admin` (länkar och logga i mejl), och Authentication → URL Configuration →
   Site URL `https://vastkustbygg.se/admin/`. Domänen är redan godkänd för inloggning och offertformuläret.

## Kontroll efter lanseringen

- https://vastkustbygg.se och https://www.vastkustbygg.se visar nya sidan med hänglås.
- elevatestudio018.github.io/vastkust-bygg skickar vidare till vastkustbygg.se.
- Video, omdömen, /omdomen, /integritetspolicy, tjänstesidorna, /cw/konsulting.html och /admin fungerar.
- Skicka en offertförfrågan; den syns i adminpanelen och mejlet kommer fram.

## Mejlen

DNS-ändringarna rör bara webbposterna. Kontroll före och efter: skicka ett mejl till info@vastkustbygg.se från en
annan adress och svara från det. MX-posterna ska fortfarande visa `mx1–mx4.pub.mailpod11-cph3.one.com`
(`dig MX vastkustbygg.se` eller https://dns.google/resolve?name=vastkustbygg.se&type=MX).

Offertmejl till info@vastkustbygg.se (i stället för Elevate) kräver att domänen verifieras i Resend. Det är nya poster
som Resend anger (för `send.` och `resend._domainkey`); de ersätter inget befintligt men är mejlposter och läggs bara in
efter beslut. Sedan sätts `QUOTE_NOTIFY_EMAIL=info@vastkustbygg.se` och `EMAIL_FROM` i Supabase.

## Om något går fel

1. Hos one.com: ta bort GitHub-posterna och lägg tillbaka de gamla värdena ovan (A, AAAA och www). Den gamla sidan är
   tillbaka när DNS slagit igenom.
2. GitHub: Settings → Pages → ta bort Custom domain, och ta bort variabeln `SITE_DOMAIN`. Kör workflowet igen så är
   förhandsadressen tillbaka.
3. Supabase: ändra tillbaka `SITE_URL`/`ADMIN_URL` och Site URL om de hann ändras.
