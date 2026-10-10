# Kako objaviti na Leanpub-u

Ovo je kompletan rukopis kao kandidat za objavljivanje, uz prateći kod i branding. Nije već objavljena knjiga. Autor je **Aleksandar Popovic**, profil https://github.com/alekpopovic. Paket ne sadrži prijavu na tvoj nalog, podatke za isplatu ili tvrdnju da je nezavisna stručna recenzija završena.

## Pre objavljivanja

1. Koristi autora Aleksandar Popovic i GitHub profil iz `book-metadata.json`; proširi kratku biografiju samo podacima koje želiš javno da navedeš.
2. Pregledaj svaku lekciju i uradi završnu jezičku i stručnu recenziju.
3. Na Linux hostu izvrši Nginx i Unix-socket vežbe; za produkcione tvrdnje izvrši i odgovarajuće Vector/PostgreSQL/Go zadatke.
4. Proveri da naziv LogBranik odgovara tvojoj konačnoj komercijalnoj nameni. Predlog nije provera žiga.
5. Autor je već na koricama i u metapodacima; posle daljih izmena regeneriši izdanja i ažuriraj AI izjavu samo stvarno obavljenim radom.

## Preporučena putanja: Git/GitHub

Napravi javni repozitorijum u svom GitHub nalogu za celu knjigu, kod i branding. Zadrži `LICENSE.md`, obe licence, `CONTENT_RIGHTS.md` i font notice u repozitorijumu. Stvarni URL repozitorijuma upiši u `book-metadata.json` i `CONTRIBUTING.md` kada ga napraviš. Link ka profilu nije URL repozitorijuma. Njegov koren treba da sadrži `manuscript/` iz ovog paketa. `Book.txt` nabraja poglavlja redom, a `Sample.txt` određuje besplatan uzorak. Generisani `.txt` fajlovi sadrže isti Markdown tekst kao izvorne lekcije.

Na [Leanpub Create Book](https://leanpub.com/create/book) izaberi engleski jezik i Git/GitHub način pisanja. Poveži svoj repozitorijum kroz važeće uputstvo koje Leanpub prikaže tvom nalogu. Učitaj `branding/book-cover.png` kao korice. Unesi naslov, podnaslov i pregledani tekst iz `SALES_PAGE.md`.

Generiši platformsku probnu verziju i pregledaj sadržaj, tabelu, kod, sliku i besplatan uzorak. Lokalni PDF/EPUB su provereni izvozi ovog rukopisa; nisu rezultat Leanpub generatora. Tek nakon platformskog pregleda i završnog autorskog odobrenja objavi prodajnu verziju.

## Alternativa: upload gotovih izdanja

Izaberi Leanpub način za upload sopstvenih ebook fajlova i učitaj PDF i EPUB iz `output/`, prema mogućnostima koje tvoj nalog prikazuje. Ta putanja ne znači da se ZIP automatski uvozi kao knjiga. ZIP je radni paket za tebe; čitaocima se isporučuju ebook i odvojeni prateći materijali koje podesiš.

## Markdown lekcije

Autoritativni sadržaj je u `lessons/*.md`. Posle izmene pokreni:

```bash
python3 tools/create_branding.py
python3 tools/build_book.py
python3 tools/validate_release.py
```

Za EPUB je potreban Pandoc. Za lokalni PDF potrebne su biblioteke iz `tools/requirements-book.txt` i DejaVu fontovi. Izvoz osvežava Leanpub poglavlja; nemoj paralelno ručno menjati i `.md` i generisani `.txt`.

## AI upotreba

Leanpub ima politiku protiv sadržaja slabog kvaliteta i očekuje ljudsku obradu. U ovom paketu AI je generisao tekst i kod, ne samo lektorisao. Zadrži transparentnu izjavu u predgovoru. Pregledaj i AI Usage podešavanje svog naloga; ono nije zamena za vidljivu izjavu u knjizi. Vodi se aktuelnim interfejsom i uslovima platforme.

## Naloga i isplate

Podatke o autoru, isplati i eventualnim poreskim obrascima unosiš na svom nalogu. Ovaj paket ne tvrdi da je dostupnost isplate za tvoju državu proverena. Pre komercijalnog objavljivanja proveri opcije koje Leanpub stvarno ponudi. Izvori cele knjige treba da budu besplatno dostupni u javnom repozitorijumu. Predloženi minimum za ebook je 0 USD, ako izabrani Leanpub način to podržava; iznos dobrovoljne podrške ostaje tvoja odluka. Moguće plaćeno izdanje ne menja otvorene licence. Ovaj paket ne menja cene ili podešavanja na tvom nalogu.

Relevantni izvori: [Git/GitHub workflow](https://help.leanpub.com/en/articles/2916385-getting-started-using-leanpub-s-git-and-github-writing-mode-to-write-and-publish-a-book), [AI kvalitet](https://help.leanpub.com/en/articles/11853585-ai-slop-is-not-permitted-on-leanpub), [AI podešavanje](https://help.leanpub.com/en/articles/9363893-ai-usage-disclosure-details-for-leanpub-authors), [uslovi](https://leanpub.com/terms). Provereno u oktobru 2026.
