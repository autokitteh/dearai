#!/bin/bash

set -euo pipefail

rm -fR data
mkdir data
cd data

curl -L --progress-bar https://github.com/autokitteh/kittehub/archive/refs/heads/main.zip > kittehub.zip
unzip kittehub.zip 
rm -f kittehub.zip

curl -L --progress-bar https://github.com/autokitteh/autokitteh/archive/refs/heads/main.zip > autokitteh.zip
unzip autokitteh.zip
rm -f autokitteh.zip

git clone --depth=1 --branch=main https://github.com/autokitteh/docs.autokitteh.com.git 
rm -fR docs.autokitteh.com/.git 

cd kittehub-main/tests
printf 'import metadata_definitions; print("\\n".join(sorted(metadata_definitions.ALLOWED_INTEGRATIONS)))' | python3 > ../../integrations.txt
cd -

rm -fR kittehub-main/.git kittehub-main/.github kittehub-main/tests
find kittehub-main/ -maxdepth 1 -type f -exec rm -f {} \;
find . \( -name \*.gpx -or -name \*.png -or -name \*.gz -or -name \*.gif \) -exec rm -f {} \;

sed -n '/^#.*/!p' <  "autokitteh-main/runtimes/pythonrt/py-sdk/docs/requirements.txt" | sed -n "/^$/!p" > requirements.txt

cp -r autokitteh-main/runtimes/pythonrt/py-sdk/autokitteh pyak

find pyak -name "*.py" -exec ../scripts/abrv.sh {} \;
find pyak -name "*_test.py" -exec rm -f {} \;
