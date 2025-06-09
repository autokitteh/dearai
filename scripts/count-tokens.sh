#!/bin/bash

set -euo pipefail

cd scripts || exit 1

for path in ../digests/*.txt; do
    echo -n "$(basename "${path}"): "
	uv run -q --with tiktoken count_tokens.py < "${path}"
done
