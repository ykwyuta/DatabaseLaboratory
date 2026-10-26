#!/bin/sh
set -eu
# A client sidecar avoids depending on undocumented Omni initialization hooks.
if ! PGUSER=postgres PGDATABASE=postgres psql -Atc "SELECT 1 FROM pg_roles WHERE rolname='rava'" | grep -qx 1; then
  PGUSER=postgres PGDATABASE=postgres psql -v ON_ERROR_STOP=1 -c "CREATE ROLE rava LOGIN SUPERUSER PASSWORD 'Rava_Test_2026!';"
fi
if ! PGUSER=postgres PGDATABASE=postgres psql -Atc "SELECT 1 FROM pg_database WHERE datname='rava'" | grep -qx 1; then
  PGUSER=postgres PGDATABASE=postgres createdb -O rava rava
fi
if ! psql -Atc 'SELECT dataset_version FROM demo_ready WHERE id=1' 2>/dev/null | grep -qx rava-v1; then
  psql -v ON_ERROR_STOP=1 -f /demo/init.sql
fi
echo 'Rava: AlloyDB Omni sample data ready'
# The healthcheck queries the server continuously, including after server restarts.
exec sleep infinity
