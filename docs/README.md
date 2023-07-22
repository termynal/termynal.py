# Termynal

A lightweight and modern animated terminal window.
Built for [mkdocs](https://www.mkdocs.org/).

## Installation

<!-- termynal -->

```
$ pip install termynal
---> 100%
Installed
```

[Example](https://daxartio.github.io/termynal/)

## Usage

Use `<!-- termynal -->` before code block

````
<!-- termynal -->

```
// code
```
````

or `console` in code block

````
```console
// code
```
````

<!-- termynal -->

```
// code
```

progress, prompt `---> 100%`

````
```
$ show progress
---> 100%
Done!
```
````

<!-- termynal -->

```
$ show progress
---> 100%
Done!
```

command, start with `$`

````
```console
$ command
```
````

<!-- termynal -->

```
$ command
```

Multiline commands

````
```console
> some longish command with \
  many \
    many \
      many \
  arguments
and this is the output
```
````

<!-- termynal -->

```
> some longish command with \
  many \
    many \
      many \
  arguments
and this is the output
```

comment, start with `#`

````
```console
# comment
```
````

<!-- termynal -->

```console
# comment
```

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
markdown_extensions:
  - termynal:
      prompt_literal_start:
        - "$ "
        - "&gt; "
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
<!-- termynal -->

```
> pip install termynal
---> 100%
Installed
```

## Credits

Thanks [ines](https://github.com/ines/termynal)
