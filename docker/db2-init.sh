#!/bin/bash
set -euo pipefail
if ! su - db2inst1 -c 'db2 connect to DBLAB >/dev/null && db2 -x "SELECT dataset_version FROM demo_ready WHERE id=1"' 2>/dev/null | grep -q dblab-v1; then
  su - db2inst1 -c 'export DB2CODEPAGE=1208; db2 connect to DBLAB && db2 -stvf /demo/init.sql'
fi
touch /database/dblab-ready
echo 'Demo: Db2 sample data ready'
