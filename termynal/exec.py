"""Run a command and emit a termynal-ready Markdown block.

This is a *standalone* authoring helper. It executes a command and prints a
fenced ``<!-- termynal -->`` block that captures the command's (optionally
colored) output. termynal's rendering core stays a pure text->HTML transform:
execution lives here, in an explicit step you run yourself (locally, in a
pre-commit hook, or in CI), never inside ``mkdocs build``.

The block it prints is *termynal-ready Markdown*, not HTML. termynal remains the
single renderer that turns ANSI sequences into colored spans and the prompt line
into an animated input, so there is exactly one ANSI converter and one set of
color schemes to maintain.

Example::

    python -m termynal.exec mytool --help

Pipe the output into a docs page, or paste it in. Colors come through because we
run the command with ``FORCE_COLOR=1`` (respected by rich/click/typer and many
others); use ``--pty`` for CLIs that strictly check ``isatty``.
"""

import argparse
import os
import shlex
import subprocess
import sys
from typing import Dict, List, Optional, Sequence


def run_command(
    command: Sequence[str],
    *,
    columns: int = 80,
    timeout: Optional[float] = 30.0,
    cwd: Optional[str] = None,
    env: Optional[Dict[str, str]] = None,
    color: bool = True,
    merge_stderr: bool = True,
    use_pty: bool = False,
) -> str:
    """Run ``command`` and return its captured output as text.

    ``columns`` pins terminal width so output wrapping is reproducible.
    ``color`` sets ``FORCE_COLOR``/``NO_COLOR`` so ANSI is kept (or dropped)
    even though stdout is captured rather than a TTY. ``use_pty`` runs the
    command under a pseudo-terminal (POSIX only) for CLIs that ignore
    ``FORCE_COLOR`` and check ``isatty`` directly.
    """
    run_env = dict(os.environ if env is None else env)
    run_env["COLUMNS"] = str(columns)
    if color:
        run_env["FORCE_COLOR"] = "1"
        run_env.pop("NO_COLOR", None)
    else:
        run_env["NO_COLOR"] = "1"
        run_env.pop("FORCE_COLOR", None)

    if use_pty:
        return _run_with_pty(command, run_env, cwd, timeout, columns)

    proc = subprocess.run(  # noqa: S603
        list(command),
        capture_output=True,
        text=True,
        timeout=timeout,
        cwd=cwd,
        env=run_env,
        check=False,
    )
    out = proc.stdout or ""
    if merge_stderr and proc.stderr:
        out = f"{out}{proc.stderr}" if out else proc.stderr
    return out


def _run_with_pty(
    command: Sequence[str],
    env: Dict[str, str],
    cwd: Optional[str],
    timeout: Optional[float],
    columns: int,
) -> str:
    """Run ``command`` under a pseudo-terminal and return combined output.

    POSIX only. stdout and stderr are interleaved on the same stream, exactly
    as a real terminal would see them.
    """
    import fcntl
    import pty
    import select
    import struct
    import termios
    import time

    master, slave = pty.openpty()
    fcntl.ioctl(master, termios.TIOCSWINSZ, struct.pack("HHHH", 24, columns, 0, 0))
    proc = subprocess.Popen(  # noqa: S603
        list(command),
        stdin=slave,
        stdout=slave,
        stderr=slave,
        cwd=cwd,
        env=env,
        close_fds=True,
    )
    os.close(slave)

    chunks: List[bytes] = []
    deadline = None if timeout is None else time.monotonic() + timeout
    try:
        while True:
            wait = None if deadline is None else max(0.0, deadline - time.monotonic())
            if deadline is not None and wait == 0.0:
                proc.kill()
                raise subprocess.TimeoutExpired(list(command), timeout)
            ready, _, _ = select.select([master], [], [], wait)
            if not ready:
                continue
            try:
                data = os.read(master, 4096)
            except OSError:
                break
            if not data:
                break
            chunks.append(data)
    finally:
        os.close(master)
        proc.wait()
    return b"".join(chunks).decode("utf-8", errors="replace")


def to_termynal_block(
    command_display: str,
    output: str,
    *,
    ansi: bool = True,
    prompt: str = "$",
    title: Optional[str] = None,
    fence: str = "```",
) -> str:
    """Build a termynal Markdown block from a command and its captured output.

    The command becomes the animated input line; ``output`` follows verbatim,
    ANSI escapes and all, for termynal to render when ``ansi`` is enabled.
    """
    options: Dict[str, object] = {}
    if ansi:
        options["ansi"] = True
    if title is not None:
        options["title"] = title

    if not options:
        header = "<!-- termynal -->"
    elif list(options) == ["ansi"]:
        # Single key: match the plain form used throughout the docs.
        header = "<!-- termynal: ansi: true -->"
    else:
        inner = ", ".join(_format_option(k, v) for k, v in options.items())
        header = f"<!-- termynal: {{{inner}}} -->"

    lines = [f"{prompt} {command_display}"]
    body = output.replace("\r\n", "\n").rstrip("\n")
    if body:
        lines.extend(body.split("\n"))
    return f"{header}\n{fence}\n" + "\n".join(lines) + f"\n{fence}\n"


def _format_option(key: str, value: object) -> str:
    if isinstance(value, bool):
        return f"{key}: {'true' if value else 'false'}"
    return f"{key}: {value}"


def render(
    command: Sequence[str],
    *,
    command_display: Optional[str] = None,
    ansi: bool = True,
    prompt: str = "$",
    title: Optional[str] = None,
    **run_kwargs: object,
) -> str:
    """Run ``command`` and return a termynal-ready Markdown block."""
    output = run_command(command, **run_kwargs)  # type: ignore[arg-type]
    display = command_display if command_display is not None else shlex.join(command)
    return to_termynal_block(
        display,
        output,
        ansi=ansi,
        prompt=prompt,
        title=title,
    )


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m termynal.exec",
        description="Run a command and print a termynal-ready Markdown block.",
    )
    parser.add_argument(
        "command",
        nargs="+",
        help="Command to run, e.g. mytool --help (quote it or use -- to pass flags).",
    )
    parser.add_argument("--prompt", default="$", help="Prompt shown before the command.")
    parser.add_argument("--title", default=None, help="Terminal title for the block.")
    parser.add_argument(
        "--columns",
        type=int,
        default=80,
        help="Terminal width passed to the command (default: 80).",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="Seconds before the command is killed (default: 30).",
    )
    parser.add_argument("--cwd", default=None, help="Working directory for the command.")
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Do not force ANSI color; emit a plain block.",
    )
    parser.add_argument(
        "--no-ansi",
        action="store_true",
        help="Omit 'ansi: true' from the block even when color is captured.",
    )
    parser.add_argument(
        "--pty",
        action="store_true",
        help="Run under a pseudo-terminal (POSIX) for CLIs that check isatty.",
    )
    args = parser.parse_args(argv)

    # A single quoted argument like "mytool --help" is split into argv.
    command = shlex.split(args.command[0]) if len(args.command) == 1 else args.command

    block = render(
        command,
        command_display=shlex.join(command),
        ansi=not args.no_ansi,
        prompt=args.prompt,
        title=args.title,
        columns=args.columns,
        timeout=args.timeout,
        cwd=args.cwd,
        color=not args.no_color,
        use_pty=args.pty,
    )
    sys.stdout.write(block)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
