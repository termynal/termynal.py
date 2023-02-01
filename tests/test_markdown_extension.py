# pylint:disable=redefined-outer-name
# pylint:disable=invalid-name
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
<span data-ty="input">pip install termynal</span>
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
<span data-ty="input">pip install termynal</span>
<span data-ty="progress"></span>
<span data-ty></span>
</div></p>"""


@pytest.mark.parametrize(
    ("md", "expected_html"),
    [(md, expected_html), (md2, expected_html2), (md3, expected_html3)],
)
def test_converting(md, expected_html):
    html = markdown(
        md,
        extensions=[
            "fenced_code",
            TermynalExtension(),
        ],
    )
    assert html == expected_html
