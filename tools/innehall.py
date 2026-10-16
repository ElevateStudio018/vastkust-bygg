"""All text och alla uppgifter för Västkust Bygg & Montage AB:s webbplats.

Texterna som står inom citattecken i kommentarerna "Från vastkustbygg.se" är hämtade från nuvarande hemsida
(skrapat/text.txt efter scripts/skrapa.py). Det som är märkt FÖRSLAG är skrivet av oss utifrån sajtens innehåll och
ska bekräftas av Västkust Bygg före lansering.
"""
from urllib.parse import quote_plus

# --- Företaget (från vastkustbygg.se) ----------------------------------------------------------------------------
NAME = "Västkust Bygg & Montage AB"
SHORT = "Västkust Bygg"
PHONE, TEL = "076-882 03 33", "+46768820333"
EMAIL = "info@vastkustbygg.se"
HOURS = [("Måndag–fredag", "08.00–17.00"), ("Lördag–söndag", "Stängt")]
HOURS_SHORT = "Mån–fre 08–17"
CONTACT_PERSON = ("Emanuel Ström", "Arbetsledare")
# Google-platsen som länkas från nuvarande sajt. Gatuadress saknas på sajten (där står bara en mallrad) och visas inte.
MAPS_LINK = "https://www.google.com/maps/place/?q=place_id:ChIJrz2xu5lvzC4RC-5UkH9xpUw"
# FÖRSLAG: området bygger på orterna i kundomdömena (Malevik, Lindome, Västra Frölunda, Hovås).
AREA = "Göteborg och Kungsbacka"
AREA_PLACES = ["Göteborg", "Västra Frölunda", "Hovås", "Askim", "Mölndal", "Lindome", "Kungsbacka", "Malevik"]

# Offertformuläret skickar via FormSubmit. Under förhandsvisningen går förfrågningarna till Elevate Studio;
# byt till info@vastkustbygg.se vid lansering (första förfrågan till en ny adress skickar ett aktiveringsmejl).
FORM_EMAIL = "elevate.studio018@gmail.com"
SITE_URL = "https://elevatestudio018.github.io/vastkust-bygg/"
MAP_EMBED = "https://www.google.com/maps?q=" + quote_plus("Göteborg") + "&z=10&hl=sv&output=embed"

# --- Bilder: webbnamn -> originalfil i skrapat/original/ -----------------------------------------------------------
PHOTOS = {
    # Kök (före och efter, samma kök)
    "kok-fore": "1000002889.jpg",
    "kok-efter-1": "1000003244.jpg",
    "kok-efter-2": "1000003251.jpg",
    "kok-detalj": "1000003250.jpg",
    # Badrum 1: grå storformatsplattor, nisch och tvättställ på trä
    "bad1-1": "1000007980.jpg",
    "bad1-2": "1000007951.jpg",
    "bad1-3": "1000007957.jpg",
    "bad1-4": "1000007981.jpg",
    "bad1-5": "1000007982.jpg",
    "bad1-6": "1000007953.jpg",
    "bad1-7": "1000007954.jpg",
    "bad1-8": "1000007956.jpg",
    # Badrum 2: snedtak, före – under – efter
    "bad2-fore": "20241104_081622.jpg",
    "bad2-under": "20241202_145944.jpg",
    "bad2-1": "20241204_142409.jpg",
    "bad2-2": "20241204_142420.jpg",
    "bad2-3": "20241204_142439.jpg",
    # Badrum 3 och bastu
    "bad3-1": "1000008336.jpg",
    "bad3-2": "1000008339.jpg",
    "bastu": "1000006176.jpg",
    # Kontor: lokalanpassning från regelstomme till glasvägg
    "kontor-1": "1000008535.jpg",
    "kontor-2": "1000008540.jpg",
    "kontor-3": "1000008717.jpg",
    "kontor-4": "1000008634.jpg",
    "kontor-5": "1000008636.jpg",
    "kontor-6": "1000008637.jpg",
    "kontor-glas": "1000007943.jpg",
    "kontor-klar": "1000007944.jpg",
}
# Märken och loggor (visas i originalform, på vit platta)
BADGES = {
    "badge-vatrum": "bkr_våtrum.jpg",
    "badge-id06": "ID06_card_digital_ID.PNG",
    "badge-lf": "lansforsakringar-logotyp___serialized1.png",
    "badge-fora": "Fora_logo-1920x1200-3___serialized1.webp",
}
LOGO_SRC = "IMG_20231205_225029_958.webp"

