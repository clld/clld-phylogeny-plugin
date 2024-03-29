Releasing clld-phylogeny-plugin
===============================

- Do platform test via tox (making sure statement coverage is at 100%):
```shell
tox -r
```

```shell
flake8 src
```

- Change setup.cfg version to the new version number.

- Create the release commit:
```shell
git commit -a -m "release <VERSION>"
```

- Create a release tag:
```shell
git tag -a v<VERSION> -m "<VERSION> release"
```

- Release to PyPI:
```shell
git checkout tags/v<VERSION>
python setup.py clean --all
rm dist/*
python -m build -n
twine upload dist/*
```

- Push to github:
```shell
git push origin
git push --tags origin
```

- Append `.dev0` to the version number in `setup.cfg` for the new development cycle.

- Commit/push the version change:
```shell
git commit -a -m "bump version for development"
git push origin
```
