# pylint:disable=redefined-outer-name
from tempfile import TemporaryDirectory

import pytest

from termynal.plugin import TermynalPlugin


@pytest.fixture()
def plugin():
    return TermynalPlugin()


@pytest.fixture()
def empty_config():
    return {
        "extra_css": [],
        "extra_javascript": [],
        "markdown_extensions": [],
        "mdx_configs": {},
    }


@pytest.fixture()
def config():
    return {
        "extra_css": ["termynal.css"],
        "extra_javascript": ["termynal.js"],
        "markdown_extensions": ["termynal"],
        "mdx_configs": {"termynal": {}},
    }


def test_on_config(plugin, config):
    assert plugin.on_config(config) == config


def test_on_config_if_empty(plugin, empty_config, config):
    assert plugin.on_config(empty_config) == config


def test_on_post_build(plugin):
    with TemporaryDirectory() as tmpdir:
        plugin.on_post_build(config={"site_dir": tmpdir})
