import os
import re
from enum import Enum
from textwrap import dedent
from typing import TYPE_CHECKING, Any, Dict, Iterable, List, NamedTuple, Optional, Union

import yaml
import yaml.parser
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor

TERMYNAL_PREPROCESSOR_PRIORITY = int(os.getenv("TERMYNAL_PREPROCESSOR_PRIORITY", "35"))

if TYPE_CHECKING:  # pragma:no cover
    from markdown import core


class Buttons(str, Enum):
    MACOS = "macos"
    WINDOWS = "windows"


class Config(NamedTuple):
    title: str
    prompt_literal_start: Iterable[str]
    buttons: Buttons


class Command(NamedTuple):
    prompt: str
    lines: List[str]


class Comment(NamedTuple):
    lines: List[str]


class Output(NamedTuple):
    lines: List[str]


class Progress:
    def __repr__(self) -> str:  # pragma:no cover
        return "Progress()"


ParsedBlock = Union[Command, Comment, Output, Progress]


def make_regex_prompts(prompt_literal_start: Iterable[str]) -> "re.Pattern[str]":
    prompt_literal_start = [re.escape(p).strip() for p in prompt_literal_start]
    prompt_to_replace = {
        ">": "&gt;",
        "<": "&lt;",
    }
    for p, code in prompt_to_replace.items():
        for i, prompt in enumerate(prompt_literal_start):
            prompt_literal_start[i] = prompt.replace(p, code)
    prompt_literal_start_re = "|".join(f"{p} " for p in prompt_literal_start)
    return re.compile(f"^({prompt_literal_start_re})")


def escape(txt: str) -> str:
    txt = txt.replace("&", "&amp;")
    txt = txt.replace("<", "&lt;")
    txt = txt.replace(">", "&gt;")
    txt = txt.replace('"', "&quot;")
    return txt  # noqa:RET504


def remove_spaces(code: str, spaces: str) -> str:
    result = []
    for line in code.split("\n"):
        new_line = line
        if new_line.startswith(spaces):
            new_line = line[len(spaces) :]

        result.append(f"{new_line}")

    return "\n".join(result)


def add_spaces(code: str, spaces: str) -> str:
    result = []
    for line in code.split("\n"):
        result.append(f"{spaces}{line}")

    return "\n".join(result)


def parse_config(raw: str) -> Optional[Config]:
    try:
        config = yaml.full_load(raw)
    except yaml.parser.ParserError:  # pragma:no cover
        return None

    if not isinstance(config, dict):
        return None

    return parse_config_from_dict(config)


def parse_config_from_dict(config: Dict[str, Any]) -> Config:
    return Config(
        title=str(config.get("title", "bash")),
        prompt_literal_start=list(config.get("prompt_literal_start", ("$",))),
        buttons=Buttons(config.get("buttons", "macos")),
    )


class Termynal:
    """Converts bash code to termynal HTML."""

    def __init__(
        self,
        config: Config,
        progress_literal_start="---&gt; 100%",
        comment_literal_start="# ",
    ):
        self.config = config
        self.regex_prompts = make_regex_prompts(config.prompt_literal_start)
        self.progress_literal_start = progress_literal_start
        self.comment_literal_start = comment_literal_start

    def convert(self, code: str) -> str:
        """Converts bash code to termynal HTML.

        Apply rules:
        - If a line starts with a prompt, it is a command.
        - If a line starts with a comment literal, it is a comment.
        - If a line starts with a progress literal, it is a progress bar.
        - If a line starts with anything else, it is an output.
        """
        code_lines: List[str] = []
        code_lines.append(
            f'<div class="termy" data-termynal data-ty-{self.config.buttons.value} '
            f'data-ty-title="{self.config.title}">',
        )

        for block in self._parse(code.split("\n")):
            if isinstance(block, Command):
                lines = "\n".join(block.lines)
                code_lines.append(
                    f'<span data-ty="input" data-ty-prompt="{block.prompt}">'
                    f"{lines}</span>",
                )

            elif isinstance(block, Comment):
                lines = "\n".join(block.lines)
                code_lines.append(
                    f'<span class="termynal-comment" data-ty>{lines}</span>',
                )

            elif isinstance(block, Progress):
                code_lines.append('<span data-ty="progress"></span>')

            elif isinstance(block, Output):
                lines = "<br>".join(block.lines)
                code_lines.append(f"<span data-ty>{lines}</span>")

        code_lines.append("</div>")
        return "".join(code_lines)

    def _parse(self, code_lines: List[str]) -> List[ParsedBlock]:
        parsed: List[ParsedBlock] = []
        multiline = False
        used_prompt = None
        prev: Optional[ParsedBlock] = None
        for line in code_lines:
            if match := self.regex_prompts.match(line):
                used_prompt = match.group()
                prev = Command(used_prompt.strip(), [line.rsplit(used_prompt)[1]])
                parsed.append(prev)
                multiline = bool(line.endswith("\\"))

            elif multiline:
                if prev and isinstance(prev, Command):
                    prev.lines.append(line)
                multiline = bool(line.endswith("\\"))

            elif line.startswith(self.comment_literal_start):
                prev = None
                parsed.append(Comment([line]))

            elif line.startswith(self.progress_literal_start):
                prev = None
                parsed.append(Progress())

            elif prev and isinstance(prev, Output):
                prev.lines.append(line)
            else:
                prev = Output([line])
                parsed.append(prev)

        return parsed


