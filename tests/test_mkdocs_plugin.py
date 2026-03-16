# pylint:disable=redefined-outer-name
from tempfile import TemporaryDirectory
from pathlib import Path

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


def test_on_config_with_inline_assets(plugin, empty_config):
    plugin.config = {"include_assets": True}
    result = plugin.on_config(empty_config)

    assert result == {
        "extra_css": [],
        "extra_javascript": [],
        "markdown_extensions": ["termynal"],
        "mdx_configs": {"termynal": {"include_assets": True}},
    }


def test_on_post_build_with_inline_assets(plugin):
    plugin.config = {"include_assets": True}
    with TemporaryDirectory() as tmpdir:
        plugin.on_post_build(config={"site_dir": tmpdir})
        assert not Path(tmpdir, "termynal.css").exists()
        assert not Path(tmpdir, "termynal.js").exists()


def test_on_config_with_asset_overrides(plugin, empty_config):
    plugin.config = {
        "assets_override_css": "stylesheets/termynal.css",
        "assets_override_js": "javascripts/termynal.js",
    }
    result = plugin.on_config(empty_config)

    assert result == {
        "extra_css": ["stylesheets/termynal.css"],
        "extra_javascript": ["javascripts/termynal.js"],
        "markdown_extensions": ["termynal"],
        "mdx_configs": {
            "termynal": {
                "assets_override_css": "stylesheets/termynal.css",
                "assets_override_js": "javascripts/termynal.js",
            },
        },
    }


def test_on_post_build_with_asset_overrides(plugin):
    plugin.config = {
        "assets_override_css": "stylesheets/termynal.css",
        "assets_override_js": "javascripts/termynal.js",
    }
    with TemporaryDirectory() as tmpdir:
        plugin.on_post_build(config={"site_dir": tmpdir})
        assert not Path(tmpdir, "termynal.css").exists()
        assert not Path(tmpdir, "termynal.js").exists()
