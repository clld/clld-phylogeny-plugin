from clld.interfaces import IParameter
from clld.web.adapters.base import Representation
from clld_phylogeny_plugin.models import Phylogeny
from clld_phylogeny_plugin.datatables import Phylogenies
from clld_phylogeny_plugin.interfaces import IPhylogeny, ITree
from clld_phylogeny_plugin.tree import Tree


def includeme(config):
    config.add_static_view('clld-phylogeny-plugin-static', 'clld_phylogeny_plugin:static')
    config.registry.settings['mako.directories'].append(
        'clld_phylogeny_plugin:templates')
    # We must make sure to register the datatable before registering the resource, to
    # prevent a default DataTable to be registered.
    config.register_datatable('phylogenys', Phylogenies, overwrite=False)
    config.register_resource('phylogeny', Phylogeny, IPhylogeny, with_index=True)
    specs = [
        [
            IParameter,
            Representation,
            'application/vnd.clld.valuetable+xml',
            'valuetable.html',
            'parameter/valuetable_html.mako',
            {'rel': None}],
        [
            IPhylogeny,
            Representation,
            'application/vnd.clld.description+xml',
            'description.html',
            'phylogeny/description_html.mako',
            {'rel': None}],
    ]
    config.register_adapters(specs)
    config.register_utility(Tree, ITree, overwrite=False)
