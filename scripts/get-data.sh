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

find kittehub-main -name autokitteh.yaml -exec grep integration: {} \; | cut -d:  -f 2 | xargs -n 1 echo - | sort -u > integrations.txt

sed -n '/^#.*/!p' <  "autokitteh-main/runtimes/pythonrt/py-sdk/docs/requirements.txt" | sed -n "/^$/!p" > requirements.txt

cp -r autokitteh-main/runtimes/pythonrt/py-sdk/autokitteh pyak

find pyak -name "*.py" -exec ../scripts/abrv.sh {} \;
find pyak -name "*_test.py" -exec rm -f {} \;
