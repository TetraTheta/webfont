#!/bin/bash

VENV_PATH="./.venv"
SOURCE_DIR="fonts-original"
OUTPUT_BASE="dist/fonts"
GLYPHS_FILE="glyphs/glyphs.txt"

declare -A FONT_MAP
FONT_MAP["Goorm Sans Code"]="goorm_Sans_Code_400.ttf"
FONT_MAP["Noto Sans KR Bold"]="NotoSansKR-Bold.ttf"
FONT_MAP["Noto Sans KR"]="NotoSansKR-Regular.ttf"
FONT_MAP["RIDI Batang"]="RIDIBatang.otf"

if [ ! -d "$VENV_PATH" ]; then
  echo "Creating Python Virtual Environment..."
  python -m venv $VENV_PATH
  # shellcheck disable=SC1091
  source "$VENV_PATH/Scripts/activate"
  echo "Installing dependencies..."
  if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
  else
    echo "ERROR: requirements.txt is missing. Aborting..."
    exit 1
  fi
else
  # shellcheck disable=SC1091
  source "$VENV_PATH/Scripts/activate"
fi

if [ -d ".git" ] && [ -f ".gitmodules" ]; then
  echo "Initializing and updating submodules..."
  git submodule update --init --recursive

  if [ ! -f "$GLYPHS_FILE" ]; then
    echo "WARNING: Submodule updated, but '$GLYPHS_FILE' is still missing."
  fi
else
  if [ ! -d "glyphs" ]; then
    echo "ERROR: 'glyphs' directory not found and not in a git repository."
    echo "Please ensure the glyphs submodule is downloaded."
    exit 1
  fi
fi

# slugify: Uppercase -> Lowercase, Space -> Dash
slugify() {
  echo "$1" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | sed 's/\.[^.]*$//'
}

run_conversion() {
  local NAME="$1"
  local SRC_FILE="$SOURCE_DIR/$2"
  local TYPE="$3"
  local SLUG
  SLUG=$(slugify "$NAME")
  local OUT_NAME="${SLUG}"

  if [[ "$TYPE" == "subset" ]]; then
    OUT_NAME="${SLUG}-subset"
  fi

  mkdir -p "$OUTPUT_BASE"

  if [ ! -f "$SRC_FILE" ]; then
    echo "ERROR: Source font file '$SRC_FILE' not found for '$NAME'."
    return 1
  fi

  for FLAVOR in "woff" "woff2"; do
    echo "Generating $TYPE $FLAVOR for $NAME..."
    local ARGS=("$SRC_FILE" "--flavor=$FLAVOR" "--output-file=$OUTPUT_BASE/$OUT_NAME.$FLAVOR")
    ARGS+=(
      "--layout-features=*"
      "--glyph-names"
      "--symbol-cmap"
      "--legacy-cmap"
      "--notdef-glyph"
      "--notdef-outline"
      "--recommended-glyphs"
      "--name-legacy"
      "--name-IDs=*"
      "--name-languages=*"
    )

    if [[ "$FLAVOR" == "woff" ]]; then
      ARGS+=("--with-zopfli")
    fi

    if [[ "$TYPE" == "subset" ]]; then
      ARGS+=("--text-file=$GLYPHS_FILE")
    else
      ARGS+=("--unicodes=*")
    fi

    pyftsubset "${ARGS[@]}"
    echo "DONE: $NAME ($TYPE)"
  done
}

SELECTED_FONT=""
DO_ALL=false
MODE="full"

for i in "$@"; do
  case $i in
    --font=*)
      SELECTED_FONT="${i#*=}"
      shift
      ;;
    --all)
      DO_ALL=true
      shift
      ;;
    --subset)
      MODE="subset"
      shift
      ;;
    --full)
      MODE="full"
      shift
      ;;
    --both)
      MODE="both"
      shift
      ;;
    *)
      # Unknown option
      ;;
  esac
done

if [[ "$DO_ALL" == false && -z "$SELECTED_FONT" ]]; then
  echo "--- Font Generation Tool ---"
  PS3="Select a font to generate (or 'All'): "
  OPTIONS=("All" "${!FONT_MAP[@]}" "Quit")
  
  select opt in "${OPTIONS[@]}"; do
    case $opt in
      "All")
        DO_ALL=true
        break
        ;;
      "Quit")
        exit 0
        ;;
      *)
        if [[ -n "${FONT_MAP[$opt]}" ]]; then
          SELECTED_FONT="$opt"
          break
        else
          echo "Invalid option."
        fi
        ;;
    esac
  done

  if [[ "$MODE" == "full" ]]; then # default
    echo "Select generation type:"
    select m in "Full" "Subset" "Both"; do
      MODE=$(echo "$m" | tr '[:upper:]' '[:lower:]')
      break
    done
  fi
fi

process_font() {
  local F_NAME="$1"
  local F_FILE="${FONT_MAP[$1]}"
  
  if [[ "$MODE" == "full" || "$MODE" == "both" ]]; then
    run_conversion "$F_NAME" "$F_FILE" "full"
  fi
  if [[ "$MODE" == "subset" || "$MODE" == "both" ]]; then
    run_conversion "$F_NAME" "$F_FILE" "subset"
  fi
}

if [[ "$DO_ALL" == true ]]; then
  for FNAME in "${!FONT_MAP[@]}"; do
    process_font "$FNAME"
  done
else
  if [[ -z "${FONT_MAP[$SELECTED_FONT]}" ]]; then
    echo "Error: Font family '$SELECTED_FONT' not recognized in FONT_MAP."
    exit 1
  fi
  process_font "$SELECTED_FONT"
fi

echo "Workflow complete."
read -r -p "Press enter to continue"