class TermynalPreprocessor(Preprocessor):
    """Converts fenced code blocks to termynal HTML."""

    FENCED_BLOCK_RE = re.compile(
        dedent(
            r"""
            (?P<termynal>
            (?P<comment>(?P<spaces>^[ ]*?)<!--[ ]*termynal:?(?P<config>.*?)-->)
            ([ ]|\n)*
            (?P<fence>(?P=spaces)(?:~{3,}|`{3,}))[ ]*
            ((\{(?P<attrs>[^\}\n]*)\})|
            (\.?(?P<lang>[\w#.+-]*)[ ]*)?
            (hl_lines=(?P<quot>"|')
            (?P<hl_lines>.*?)(?P=quot)[ ]*)?)
            \n
            (?P<code>.*?)(?<=\n)
            (?P=fence)[ ]*
            )$
            """,
        ),
        re.MULTILINE | re.DOTALL | re.VERBOSE,
    )

    def __init__(self, config: Config, md: "core.Markdown"):
        super(TermynalPreprocessor, self).__init__(md=md)
        self.config = config

    def run(self, lines: List[str]) -> List[str]:
        text = "\n".join(lines)

        default_termynal = Termynal(self.config)
        termynal = default_termynal
        while True:
            m = self.FENCED_BLOCK_RE.search(text)
            if m:
                start = m.start("termynal")
                end = m.end()
                code = m.group("code")
                spaces = m.group("spaces") or ""
                config_raw = (m.group("config") or "").strip()
                if config_raw:
                    config = parse_config(config_raw)
                    if config:
                        termynal = Termynal(config)

                converted_code = add_spaces(
                    termynal.convert(escape(remove_spaces(code, spaces))),
                    spaces,
                )
                text = f"{text[:start]}\n{converted_code}\n{text[end:]}"
                termynal = default_termynal
            else:
                break

        return text.split("\n")


class TermynalExtension(Extension):
    def __init__(self, *args: Any, **kwargs: Any):
        self.config = {
            "title": [
                "bash",
                "Default: 'bash'",
            ],
            "buttons": [
                "macos",
                "Default: 'macos'",
            ],
            "prompt_literal_start": [
                [
                    "$",
                ],
                "A list of prompt characters start to consider as console - "
                "Default: ['$']",
            ],
        }

        super(TermynalExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md: "core.Markdown") -> None:  # noqa:N802
        """Register the extension."""
        md.registerExtension(self)
        config = parse_config_from_dict(self.getConfigs())
        md.preprocessors.register(
            TermynalPreprocessor(config, md),
            "termynal",
            TERMYNAL_PREPROCESSOR_PRIORITY,
        )


def makeExtension(  # noqa:N802  # pylint:disable=invalid-name
    *args: Any,
    **kwargs: Any,
) -> TermynalExtension:
    """Return extension."""
    return TermynalExtension(*args, **kwargs)
