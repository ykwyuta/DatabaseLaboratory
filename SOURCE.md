# 取得元

- リポジトリ: https://github.com/ykwyuta/yyeditor
- コミット: `5d2dbfc5859afab33791a67a2260907ee4712543`
- 取得日: 2026-10-26
- 主な取得対象: `demo/yydbmanager/compose.yaml`, `docker/`, `init/`, `sql/`, `tools/generate.py`

既存の5種類のDBの初期化・永続化・準備確認と受注サンプルを基に、アプリ固有の依存を除きました。接続ユーザー・DB名・データセット識別子・パスワード・ポートをDatabaseLaboratory用に変更し、SQL Serverのサーバー権限付与をmaster上で実行するよう修正しています。

MariaDB・MongoDB・Redis・ClickHouse・AlloyDB Omni・Spanner Emulator、共通操作・検証ツール、オフライン検証とCIを追加しました。SQLite / DuckDBは生成SQLから各利用者の出力先に作成します。取得元アプリの実行ファイル・クレート・設定ファイルを必要としません。

イメージ・初期化方式の参照先:

- https://hub.docker.com/_/postgres
- https://hub.docker.com/_/mysql
- https://mariadb.com/docs/server/server-management/automated-mariadb-deployment-and-administration/docker-and-mariadb/using-healthcheck-sh
- https://learn.microsoft.com/en-us/sql/linux/containers/configure
- https://github.com/oracle/docker-images/tree/main/OracleDatabase/SingleInstance
- https://www.ibm.com/docs/en/db2/12.1.0?topic=system-linux
- https://hub.docker.com/_/mongo
- https://hub.docker.com/_/redis
- https://github.com/ClickHouse/ClickHouse/blob/master/docker/server/README.src/content.md
- https://docs.cloud.google.com/alloydb/omni/containers/17.9.0/docs/deploy-vm
- https://docs.cloud.google.com/spanner/docs/emulator
