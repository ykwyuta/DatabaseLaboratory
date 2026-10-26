# Rava

汎用的なデータベース検証環境。アプリケーションや特定のドライバーに依存せず、接続、SQLの互換性、型・精度、制約、実行計画、インポート・エクスポートを試すためのプロジェクトです。

DBごとの設計思想・性能分析・SQL差異・運用・バックアップ・冗長化・差分配信は、[ドキュメント総合目次](docs/README.md)から参照できます。13種類それぞれに7章と詳細目次を用意しています。

Docker Composeで必要なDBだけを起動し、初期データ投入とヘルスチェックまで自動で行います。Windows / Linux / macOSで同じComposeを使えます。Docker DesktopではLinuxコンテナーを使用してください。SQL Server・Db2・AlloyDB Omniなどはamd64環境を推奨し、各イメージの対応CPUと利用条件に従います。

## 起動

Dockerと `docker compose up --wait` に対応したCompose v2以降が必要です。リポジトリのルートで実行します。

```sh
# 既定はPostgreSQLだけ。初期データ投入まで待つ
docker compose up -d --wait --wait-timeout 180

# 指定したDBだけ（PostgreSQLは追加起動されない）
docker compose up -d --wait --wait-timeout 1200 mysql mariadb
docker compose up -d --wait --wait-timeout 1200 alloydb spanner

# 全DB。メモリ・ディスクに余裕のある環境で実行
docker compose --profile "*" up -d --wait --wait-timeout 1200
```

各追加DBには同名のプロファイルがあります。`docker compose --profile mysql up -d --wait` なら既定のPostgreSQLも起動します。初回のイメージ取得・Oracle / Db2のDB作成には数分以上かかることがあります。

Python 3.10以降があれば、標準ライブラリだけの共通ツールも使えます。実行ディレクトリに依存せず、選択したDBだけを起動します。

```sh
python tools/rava.py up                      # PostgreSQL
python tools/rava.py up mysql mariadb        # 選択起動
python tools/rava.py up alloydb spanner
python tools/rava.py up all                  # 全DB
python tools/rava.py status
python tools/rava.py verify                  # 起動中のDBを検証
python tools/rava.py verify postgres mysql   # 指定DBを検証
python tools/rava.py logs spanner
python tools/rava.py stop                    # データを残して全DB停止
python tools/rava.py down                    # コンテナー削除、ボリューム保持
```

## 接続先

すべてホスト `127.0.0.1`、パスワード `Rava_Test_2026!`。ローカル検証専用の公開された固定資格情報です。TLSや本番向けの権限分離は設定していません。既存のyyeditorデモとはポート・Composeプロジェクト・ボリュームを分けています。

| DB / サービス・プロファイル | イメージ | ポート | DB / サービス | ユーザー |
| --- | --- | ---: | --- | --- |
| PostgreSQL / `postgres`（既定） | `postgres:17-alpine` | 35432 | rava | rava |
| MySQL / `mysql` | `mysql:8.4` | 33306 | rava | rava |
| MariaDB / `mariadb` | `mariadb:11.4` | 33307 | rava | rava |
| SQL Server / `sqlserver` | `mcr.microsoft.com/mssql/server:2022-latest` | 31433 | rava | rava（管理者 sa） |
| Oracle Free / `oracle` | `container-registry.oracle.com/database/free:latest-lite` | 31521 | FREEPDB1 | rava |
| Db2 Community / `db2` | `icr.io/db2_community/db2:12.1.5.0` | 35000 | RAVA | db2inst1 |
| MongoDB / `mongo` | `mongo:8.0` | 37017 | rava（authSource=admin） | rava |
| Redis / `redis` | `redis:7.4-alpine` | 36379 | DB 0 | default |
| ClickHouse / `clickhouse` | `clickhouse/clickhouse-server:25.8` | 38123 HTTP / 39000 Native | rava | rava |
| AlloyDB Omni / `alloydb` | `google/alloydbomni:17.9.0` | 35433 | rava | rava（管理者 postgres） |
| Spanner Emulator / `spanner` | `gcr.io/cloud-spanner-emulator/emulator:1.5.41` | 39010 gRPC / 39020 REST | 下記 | 認証なし |

