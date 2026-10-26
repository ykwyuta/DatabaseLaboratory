#!/bin/sh
set -eu
# A client sidecar avoids depending on undocumented Omni initialization hooks.
if ! PGUSER=postgres PGDATABASE=postgres psql -Atc "SELECT 1 FROM pg_roles WHERE rolname='dblab'" | grep -qx 1; then
  PGUSER=postgres PGDATABASE=postgres psql -v ON_ERROR_STOP=1 -c "CREATE ROLE dblab LOGIN SUPERUSER PASSWORD 'DatabaseLaboratory_Test_2026!';"
fi
if ! PGUSER=postgres PGDATABASE=postgres psql -Atc "SELECT 1 FROM pg_database WHERE datname='dblab'" | grep -qx 1; then
  PGUSER=postgres PGDATABASE=postgres createdb -O dblab dblab
fi
if ! psql -Atc 'SELECT dataset_version FROM demo_ready WHERE id=1' 2>/dev/null | grep -qx dblab-v1; then
  psql -v ON_ERROR_STOP=1 -f /demo/init.sql
fi
echo 'DatabaseLaboratory: AlloyDB Omni sample data ready'
# The healthcheck queries the server continuously, including after server restarts.
exec sleep infinity
