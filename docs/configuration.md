# Configuration

## Options

| **name**             | **default** |                        |
|----------------------|-------------|------------------------|
| title                | `"bash"`    |                        |
| buttons              | `"macos"`   | `"macos"`, `"windows"` |
| prompt_literal_start | `["$"]`     |                        |
| include_assets       | `false`     |                        |
| assets_override_css  | `null`      | path to custom css file |
| assets_override_js   | `null`      | path to custom js file  |
| ansi                 | `false`     | render ANSI colors as HTML |
| ansi_scheme          | `"xterm"`   | `ansi2html`, `dracula`, `mint-terminal`, `osx`, `osx-basic`, `osx-solid-colors`, `solarized`, `xterm` |
| ansi_dark_bg         | `true`      | dark-background palette variant |

## Global configuration

Set defaults for every block in `mkdocs.yml`:

```yaml
plugins:
  - termynal:
      title: bash
      buttons: macos
      prompt_literal_start:
        - "$"
      include_assets: false
      assets_override_css: null
      assets_override_js: null
      ansi: false
      ansi_scheme: xterm
      ansi_dark_bg: true
```

## Per-block overrides

You can override configurations for each block. If you set a part of the settings, the other part will be set to the default value from `mkdocs.yml`.

### Custom prompt and buttons

`<!-- termynal: {"prompt_literal_start": ["$", ">>>", "PS >"], title: powershell, buttons: windows} -->`

````
```
PS > python
>>> import json
```
````

<!-- termynal: {"prompt_literal_start": ["$", ">>>", "PS >"], title: powershell, buttons: windows} -->

```
PS > python
>>> import json
```

### Colored output

With `ansi: true` (requires `pip install 'termynal[ansi]'`), ANSI color
sequences from tools like [rich](https://github.com/Textualize/rich) and
[typer](https://github.com/fastapi/typer) are rendered as colored HTML instead
of being escaped. Paste the raw colored output into the block:

<!-- termynal: ansi: true -->

```
$ uv -h
An extremely fast Python package manager.

[1m[32mUsage:[0m [1m[36muv[0m [36m[OPTIONS][0m [36m<COMMAND>[0m

[1m[32mCommands:[0m
  [1m[36mrun[0m      Run a command or script
  [1m[36minit[0m     Create a new project
  [1m[36madd[0m      Add dependencies to the project
  [1m[36mremove[0m   Remove dependencies from the project
  [1m[36msync[0m     Update the project's environment
  [1m[36mlock[0m     Update the project's lockfile
```

