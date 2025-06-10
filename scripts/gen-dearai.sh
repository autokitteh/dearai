#!/bin/bash

set -euo pipefail

rm -fR dearai
mkdir dearai

find src -type d ! -name "_*" -exec mkdir -p dearai/{} \;
find src -type f ! -name "_*" -exec uvx jinja2 --strict {} -o dearai/{} \;

mv dearai/src/* dearai
rm -fR dearai/src