# --- Tjänster ----------------------------------------------------------------------------------------------------
# title/short: från vastkustbygg.se. lead, body och items: FÖRSLAG.
SERVICES = [
    dict(
        slug="badrum", title="Badrumsrenovering", nav="Badrum",
        short="Vi skapar funktionella och stilrena badrum genom skräddarsydda renoveringar som passar dina önskemål.",
        photo="bad1-1", pos="50% 60%", alt="Renoverat badrum med grå storformatsplattor, nisch och vägghängd toalett",
        lead="Behöriga våtrumsbyggare enligt Byggkeramikrådets branschregler. När badrummet är klart får du ett kvalitetsdokument.",
        body=[
            "Ett badrum ska hålla i många år – därför är det tätskiktet du inte ser som är viktigast. Vi har gått Byggkeramikrådets utbildning och arbetar efter deras branschregler, BBV. Efter avslutad entreprenad lämnar vi ett Kvalitetsdokument till dig som beställare.",
            "Vi tar hand om hela kedjan: rivning, underarbete, tätskikt, plattsättning och montering av inredning. Du får hjälp att bolla idéer om planlösning, plattor och förvaring, och en tydlig plan för när vad händer.",
        ],
        items=["Rivning och bortforsling", "Underarbete och golvfall", "Tätskikt enligt BBV",
               "Plattsättning på golv och vägg", "Nischer och inbyggd förvaring", "Montering av kommod, wc och dusch",
               "Kvalitetsdokument efter avslutat arbete"],
        project="badrum",
    ),
    dict(
        slug="kok", title="Köksrenovering", nav="Kök",
        short="Få ditt drömkök med våra kökrenoveringstjänster som kombinerar design, funktionalitet och kvalitet på ett professionellt sätt.",
        photo="kok-efter-1", pos="50% 55%", alt="Nyrenoverat kök med ljusa trästommar, massiv bänkskiva och marmorstänkskydd",
        lead="Från rivning till sista list – vi bygger om köket så att det fungerar för just ert hem.",
        body=[
            "Ett nytt kök handlar om mer än luckor. Vi river det gamla, rättar till väggar och golv och monterar stommar, bänkskivor, vitvaror och stänkskydd så att allt sitter som det ska.",
            "Vill du flytta om eller öppna upp planlösningen går vi igenom förutsättningarna tillsammans innan vi börjar, så att det är tydligt vad som ingår.",
        ],
        items=["Rivning av gammalt kök", "Väggar, golv och tak", "Montering av stommar och luckor",
               "Bänkskivor och stänkskydd", "Inbyggda vitvaror", "Belysning i samråd med elektriker", "Lister och anpassningar"],
        project="kok",
    ),
    dict(
        slug="renovering", title="Renovering och ombyggnation", nav="Renovering & ombyggnad",
        short="Vårt team utför noggranna renoveringar och ombyggnationer för att förvandla ditt utrymme till något nytt och modernt.",
        photo="kontor-2", pos="50% 55%", alt="Regelstomme till nya innerväggar i en kontorslokal under ombyggnad",
        lead="Nya väggar, ny planlösning eller en hel lokal som ska anpassas – för privatpersoner och företag.",
        body=[
            "Vi bygger om bostäder och lokaler: nya innerväggar, glaspartier, undertak, golv och ytskikt. På kontor och i lokaler planerar vi arbetet så att verksamheten störs så lite som möjligt.",
            "Även mindre jobb är välkomna – en fuktskada ovanför ett fönster eller en omfogning vid duschen. ”Jag hade inget stort byggprojekt men kände att jag var lika prioriterad som de med större projekt”, skrev en kund i Västra Frölunda.",
        ],
        items=["Lokalanpassningar för kontor", "Nya innerväggar och glaspartier", "Ändrad planlösning",
               "Golv, väggar och undertak", "Fuktskador och reparationer", "Fogning i våtrum", "Bastu"],
        project="kontor",
    ),
    dict(
        slug="nybyggnation", title="Nybyggnation", nav="Nybyggnation",
        short="Vi specialiserar oss på att skapa unika och hållbara nybyggnationer som passar dina önskemål och behov.",
        photo="kontor-glas", pos="50% 45%", alt="Ny glasvägg och mötesrum i en ombyggd kontorslokal",
        lead="Från idé till färdigt projekt – med en kontaktperson som håller ihop helheten.",
        body=[
            "Vi bygger nytt med samma noggrannhet som i våra renoveringar. Tillsammans går vi igenom önskemål, förutsättningar och tidplan, och du vet hela tiden vem du pratar med.",
            "Bolaget har utbildning för byggarbetsmiljösamordning (BAS P och BAS U), så att arbetsmiljön är planerad redan från början.",
        ],
        items=["Tillbyggnader", "Attefallshus och komplementbyggnader", "Uterum och förråd",
               "Stomme, tak och fasad", "Invändig färdigställning", "Byggarbetsmiljösamordning (BAS P/U)"],
        project=None,
    ),
]
WORK_TYPES = [s["title"] for s in SERVICES] + ["Lokalanpassning", "Mindre jobb / reparation", "Annat"]
SMALL_JOBS = ["Fuktskador", "Omfogning i våtrum", "Bastu", "Glaspartier", "Undertak", "Golv och lister"]

