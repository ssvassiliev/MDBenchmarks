#!/bin/bash
# This script will create a new serial/parallel benchmark or software entry
# by duplicating a benchmark or software with a specific user supplied PK
# Usage: bash ./duplicate_model <serial|parallel|software> <PK>
# Create directory for temporary files: mkdir -p mdbench/fixtures/

if [ $# != 2 ]; then
  echo "Usage: bash ./duplicate_model.sh serial|parallel|software pk"
  exit
fi

source ~/.bashrc

if  [ $1 = "serial" ]; then
  python3 manage.py dumpdata mdbench.SerialBenchmarkInstance \
  --pks $2 --format yaml > mdbench/fixtures/tmp.yaml
elif  [ $1 = "parallel" ]; then
  python3 manage.py dumpdata mdbench.BenchmarkInstance \
  --pks $2 --format yaml > mdbench/fixtures/tmp.yaml
elif  [ $1 = "software" ]; then
  python3 manage.py dumpdata mdbench.Software \
  --pks $2 --format yaml > mdbench/fixtures/tmp.yaml
else
  echo 'Error: argument #1 should be "serial", "parallel", or "software"'
  exit
fi

# Replace pk with null
sed '2s/.*/  pk: null/' mdbench/fixtures/tmp.yaml > mdbench/fixtures/tmp2.yaml

python3 manage.py loaddata mdbench/fixtures/tmp2.yaml
rm mdbench/fixtures/tmp*.yaml
