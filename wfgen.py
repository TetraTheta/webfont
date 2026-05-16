"""CLI entrypoint for webfont generation."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence

from generator import (
    FONT_MAP,
    BuildMode,
    FontGenerationError,
    ensure_environment,
    process_font,
    select_mode_interactively,
    select_target_font_interactively,
)


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate webfont files from source fonts.")
    parser.add_argument("--font", choices=sorted(FONT_MAP.keys()), help="Single font family to generate.")
    parser.add_argument("--all", action="store_true", help="Generate all configured font families.")
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument("--subset", action="store_true", help="Generate only subset webfonts.")
    mode_group.add_argument("--full", action="store_true", help="Generate only full webfonts.")
    mode_group.add_argument("--both", action="store_true", help="Generate full and subset webfonts.")
    return parser.parse_args(argv)


def resolve_mode(args: argparse.Namespace) -> BuildMode:
    if args.subset:
        return "subset"
    if args.both:
        return "both"
    return "full"


def main(argv: Sequence[str] | None = None) -> int:
    arguments = parse_args(argv or sys.argv[1:])

    selected_font = arguments.font
    do_all = bool(arguments.all)
    mode = resolve_mode(arguments)

    if not do_all and not selected_font:
        selected_font = select_target_font_interactively()
        if selected_font is None:
            return 0
        if selected_font == "__ALL__":
            do_all = True
            selected_font = None
        mode = select_mode_interactively(default_mode=mode)

    if do_all and selected_font:
        print("`--all`과 `--font`는 함께 사용할 수 없습니다.")
        return 2

    try:
        ensure_environment(require_subset=(mode in ("subset", "both")))

        if do_all:
            for font_name in FONT_MAP:
                process_font(font_name=font_name, mode=mode)
        else:
            if selected_font is None:
                print("생성 대상 폰트가 지정되지 않았습니다.")
                return 2
            process_font(font_name=selected_font, mode=mode)
    except FontGenerationError as error:
        print(f"오류: {error}")
        return 1

    print("작업이 완료되었습니다.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
