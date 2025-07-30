#!/bin/bash

set -euo pipefail

digest() {
    in="$1"
    out="$2"
    shift 2
    
    kind="$(basename "${in}")"
    pre="src/_preambles/${kind}.md"

    if [[ -r "${pre}" ]]; then
        tmp="digests/${kind}_"
        uvx gitingest@0.1.5 "${in}" --output "${tmp}" "$@"
        cat "${pre}" "${tmp}" > "${out}"
        rm -f "${tmp}"
    else
        uvx gitingest@0.1.5 "${in}" --output "${out}" "$@"
    fi
}

rm -fR digests
mkdir digests

digest dearai digests/dearai.txt -e kittehub
digest dearai/pyak digests/pyak.txt
digest dearai/integrations digests/integrations.txt
digest dearai/kittehub digests/kittehub.txt

./scripts/filter_digest.sh digests/kittehub.txt --include-tag "essential" > digests/kittehub-essential.txt
