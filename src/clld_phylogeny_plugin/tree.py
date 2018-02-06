# coding: utf8
from __future__ import unicode_literals, print_function, division

from itertools import chain
from operator import eq

from six import PY2

from zope.interface import implementer
from sqlalchemy.orm import joinedload
from clldutils.misc import lazyproperty
from clld.db.meta import DBSession
from clld.db.models.common import Parameter
from clld.web.util.component import Component
from clld.web.util.htmllib import HTML
from clld.web.util.helpers import link, map_marker_img
import ete3

from clld_phylogeny_plugin.interfaces import ITree


def all_equal(iterator, op=eq):
    iterator = iter(iterator)
    try:
        first = next(iterator)
    except StopIteration:
        return True
    return all(op(first, rest) for rest in iterator)


@implementer(ITree)
class Tree(Component):
    """Represents the configuration for a leaflet map."""

    __template__ = 'clld_phylogeny_plugin:templates/tree.mako'

    def __init__(self, ctx, req, eid='tree'):
        """Initialize.

        :param ctx: context object of the current request.
        :param req: current pyramid request object.
        :param eid: Page-unique DOM-node ID.
        """
        self.req = req
        self.ctx = ctx
        self.eid = eid
        if 'parameter' in req.params:
            self.parameter = DBSession.query(Parameter) \
                .filter(Parameter.id == req.params['parameter']) \
                .options(joinedload(Parameter.valuesets)) \
                .one()
        else:
            self.parameter = None

    @lazyproperty
    def newick(self):
        if self.parameter:
            t = ete3.Tree(self.ctx.newick, format=1)
            nodes = [n.encode('utf8') if PY2 else n for n in self.labelSpec.keys()]
            try:
                t.prune(nodes, preserve_branch_length=True)
            except ValueError as e:  # pragma: no cover
                if 'Node names not found: [' in e.message:
                    for name in eval('[' + e.message.split('[')[1]):
                        try:
                            nodes.remove(name.encode('utf8') if PY2 else name)
                        except ValueError:
                            pass
                    t.prune(nodes, preserve_branch_length=True)
                else:
                    raise
            return t.write(format=1)
        return self.ctx.newick

    def get_label_properties(self, label):
        #
        # FIXME: in case of different values for languages, display marker in tooltip,
        # and use triangle as shape!!
        #
        res = {
            'eid': 'tlpk{0}'.format(label),
            'shape': 'c',
            'color': '#ff6600',
            'conflict': False,
            'tooltip_title': 'Related {0}'.format(self.req.translate('Languages')),
        }
        if self.parameter:
            def comp(a, b):
                if self.parameter.domain:
                    return a.domainelement_pk == b.domainelement_pk
                return a.name == b.name

            values = list(chain(*[
                self.language2valueset[l.pk].values for l in label.languages
                if l.pk in self.language2valueset]))
            res['conflict'] = not all_equal(values, op=comp)
            if not res['conflict']:
                lis = [
                    HTML.li(link(self.req, l)) for l in label.languages
                    if l.pk in self.language2valueset]
            else:
                lis = []
                for v in values:
                    lis.append(HTML.li(map_marker_img(self.req, v), link(self.req, v.valueset.language)))
            res['tooltip'] = HTML.ul(*lis, class_='unstyled')
            for lang in label.languages:
                if lang.pk in self.language2valueset:
                    res['shape'], res['color'] = self.get_marker(self.language2valueset[lang.pk])
                    break
        else:
            res['tooltip'] = HTML.ul(*[HTML.li(link(self.req, l)) for l in label.languages])
        return res

    @staticmethod
    def head(req):
        return '\n'.join(
            "{0}".format(e) for e in [
                HTML.link(rel="stylesheet", href=req.static_url('clld_phylogeny_plugin:static/phylotree.css')),
                HTML.script(src="//d3js.org/d3.v3.min.js"),
                HTML.script(src="https://cdnjs.cloudflare.com/ajax/libs/underscore.js/1.8.3/underscore-min.js", charset="utf-8"),
                HTML.script(type="text/javascript", src=req.static_url('clld_phylogeny_plugin:static/phylotree.js')),
                HTML.script(type="text/javascript", src=req.static_url('clld_phylogeny_plugin:static/clld_phylogeny_plugin.js')),
            ])

    @lazyproperty
    def language2valueset(self):
        if self.parameter:
            return {vs.language_pk: vs for vs in self.parameter.valuesets}
        return {}

    @lazyproperty
    def labelSpec(self):
        if self.parameter:
            return {
                l.name: self.get_label_properties(l) for l in self.ctx.treelabels
                if any(lang.pk in self.language2valueset for lang in l.languages)}
        return {l.name: self.get_label_properties(l) for l in self.ctx.treelabels if l.languages}

    def get_default_options(self):
        return {
            'reroot': False,
            'brush': False,
            'align-tips': True,
            'show-scale': False
        }

    def get_marker(self, valueset):
        return 'c', '#ff6600'
