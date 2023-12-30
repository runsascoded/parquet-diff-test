#!/usr/bin/env bash

pip freeze > pip.txt
parquet-diff-test

git add .
git commit -m "run.sh"
