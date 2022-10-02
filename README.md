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

progress, prompt `---> 100%`

````
```console
$ show progress
---> 100%
Done!
```
````

command, start with `$`

````
```console
$ command
```
````

comment, start with `#`

````
```console
# comment
```
````

`mkdocs` plugin

```yaml
...
plugins:
  - termynal
...
```

Thanks [ines](https://github.com/ines/termynal)
