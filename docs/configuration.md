# Configuration

| **name**             | **default** |                        |
|----------------------|-------------|------------------------|
| title                | `"bash"`    |                        |
| buttons              | `"macos"`   | `"macos"`, `"windows"` |
| prompt_literal_start | `["$"]`     |                        |

```yaml
plugins:
  - termynal:
      title: bash
      buttons: macos
      prompt_literal_start:
        - "$"
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
