XOT=luca.xot
XINS=xins/product.xin

TARGETS=product.xml person.xml

PYTHON ?= python
COLORIZER= cat
COLORIZER ?= tools/ppython
EPYDOC ?= epydoc
EPYDOC_OPTS ?=
TESTOPTS ?=

all: $(TARGETS) model

%.xml: xins/%.xin $(XOT)
	exotic -n -eCimarronXMLui -Oxin:$< $(XOT) > $@ || rm $@

test:
	PYTHONPATH=.:$$PYTHONPATH $(PYTHON) test/run.py $(TESTOPTS) 2>&1 | $(COLORIZER)

# set these variables
DST=luca.sql
HOST=localhost
USER=papo
ADAPTOR=Postgresql
DATABASE=Luca

.PRECIOUS=%.py

model: build-stamp

build-stamp: ${DST} $(patsubst %.sql,%.py,${DST})
	mdl_generate_python_code.py -B $(patsubst %.sql,%.py,${DST}) && touch $@

%.py: %.xot
	exotic --no-pickle -eMod -Odatabase:${DATABASE},host:${HOST},user:${USER},adaptorName:${ADAPTOR} $< > $@ || rm $@

%.sql: %.py
	mdl_generate_DB_schema.py -c -A $< > $@ || rm $@

clean:
	rm -rf ${DST} build-stamp

.PHONY: test model all clean
