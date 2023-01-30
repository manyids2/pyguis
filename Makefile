SHELL := /usr/bin/fish
DOCSDIR=./docs
VENVDIR="/home/x/.cache/pypoetry/virtualenvs/pyguis-ZdrWZpyJ-py3.10/bin/"

docs:
	source env.fish; \
	cd $(DOCSDIR); \
	make html

.PHONY: docs clean

clean:
	rm -r $(DOCSDIR)/build
