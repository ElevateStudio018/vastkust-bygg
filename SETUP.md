# Koppla in adminpanelen

Hemsidan och adminpanelen är färdigbyggda. Kvar är att koppla in Supabase, som är databasen bakom adminpanelen. Del 1
är det du gör, och del 2 är instruktioner för Claude.

**Under testperioden går alla mejl till elevate.studio018@gmail.com:** offertförfrågningar, medarbetarnas förslag
och inbjudan till adminpanelen. Du är admin. Västkust Bygg får ingenting förrän du säger till (se "Vid lansering"
längst ner).

## Del 1 – det här gör du

Bara steg 1–3 behövs för att komma igång, och de tar runt 10 minuter. Klistra aldrig in nycklar eller lösenord i
chatten.

### Steg 0 – Slå på GitHub Pages

Settings → Pages → **Build and deployment** → Source: **GitHub Actions**. (Inte "Deploy from a branch" – sajten byggs
nu av `.github/workflows/deploy-pages.yml`.) Kör sedan workflowet en gång under Actions → *Deploy preview to GitHub
Pages* → **Run workflow**, eller pusha något. Hemsidan fungerar direkt; adminpanelen visar "inte ansluten" tills
Supabase är inkopplat.

### Steg 1 – Skapa ett Supabase-projekt

