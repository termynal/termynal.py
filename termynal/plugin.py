from pathlib import Path
from typing import TYPE_CHECKING, Optional

from mkdocs import utils
from mkdocs.plugins import BasePlugin

if TYPE_CHECKING:  # pragma:no cover
    from mkdocs.config.base import Config
    from mkdocs.config.defaults import MkDocsConfig

base_path = Path(__file__).parent


class TermynalPlugin(BasePlugin):
    def on_config(self, config: "MkDocsConfig") -> Optional["Config"]:
        if "termynal.css" not in config["extra_css"]:
            config["extra_css"].append("termynal.css")

        if "termynal.js" not in config["extra_javascript"]:
            config["extra_javascript"].append("termynal.js")

        if "termynal" not in config["markdown_extensions"]:
            config["markdown_extensions"].append("termynal")

        return config

    def on_post_build(self, *, config: "MkDocsConfig") -> None:
        output_base_path = Path(config["site_dir"])

        for filename in ["termynal.css", "termynal.js"]:
            from_path = base_path / "assets" / filename
            to_path = output_base_path / filename
            utils.copy_file(str(from_path), str(to_path))
