import operator
import itertools
import collections

from zope.interface import implementer
from sqlalchemy.orm import joinedload
from clldutils.misc import lazyproperty
from clld.db.meta import DBSession
from clld.db.models.common import Parameter, ValueSet
from clld.web.util.component import Component
from clld.web.util.htmllib import HTML
from clld.web.util.helpers import link, map_marker_img
import ete3
from ete3.coretype.tree import TreeError

from clld_phylogeny_plugin.interfaces import ITree


def all_equal(iterator, op=operator.eq):
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

    @lazyproperty
    def parameters(self):
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

    @lazyproperty
    def domains(self):
        return [
            collections.OrderedDict([(de.pk, de) for de in p.domain])
            for p in self.parameters]

    @lazyproperty
    def newick(self):
        if self.parameters:
            t = ete3.Tree(self.ctx.newick, format=1)
            nodes = set(n for n in self.labelSpec.keys())
            try:
                t.prune(
                    nodes.intersection(set(n.name for n in t.traverse())),
                    preserve_branch_length=True)
            except TreeError:
                return
            return t.write(format=1)
        return self.ctx.newick

    def get_label_properties(self, label, pindex=None):
        res = {
            'eid': 'tlpk{0}-{1}'.format(label, pindex),
            'shape': 'c',
            'color': '#ff6600',
            'conflict': False,
            'tooltip_title': 'Related {0}'.format(self.req.translate('Languages')),
        }
        if pindex is not None:
            parameter = self.parameters[pindex]
            domain = self.domains[pindex]
            language2valueset = {
                k: v[pindex] for k, v in self.language2valueset.items() if v[pindex]}

            def vname(v):
                return domain[v.domainelement_pk].name if v.domainelement_pk else v.name

            def comp(a, b):
                if parameter.domain:
                    return a.domainelement_pk == b.domainelement_pk
                return a.name == b.name

            values = list(itertools.chain(*[
                language2valueset[l.pk].values for l in label.languages
                if l.pk in language2valueset]))
            if not values:
                res['tooltip_title'] = 'Missing data'
                res['tooltip'] = None
                res['shape'] = 's'
                res['color'] = '#fff'
            else:
                res['conflict'] = not all_equal(values, op=comp)
                if not res['conflict']:
                    res['tooltip_title'] = '{0}: {1}'.format(
                        values[0].valueset.parameter.id, vname(values[0]))
                    lis = [
                        HTML.li(link(self.req, l)) for l in label.languages
                        if l.pk in language2valueset]
                else:
                    res['tooltip_title'] = '{0}'.format(values[0].valueset.parameter.id)
                    lis = []
                    for v in values:
                        lis.append(HTML.li(
                            map_marker_img(
                                self.req, domain[v.domainelement_pk]
                                if v.domainelement_pk else v),
                            '{0}: '.format(vname(v)),
                            link(self.req, v.valueset.language)))
                res['tooltip'] = HTML.ul(*lis, class_='unstyled')
                for lang in label.languages:
                    if lang.pk in language2valueset:
                        res['shape'], res['color'] = self.get_marker(
                            language2valueset[lang.pk])
                        break
        else:
            res['tooltip'] = HTML.ul(
                *[HTML.li(link(self.req, l)) for l in label.languages])
        return res

    @staticmethod
    def head(req):
        return '\n'.join(
            "{0}".format(e) for e in [
                HTML.link(
                    rel="stylesheet",
                    href=req.static_url('clld_phylogeny_plugin:static/phylotree.css')),
                HTML.script(
                    src="https://d3js.org/d3.v3.min.js"),
                HTML.script(
                    src="https://cdnjs.cloudflare.com/ajax/libs/underscore.js/1.8.3/"
                        "underscore-min.js",
                    charset="utf-8"),
                HTML.script(
                    type="text/javascript",
                    src=req.static_url('clld_phylogeny_plugin:static/phylotree.js')),
                HTML.script(
                    type="text/javascript",
                    src=req.static_url(
                        'clld_phylogeny_plugin:static/clld_phylogeny_plugin.js')),
            ])

    @lazyproperty
    def language2valueset(self):
        if self.parameters:
            res = collections.defaultdict(lambda: [None] * len(self.parameters))
            for i, param in enumerate(self.parameters):
                for vs in param.valuesets:
                    res[vs.language_pk][i] = vs
            return res

    @lazyproperty
    def labelSpec(self):
        if self.parameters:
            return {
                l.name: [self.get_label_properties(l, i)
                         for i in range(len(self.parameters))]
                for l in self.ctx.treelabels
                if any(lang.pk in self.language2valueset for lang in l.languages)}
        return {
            l.name: [self.get_label_properties(l)]
            for l in self.ctx.treelabels if l.languages}

    def get_default_options(self):
        return {
            'reroot': False,
            'brush': False,
            'align-tips': True,
            'show-scale': False
        }

    def get_marker(self, valueset):
        if valueset.values:
            val = valueset.values[0]
            if val.domainelement and val.domainelement.jsondatadict.get('icon'):
                icon = val.domainelement.jsondatadict.get('icon')
                return icon[:1], '#' + icon[1:]
        return 'c', '#ff6600'