# --- Projekt (bilder från vastkustbygg.se, texterna är FÖRSLAG utifrån bilderna) ----------------------------------
PROJECTS = [
    dict(
        slug="badrum", title="Badrumsrenoveringar", tag="Badrum", cover="bad1-1", count=None,
        intro="Ett urval av badrummen vi har renoverat – från rivning till färdigt rum med kvalitetsdokument.",
        parts=[
            dict(h="Grått och varmt", eyebrow="Helrenovering",
                 text=["Storformatsplattor från golv till tak, en upplyst nisch ovanför toaletten och en kommod i trä med tvättställ ovanpå.",
                       "Glasväggen ger ett öppet duschutrymme och fönstret får släppa in ljuset hela vägen."],
                 photos=["bad1-1", "bad1-2", "bad1-3", "bad1-4", "bad1-5", "bad1-6", "bad1-7", "bad1-8"],
                 tile="Ordning och reda, snyggt och prydligt från start till mål. – Lotta, Malevik"),
            dict(h="Badrum under snedtak", eyebrow="Före – under – efter",
                 text=["Ett äldre badrum med badkar på lejonfötter och plastmatta blev ett ljust duschrum med grå plattor.",
                       "Snedtaket kläddes in, golvet fick nytt fall och en böjd duschvägg gör att det lilla rummet känns större."],
                 photos=["bad2-fore", "bad2-under", "bad2-1", "bad2-2", "bad2-3"],
                 captions={"bad2-fore": "Före", "bad2-under": "Under arbetet"}),
            dict(h="Ljust duschrum och bastu", eyebrow="Fler projekt",
                 text=["Ett ljust badrum med duschhörna i glas och spegelskåp, och en bastu med lavar i trä."],
                 photos=["bad3-1", "bad3-2", "bastu"]),
        ],
    ),
    dict(
        slug="kok", title="Köksrenoveringar", tag="Kök", cover="kok-efter-1",
        intro="Samma kök, före och efter. Det gamla köket revs ut och ersattes med nytt från golv till tak.",
        parts=[
            dict(h="Från 70-tal till nytt", eyebrow="Totalrenovering",
                 text=["Ut åkte de gamla luckorna, kaklet och korkmattan. In kom ljusa trästommar, en massiv bänkskiva, stänkskydd i marmormönster och inbyggda vitvaror i ett högskåp.",
                       "Taket fick ny belysning och vi rättade till väggarna innan något monterades."],
                 photos=["kok-fore", "kok-efter-1", "kok-efter-2", "kok-detalj"],
                 captions={"kok-fore": "Före"},
                 tile="Bra genomfört arbete där arbetet utförts enligt utsatt tid. – Maria, Lindome"),
        ],
    ),
    dict(
        slug="kontor", title="Kontor och lokalanpassningar", tag="Kontor", cover="kontor-glas",
        intro="En kontorslokal som anpassades med nya väggar, glaspartier och undertak – här steg för steg.",
        parts=[
            dict(h="Från regelstomme…", eyebrow="Under arbetet",
                 text=["Nya rum byggdes upp i en öppen kontorsyta: regelstommar, gips och nya dörrar, med undertaket öppet för installationer."],
                 photos=["kontor-1", "kontor-2", "kontor-3", "kontor-4", "kontor-5", "kontor-6"],
                 tile="Vi planerar arbetet så att verksamheten kan fortsätta runt omkring."),
            dict(h="…till färdigt kontor", eyebrow="Resultat",
                 text=["Glaspartier mot det öppna landskapet ger ljus in i mötesrummen, och de nya väggarna är klara för tavlor och skärmar."],
                 photos=["kontor-glas", "kontor-klar"]),
        ],
    ),
]

