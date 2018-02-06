# coding: utf8
from __future__ import unicode_literals, print_function, division

from clld.web.datatables.base import DataTable, LinkCol, Col


class Phylogenies(DataTable):
    def col_defs(self):
        return [
            LinkCol(self, 'name'),
            Col(self, 'description'),
        ]
