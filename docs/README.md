# Termynal

A lightweight and modern animated terminal window.
Built for [mkdocs](https://www.mkdocs.org/).

## Installation

<!--termynal: {title: bash, prompt_literal_start: [$]}-->

```
$ pip install termynal
---> 100%
Installed
```

## Usage

Use `<!-- termynal -->` before code block

=== "HTML"

    <!-- termynal -->

    ```
    // code
    ```

=== "Markdown"

    ````
    ```
    // code
    ```
    ````

### progress

progress, prompt `---> 100%`

=== "HTML"
    <!-- termynal -->

    ```
    $ show progress
    ---> 100%
    Done!
    ```

=== "Markdown"
    ````
    ```
    $ show progress
    ---> 100%
    Done!
    ```
    ````

### command

command, start with `$`. You can change it with `prompt_literal_start` option.

=== "HTML"
    <!-- termynal -->

    ```
    $ python
    >>> import requests
    >>> requests.get('https://exampls.com')
    <Response [200]>
    >>>
    ```

=== "Markdown"
    ````
    ```
    $ python
    >>> import requests
    >>> requests.get('https://exampls.com')
    <Response [200]>
    >>>
    ```
    ````

### multiline command

=== "HTML"
    <!-- termynal -->

    ```
    > some longish command with \
      many \
        many \
          many \
      arguments
    and this is the output
    ```

=== "Markdown"
    ````
    ```
    > some longish command with \
      many \
        many \
          many \
      arguments
    and this is the output
    ```
    ````

### comment

comment, start with `#`

=== "HTML"
    <!-- termynal -->

    ```console
    # comment
    ```

=== "Markdown"

    ````
    ```
    # comment
    ```
    ````

### output

tool's help looks like this:

=== "HTML"
    <!-- termynal -->

    ```
    $ uv -h

    An extremely fast Python package manager.

    Usage: uv [OPTIONS] <COMMAND>

    Commands:
      run      Run a command or script
      init     Create a new project
      add      Add dependencies to the project
      remove   Remove dependencies from the project
      sync     Update the project's environment
      lock     Update the project's lockfile
      export   Export the project's lockfile to an alternate format
      tree     Display the project's dependency tree
      tool     Run and install commands provided by Python packages
      python   Manage Python versions and installations
      pip      Manage Python packages with a pip-compatible interface
      venv     Create a virtual environment
      build    Build Python packages into source distributions and wheels
      publish  Upload distributions to an index
      cache    Manage uv's cache
      self     Manage the uv executable
      version  Display uv's version
      help     Display documentation for a command

    Cache options:
      -n, --no-cache               Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation [env: UV_NO_CACHE=]
          --cache-dir <CACHE_DIR>  Path to the cache directory [env: UV_CACHE_DIR=]

    Python options:
          --python-preference <PYTHON_PREFERENCE>  Whether to prefer uv-managed or system Python installations [env: UV_PYTHON_PREFERENCE=] [possible values: only-managed, managed, system, only-system]
          --no-python-downloads                    Disable automatic downloads of Python. [env: "UV_PYTHON_DOWNLOADS=never"]

    Global options:
      -q, --quiet                                      Do not print any output
      -v, --verbose...                                 Use verbose output
          --color <COLOR_CHOICE>                       Control colors in output [default: auto] [possible values: auto, always, never]
          --native-tls                                 Whether to load TLS certificates from the platform's native certificate store [env: UV_NATIVE_TLS=]
          --offline                                    Disable network access
          --allow-insecure-host <ALLOW_INSECURE_HOST>  Allow insecure connections to a host [env: UV_INSECURE_HOST=]
          --no-progress                                Hide all progress outputs [env: UV_NO_PROGRESS=]
          --directory <DIRECTORY>                      Change to the given directory prior to running the command
          --project <PROJECT>                          Run the command within the given project directory
          --config-file <CONFIG_FILE>                  The path to a `uv.toml` file to use for configuration [env: UV_CONFIG_FILE=]
          --no-config                                  Avoid discovering configuration files (`pyproject.toml`, `uv.toml`) [env: UV_NO_CONFIG=]
      -h, --help                                       Display the concise help for this command
      -V, --version                                    Display the uv version

    Use `uv help` for more details.

    ```

=== "Markdown"
    ````
    ```
    $ uv -h

    ...
    ```
    ````

## Mkdocs integration

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

=== "HTML"
    <!-- termynal -->

    ```
    > command with >
    Ok!
    ```

=== "Markdown"
    ````markdown
    ```
    > command with >
    Ok!
    ```
    ````

## Credits

Thanks [ines](https://github.com/ines/termynal)
