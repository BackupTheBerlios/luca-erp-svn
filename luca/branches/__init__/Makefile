XOT=luca.xot

TARGETS=product.xml person.xml luca.sql luca.py

PYTHON ?= python
COLORIZER ?= tools/ppython
EPYDOC ?= epydoc
EPYDOC_OPTS ?=
TESTOPTS ?=
EXOTIC ?= exotic
EXOTIC_OPTS ?= --no-pickle

# set these variables
LUCA_DATABASE ?= luca
LUCA_HOST ?= localhost
LUCA_USER ?= papo
LUCA_ADAPTOR ?= Postgresql
LUCA_MODEL ?= Luca
LUCA_PACKAGE ?= fvl.luca
LUCA_MODULE ?= model

EXOTIC_PYTHON_OPTS := $(EXOTIC_OPTS) -eMod -Odatabase:$(LUCA_DATABASE)
EXOTIC_PYTHON_OPTS := $(EXOTIC_PYTHON_OPTS),host:$(LUCA_HOST)
EXOTIC_PYTHON_OPTS := $(EXOTIC_PYTHON_OPTS),user:$(LUCA_USER)
EXOTIC_PYTHON_OPTS := $(EXOTIC_PYTHON_OPTS),adaptorName:$(LUCA_ADAPTOR)
EXOTIC_PYTHON_OPTS := $(EXOTIC_PYTHON_OPTS),modelName:$(LUCA_MODEL)
EXOTIC_PYTHON_OPTS := $(EXOTIC_PYTHON_OPTS),packageName:$(LUCA_PACKAGE)
EXOTIC_PYTHON_OPTS := $(EXOTIC_PYTHON_OPTS),moduleName:$(LUCA_MODULE)

all: $(TARGETS)

%.xml: xins/%.xin $(XOT)
	$(EXOTIC) -n -eCimarronXMLui -Oxin:$< $(XOT) > $@

test: luca.py
	PYTHONPATH=.:$$PYTHONPATH $(PYTHON) test/run.py $(TESTOPTS) 2>&1 | $(COLORIZER)

%.py: %.xot
	$(EXOTIC) $(EXOTIC_PYTHON_OPTS) $< > $@

%.sql: %.py
	mdl_generate_DB_schema.py -c -A $< > $@

clean:
	$(RM) $(TARGETS)

distclean: clean
	find '(' -name '*.py[co]' -o -name '*~' ')' -print0 | xargs -0 -r $(RM)

.PHONY: test model all clean

.DELETE_ON_ERROR:
