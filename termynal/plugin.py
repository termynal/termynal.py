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
    include_assets = c.Type(bool, default=False)
    assets_override_css = c.Optional(c.Type(str))
    assets_override_js = c.Optional(c.Type(str))


class TermynalPlugin(BasePlugin[TermynalPluginConfig]):
    def on_config(self, config: "MkDocsConfig") -> Optional["MkDocsConfig"]:
        include_assets = bool(self.config.get("include_assets", False))
        css_asset = self.config.get("assets_override_css") or "termynal.css"
        js_asset = self.config.get("assets_override_js") or "termynal.js"

        if not include_assets and css_asset not in config["extra_css"]:
            config["extra_css"].append(css_asset)

        if not include_assets and js_asset not in config["extra_javascript"]:
            config["extra_javascript"].append(js_asset)

        if "termynal" not in config["markdown_extensions"]:
            config["markdown_extensions"].append("termynal")

        md_config = config["mdx_configs"].setdefault("termynal", {})
        config["mdx_configs"]["termynal"] = {**self.config, **md_config}

        return config

    def on_post_build(self, *, config: "MkDocsConfig") -> None:
        if self.config.get("include_assets", False):
            return

        output_base_path = Path(config["site_dir"])
        if not self.config.get("assets_override_css"):
            from_path = base_path / "assets" / "termynal.css"
            to_path = output_base_path / "termynal.css"
            utils.copy_file(str(from_path), str(to_path))

        if not self.config.get("assets_override_js"):
            from_path = base_path / "assets" / "termynal.js"
            to_path = output_base_path / "termynal.js"
            utils.copy_file(str(from_path), str(to_path))
