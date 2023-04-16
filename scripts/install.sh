#!/usr/bin/env bash

mkdir data

git clone https://github.com/voussoir/timesearch
cd timesearch
git checkout 01f2cdb
cd ..

python3 -m venv venv
source venv/bin/activate
pip install -r timesearch/requirements.txt
pip install -r generate/requirements.txt
pip install -r refresh/requirements.txt

mv scripts/bot.py timesearch/
./scripts/patch.sh
