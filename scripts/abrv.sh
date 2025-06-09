#!/bin/bash

set -euo pipefail

fn="$1"

uv run --with astor "$(dirname "$0")/abrv.py" < "${fn}" > "${fn}.tmp"
mv "${fn}.tmp" "${fn}"
