#!/bin/bash

set -euo pipefail

exec uv run --with python-frontmatter --with click "$(dirname "$0")/filter-digest.py" "$@"