# --- Om oss (från vastkustbygg.se) --------------------------------------------------------------------------------
ABOUT = [
    "Västkust Bygg & Montage AB är med er hela vägen, från idé till färdigt projekt. Vi erbjuder en helhetslösning där kompetens, noggrannhet och tydlighet är viktiga faktorer för oss. Vår erfarenhet och expertis inom byggbranschen gör oss till det optimala valet för ditt projekt.",
    "Vår unika helhetslösning skiljer oss från konkurrenterna. Genom att integrera kompetens, noggrannhet och tydlighet levererar vi enastående resultat som överträffar förväntningarna. Vårt dedikerade team står redo att ta ansvar och säkerställa att varje projekt blir en framgång.",
]
TEAM_TEXT = "Västkust Bygg & Montage AB:s hantverkare har lång erfarenhet inom byggbranschen, vilket gör oss till en pålitlig partner för ditt projekt. Vi strävar alltid efter att leverera högkvalitativt arbete och nöjda kunder."
VALUES = [
    ("Skickliga hantverkare",
     "Vi har ett team av skickliga hantverkare som är experter inom sitt arbete och levererar högkvalitativa resultat med precision och noggrannhet."),
    ("Innovativa lösningar",
     "Vi strävar efter att implementera innovativa lösningar och tekniker i våra projekt för att säkerställa effektivitet, hållbarhet och modern design."),
    ("Kundanpassad service",
     "Vår kundanpassade service innebär att vi lyssnar aktivt på våra kunders önskemål och behov för att skapa skräddarsydda lösningar som överträffar deras förväntningar."),
]

# FÖRSLAG: arbetsgången
STEPS = [
    ("Idé och kontakt", "Du ringer, mejlar eller fyller i formuläret och berättar vad du vill göra."),
    ("Besök och offert", "Vi tittar på plats och lämnar en skräddarsydd offert med vad som ingår."),
    ("Vi bygger", "En kontaktperson, tydlig tidplan och ordning och reda på arbetsplatsen."),
    ("Klart och dokumenterat", "Gemensam genomgång – och för våtrum ett kvalitetsdokument enligt BBV."),
]

# --- Certifikat och försäkringar (från vastkustbygg.se) -----------------------------------------------------------
CERTS = [
    dict(
        slug="vatrum", title="Våtrumsbehörighet", short="Behörig enligt Byggkeramikrådets branschregler (BBV).",
        badge="badge-vatrum",
        text=["Vi har gått utbildning hos Byggkeramikrådet och är behöriga att arbeta efter deras branschregler, BBV. Efter avslutad entreprenad lämnar vi ett Kvalitetsdokument till dig som beställare."],
        photos=["bad2-under", "bad1-6"],
    ),
    dict(
        slug="id06", title="ID06", short="Personalliggare, utbildningsbevis och säker identifiering.",
        badge="badge-id06",
        text=["Vi nyttjar ID06 mjukvarusystem och IT-lösningar som hjälper oss att effektivisera den dagliga verksamheten. Till exempel används ID06 för närvaroregistrering av personer på arbetsplatsens personalliggare, digitalisering av arbetares utbildningsbevis och inpasserings- och låsfunktioner i lokala system.",
              "Med ID06 kan våra kunder enkelt identifiera personer på arbetsplatsen och koppla varje person till ett företag, på ett säkert sätt.",
              "ID06 främsta uppdrag och mål är att främja sund konkurrens och säkra arbetsplatser. Effekten av målbilden blir att vi med ID06 är med och skapar ett socialt hållbart samhälle, där vi också motverkar svartarbete, ekonomisk brottslighet och annan kriminalitet."],
        photos=["kontor-4"],
    ),
    dict(
        slug="bas", title="BAS P och BAS U", short="Utbildning i byggarbetsmiljösamordning.",
        badge=None,
        text=["Bolaget har genomgått byggarbetsmiljösamordnarutbildning för att kunna hantera arbetsmiljöfrågor i projekterings- och planeringsfasen (BAS P) och/eller i genomförandefasen (BAS U)."],
        photos=["kontor-3"],
    ),
    dict(
        slug="forsakring", title="Försäkringar", short="Allrisk- och ansvarsförsäkring samt kollektivavtalade försäkringar.",
        badge="badge-lf", badge2="badge-fora",
        text=["Bolaget innehar en allrisk- och ansvarsförsäkring via Länsförsäkringar.",
              "Bolagets anställda omfattas av kollektivavtalade försäkringar via FORA."],
        photos=[],
    ),
]
CERTS_INTRO = "Vi är stolta över våra branschackrediteringar och certifieringar som säkerställer högsta kvalitet och professionalism i vårt arbete."

