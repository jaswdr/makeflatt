# MakeFlatt
> Simple library to make your dictionary flatten in Python

[![PyPI version](https://badge.fury.io/py/makeflatt.svg)](https://badge.fury.io/py/makeflatt)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/makeflatt)
[![Unit Tests](https://github.com/jaswdr/makeflatt/actions/workflows/unit-tests.yml/badge.svg?branch=master)](https://github.com/jaswdr/makeflatt/actions/workflows/unit-tests.yml)
![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)
![PyPI - License](https://img.shields.io/pypi/l/makeflatt)


### Installation

```bash
pip install makeflatt
```

### Usage

Quick start:

```python
>>> from makeflatt import FlattMaker
>>> mf = FlattMaker()
>>> mf.apply({"a": {"b": {"c": "test"}}})
{'a.b.c': 'test'}
```

Make nested structured flatten:

```python
>>> mf.apply({"a": {"b": ["b1", "b2", "b3"]}})
{'a.b.0': 'b1', 'a.b.1': 'b2', 'a.b.2': 'b3'}
```

If you don't wan't to expand nested lists you can set `include_lists` to `False`:

```python
>>> mf.apply({"a": {"b": ["b1", "b2", "b3"]}}, include_lists=False)
{'a.b': ['b1', 'b2', 'b3']}
```

You can also change the separator and define your own:

```python
>>> mf = FlattMaker(sep=":")
>>> mf.apply({"a": {"b": ["b1", "b2", "b3"]}})
{'a:b:0': 'b1', 'a:b:1': 'b2', 'a:b:2': 'b3'}
```

### License

MakeFlatt is released under the MIT Licence. See the bundled LICENSE file for details.

### Development

Check the [CONTRIBUTING](CONTRIBUTING.md) file.

### Versioning

This package attempts to use semantic versioning. API changes are indicated by the major version, non-breaking improvements by the minor, and bug fixes in the revision.

It is recommended that you pin your targets to greater or equal to the current version and less than the next major version.

### Maintainer

Created and maitained by Jonathan Schweder (@jaswdr)
