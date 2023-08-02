import re
from enum import Enum
from textwrap import dedent
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Iterable,
    List,
    NamedTuple,
    Optional,
    Union,
)

import yaml
import yaml.parser
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor

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


def parse_config(raw: str) -> Optional[Config]:
    try:
        config = yaml.full_load(raw)
    except yaml.parser.ParserError:
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

    def parse(self, code_lines: List[str]) -> List[ParsedBlock]:
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

    def convert(self, code: str) -> str:
        code_lines: List[str] = []
        code_lines.append(
            f'<div class="termy" data-termynal data-ty-{self.config.buttons.value} '
            f'data-ty-title="{self.config.title}">',
        )

        for block in self.parse(code.split("\n")):
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


class TermynalPreprocessor(Preprocessor):
    ty_comment = re.compile(r"<!--\s*termynal:?(.*)-->")
    marker = "9HDrdgVBNLga"
    FENCED_BLOCK_RE = re.compile(
        dedent(
            r"""
            (?P<fence>^(?:~{3,}|`{3,}))[ ]*   # opening fence
            ((\{(?P<attrs>[^\}\n]*)\})|       # (optional {attrs} or
            (\.?(?P<lang>[\w#.+-]*)[ ]*)?     # optional (.)lang
            (hl_lines=(?P<quot>"|')           # optional hl_lines)
            (?P<hl_lines>.*?)(?P=quot)[ ]*)?)
            \n                                # newline (end of opening fence)
            (?P<code>.*?)(?<=\n)              # the code block
            (?P=fence)[ ]*$                   # closing fence
        """,
        ),
        re.MULTILINE | re.DOTALL | re.VERBOSE,
    )

    def __init__(self, config: Config, md: "core.Markdown"):
        super(TermynalPreprocessor, self).__init__(md=md)
        self.config = config

    def run(self, lines: List[str]) -> List[str]:
        placeholder_i = 0
        text = "\n".join(lines)
        store = {}
        while 1:
            m = self.FENCED_BLOCK_RE.search(text)
            if m:
                code = m.group("code")
                placeholder = f"{self.marker}-{placeholder_i}"
                placeholder_i += 1
                store[placeholder] = (code, text[m.start() : m.end()])
                text = f"{text[:m.start()]}\n{placeholder}\n{text[m.end():]}"
            else:
                break

        default_termynal = Termynal(self.config)
        termynal = default_termynal

        new_lines: List[str] = []
        is_ty_code = False
        for line in text.split("\n"):
            ty_match = self.ty_comment.match(line)
            if ty_match:
                configs_raw = ty_match.group(1)
                if configs_raw and configs_raw.strip():
                    config = parse_config(configs_raw)
                    if config:
                        termynal = Termynal(config)
                is_ty_code = True
                continue

            if is_ty_code and line in store:
                new_lines.append(termynal.convert(self._escape(store[line][0])))
                termynal = default_termynal
                is_ty_code = False
            elif line in store:
                new_lines.append(store[line][1])
            else:
                new_lines.append(line)

        return new_lines

    def _escape(self, txt: str) -> str:
        txt = txt.replace("&", "&amp;")
        txt = txt.replace("<", "&lt;")
        txt = txt.replace(">", "&gt;")
        txt = txt.replace('"', "&quot;")
        return txt  # noqa:RET504


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
        md.preprocessors.register(TermynalPreprocessor(config, md), "termynal", 35)


def makeExtension(  # noqa:N802  # pylint:disable=invalid-name
    *args: Any,
    **kwargs: Any,
) -> TermynalExtension:
    """Return extension."""
    return TermynalExtension(*args, **kwargs)
