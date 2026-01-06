#!/usr/bin/env bash
set -euo pipefail

if ! command -v clang-format >/dev/null 2>&1; then
  echo "clang-format is required" >&2
  exit 1
fi

files=$(find include src tests consumer/src \( -name "*.cpp" -o -name "*.h" \) | sort)

if [[ -z "$files" ]]; then
  echo "No source files to format"
  exit 0
fi

clang-format --style=file --dry-run --Werror ${files}
