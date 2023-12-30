#!/usr/bin/env bash

set -e

pip freeze > pip.txt
parquet-diff-test

git add .
git commit -m "run.sh"
