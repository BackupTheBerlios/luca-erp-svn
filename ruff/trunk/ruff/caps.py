# -*- python -*- coding: latin1 -*-
#
# Copyright 2003,2004 Fundación Vía Libre
#
# This file is part of ruff.
#
# ruff is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# ruff is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PAPO; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

from ConfigParser import ConfigParser
import re

class InvalidCapName(Exception):
    pass

escapes = {
    "NUL": 0x00,
    "SOH": 0x01,
    "STX": 0x02,
    "ETX": 0x03,
    "EOT": 0x04,
    "ENQ": 0x05,
    "ACK": 0x06,
    "BEL": 0x07,
    "BS": 0x08,
    "HT": 0x09,
    "LF": 0x0A,
    "VT": 0x0B,
    "FF": 0x0C,
    "CR": 0x0D,
    "SO": 0x0E,
    "SI": 0x0F,
    "DLE": 0x10,
    "DC1": 0x11,
    "DC2": 0x12,
    "DC3": 0x13,
    "DC4": 0x14,
    "NAK": 0x15,
    "SYN": 0x16,
    "ETB": 0x17,
    "CAN": 0x18,
    "EM": 0x19,
    "SUB": 0x1A,
    "ESC": 0x1B,
    "FS": 0x1C,
    "GS": 0x1D,
    "RS": 0x1E,
    "US": 0x1F,
    "SPACE": 0x20,
    "SPC": 0x20,
    "DEL": 0x7F,
    }


class Caps (object):
    def __init__(self, capfile):
        d = {'start': '', 'end': '', 'width': '0.0', 'description': ''}
        r = re.compile('\s*')
        config = ConfigParser(d)
        config.read(capfile)
        self.sections = {}
        for i in config.sections():
            if i.find(",") is not -1:
                raise InvalidCapName, "cap names can't contain commas; `%s' does." % i
            h = {}
            for j in d.keys():
                if j in ('start', 'end'):
                    h[j] = "".join([escapes.has_key(k)
                                    and chr(escapes[k])
                                    or k for k in r.split(config.get(i, j))])
                else:
                    h[j] = config.get(i, j)
            self.sections[i] = h

    def start(self, caps):
        caps = [self.sections[cap.strip()]['start'] for cap in caps.split("+")]
        return "".join(caps)
    def end(self, caps):
        caps = [self.sections[cap.strip()]['end'] for cap in caps.split("+")]
        caps.reverse()
        return "".join(caps)
    def width(self, caps):
        caps = [self.sections[cap.strip()]['width'] for cap in caps.split("+")]
        return reduce(lambda a, b: a+b, caps, 0)
    def description(self, caps):
        caps = [self.sections[cap.strip()]['description'] for cap in caps.split("+")]
        return ", ".join(caps)

    def apply(self, caps, thing):
        return self.start(caps) + str(thing) + self.end(caps)