例：PostgreSQLは `postgresql://rava:Rava_Test_2026!@127.0.0.1:35432/rava`、AlloyDB Omniは同じ形式でポート35433。MongoDBは `mongodb://rava:Rava_Test_2026!@127.0.0.1:37017/rava?authSource=admin`。

ポートが競合したら `.env.example` を `.env` にコピーし、`RAVA_*_PORT` を変更してください。Composeの再実行で反映します。資格情報は初期化SQLと合わせて固定しているため、`.env` でのパスワード変更には対応しません。並行した別環境は `docker compose -p rava-other ...` または `.env` の `COMPOSE_PROJECT_NAME` と別ポートを使います。

SQL ServerはDeveloper版、OracleはFree、Db2はCommunity版です。Db2の公式イメージには `privileged: true` が必要で、初期化フックを追加してビルドします。Oracleの `latest-lite` など一部タグの内容は更新されるため、検証ツールは使用したイメージIDをレポートに記録します。

## GoogleのDB

AlloyDBは、Googleが提供するローカル実行用の **AlloyDB Omni** を使用します。サーバー `alloydb-server` と初期化・接続確認用の `alloydb` が連動します。PostgreSQLと共通の受注データを作成し、PostgreSQLプロトコルで接続できます。マネージドAlloyDBのクラスタ管理やIAMの検証は対象外です。[Google公式インストール手順](https://docs.cloud.google.com/alloydb/omni/containers/17.9.0/docs/deploy-vm)

Spannerは公式エミュレーターを使用します。Cloudアカウント・gcloud・認証情報は不要です。`spanner-emulator` がAPIを提供し、`spanner` がREST経由で初期化と継続した準備状態の確認を行います。

| 項目 | 値 |
| --- | --- |
| Project | `rava-local` |
| Instance | `rava` |
| Database / SQL方言 | `rava` / GoogleSQL |
| リソース名 | `projects/rava-local/instances/rava/databases/rava` |
| SDK設定（PowerShell） | `$env:SPANNER_EMULATOR_HOST = '127.0.0.1:39010'` |
| SDK設定（sh） | `export SPANNER_EMULATOR_HOST=127.0.0.1:39010` |
| Compose内の接続先 | `spanner-emulator:9010` |

Spannerはインメモリで、**停止・再起動時に変更データが消えます**。起動中の初期化サービスがサンプルを再作成します。IAM・TLS・本番性能・分散処理の特性・実行計画はエミュレーターで検証できません。この構成はGoogleSQLを準備し、PostgreSQL方言やPGAdapterは含めません。[Google公式エミュレーター仕様](https://docs.cloud.google.com/spanner/docs/emulator)

## データと検証

PostgreSQL / MySQL / MariaDB / SQL Server / Oracle / Db2 / AlloyDB Omni、およびローカル生成するSQLite / DuckDBは共通の受注モデルです。

| テーブル | 件数 | 主な確認点 |
| --- | ---: | --- |
| departments | 3 | 日本語 |
| employees | 8 | FK、上司への自己参照、NULL |
| customers | 24 | 一意制約、NULL |
| products | 8 | 金額、有効フラグ |
| orders | 1200 | 顧客1への900件の偏り、日付、索引 |
| order_items | 3600 | 複合主キー、FK |
| support_tickets | 6 | 物理FKのない顧客コードの関係 |
| exact_values | 3 | BIGINT境界、2^53超の整数、DECIMAL(31,8)、空文字・NULL |
| demo_ready | 1 | 初期データのバージョン `rava-v1` |

`customer_sales` ビューも作成します。SQLiteの大きな小数は精度保持のためTEXT、Oracleの空文字はNULLになります。

`sql/00-verify-counts.sql` は件数照合、`01`～`04` は結合・集計・索引選択性・精度・論理関係のサンプルです。`sql/performance/` はDB固有の性能分析、`sql/plan-files/` は実行計画取得例です。サンプルはSQL方言による違いを確認しながら実行してください。

MongoDBは顧客3件・受注1200件・ネスト・配列・索引・Int64・Decimal128、ClickHouseはイベント1200件・MergeTree・Nullable・Decimalを用意します。Spannerは顧客3件・受注1200件・FK・索引・INT64・NUMERICを用意します。これらは共通SQLモデルとは別のデータセットです。

Redisは空のDBから始めます。検証ではランダムな専用キーで文字列・Hash・List・Set・Sorted Set・TTLを確認し、キーを削除します。他のDBの検証は読み取り専用です。

```sh
python tools/rava.py verify
```

全RDBMSの件数・日本語・整数/小数精度・偏り・ビューと共通サンプル実行、MongoDB / ClickHouse / Spannerの件数・数値精度を検証します。`reports/verification.json` に時刻・イメージID・成功/失敗を保存し、失敗時は非ゼロで終了します。DB固有の性能分析SQLは自動検証に含めません。サーバーの `healthy` は投入完了を表し、より詳しい確認には `verify` を実行します。RedisのhealthyはPING成功を表します。

`data/import_sample.{csv,tsv,psv}` は同じ5行を収録し、引用符・カンマ・改行・タブ・空文字・NULLマーカー `\N` の入出力検証に使えます。固定長データとCOBOLコピー句もあります。

## Docker不要のSQLite / DuckDB

```sh
python tools/rava.py local sqlite --output .local/rava.sqlite
# DuckDBのみ、任意のPython環境へ pip install duckdb を先に実行
python tools/rava.py local duckdb --output .local/rava.duckdb
```

既存ファイルは上書きしません。SQLiteはPython標準ライブラリで作れます。DuckDBの追加パッケージはこの機能だけで使用します。

## 停止・再開・初期化

```sh
docker compose --profile "*" stop
docker compose up -d --wait                    # PostgreSQL再開
docker compose --profile "*" ps -a
docker compose logs --tail 100 postgres
docker compose --profile "*" down             # ボリューム保持
```

Spanner以外は専用の名前付きボリュームに永続化し、初期投入は一度だけ行います。データを消して最初から検証する場合に限り、次を実行します。**Ravaの全DB・全ボリュームを削除します。**

```sh
python tools/rava.py reset --yes
# または docker compose --profile "*" down -v
```

初期化SQLの変更は既存ボリュームには反映されません。初期化失敗時はログの原因を解消してから対象環境を再作成してください。単に接続できない場合は、まず `status` と `logs`、ポート競合、Dockerのメモリ・空きディスクを確認します。

## 開発・拡張

```sh
python tools/generate.py                     # 共通SQLとファイル入出力データを再生成
python -m unittest discover -s tests -v       # Docker不要の検証
docker compose --profile "*" config --quiet  # 全プロファイルの構文確認
```

`init/` が投入SQL、`docker/` が起動・準備確認、`sql/` が利用者向けクエリー、`tools/rava.py` が操作と検証です。新しいDBはプロファイル・localhostの専用ポート・永続化・投入完了のヘルスチェックを追加し、検証ツールと接続表を更新してください。

GitHub Actionsはオフライン検証と主要8種類のDBの起動・検証を行います。Oracle / Db2 / AlloyDB Omniはリソース消費が大きいため手動実行で選べます。

この環境は [yyeditor](https://github.com/ykwyuta/yyeditor) のCompose・初期データ・SQLを取り出して汎用化しました。取得元と変更点は [SOURCE.md](SOURCE.md) を参照してください。
