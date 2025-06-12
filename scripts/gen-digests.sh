#!/bin/bash

set -euo pipefail

digest() {
    in="$1"
    out="$2"
    kind="$(basename "${in}")"
    pre="src/_preambles/${kind}.md"

    if [[ -r "${pre}" ]]; then
        tmp="digests/${kind}_"
        uvx gitingest "${in}" --output "${tmp}"
        cat "${pre}" "${tmp}" > "${out}"
        rm -f "${tmp}"
    else
        uvx gitingest "${in}" --output "${out}"
    fi
}

rm -fR digests
mkdir digests

digest dearai digests/dearai.txt
digest dearai/pyak digests/pyak.txt
digest dearai/samples digests/samples.txt
digest dearai/integrations digests/integrations.txt
