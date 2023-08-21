from pathlib import Path
from typing import TYPE_CHECKING, Optional

from mkdocs import utils
from mkdocs.config import base
from mkdocs.config import config_options as c
from mkdocs.plugins import BasePlugin

if TYPE_CHECKING:  # pragma:no cover
    from mkdocs.config.defaults import MkDocsConfig

base_path = Path(__file__).parent


class TermynalPluginConfig(base.Config):
    title = c.Type(str, default="bash")
    buttons = c.Choice(("macos", "windows"), default="macos")
    prompt_literal_start = c.ListOfItems(c.Type(str), default=["$"])


class TermynalPlugin(BasePlugin[TermynalPluginConfig]):
    def on_config(self, config: "MkDocsConfig") -> Optional["MkDocsConfig"]:
        if "termynal.css" not in config["extra_css"]:
            config["extra_css"].append("termynal.css")

        if "termynal.js" not in config["extra_javascript"]:
            config["extra_javascript"].append("termynal.js")

        if "termynal" not in config["markdown_extensions"]:
            config["markdown_extensions"].append("termynal")

        md_config = config["mdx_configs"].setdefault("termynal", {})
        config["mdx_configs"]["termynal"] = {**self.config, **md_config}

        return config

    def on_post_build(self, *, config: "MkDocsConfig") -> None:
        output_base_path = Path(config["site_dir"])

        for filename in ["termynal.css", "termynal.js"]:
            from_path = base_path / "assets" / filename
            to_path = output_base_path / filename
            utils.copy_file(str(from_path), str(to_path))
