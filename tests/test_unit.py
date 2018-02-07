# coding: utf8
from __future__ import unicode_literals, print_function, division


def test_all_equal():
    from clld_phylogeny_plugin.tree import all_equal

    assert all_equal([])
    assert all_equal([1])
    assert all_equal([1, 1])
    assert not all_equal([1, 2])
