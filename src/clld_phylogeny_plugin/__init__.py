from __future__ import unicode_literals

from clld_phylogeny_plugin.models import Phylogeny
from clld_phylogeny_plugin.datatables import Phylogenies
from clld_phylogeny_plugin.interfaces import IPhylogeny, ITree
from clld_phylogeny_plugin.tree import Tree


def includeme(config):
    config.add_static_view('clld-phylogeny-plugin-static', 'clld_phylogeny_plugin:static')
    config.registry.settings['mako.directories'].append(
        'clld_phylogeny_plugin:templates')
    config.register_resource('phylogeny', Phylogeny, IPhylogeny, with_index=True)
    config.register_datatable('phylogenys', Phylogenies, overwrite=False)
    config.register_utility(Tree, ITree, overwrite=False)
