# clld-phylogeny-plugin

Plugin for the [clld](https://github.com/clld/clld) framework providing
support for phylogenetic trees in clld apps.

This plugin includes the [phylotree](https://github.com/veg/phylotree.js/tree/master)
library to render phylogenetic trees in the browser.

[![Build Status](https://travis-ci.org/clld/clld-phylogeny-plugin.svg?branch=master)](https://travis-ci.org/clld/clld-phylogeny-plugin)
[![codecov](https://codecov.io/gh/clld/clld-phylogeny-plugin/branch/master/graph/badge.svg)](https://codecov.io/gh/clld/clld-phylogeny-plugin)
[![PyPI](https://img.shields.io/pypi/v/clld-phylogeny-plugin.svg)](https://pypi.python.org/pypi/clld-phylogeny-plugin)


## Introduction

While plotting cross-linguistic data on a map serves as quick visualization of the correlation between the data and geography, plotting the data on a phylogenetic tree allows inspection of the correlation between the data and some theory about language relatedness, embodied in the tree.

The `clld-phylogeny-plugin` package supports this kind of visualization by
- adding [database models](https://github.com/clld/clld-phylogeny-plugin/blob/master/src/clld_phylogeny_plugin/models.py) to store phylogenetic trees (and how the tree labels correspond to `Language` objects)
- adding a [`Tree` component](https://github.com/clld/clld-phylogeny-plugin/blob/f98e83681e7464d3abfb05eae2f1a3c74fdabc1f/src/clld_phylogeny_plugin/tree.py#L34), allowing simple rendering of a tree on a page
- adding support for "plotting" `Parameter` objects on a tree, i.e. plotting the value for a given (`Parameter`, `Language`) pair next to the language's label on the tree.


## Usage

TODO: See https://github.com/clld/grambank/commit/4101243597c3c95d21786fe8bdcf8cf060da609b for a minimal example.

To make `clld-phylogeny-plugin` functionality available to a `clld` app, it must be included in the app's configuration - typically in `<app>:main`:
```python
    config.include('clld_phylogeny_plugin')
```

This will add a *Resource* `Phylogeny` with corresponding routes
- `/phylogenys` - the index page listing all available phylogenies
- `/phylogenys/<ID>` - a phylogeny's details page, by default rendering the associated tree.


### Plotting parameters on trees

To synchronize plotting of markers for parameter values on maps and trees, the `Tree.get_marker` method may need to
be adjusted. This can be done by registering a derived `Tree` class as `ITree` utility:
```python
class MyTree(clld_phylogeny_plugin.tree.Tree):
    def get_marker(self, valueset):
        # compute marker shape and color from valueset
        return shape, color

....
    config.registry.registerUtility(MyTree, ITree)
```
