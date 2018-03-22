# coding: utf8
from __future__ import unicode_literals, print_function, division

import pytest


@pytest.mark.parametrize(
    "method,url,content",
    [
        ('get_html', '/phylogenys', 'Phylogenys'),
        ('get_dt', '/phylogenys', None),
        ('get_html', '/phylogenys/p', 'phy'),
        ('get_html', '/phylogenys/p?parameter=p1&parameter=p3', 'p3'),
        ('get_html', '/phylogenys/p?parameters=p1%2Cp2', 'phy'),
        ('get_html', '/phylogenys/p?parameter=p1&parameter=p3', 'phy'),
        ('get_html', '/phylogenys/p?parameter=p2', 'CLLD_PHYLOGENY_PLUGIN'),
        ('get_html', '/phylogenys/p?parameter=p3', 'No leaf node'),
    ])
def test_url(testapp, method, url, content):
    res = getattr(testapp, method)(url)
    if content:
        assert content in res.body.decode('utf8')
