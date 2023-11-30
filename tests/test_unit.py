
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

    t = TTree(mocker.Mock(newick='(A:1.5,B:1,(C:1,D:1)E:1)F:1;'), mocker.Mock())
    assert t.newick == '(A:1.5,C:2.0):1;'
