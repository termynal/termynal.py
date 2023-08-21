# Termynal

![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/mkdocs-plugins/termynal/check.yml)
[![PyPI](https://img.shields.io/pypi/v/termynal)](https://pypi.org/project/termynal/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/termynal)](https://www.python.org/downloads/)
[![Docs](https://img.shields.io/badge/docs-latest-blue)](https://mkdocs-plugins.github.io/termynal/)
![GitHub](https://img.shields.io/github/license/mkdocs-plugins/termynal)
![PyPI - Downloads](https://img.shields.io/pypi/dm/termynal)
![GitHub last commit](https://img.shields.io/github/last-commit/mkdocs-plugins/termynal)

A lightweight and modern animated terminal window.
Built for [mkdocs](https://www.mkdocs.org/).

## Installation

![termynal](termynal.gif)

[Examples](https://mkdocs-plugins.github.io/termynal/)

## Usage

Use `<!-- termynal -->` before code block

````
<!-- termynal -->

```
$ python script.py
```
````

### Mkdocs integration

Declare the plugin:

```yaml
...
plugins:
  - termynal
...
```

Optionally, pass options to the processor:

```yaml
[...]
plugins:
  - termynal:
      prompt_literal_start:
        - "$"
        - ">"
[...]
```

This config allows you to use another prompt:

````markdown
<!-- termynal -->

```
> pip install termynal
---> 100%
Installed
```

````

## Credits

Thanks [ines](https://github.com/ines/termynal)

## Contribution

[Contribution guidelines for this project](CONTRIBUTING.md)
