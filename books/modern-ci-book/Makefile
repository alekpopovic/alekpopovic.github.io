.PHONY: check site pdf epub sample all clean
PYTHON ?= python3
check:
	$(PYTHON) scripts/check.py
	$(PYTHON) -m unittest discover -s scripts -p 'test_*.py' -v
	cd examples/lab && go test -count=1 ./... && go test -race -count=1 ./... && go vet ./...
site:
	$(PYTHON) scripts/build.py site
pdf:
	$(PYTHON) scripts/build.py pdf
epub:
	$(PYTHON) scripts/build.py epub
sample:
	$(PYTHON) scripts/build.py sample
all: check
	$(PYTHON) scripts/build.py all
clean:
	$(PYTHON) -c "import shutil; shutil.rmtree('dist', ignore_errors=True)"
