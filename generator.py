"""Font generation helpers based on fontTools Python API."""

from __future__ import annotations

from collections import OrderedDict
from pathlib import Path
from typing import Literal

from fontTools.subset import Options, Subsetter, load_font, save_font

BuildMode = Literal["full", "subset", "both"]

REPO_ROOT = Path(__file__).resolve().parent
SOURCE_DIR = REPO_ROOT / "fonts-original"
OUTPUT_DIR = REPO_ROOT / "dist" / "fonts"
GLYPHS_FILE = REPO_ROOT / "glyphs" / "glyphs.txt"

FONT_MAP: OrderedDict[str, str] = OrderedDict(
    {
        "Goorm Sans Code": "goorm_Sans_Code_400.ttf",
        "Noto Sans KR Bold": "NotoSansKR-Bold.ttf",
        "Noto Sans KR": "NotoSansKR-Regular.ttf",
        "RIDI Batang": "RIDIBatang.otf",
    }
)


class FontGenerationError(Exception):
    """Raised when font generation preconditions are not met."""


def slugify(font_name: str) -> str:
    return font_name.strip().lower().replace(" ", "-")


def ensure_environment(require_subset: bool) -> None:
    if not SOURCE_DIR.exists():
        raise FontGenerationError(f"소스 폰트 디렉터리가 없습니다: {SOURCE_DIR}. 필요한 파일을 준비해 주세요.")

    missing_sources = [
        str(SOURCE_DIR / source_file) for source_file in FONT_MAP.values() if not (SOURCE_DIR / source_file).exists()
    ]
    if missing_sources:
        raise FontGenerationError("다음 소스 폰트 파일이 없습니다:\n" + "\n".join(missing_sources))

    if require_subset and not GLYPHS_FILE.exists():
        in_git_repo = (REPO_ROOT / ".git").exists() and (REPO_ROOT / ".gitmodules").exists()
        hint = (
            "git submodule update --init --recursive 를 먼저 실행해 주세요."
            if in_git_repo
            else "glyphs 서브모듈(또는 동등한 glyphs 파일)을 먼저 준비해 주세요."
        )
        raise FontGenerationError(f"서브셋 글리프 파일이 없습니다: {GLYPHS_FILE}. {hint}")


def make_options(flavor: Literal["woff", "woff2"]) -> Options:
    options = Options()
    options.set(
        flavor=flavor,
        layout_features=["*"],
        glyph_names=True,
        symbol_cmap=True,
        legacy_cmap=True,
        notdef_glyph=True,
        notdef_outline=True,
        recommended_glyphs=True,
        name_legacy=True,
        name_IDs=["*"],
        name_languages=["*"],
        with_zopfli=(flavor == "woff"),
    )
    return options


def resolve_flavor(output_file: Path) -> Literal["woff", "woff2"]:
    suffix = output_file.suffix.lstrip(".")
    if suffix == "woff":
        return "woff"
    if suffix == "woff2":
        return "woff2"
    raise FontGenerationError(f"지원하지 않는 출력 포맷입니다: {suffix}")


def run_subset(source_file: Path, output_file: Path, generation_type: Literal["full", "subset"]) -> None:
    options = make_options(flavor=resolve_flavor(output_file))
    subsetter = Subsetter(options=options)
    font = load_font(source_file, options)

    if generation_type == "subset":
        subsetter.populate(text=GLYPHS_FILE.read_text(encoding="utf-8"))
    else:
        # Python API의 populate는 CLI의 `--unicodes=*` 와일드카드를 지원하지 않으므로
        # 전체 글리프 이름을 명시적으로 전달해 full 출력 동작을 동일하게 맞춘다.
        subsetter.populate(glyphs=font.getGlyphOrder())

    subsetter.subset(font)
    save_font(font, output_file, options)


def run_conversion(font_name: str, source_filename: str, generation_type: Literal["full", "subset"]) -> None:
    slug = slugify(font_name)
    output_name = f"{slug}-subset" if generation_type == "subset" else slug

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    source_file = SOURCE_DIR / source_filename
    if not source_file.exists():
        raise FontGenerationError(f"소스 폰트 파일이 없습니다: {source_file}")

    for flavor in ("woff", "woff2"):
        output_file = OUTPUT_DIR / f"{output_name}.{flavor}"
        print(f"{font_name} {generation_type} {flavor} 생성 중...")
        run_subset(source_file=source_file, output_file=output_file, generation_type=generation_type)

    print(f"{font_name} ({generation_type}) 생성 완료")


def process_font(font_name: str, mode: BuildMode) -> None:
    source_filename = FONT_MAP.get(font_name)
    if source_filename is None:
        raise FontGenerationError(f"알 수 없는 폰트 이름입니다: {font_name}")

    if mode in ("full", "both"):
        run_conversion(font_name=font_name, source_filename=source_filename, generation_type="full")
    if mode in ("subset", "both"):
        run_conversion(font_name=font_name, source_filename=source_filename, generation_type="subset")


def select_target_font_interactively() -> str | None:
    options = ["All", *FONT_MAP.keys(), "Quit"]
    print("--- Font Generation Tool ---")
    for index, option in enumerate(options, start=1):
        print(f"{index}. {option}")

    raw = input("번호를 선택하세요: ").strip()
    if not raw.isdigit():
        raise FontGenerationError("숫자를 입력해 주세요.")

    selected_index = int(raw)
    if selected_index < 1 or selected_index > len(options):
        raise FontGenerationError("유효하지 않은 선택입니다.")

    choice = options[selected_index - 1]
    if choice == "Quit":
        return None
    if choice == "All":
        return "__ALL__"
    return choice


def select_mode_interactively(default_mode: BuildMode) -> BuildMode:
    if default_mode != "full":
        return default_mode

    mode_map: dict[str, BuildMode] = {"1": "full", "2": "subset", "3": "both"}
    print("생성 모드를 선택하세요:")
    print("1. Full")
    print("2. Subset")
    print("3. Both")
    selected = input("번호를 선택하세요: ").strip()
    mode = mode_map.get(selected)
    if mode is None:
        raise FontGenerationError("유효하지 않은 모드 선택입니다.")
    return mode
