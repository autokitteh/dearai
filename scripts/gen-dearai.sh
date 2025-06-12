#!/bin/bash

set -euo pipefail

rm -fR dearai
mkdir dearai
mkdir dearai/src
mkdir dearai/src/integrations

find src -type f ! -name "_*" -not -path "*/_*/*" -exec uvx jinja2 --strict {} -o dearai/{} \;

cp -r src/pyak dearai/pyak
cp -r src/samples dearai/samples

find dearai/samples -name "README.md" -exec rm -f {} \;

mv dearai/src/* dearai
rm -fR dearai/src
