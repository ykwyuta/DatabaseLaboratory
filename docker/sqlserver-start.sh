#!/bin/bash
set -euo pipefail
# Keep sqlservr as PID 1, and seed using its bundled client once TCP is ready.
(
  ready=false
  for attempt in $(seq 1 180); do
    if /opt/mssql-tools18/bin/sqlcmd -S 127.0.0.1 -U sa -C -b -d master -Q "IF DB_ID(N'rava') IS NOT NULL EXEC(N'USE rava; SELECT 1'); SELECT 1" >/dev/null 2>&1; then
      ready=true
      break
    fi
    sleep 2
  done
  if [ "$ready" != true ]; then echo 'Demo: SQL Server did not become ready' >&2; exit 1; fi
  if ! /opt/mssql-tools18/bin/sqlcmd -S 127.0.0.1 -U sa -C -b -d rava -Q 'SELECT dataset_version FROM demo_ready WHERE id=1' >/dev/null 2>&1; then
    /opt/mssql-tools18/bin/sqlcmd -S 127.0.0.1 -U sa -C -b -d master -I -f 65001 -i /demo/init.sql
  fi
  touch /var/opt/mssql/rava-ready
  echo 'Demo: SQL Server sample data ready'
) &
exec /opt/mssql/bin/sqlservr
