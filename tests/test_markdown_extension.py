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
