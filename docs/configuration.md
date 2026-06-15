# Configuration

| **name**             | **default** |                        |
|----------------------|-------------|------------------------|
| title                | `"bash"`    |                        |
| buttons              | `"macos"`   | `"macos"`, `"windows"` |
| prompt_literal_start | `["$"]`     |                        |
| include_assets       | `false`     |                        |
| assets_override_css  | `null`      | path to custom css file |
| assets_override_js   | `null`      | path to custom js file  |
| animate              | `true`      | `false` renders instantly, without animation |

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
      animate: true
```

You can override configurations for each block. If you set a part of the settings, the other part will be set to the default value from `mkdocs.yml`.

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

Set `animate: false` to render a block instantly, without the typing animation.
Compare the two blocks below (the "Instant" tab skips the animation entirely):

=== "Instant"

    `<!-- termynal: animate: false -->`

    <!-- termynal: animate: false -->

    ```
    $ pip install termynal
    ---> 100%
    Installed
    ```

=== "Animated (default)"

    `<!-- termynal -->`

    <!-- termynal -->

    ```
    $ pip install termynal
    ---> 100%
    Installed
    ```
