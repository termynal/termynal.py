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


def test_ansi_output_is_converted_to_spans():
    md = "<!-- termynal -->\n```\n$ run\n\x1b[31mred\x1b[0m line\n```\n"
    html = markdown(
        md,
        extensions=["fenced_code", TermynalExtension(ansi=True)],
    )
    assert '<span style="color: #cd0000">red</span> line' in html
    assert '<span data-ty="input" data-ty-prompt="$">run</span>' in html


def test_ansi_disabled_keeps_escape_codes_literal():
    md = "<!-- termynal -->\n```\n\x1b[31mred\x1b[0m line\n```\n"
    html = markdown(
        md,
        extensions=["fenced_code", TermynalExtension()],
    )
    assert "color: #aa0000" not in html


def test_ansi_does_not_alter_ansi_free_output():
    md = "<!-- termynal -->\n```\n$ echo hi\nplain \"quoted\" & <stuff>\n```\n"
    off = markdown(md, extensions=["fenced_code", TermynalExtension(ansi=False)])
    on = markdown(md, extensions=["fenced_code", TermynalExtension(ansi=True)])
    assert off == on


def test_ansi_default_scheme_is_xterm():
    md = "<!-- termynal -->\n```\n\x1b[31mred\x1b[0m\n```\n"
    html = markdown(md, extensions=["fenced_code", TermynalExtension(ansi=True)])
    assert "color: #cd0000" in html


def test_ansi_scheme_override():
    md = "<!-- termynal -->\n```\n\x1b[31mred\x1b[0m\n```\n"
    html = markdown(
        md,
        extensions=["fenced_code", TermynalExtension(ansi=True, ansi_scheme="osx")],
    )
    assert "color: #c23621" in html


def test_ansi_invalid_scheme_falls_back_to_default():
    md = "<!-- termynal -->\n```\n\x1b[31mred\x1b[0m\n```\n"
    html = markdown(
        md,
        extensions=[
            "fenced_code",
            TermynalExtension(ansi=True, ansi_scheme="not-a-scheme"),
        ],
    )
    assert "color: #cd0000" in html


def test_ansi_per_block_override():
    md = (
        "<!-- termynal: ansi: true -->\n"
        "```\n$ run\n\x1b[32mgreen\x1b[0m\n```\n"
    )
    html = markdown(
        md,
        extensions=["fenced_code", TermynalExtension()],
    )
    assert "color: #00cd00" in html
