PYTHON ?= python3
.PHONY: check test verify book html pdf epub serve clean
check:
	$(PYTHON) scripts/check.py
test:
	cd examples/go-core && go test -race ./... && go vet ./...
	$(PYTHON) -m unittest discover -s examples/audit -v
	$(PYTHON) -m unittest discover -s examples/kubernetes -v
verify: check test
book:
	$(PYTHON) scripts/build.py --format all
	$(PYTHON) scripts/check_epub.py dist/AgentPlane-Book.epub
html:
	$(PYTHON) scripts/build.py --format html
pdf:
	$(PYTHON) scripts/build.py --format pdf
epub:
	$(PYTHON) scripts/build.py --format epub
	$(PYTHON) scripts/check_epub.py dist/AgentPlane-Book.epub
serve: html
	$(PYTHON) -m http.server --bind 127.0.0.1 --directory _site 8000
clean:
	$(PYTHON) -c "import shutil; [shutil.rmtree(p, ignore_errors=True) for p in ['_site', '.build']]"
