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

class RuffError(Exception):
    pass

class RuffTemplateError(RuffError):
    pass

class UnboundFieldError(RuffTemplateError):
    pass

class DuplicateFQDN(RuffTemplateError):
    pass

class InvalidTemplateError(RuffTemplateError):
    pass

class UnknownFieldError(RuffTemplateError):
    pass

class RuffReportError(RuffError):
    pass

class InvalidExtremaError(RuffReportError):
    pass

class ReportOverflowError(RuffReportError):
    pass

