import re
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Iterable,
    List,
    NamedTuple,
    Optional,
    Tuple,
    Union,
)

from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor

if TYPE_CHECKING:  # pragma:no cover
    from markdown import core


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


class Termynal:
    def __init__(
        self,
        title: Optional[str] = None,
        prompt_literal_start: Iterable[str] = ("$",),
        progress_literal_start="---&gt; 100%",
        comment_literal_start="# ",
    ):
        self.title = title
        self.regex_prompts = make_regex_prompts(prompt_literal_start)
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

            else:
                if prev and isinstance(prev, Output):
                    prev.lines.append(line)
                else:
                    prev = Output([line])
                    parsed.append(prev)

        return parsed

    def convert(self, code: str) -> str:
        code_lines: List[str] = []
        if self.title is not None:
            code_lines.append(
                f'<div class="termy" data-termynal data-ty-title="{self.title}">',
            )
        else:
            code_lines.append('<div class="termy">')

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
        return "\n".join(code_lines)


class TermynalPreprocessor(Preprocessor):
    rexep = re.compile("(<code.*>)((.|\n)*?)(</code>)")
    comment = "<!-- termynal -->"
    language_class = 'class="language-console"'

    def __init__(self, config: Dict[str, Any], md: "core.Markdown"):
        self.title = config.get("title", None)
        self.prompt_literal_start = config.get("prompt_literal_start", ("$ ",))

        super(TermynalPreprocessor, self).__init__(md=md)

    def run(self, lines: List[str]) -> List[str]:
        content_by_placeholder = {}
        for i in range(self.md.htmlStash.html_counter):
            placeholder = self.md.htmlStash.get_placeholder(i)
            content = self.md.htmlStash.rawHtmlBlocks[i]
            content_by_placeholder[placeholder] = (content, i)

        target_code_by_placeholder = self._get_lines(lines, content_by_placeholder)

        new_lines = []
        for line in lines:
            if line in target_code_by_placeholder:
                new_lines.append(target_code_by_placeholder[line])
            else:
                new_lines.append(line)

        return new_lines

    def _get_lines(
        self,
        lines: List[str],
        content_by_placeholder: Dict[str, Tuple[str, int]],
    ) -> Dict[str, str]:  # pylint:disable=too-many-nested-blocks
        termynal_obj = Termynal(
            title=self.title,
            prompt_literal_start=self.prompt_literal_start,
        )
        lines_by_placeholder = {}
        is_termynal_code = False
        for line in lines:
            if line in content_by_placeholder:
                (content, i) = content_by_placeholder[line]

                if not isinstance(content, str):
                    continue

                if content.startswith(self.comment):
                    is_termynal_code = True
                    continue

                matches = self.rexep.search(content)
                if not matches:
                    continue

                if self.language_class in matches.group(1):
                    is_termynal_code = True

                if not is_termynal_code:
                    continue

                is_termynal_code = False
                content = matches.group(2)
                target_code = termynal_obj.convert(code=content)
                if target_code:
                    self.md.htmlStash.rawHtmlBlocks[i] = ""
                    lines_by_placeholder[line] = target_code

        return lines_by_placeholder


class TermynalExtension(Extension):
    def __init__(self, *args: Any, **kwargs: Any):
        self.config = {
            "title": [
                "bash",
                "Default: 'bash'",
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
        config = self.getConfigs()
        md.preprocessors.register(TermynalPreprocessor(config, md), "termynal", 20)


def makeExtension(  # noqa:N802  # pylint:disable=invalid-name
    *args: Any,
    **kwargs: Any,
) -> TermynalExtension:
    """Return extension."""
    return TermynalExtension(*args, **kwargs)
