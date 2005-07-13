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

# SRC=stock.xot
# DST=stock.py
# DST=model/stock.sql model/receipt.sql
DST=luca.sql
# SQL=stock.sql
# set these variables
HOST=moby
USER=papo
ADAPTOR=Postgresql
DATABASE=Luca

.PRECIOUS=%.py

# model: build-stamp ${SQL}
model: build-stamp

build-stamp: ${DST}
	$(foreach i,$(patsubst %.sql,%.py,${DST}),mdl_generate_python_code.py -B $(i) && touch $@;)

# ${DST}: ${SRC}
%.py: %.xot
	exotic --no-pickle -eMod -Odatabase:${DATABASE},host:${HOST},user:${USER},adaptorName:${ADAPTOR} $< > $@ || rm $@

# ${SQL}: ${DST}
%.sql: %.py
	mdl_generate_DB_schema.py -c -A $< > $@ || rm $@
# ${SQL}: ${SRC}
# 	exotic --no-pickle -ePg $< > $@ || rm $@

clean:
	rm -rf ${DST} build-stamp

.PHONY: test model all clean
