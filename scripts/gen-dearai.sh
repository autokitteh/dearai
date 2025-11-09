#!/bin/bash

set -euo pipefail

rm -fR dearai
mkdir dearai
mkdir dearai/src
mkdir dearai/src/integrations

find src -type f ! -name "_*" -not -path "*/_*/*" -exec uvx --from jinja2-cli jinja2 --strict {} -o dearai/{} \;

cp -r src/pyak dearai/pyak
cp -r data/kittehub-main dearai/kittehub

# truncate all README.md files to the metadata.
find dearai/kittehub -type f -name "README.md" -exec sh -c 'awk "BEGIN{c=0} /^---$/ {c++; next} c==1 {print} c==2 {exit}" "$1" > tmp && mv tmp "$1"' _ {} \;

mv dearai/src/* dearai
rm -fR dearai/src
