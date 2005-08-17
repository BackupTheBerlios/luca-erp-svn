# Copyright 2005 Fundación Via Libre
#
# This file is part of PAPO.
#
# PAPO is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# PAPO is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# PAPO; if not, write to the Free Software Foundation, Inc., 59 Temple Place,
# Suite 330, Boston, MA 02111-1307 USA

XOT=luca.xot

PYMODEL=fvl/luca/model/pymodel_luca.py
SQL=luca.sql
TARGETS=product.xml \
	person.xml \
	document_type.xml \
	$(SQL) $(PYMODEL)

PYTHON ?= python
COLORIZER ?= 2>&1 | tools/ppython
EPYDOC ?= epydoc
EPYDOC_OPTS ?=
TESTOPTS ?=
EXOTIC ?= exotic
EXOTIC_OPTS ?= --no-pickle

# set these variables
LUCA_DATABASE ?= Luca
LUCA_HOST ?= localhost
LUCA_USER ?= $$USER
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

# transaction test database
TR_TEST_PYMODEL = test/tr_pymodel_test.py
TR_TEST_DB = tr_test.db
TR_CACHE_TEST_DB = tr_cache.db

# luca tests database
LUCA_TEST_PYMODEL = test/luca_pymodel_test.py
LUCA_TEST_DB = luca_test.db
LUCA_CACHE_TEST_DB = luca_cache.db
LUCA_TEST_INI=test/luca_test.ini

all: $(TARGETS)

%.xml: xins/%.xin $(XOT)
	$(EXOTIC) -n -eCimarronXMLui -Oxin:$< $(XOT) > $@

test: $(LUCA_TEST_PYMODEL) $(TR_CACHE_TEST_DB) $(LUCA_CACHE_TEST_DB)
	PYTHONPATH=.:$$PYTHONPATH MDL_DB_CONNECTIONS_CFG=$(LUCA_TEST_INI) \
		LUCA_PYMODEL=$(LUCA_TEST_PYMODEL) \
		$(PYTHON) test/run.py $(TESTOPTS) $(COLORIZER)
	$(RM) *_test.db

$(LUCA_TEST_PYMODEL): $(XOT)
	$(EXOTIC) -eMod -Odatabase:test.db,adaptorName:SQLite $< > $@

%_cache.db: %_test.db
	mv $< $@

%_test.db: test/%_pymodel_test.py
	$(RM) $@
	mdl_generate_DB_schema.py -C --admin-dsn :$@:: $<

$(PYMODEL): $(XOT)
	$(EXOTIC) $(EXOTIC_PYTHON_OPTS) $< > $@

$(SQL): $(PYMODEL)
	mdl_generate_DB_schema.py -c -A $< > $@

clean:
	$(RM) $(TARGETS) $(TR_TEST_DB) $(TR_CACHE_TEST_DB) $(LUCA_TEST_DB) $(LUCA_CACHE_TEST_DB)

distclean: clean
	find '(' -name '*.py[co]' -o -name '*~' ')' -print0 | xargs -0 -r $(RM)
	$(RM) $(TR_CACHE_TEST_DB)

.PHONY: test model all clean

.DELETE_ON_ERROR:

.INTERMEDIATE: $(TR_TEST_DB) $(LUCA_TEST_DB)
