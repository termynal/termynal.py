# Termynal

![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/termynal/termynal.py/check.yml)
[![PyPI](https://img.shields.io/pypi/v/termynal)](https://pypi.org/project/termynal/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/termynal)](https://www.python.org/downloads/)
[![Docs](https://img.shields.io/badge/docs-latest-blue)](https://termynal.github.io/termynal.py/)
![GitHub](https://img.shields.io/github/license/termynal/termynal.py)
![PyPI - Downloads](https://img.shields.io/pypi/dm/termynal)
![GitHub last commit](https://img.shields.io/github/last-commit/termynal/termynal.py)

A lightweight and modern animated terminal window.
Built for [mkdocs](https://www.mkdocs.org/) and [zensical](https://zensical.org/).

## Installation

![termynal](termynal.gif)

[Examples](https://termynal.github.io/termynal.py/)

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

If you do not want to copy `termynal.css` and `termynal.js` as static files,
you can embed them directly in generated HTML:

```yaml
[...]
plugins:
  - termynal:
      include_assets: true
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

### Zensical integration

`zensical` does not support arbitrary MkDocs plugins yet, but it supports Python Markdown extensions.
Use `termynal` as a markdown extension and enable inline assets:

```toml
[project.markdown_extensions.termynal]
include_assets = true
title = "bash"
buttons = "macos"
prompt_literal_start = ["$"]
```

You can override default assets with your own files:

```toml
[project.markdown_extensions.termynal]
include_assets = true
assets_override_css = "docs/stylesheets/termynal.css"
assets_override_js = "docs/javascripts/termynal.js"
```

For Zensical-style asset management, keep `include_assets = false` and register
assets explicitly:

```toml
[project]
extra_css = ["stylesheets/termynal.css"]
extra_javascript = ["javascripts/termynal.js"]

[project.markdown_extensions.termynal]
include_assets = false
```

## Credits

Thanks [ines](https://github.com/ines/termynal)

## Contribution

[Contribution guidelines for this project](CONTRIBUTING.md)
