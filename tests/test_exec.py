# pylint:disable=invalid-name
import sys

import pytest
from markdown import markdown

from termynal.exec import render, run_command, to_termynal_block
from termynal.markdown import TermynalExtension

# A tiny program that prints red + green via ANSI, independent of FORCE_COLOR so
# the assertions stay deterministic across environments.
ANSI_SNIPPET = (
    "import sys; "
    r"sys.stdout.write('\x1b[31mred\x1b[0m and \x1b[32mgreen\x1b[0m\n')"
)


def test_run_command_captures_stdout():
    out = run_command([sys.executable, "-c", "print('hello world')"])
    assert out.strip() == "hello world"


def test_run_command_merges_stderr_by_default():
    out = run_command(
        [sys.executable, "-c", "import sys; print('out'); print('err', file=sys.stderr)"],
    )
    assert "out" in out
    assert "err" in out


def test_run_command_can_drop_stderr():
    out = run_command(
        [sys.executable, "-c", "import sys; print('out'); print('err', file=sys.stderr)"],
        merge_stderr=False,
    )
    assert "out" in out
    assert "err" not in out


def test_run_command_times_out():
    with pytest.raises(Exception):  # noqa: B017,PT011 - TimeoutExpired
        run_command([sys.executable, "-c", "import time; time.sleep(5)"], timeout=0.5)


def test_to_termynal_block_single_ansi_key_uses_plain_form():
    block = to_termynal_block("mytool --help", "output line")
    assert block.startswith("<!-- termynal: ansi: true -->\n")
    assert "$ mytool --help" in block
    assert "output line" in block


def test_to_termynal_block_multiple_keys_use_inline_yaml():
    block = to_termynal_block("mytool", "out", title="demo")
    assert block.startswith("<!-- termynal: {ansi: true, title: demo} -->\n")


def test_to_termynal_block_without_ansi():
    block = to_termynal_block("mytool", "out", ansi=False)
    assert block.startswith("<!-- termynal -->\n")


def test_to_termynal_block_normalizes_crlf_and_trailing_newlines():
    block = to_termynal_block("c", "a\r\nb\n\n")
    body = block.split("```\n", 1)[1].rsplit("\n```", 1)[0]
    assert body == "$ c\na\nb"


def test_render_round_trips_through_termynal():
    block = render([sys.executable, "-c", ANSI_SNIPPET], title="demo")
    html = markdown(block, extensions=["fenced_code", TermynalExtension(ansi=True)])
    assert 'data-ty="input"' in html
    assert '<span style="color: #cd0000">red</span>' in html
    assert '<span style="color: #00cd00">green</span>' in html
    assert html.count("<span") == html.count("</span>")


def test_render_command_display_defaults_to_quoted_command():
    block = render([sys.executable, "-c", "print(1)"], title=None)
    # shlex.join quotes the snippet so the input line is copy-pasteable.
    assert f"$ {sys.executable}" in block
