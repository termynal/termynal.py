# pylint:disable=redefined-outer-name
# pylint:disable=invalid-name
from pathlib import Path

import pytest
import yaml
from markdown import markdown

from termynal.markdown import TermynalExtension

cases = yaml.full_load(Path("tests/test_cases.yml").read_text())


@pytest.mark.parametrize(
    ("md", "expected_html", "config"),
    [
        (
            case["md"],
            str(case["expected_html"]).strip(),
            case["config"],
        )
        for case in cases
    ],
    ids=[case["name"] for case in cases],
)
def test_cases_yml(
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
    assert html == expected_html, (
        "The expected html is different, see tests/test_cases.yml"
    )


def test_include_assets():
    md = """\
<!-- termynal -->
```
$ echo first
```

<!-- termynal -->
```
$ echo second
```
"""
    html = markdown(
        md,
        extensions=[
            "fenced_code",
            TermynalExtension(include_assets=True),
        ],
    )
    assert html.count('data-termynal-inline="true"') == 2


def test_include_assets_is_disabled_by_default():
    md = """\
<!-- termynal -->
```
$ echo termynal
```
"""
    html = markdown(
        md,
        extensions=[
            "fenced_code",
            TermynalExtension(),
        ],
    )
    assert 'data-termynal-inline="true"' not in html


def test_include_assets_with_overrides(tmp_path):
    css_path = tmp_path / "termynal.css"
    js_path = tmp_path / "termynal.js"
    css_path.write_text(".termy { border: 1px solid red; }", encoding="utf-8")
    js_path.write_text("window.__termynal_override = true;", encoding="utf-8")

    md = """\
<!-- termynal -->
```
$ echo termynal
```
"""
    html = markdown(
        md,
        extensions=[
            "fenced_code",
            TermynalExtension(
                include_assets=True,
                assets_override_css=str(css_path),
                assets_override_js=str(js_path),
            ),
        ],
    )
    assert ".termy { border: 1px solid red; }" in html
    assert "window.__termynal_override = true;" in html
    assert "data-terminal-control" not in html
