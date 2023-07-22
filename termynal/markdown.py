import re
from typing import TYPE_CHECKING, Dict, List

from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor

if TYPE_CHECKING:  # pragma:no cover
    from markdown import core


class Termynal:
    progress_literal_start = "---&gt; 100%"
    custom_literal_start = "# "

    def __init__(
        self,
        prompt_literal_start: tuple = ("$ ",),
        promt_in_multiline: bool = False,
    ):
        """Initialize."""
        self.prompt_literal_start = "|".join(re.escape(p) for p in prompt_literal_start)
        self.regex_prompts = re.compile(f"^({self.prompt_literal_start})")
        self.promt_in_multiline = promt_in_multiline

    def convert(self, code: str) -> List[str]:
        code_lines = []
        code_lines.append('<div class="termy" data-termynal>')
        multiline = False
        used_prompt = None
        for line in code.split("\n"):
            if match := self.regex_prompts.match(line):
                used_prompt = match.group()
                code_lines.append(
                    f'<span data-ty="input" data-ty-prompt="{used_prompt.strip()}">'
                    f"{line.rsplit(used_prompt)[1].replace(' ', '&nbsp;')}</span>",
                )
                multiline = bool(line.endswith("\\"))
            elif multiline:
                used_prompt = used_prompt or ""
                if not self.promt_in_multiline:
                    used_prompt = ""
                code_lines.append(
                    f'<span data-ty="input" data-ty-prompt="{used_prompt.strip()}">'
                    f'{line.replace(" ", "&nbsp;")}</span>',
                )
                multiline = bool(line.endswith("\\"))

            elif line.startswith(self.custom_literal_start):
                code_lines.append(
                    f'<span class="termynal-comment" data-ty>{line}</span>',
                )
            elif line.startswith(self.progress_literal_start):
                code_lines.append('<span data-ty="progress"></span>')
            else:
                code_lines.append(f"<span data-ty>{line}</span>")
        code_lines.append("</div>")
        return code_lines


class TermynalPreprocessor(Preprocessor):
    rexep = re.compile("(<code.*>)((.|\n)*?)(</code>)")
    comment = "<!-- termynal -->"
    language_class = 'class="language-console"'

    def __init__(self, config: dict, md: "core.Markdown"):
        """Initialize."""
        self.prompt_literal_start = config.get("prompt_literal_start", ("$ ",))
        self.promt_in_multiline = config.get("promt_in_multiline", False)

        super(TermynalPreprocessor, self).__init__(md=md)

    def run(self, lines: List):
        content_by_placeholder = {}
        for i in range(self.md.htmlStash.html_counter):
            placeholder = self.md.htmlStash.get_placeholder(i)
            content = self.md.htmlStash.rawHtmlBlocks[i]
            content_by_placeholder[placeholder] = (content, i)

        lines_by_placeholder = self._get_lines(lines, content_by_placeholder)

        new_lines = []
        for line in lines:
            new_lines.append(line)
            if line in lines_by_placeholder:
                new_lines.extend(lines_by_placeholder[line])

        return new_lines

    def _get_lines(
        self,
        lines: List,
        content_by_placeholder: Dict,
    ):  # pylint:disable=too-many-nested-blocks
        termynal_obj = Termynal(
            prompt_literal_start=self.prompt_literal_start,
            promt_in_multiline=self.promt_in_multiline,
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
                self.md.htmlStash.rawHtmlBlocks[i] = ""
                content = matches.group(2)
                code_lines = termynal_obj.convert(code=content)
                if code_lines:
                    lines_by_placeholder[line] = code_lines

        return lines_by_placeholder


class TermynalExtension(Extension):
    def __init__(self, *args, **kwargs):
        """Initialize."""
        self.config = {
            "prompt_literal_start": [
                [
                    "$ ",
                ],
                "A list of prompt characters start to consider as console - "
                "Default: ['$ ',]",
            ],
            "promt_in_multiline": [
                False,
                "Default: False",
            ],
        }

        super(TermynalExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md: "core.Markdown"):  # noqa:N802
        """Register the extension."""
        md.registerExtension(self)
        config = self.getConfigs()
        md.preprocessors.register(TermynalPreprocessor(config, md), "termynal", 20)


def makeExtension(*args, **kwargs):  # noqa:N802  # pylint:disable=invalid-name
    """Return extension."""
    return TermynalExtension(*args, **kwargs)