1. Gå till [supabase.com](https://supabase.com) och logga in. "Continue with GitHub" fungerar.
2. Tryck **New project**.
3. Namn: `vastkust-bygg`. Region: Stockholm, eller annars närmaste i Europa.
4. Databaslösenord: tryck **Generate a password** och spara lösenordet i din lösenordshanterare. Det behövs inte i
   chatten.
5. Planen **Free** räcker för att testa. Tryck **Create new project** och vänta ett par minuter.

### Steg 2 – Koppla Supabase till Claude

1. Öppna [claude.ai/customize/connectors](https://claude.ai/customize/connectors).
2. Leta upp **Supabase** och tryck **Connect**. Logga in och godkänn.

### Steg 3 – Starta en ny session

Claude läser in kopplingar (connectors) när en session startar, så Supabase syns först i en ny session.

1. Starta en ny Claude Code-session på repot **ElevateStudio018/vastkust-bygg**, grenen
   **claude/happy-wright-lhp01u**.
2. Skriv: **Koppla in Supabase enligt SETUP.md**

Claude lägger in databasen och funktionerna och kopplar ihop hemsidan med adminpanelen. Sedan skapar du inloggningen
direkt i Supabase, så att inget mejl behövs:

- Authentication → Users → **Add user** → **Create new user**
- E-post: **elevate.studio018@gmail.com** (den enda adress som är admin under förhandsvisningen)
- Lösenord: tryck på nyckeln i din lösenordshanterare och låt den skapa ett (minst 12 tecken med stora och små
  bokstäver, siffror och tecken). Spara det där – skicka det aldrig i chatten.
- Bocka i **Auto Confirm User**. Därefter loggar du in på
[elevatestudio018.github.io/vastkust-bygg/admin](https://elevatestudio018.github.io/vastkust-bygg/admin/).

### Steg 4 – Senare: tre nycklar, en i taget när du vill

Adminpanelen fungerar utan dem, men de här tre sakerna fungerar inte förrän nyckeln finns. Varje nyckel tar ett par
minuter. Lägg in dem i Supabase under ditt projekt → **Edge Functions** → **Secrets** → **Add new secret**. Namnet
ska skrivas exakt som nedan.

| Namn | Vad den gör | Var du skapar nyckeln |
| --- | --- | --- |
| `GITHUB_DISPATCH_TOKEN` | Hemsidan uppdateras när du trycker Publicera. | GitHub → din profilbild → **Settings** → **Developer settings** → **Personal access tokens** → **Fine-grained tokens** → **Generate new token**. Resource owner: `ElevateStudio018`. Repository access: **Only select repositories** → `vastkust-bygg`. Permissions → Repository → **Actions: Read and write**. |
| `RESEND_API_KEY` | Mejl om offertförfrågningar och förslag. | [resend.com](https://resend.com): registrera dig med **elevate.studio018@gmail.com** → **API Keys** → **Create API key**. Med den adressen behövs ingen egen domän under testperioden. |
| `ANTHROPIC_API_KEY` | AI-assistenten. | [console.anthropic.com](https://console.anthropic.com) → **API keys** → **Create key**. Lägg också in ett betalkort och några dollar under **Billing**. |

### Steg 5 – Google-omdömen

Hemsidan hämtar omdömena själv var sjätte timme och visar dem i stället för de som står i adminpanelen.
ServiceFinder behöver ingen nyckel. Google hämtas via [SerpApi](https://serpapi.com) (gratiskonto, inget kort,
250 hämtningar i månaden – hemsidan använder cirka 120).

Lägg in nyckeln från SerpApi (serpapi.com → **Your Account** → **API Key**) på GitHub: repot → **Settings** →
**Secrets and variables** → **Actions** → **New repository secret**. Namn: `SERPAPI_KEY`.

Västkusts Google-profil är redan inlagd (plats-id `ChIJrz2xu5lvzC4RC-5UkH9xpUw`). Vill man hellre använda Googles
egen Places API går det också: secret `GOOGLE_PLACES_API_KEY` från Google Cloud Console, då utan `SERPAPI_KEY`.

### Vid lansering (senare, när du säger till)

- Västkust Bygg (info@vastkustbygg.se) läggs till som admin och får sin inbjudan.
- Secret `QUOTE_NOTIFY_EMAIL` = `info@vastkustbygg.se`, så att offertförfrågningarna går till Västkust Bygg.
  Förslagen fortsätter till Elevate.
- Egen domän: verifiera domänen i Resend och sätt `EMAIL_FROM`, `SITE_URL`, `ADMIN_URL` och `ALLOWED_ORIGINS`
  (se `supabase/functions/.env.example`).
- Bestäm priserna på credit-paketen.

## Del 2 – for Claude: installing the backend

Everything is in this repository. The site is a Next.js static export on GitHub Pages (basePath `/vastkust-bygg`), built by
`.github/workflows/deploy-pages.yml`. Supabase holds the drafts, published versions, quote requests, staff suggestions,
images, credits and the AI conversations. `supabase/tests/README.md` describes the local test stack these steps were
verified on.

Ground rules: nothing may be e-mailed to info@vastkustbygg.se, and the customer may not be made an admin or invited,
until the user says so. Never ask the user to paste a key, token or password into the chat.

1. **Project.** With the Supabase connector, find the user's project and note its ref, URL and the legacy `anon` key.
   Use the JWT `anon` key, which everything was tested with, not a publishable key.
2. **Database.** Apply every file in `supabase/migrations/` once, in filename order, using each file's name as the
   migration name. Check which migrations are already applied first. `20261003100000_preview_admin.sql` makes
   elevate.studio018@gmail.com the only admin address during the preview.
3. **Edge Functions.** Deploy every folder in `supabase/functions/` except `_shared`. Each function needs its own
   `index.ts`, the `_shared` files it imports (they import each other too) and the import map in
   `supabase/functions/deno.json`. Deploy every function with `verify_jwt = false`, as in `supabase/config.toml`; the
   functions check the caller themselves. `supabase/functions/_shared/site` is a copy of `lib/site`, kept identical by
   `node scripts/sync-shared.mjs`.
4. **Secrets.** The user adds `GITHUB_DISPATCH_TOKEN`, `RESEND_API_KEY` and `ANTHROPIC_API_KEY` when they want
   publishing, e-mail and the AI (part 1, step 4); the admin works without them. Every other setting has a default for
   the preview (`supabase/functions/_shared/env.ts`, `.env.example`).
   `IP_HASH_SALT` and `RESET_SIGNING_SECRET` fall back to values derived from the service role key, and quote requests
   go to `AGENCY_EMAIL` until `QUOTE_NOTIFY_EMAIL` is set. Confirm the three secrets exist by name only, never by value.
5. **Auth settings.** Change these through the connector or the Management API, or have the user change them in the
   dashboard. Site URL: `https://elevatestudio018.github.io/vastkust-bygg/admin/`. Redirect URLs:
   `https://elevatestudio018.github.io/vastkust-bygg/admin/**`. Sign-ups off. Minimum password length 12, requiring
   lower- and upper-case letters, digits and symbols, as in `supabase/config.toml`.
6. **Connect the site.** Set the GitHub repository variables `NEXT_PUBLIC_SUPABASE_URL` and
   `NEXT_PUBLIC_SUPABASE_ANON_KEY`. Use the GitHub API if this session may, otherwise the user does it under Settings →
   Secrets and variables → Actions → Variables. Then run the `deploy-pages.yml` workflow (workflow_dispatch) on
   `claude/happy-wright-lhp01u` and check that it succeeds.
7. **The admin's login.** No e-mail is needed. The user creates it in the dashboard: Authentication → Users → **Add
   user** → **Create new user**, with elevate.studio018@gmail.com and a password they choose there, and **Auto Confirm
   User** ticked. The allowlist makes the account an admin. Once Resend is set up, `admin-invite` can send invitations
   instead. It invites every allowlisted address without an account, and runs with the service role key or once with a
   setup token: store the token's hash with
   `insert into public.settings (key, value) values ('setup_token_hash', to_jsonb(encode(sha256('<token>'::bytea), 'hex')))`
   and POST `{"token": "<token>"}` to `<project url>/functions/v1/admin-invite`, from the database with `pg_net` if
   this sandbox cannot reach `*.supabase.co`.
8. **Check end to end with the user.** Log in, edit and publish, send a quote request and a suggestion on `/forslag/`,
   and check that they show in the admin. With the keys in place: the site rebuilds on publishing, both forms e-mail
   Elevate, and the AI answers. Read the functions' logs through the connector when
   something fails.
