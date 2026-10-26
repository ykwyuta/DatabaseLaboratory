#!/bin/bash
set -euo pipefail
test -f /database/rava-ready
su - db2inst1 -c 'db2 connect to RAVA >/dev/null && db2 -x "SELECT dataset_version FROM demo_ready WHERE id=1"' | grep -q rava-v1
