import operator
import functools
import itertools
import collections
from typing import Any, Callable, Optional

from zope.interface import implementer
from sqlalchemy.orm import joinedload
from clld.db.meta import DBSession
from clld.db.models.common import Parameter, ValueSet
from clld.web.util.component import Component
from clld.web.util.htmllib import HTML
from clld.web.util.helpers import link, map_marker_img
from newick import loads

from clld_phylogeny_plugin.interfaces import ITree


def all_equal(iterator, op: Callable[[Any, Any], bool] = operator.eq) -> bool:
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

    @functools.cached_property
    def parameters(self) -> list[Parameter]:  # pylint: disable=C0116
        pids = []
        if 'parameter' in self.req.params:
            pids = self.req.params.getall('parameter')
        elif 'parameters' in self.req.params:
            pids = self.req.params['parameters'].split(',')

        if pids:
            return DBSession.query(Parameter)\
                .filter(Parameter.id.in_(pids))\
                .options(
                    joinedload(Parameter.valuesets).joinedload(ValueSet.values),
                    joinedload(Parameter.domain))\
                .all()
        return []

    @functools.cached_property
    def domains(self):  # pylint: disable=C0116
        return [
            collections.OrderedDict([(de.pk, de) for de in p.domain])
            for p in self.parameters]

    @functools.cached_property
    def newick(self):
        if self.parameters:
            t = loads(self.ctx.newick)[0]
            nodes = set(n for n in self.labelSpec.keys())

            def drop_internal_names(n):
                if not n.is_leaf:
                    n.name = None
            t.prune_by_names(
                nodes.intersection(set(n.name for n in t.walk() if n.name)), inverse=True)
            t.remove_redundant_nodes(preserve_lengths=True, keep_leaf_name=True)
            t.visit(drop_internal_names)
            leafs = [n for n in t.walk() if n.is_leaf]
            if len(leafs) < 2:
                return
            return t.newick + ';'
        return self.ctx.newick

    def get_label_properties(self, label, pindex=None) -> dict[str, Any]:
        res = {
            'eid': f'tlpk{label}-{pindex}',
            'shape': 'c',
            'color': '#ff6600',
            'conflict': False,
            'tooltip_title': f"Related {self.req.translate('Languages')}",
        }
        if pindex is not None:
            parameter = self.parameters[pindex]
            domain = self.domains[pindex]
            language2valueset: dict[int, ValueSet] = {
                k: v[pindex] for k, v in self.language2valueset.items() if v[pindex]}

            def vname(v):
                return domain[v.domainelement_pk].name if v.domainelement_pk else v.name

            def comp(a, b):
                if parameter.domain:
                    return a.domainelement_pk == b.domainelement_pk
                return a.name == b.name

            values = list(itertools.chain(*[
                language2valueset[lg.pk].values for lg in label.languages
                if lg.pk in language2valueset]))
            if not values:
                res['tooltip_title'] = 'Missing data'
                res['tooltip'] = None
                res['shape'] = 's'
                res['color'] = '#fff'
            else:
                res['conflict'] = not all_equal(values, op=comp)
                if not res['conflict']:
                    res['tooltip_title'] = f'{values[0].valueset.parameter.id}: {vname(values[0])}'
                    lis = [
                        HTML.li(link(self.req, lg)) for lg in label.languages
                        if lg.pk in language2valueset]
                else:
                    res['tooltip_title'] = f'{values[0].valueset.parameter.id}'
                    lis = []
                    for v in values:
                        lis.append(HTML.li(
                            map_marker_img(
                                self.req, domain[v.domainelement_pk] if v.domainelement_pk else v),
                            f'{vname(v)}: ',
                            link(self.req, v.valueset.language)))
                res['tooltip'] = HTML.ul(*lis, class_='unstyled')
                for lang in label.languages:
                    if lang.pk in language2valueset:
                        res['shape'], res['color'] = self.get_marker(language2valueset[lang.pk])
                        break
        else:
            res['tooltip'] = HTML.ul(
                *[HTML.li(link(self.req, lg)) for lg in label.languages])
        return res

    @staticmethod
    def head(req):
        return '\n'.join(
            f"{e}" for e in [
                HTML.link(
                    rel="stylesheet",
                    href=req.static_url('clld_phylogeny_plugin:static/phylotree.css')),
                HTML.script(
                    src=req.static_url('clld_phylogeny_plugin:static/d3.v5.js')),
                HTML.script(
                    src=req.static_url('clld_phylogeny_plugin:static/underscore-min.js'),
                    charset="utf-8"),
                HTML.script(
                    type="text/javascript",
                    src=req.static_url('clld_phylogeny_plugin:static/phylotree.js')),
                HTML.script(
                    type="text/javascript",
                    src=req.static_url(
                        'clld_phylogeny_plugin:static/clld_phylogeny_plugin.js')),
            ])

    @functools.cached_property
    def language2valueset(self) -> Optional[dict[int, list[Optional[ValueSet]]]]:
        if self.parameters:
            res = collections.defaultdict(lambda: [None] * len(self.parameters))
            for i, param in enumerate(self.parameters):
                for vs in param.valuesets:
                    res[vs.language_pk][i] = vs
            return res
        return None

    @functools.cached_property
    def labelSpec(self):
        if self.parameters:
            return {
                lb.name: [self.get_label_properties(lb, i) for i in range(len(self.parameters))]
                for lb in self.ctx.treelabels
                if any(lang.pk in self.language2valueset for lang in lb.languages)}
        return {
            lb.name: [self.get_label_properties(lb)] for lb in self.ctx.treelabels if lb.languages}

    def get_default_options(self):
        return {
            'align-tips': True,
            'show-scale': False,
        }

    def get_marker(self, valueset: ValueSet):
        if valueset.values:
            val = valueset.values[0]
            if val.domainelement and val.domainelement.jsondatadict.get('icon'):
                icon = val.domainelement.jsondatadict.get('icon')
                return icon[:1], '#' + icon[1:]
        return 'c', '#ff6600'
