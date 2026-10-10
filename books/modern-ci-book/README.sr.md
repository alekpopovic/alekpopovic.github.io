# Modern CI — uputstvo za početak

**Building a Reliable CI/CD Platform**  
Autor: **Aleksandar Popovic** · Izdanje 0.1 · oktobar 2026.

Ovo je samostalan repozitorijum tehničke knjige na engleskom. Sadrži 24 poglavlja,
pet dodataka, vežbe sa odgovorima, Go laboratoriju i mapu 80 implementacionih
zadataka. Nije gotova zamena za Jenkins: produkcioni sistem je predmet knjige,
a laboratorija proverava njegove odabrane principe bez mreže i kontejnera.

## Čitanje

Počni od [predgovora](manuscript/00-preface.md). Redosled svih poglavlja je u
`manuscript/Book.txt`. U isporučenom ZIP-u, folder `dist/` sadrži PDF, EPUB,
PDF uzorak i sajt spreman za lokalno pregledanje.

Izvor za sva izdanja je Markdown u folderu `manuscript/`. Izmene unosi tamo,
a zatim ponovo pokreni izvoz. Knjiga opisuje glavni aplikacioni workspace i
sedam submodula, ali se objavljuje kao poseban repo `modern-ci-book`.

## Lokalno generisanje sajta

Potrebni su Python 3.11+ i virtuelno okruženje:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-site.txt
python scripts/check.py
python scripts/build.py epub
python scripts/build.py site
python -m http.server 8000 --directory dist/site --bind 127.0.0.1
```

Otvori `http://127.0.0.1:8000`. Za PDF instaliraj `requirements-print.txt` i
sistemske biblioteke iz [uputstva za izvoz](publishing/BUILDING.md), pa pokreni
`python scripts/build.py all`.

Go testovi se pokreću iz `examples/lab/`. Komanda `make check` proverava i
publikaciju i laboratoriju. Rezultati već izvršenih provera su u
[verification/README.md](verification/README.md). SQL i produkcione integracije
nisu izvršeni u okviru ovog izdanja.

## GitHub

Raspakuj knjigu u nov direktorijum i prati
[publishing/GITHUB.md](publishing/GITHUB.md). Napravi prazan javni repozitorijum,
commituj izvorne fajlove i postavi GitHub Pages da koristi GitHub Actions.
Workflow-i su priloženi, ali objavljivanje nije izvršeno umesto tebe.
Generisani `dist/` je namerno u `.gitignore`; izdanja možeš dodati kao release
priloge, dok se sajt ponovo gradi iz izvora.

Tekst i originalni vizuelni stil su pod CC BY 4.0, a originalni kod i
konfiguracioni primeri pod MIT licencom. Tačnu podelu pogledaj u
[LICENSE.md](LICENSE.md).
