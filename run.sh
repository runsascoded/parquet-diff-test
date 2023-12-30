#!/usr/bin/env bash

pip freeze > pip.txt
python parquet_diff_test.py > output.json
xxd test.parquet > xxd.txt

git add pip.txt output.json test.parquet xxd.txt
git commit -m "run.sh"
