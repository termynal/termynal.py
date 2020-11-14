# pylint:disable=redefined-outer-name
import pytest


@pytest.fixture()
def plugin(mocker):
    return mocker.Mock()


@pytest.fixture()
def empty_config():
    return {'extra_css': [], 'extra_javascript': []}


@pytest.fixture()
def config():
    return {'extra_css': ['termynal.css'], 'extra_javascript': ['termynal.js']}


def test_on_config(plugin, config, empty_config):
    assert plugin.on_config(config, empty_config)
