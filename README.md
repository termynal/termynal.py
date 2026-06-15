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
ansi = false
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

### Colored output (rich, typer, …)

Tools like [rich](https://github.com/Textualize/rich) and
[typer](https://github.com/fastapi/typer) emit ANSI color sequences. Enable the
`ansi` option to convert those sequences into colored HTML instead of escaping
them. It requires the optional `ansi2html` dependency:

```
pip install 'termynal[ansi]'
```

Then turn it on globally:

```yaml
[...]
plugins:
  - termynal:
      ansi: true
[...]
```

or per block:

````markdown
<!-- termynal: ansi: true -->

```
$ python app.py
```
````

Paste the raw ANSI output into the code block (e.g. capture it with
`rich.console.Console(force_terminal=True)`, `FORCE_COLOR=1`, or typer's
`--color`). Each output line is converted independently with inline styles, so
no extra CSS is needed. Colors render on output lines; typed command lines are
shown as plain text by the animation.

The 16 base ANSI colors are mapped through a palette. The default is `xterm`
(the canonical reference terminal palette); other options are `ansi2html`,
`osx`, `osx-basic`, `osx-solid-colors`, `dracula`, `solarized`, and
`mint-terminal`. 256-color and 24-bit truecolor sequences are always mapped
faithfully, regardless of the scheme.

```yaml
[...]
plugins:
  - termynal:
      ansi: true
      ansi_scheme: xterm
      ansi_dark_bg: true
[...]
```

> Tip: for pixel-exact colors, tell the tool to emit 24-bit color (e.g.
> `rich.console.Console(color_system="truecolor")`) — the base-color palette is
> then bypassed entirely.

## Credits

Thanks [ines](https://github.com/ines/termynal)

## Contribution

[Contribution guidelines for this project](CONTRIBUTING.md)
