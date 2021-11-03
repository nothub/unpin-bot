help:
	@awk 'BEGIN {FS = ":.*##"; printf "targets:\n"} /^[$$()% 0-9a-zA-Z_-]+:.*?##/ { printf "  %-16s%s\n", $$1, $$2 } /^##@/ { printf "\n%s\n" } ' $(MAKEFILE_LIST)

# test build requirements
REQUIRED_BINS := python3 pip3
$(foreach bin,$(REQUIRED_BINS),\
    $(if $(shell command -v $(bin) 2> /dev/null),$(),$(error please install missing build requirement: `$(bin)`)))

.ONESHELL:
# this will be evaluated to set the shell, even when not called explicitly
shell: $(eval SHELL:=/bin/bash)

all: help

virtualenv:
	test -d venv || python3 -m venv venv

requirements: virtualenv requirements.txt
	source venv/bin/activate
	pip3 install -r requirements.txt

run: requirements ## run in virtual environment
	source venv/bin/activate
	python3 main.py

pyz: requirements ## package as self contained pyz
	source venv/bin/activate
	pip3 install shiv wheel
	python3 -m shiv \
	--entry-point main:main \
	--python '/usr/bin/env python3' \
	--compressed \
	--output-file app.pyz \
	. \
	--requirement requirements.txt

clean: ## remove temporary files
	rm app.pyz
	rm -rf __pycache__
	rm -rf venv
