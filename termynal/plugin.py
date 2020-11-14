import logging
import os

from mkdocs import utils
from mkdocs.plugins import BasePlugin

logger = logging.getLogger(__name__)
base_path = os.path.dirname(os.path.abspath(__file__))


class TermynalPlugin(BasePlugin):
    def on_config(self, config, **kwargs):  # pylint: disable=unused-argument
        if 'termynal.css' not in config['extra_css']:
            config['extra_css'].append('termynal.css')

        if 'termynal.js' not in config['extra_javascript']:
            config['extra_javascript'].append('termynal.js')

        if 'termynal' not in config['markdown_extensions']:
            config['markdown_extensions'].append('termynal')

        return config

    def on_post_build(self, config, **kwargs):  # pylint: disable=unused-argument
        output_base_path = config['site_dir']

        for filename in ['termynal.css', 'termynal.js']:
            from_path = os.path.join(base_path, 'assets', filename)
            to_path = os.path.join(output_base_path, filename)
            utils.copy_file(from_path, to_path)
