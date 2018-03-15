# coding: utf8
from __future__ import unicode_literals, print_function, division


def test_all_equal():
    from clld_phylogeny_plugin.tree import all_equal

    assert all_equal([])
    assert all_equal([1])
    assert all_equal([1, 1])
    assert not all_equal([1, 2])


def test_newick(mocker):
    from clld_phylogeny_plugin.tree import Tree

    class TTree(Tree):
        parameters = [mocker.Mock()]
        labelSpec = {'A': mocker.Mock(), 'C': mocker.Mock(), 'X': mocker.Mock()}

    t = TTree(mocker.Mock(newick='(A,B,(C,D)E)F;'), mocker.Mock())
    assert t.newick == '(A:1,C:2);'
