import os
from typing import Optional

from mkdocs import utils
from mkdocs.config.base import Config
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin

base_path = os.path.dirname(os.path.abspath(__file__))


class TermynalPlugin(BasePlugin):
    def on_config(self, config: MkDocsConfig) -> Optional[Config]:
        if 'termynal.css' not in config['extra_css']:
            config['extra_css'].append('termynal.css')

        if 'termynal.js' not in config['extra_javascript']:
            config['extra_javascript'].append('termynal.js')

        if 'termynal' not in config['markdown_extensions']:
            config['markdown_extensions'].append('termynal')

        return config

    def on_post_build(self, *, config: MkDocsConfig) -> None:
        output_base_path = config['site_dir']

        for filename in ['termynal.css', 'termynal.js']:
            from_path = os.path.join(base_path, 'assets', filename)
            to_path = os.path.join(output_base_path, filename)
            utils.copy_file(from_path, to_path)
