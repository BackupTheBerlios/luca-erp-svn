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

from ruff.ruff import Report
import time, sys

x = Report("Reporte-new.xml")

fecha=time.asctime()
x.header(fecha=fecha)

x.add_detail ('ingresos')
x.add_dentry ('item', concepto="Venta de contado",
                        cash="1",
                        cheque="10",
                        otros="100",
                        total="111",
                        )
x.add_dentry ('item', concepto="Cobranza Cartera activa",
                        cash="10",
                        cheque="100",
                        otros="1000",
                        total="1110",
                        )
x.add_dentry ('item', concepto="Cobranza Morosos",
                        cash="0",
                        cheque="10",
                        otros="2500",
                        total="2510",
                        )
x.add_dentry ('item', concepto="Ventas Inusuales",
                        cash="0",
                        cheque="100000",
                        otros="0",
                        total="100000",
                        )
x.add_dentry ('item', concepto="Extraccion Banco",
                        cash="100000",
                        cheque="0",
                        otros="0",
                        total="100000",
                        )
# x.ingresos.footer(cash="23",
                  # cheque = "1234",
                  # otros = "124",
                  # total = "12344")
x.close_detail ()

x.add_detail ('egresos')
x.add_dentry ('item', concepto="Pagos proveedores",
                       cash="0",
                       cheque="0",
                       otros="0",
                       total="0",
                       )
x.add_dentry ('item', concepto="Compra insumos",
                       cash="0",
                       cheque="0",
                       otros="0",
                       total="0",
                       )
x.add_dentry ('item', concepto="Otros",
                       cash="0",
                       cheque="0",
                       otros="0",
                       total="0",
                       )
x.add_dentry ('item', concepto="Adelantos y retiros",
                       cash="0",
                       cheque="0",
                       otros="0",
                       total="0",
                       )
x.add_dentry ('item', concepto="Deposito de valores",
                       cash="0",
                       cheque="0",
                       otros="0",
                       total="0",
                       )
x.add_dentry ('item', concepto="Banco YYY",
                       cash="0",
                       cheque="0",
                       otros="0",
                       total="0",
                       )
x.add_dentry ('item', concepto="Banco XXX",
                       cash="0",
                       cheque="0",
                       otros="0",
                       total="0",
                       )


# x.egresos.footer(cash="23",
#                  cheque = "1234",
#                  otros = "124",
#                  total = "12344")
# x.page_footer(cash="23",
#          cheque = "1234",
#          otros = "124",
#          total = "12344")

print x.render()
