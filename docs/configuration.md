# Configuration

| **name**             | **default** |
|----------------------|-------------|
| title                | `"bash"`    |
| prompt_literal_start | `["$"]`     |

```yaml
markdown_extensions:
  - termynal:
      title: bash
      prompt_literal_start:
        - "$"
```

You can override configs for each block. If you set a part of the settings, another part will be set to the default value.

````
<!-- termynal: {"prompt_literal_start": ["$", ">>>", "PS >"], title: shell} -->

```
PS > python
>>> import json
```
````

<!-- termynal: {"prompt_literal_start": ["$", ">>>", "PS >"], title: shell} -->

```
PS > python
>>> import json
```
