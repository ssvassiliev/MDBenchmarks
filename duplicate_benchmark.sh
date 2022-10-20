#!/bin/bash
# This script will create a new serial or parallel benchmark entry
# by duplicating a benchmark with a specific supplied PK
# Usage: bash ./duplicate_benchmark serial|parallel pk


if [ $# != 2 ]; then
  echo "Need exactly two arguments!"
  exit
fi

source ~/.bashrc

if  [ $1 = "serial" ]; then
  python3 manage.py dumpdata mdbench.SerialBenchmarkInstance \
  --pks $2 --format yaml > mdbench/fixtures/tmp.yaml
elif  [ $1 = "parallel" ]; then
  python3 manage.py dumpdata mdbench.BenchmarkInstance \
  --pks $2 --format yaml > mdbench/fixtures/tmp.yaml
else
  echo 'Error: argument #1 should be "serial" or "parallel"'
  exit
fi

# Replace pk with null
sed '2s/.*/  pk: null/' mdbench/fixtures/tmp.yaml > mdbench/fixtures/tmp2.yaml

python3 manage.py loaddata mdbench/fixtures/tmp2.yaml
rm mdbench/fixtures/tmp*.yaml
