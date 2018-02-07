# coding: utf8
from __future__ import unicode_literals, print_function, division

import pytest


@pytest.mark.parametrize(
    "url,content",
    [
        ('/phylogenys', 'Phylogenys'),
        ('/phylogenys/p', 'phy'),
        ('/phylogenys/p?parameter=p1', 'phy'),
        ('/phylogenys/p?parameter=p2', 'CLLD_PHYLOGENY_PLUGIN'),
        ('/phylogenys/p?parameter=p3', 'No leaf node'),
    ])
def test_url(testapp, url, content):
    res = testapp.get(url)
    assert content in res.body.decode('utf8')