# --- Omdömen (ordagrant från vastkustbygg.se) ---------------------------------------------------------------------
REVIEWS = [
    dict(name="Lotta", place="Malevik", date="26 maj 2025", job="Helrenovering av badrum",
         text="Vi är supernöjda med Västkust Bygg och Emanuel som totalrenoverat vårt badrum. Ordning och reda, snyggt och prydligt från start till mål. Vi fick hjälp med att bolla idéer och lösningsförslag under projektets gång. Vi kommer absolut anlita dem igen och rekommendera Västkust Bygg till våra vänner och bekanta."),
    dict(name="Ingvar Nore", place="Google", date="", job="Badrumsrenovering",
         text="Västkust Bygg och Montage har nu renoverat vårt badrum. Emanuel Ström har genomfört renoveringen väldigt professionellt och har under hela processen givit goda råd och lyssnat på oss som kunder. Vi anlitar gärna detta företag fler gånger."),
    dict(name="Maria", place="Lindome", date="15 apr 2025", job="Helrenovering av badrum",
         text="Bra genomfört arbete där arbetet utförts enligt utsatt tid. Uppskattar snabb kommunikation under hela processen. Nöjd med resultatet och kommer anlita Västkust Bygg och Montage AB till andra uppdrag framöver. Kan varmt rekommendera dem."),
    dict(name="Suzanne", place="Västra Frölunda", date="15 okt 2024", job="Reparera fukt ovanför ett sovrumsfönster",
         text="Jag kommer att anlita dem igen. Jag hade inget stort byggprojekt men kände att jag var lika prioriterad som de med större projekt. Kanonbemötande 😃"),
    dict(name="Niclas", place="Hovås", date="2 nov 2024", job="Foga om vid ett handfat och dusch",
         text="Jag rekommenderar detta företag för att de är snabba, har ett proffsigt bemötande och sätter kunden i fokus. De får 5 stjärnor av 5 möjliga."),
]

# FÖRSLAG: frågor och svar
FAQ = [
    ("Vilka uppdrag tar ni?",
     "Badrums- och köksrenoveringar, renoveringar och ombyggnationer, lokalanpassningar och nybyggnation – men även mindre jobb som fuktskador och omfogning."),
    ("Är ni behöriga att bygga badrum?",
     "Ja. Vi har gått Byggkeramikrådets utbildning och arbetar efter branschreglerna BBV. När badrummet är klart får du ett Kvalitetsdokument."),
    ("Hur får jag en offert?",
     f"Fyll i <a href=\"kontakt.html\">formuläret</a>, mejla <a href=\"mailto:{EMAIL}\">{EMAIL}</a> eller ring <a href=\"tel:{TEL}\">{PHONE}</a>. Oftast vill vi se på plats innan vi lämnar en offert som håller."),
    ("Var arbetar ni?",
     f"Främst i {AREA} med omnejd. Ligger ditt projekt någon annanstans – hör av dig så svarar vi om vi kan ta det."),
    ("Gäller ROT-avdrag?",
     "ROT-avdraget gäller arbetskostnaden för många renoveringar och ombyggnader i bostäder. Vi visar hur det påverkar priset i offerten."),
    ("Är ni försäkrade?",
     "Ja. Bolaget har allrisk- och ansvarsförsäkring via Länsförsäkringar, och de anställda omfattas av kollektivavtalade försäkringar via FORA."),
]
