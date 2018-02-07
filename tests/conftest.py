# coding: utf8
from __future__ import unicode_literals, print_function, division

from pyramid import testing
from pyramid import config
import pytest

from pytest_clld._app import ExtendedTestApp as TestApp


@pytest.fixture(scope='module')
def testapp():
    from clld.db.meta import DBSession, VersionedDBSession, Base
    from clld.db.models import common
    from clld_phylogeny_plugin import models

    def main():
        cfg = config.Configurator(settings={
            'sqlalchemy.url': 'sqlite://',
            'mako.directories': [
                'clld:web/templates',
                'clld_phylogeny_plugin:templates'
            ]})
        cfg.include('clld.web.app')
        cfg.include('clld_phylogeny_plugin')
        return cfg.make_wsgi_app()

    DBSession.remove()
    VersionedDBSession.remove()
    wsgi_app = main()
    Base.metadata.bind = DBSession.bind
    Base.metadata.create_all()
    DBSession.add(common.Dataset(id='1', name='test app', domain='example.org'))
    contrib = common.Contribution(id='c', name='c')

    lang1 = common.Language(id='l1', latitude=2, longitude=2)
    lang2 = common.Language(id='l2', latitude=2, longitude=2)

    # parameter without domain:
    param1 = common.Parameter(id='p1', name='p1')
    vs = common.ValueSet(id='vs1', language=lang1, parameter=param1, contribution=contrib)
    common.Value(id='v1', name='abc', valueset=vs)
    common.Value(id='v2', name='bcd', valueset=vs)

    # parameter with domain:
    param2 = common.Parameter(id='p2', name='p2')
    de = common.DomainElement(id='de', name='de', parameter=param2)
    vs = common.ValueSet(id='vs2', language=lang1, parameter=param2, contribution=contrib)
    common.Value(id='v3', name='abc', valueset=vs, domainelement=de)
    common.Value(id='v4', name='bcd', valueset=vs, domainelement=de)

    # parameter with unrelated languages only:
    param3 = common.Parameter(id='p3', name='p3')
    vs = common.ValueSet(id='vs3', language=lang2, parameter=param3, contribution=contrib)
    common.Value(id='v5', name='abc', valueset=vs)

    phy = models.Phylogeny(id='p', name='phylo', newick="((beri1255,east2533),(((baff1240,labr1244,queb1248),((anak1241,nort2944,poin1245),(kobu1239,kotz1238)),(east2535,pola1254,west2617),(cari1277,copp1244,nets1241,sigl1242)),((paci1278,kusk1241),(aiwa1238,chap1266))));")
    label = models.TreeLabel(phylogeny=phy, id='cari1277', name='cari1277')
    DBSession.add(phy)
    DBSession.flush()
    models.LanguageTreeLabel(language=lang1, treelabel=label)
    yield TestApp(wsgi_app)


@pytest.fixture(scope='module')
def configurator():
    config = testing.setUp(
        request=testing.DummyRequest(translate=lambda s: s),
        settings={
            'sqlalchemy.url': 'sqlite://',
            'mako.directories': []})
    config.include('clld.web.app')
    config.include('clld_phylogeny_plugin')
    yield config
    testing.tearDown()
