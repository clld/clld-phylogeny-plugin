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
- adding database models to store phylogenetic trees (and how the tree labels correspond to `Language` objects)
- adding a `Tree` component, allowing simple rendering of a tree on a page
- adding support for "plotting" `Parameter` objects on a tree, i.e. plotting the value for a given (`Parameter`, `Language`) pair next to the language's label on the tree.


## Usage

TODO: See https://github.com/clld/grambank/commit/4101243597c3c95d21786fe8bdcf8cf060da609b for a minimal example.
