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

#### Generating blocks from a command

Pasting `--help` output by hand goes stale. The `termynal.exec` helper runs a
command for you and prints a ready-to-paste, colored termynal block. It is a
standalone authoring step — termynal itself never executes anything, so pages
stay a pure text-to-HTML transform.

```
$ python -m termynal.exec "mytool --help" --title mytool
<!-- termynal: {ansi: true, title: mytool} -->
```

It runs the command with `FORCE_COLOR=1` and a fixed `COLUMNS` width (so wrapping
is reproducible), captures stdout and stderr, and emits the block. Colors come
through for tools that honor `FORCE_COLOR` such as rich, typer, and click; add
`--pty` for CLIs that check `isatty` directly (POSIX only).

The helper adds **no dependencies** of its own (standard library only), and the
command it runs is your own tool, already installed in your docs environment.
Rendering the captured ANSI still needs `pip install 'termynal[ansi]'`.

Pipe it into a page, or wire it into a [cog](https://nedbatchelder.com/code/cog/)
block or pre-commit hook to keep the output fresh. Useful flags:

| Flag | Purpose |
| --- | --- |
| `--title` | Terminal title for the block. |
| `--prompt` | Prompt shown before the command (default `$`). |
| `--columns` | Width passed to the command (default `80`). |
| `--timeout` | Seconds before the command is killed (default `30`). |
| `--cwd` | Working directory for the command. |
| `--no-color` / `--no-ansi` | Capture without color / omit `ansi: true`. |
| `--pty` | Run under a pseudo-terminal for stubborn CLIs. |
