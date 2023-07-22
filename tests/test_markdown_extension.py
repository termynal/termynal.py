# pylint:disable=redefined-outer-name
# pylint:disable=invalid-name
from typing import Any, Dict

import pytest
from markdown import markdown

from termynal.markdown import TermynalExtension

md = """
# Header

```
$ pip install termynal
---> 100%
```
"""


expected_html = """<h1>Header</h1>
<pre><code>$ pip install termynal
---&gt; 100%
</code></pre>"""

config: Dict[str, str] = {}

md2 = """
# Header

<!-- termynal -->

```
$ pip install termynal
---> 100%
```
"""


expected_html2 = """<h1>Header</h1>
<!-- termynal -->

<p>
<div class="termy" data-termynal>
<span data-ty="input" data-ty-prompt="$">pip&nbsp;install&nbsp;termynal</span>
<span data-ty="progress"></span>
<span data-ty></span>
</div></p>"""


md3 = """
# Header

```console
$ pip install termynal
---> 100%
```
"""


expected_html3 = """<h1>Header</h1>
<p>
<div class="termy" data-termynal>
<span data-ty="input" data-ty-prompt="$">pip&nbsp;install&nbsp;termynal</span>
<span data-ty="progress"></span>
<span data-ty></span>
</div></p>"""

# -- MD 4
md4 = """
# Header

<!-- termynal -->

```
$ pip install termynal
---> 100%
```
"""

expected_html4 = """<h1>Header</h1>
<!-- termynal -->

<p>
<div class="termy" data-termynal>
<span data-ty>$ pip install termynal</span>
<span data-ty="progress"></span>
<span data-ty></span>
</div></p>"""

config4 = {"prompt_literal_start": ["&gt; "]}

# -- MD 5 --
md5 = """
# Header

<!-- termynal -->

```
> pip install termynal
---> 100%
```
"""

expected_html5 = """<h1>Header</h1>
<!-- termynal -->

<p>
<div class="termy" data-termynal>
<span data-ty="input" data-ty-prompt="&gt;">pip&nbsp;install&nbsp;termynal</span>
<span data-ty="progress"></span>
<span data-ty></span>
</div></p>"""

config5 = {"prompt_literal_start": ["&gt; "]}

md6 = """
# Header

```console
$ pip install \\
    termynal
---> 100%
```
"""


expected_html6 = """<h1>Header</h1>
<p>
<div class="termy" data-termynal>
<span data-ty="input" data-ty-prompt="$">pip&nbsp;install&nbsp;\\</span>
<span data-ty="input" data-ty-prompt="">&nbsp;&nbsp;&nbsp;&nbsp;termynal</span>
<span data-ty="progress"></span>
<span data-ty></span>
</div></p>"""

config6: Dict[str, Any] = {}

md7 = """
# Header

```console
> pip install \\
    termynal
---> 100%
```
"""


expected_html7 = """<h1>Header</h1>
<p>
<div class="termy" data-termynal>
<span data-ty="input" data-ty-prompt="&gt;">pip&nbsp;install&nbsp;\\</span>
<span data-ty="input" data-ty-prompt="&gt;">&nbsp;&nbsp;&nbsp;&nbsp;termynal</span>
<span data-ty="progress"></span>
<span data-ty></span>
</div></p>"""

config7: Dict[str, Any] = {
    "promt_in_multiline": True,
    "prompt_literal_start": ["&gt; "],
}


@pytest.mark.parametrize(
    ("md", "expected_html", "config"),
    [
        (md, expected_html, config),
        (md2, expected_html2, config),
        (md3, expected_html3, config),
        (md4, expected_html4, config4),
        (md5, expected_html5, config5),
        (md6, expected_html6, config6),
        (md7, expected_html7, config7),
    ],
)
def test_converting(
    md: str,
    expected_html: str,
    config: dict,
):
    html = markdown(
        md,
        extensions=[
            "fenced_code",
            TermynalExtension(**config),
        ],
    )
    assert html == expected_html
