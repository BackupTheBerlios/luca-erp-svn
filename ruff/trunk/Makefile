# Copyright 2003, 2004 Fundacion Via Libre
#
# This file is part of Xot.
#
# Xot is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Xot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Xot; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

PREFIX=$(HOME)/local
PYTHONVER=2.3
BINDIR=$(PREFIX)/bin
LIBDIR=$(PREFIX)/lib/python2.3/site-packages
SHAREDIR=$(PREFIX)/share/ruff
export SHAREDIR

SUBDIRS=ruff
DATA=ruff.dtd

pwd=$(shell pwd)
python=python$(PYTHONVER)

.PHONY: install clean all

all:
	make -C ruff
	$(python) /usr/lib/$(python)/compileall.py .

install: all
	mkdir -pv $(LIBDIR)
	ln -sf $(pwd)/ruff $(LIBDIR)
	mkdir -pv $(SHAREDIR)
	ln -sf $(pwd)/ruff.dtd $(SHAREDIR)
	ln -sf $(pwd)/caps $(SHAREDIR)
	@echo "***** INSTALLED *****"
	@echo "make sure $(LIBDIR) is in you python path"

clean:
	rm -f *.pyc *.pyo
	$(foreach dir,$(SUBDIRS),make -C $(dir) clean)
