# データベース検証ドキュメント

確認日: 2026-10-26。DatabaseLaboratoryが扱う13種類を、同じ7観点で整理します。Composeの実測結果と、公式資料に基づく構成設計を区別します。

## 読み方

まず各DBの設計思想を読み、性能分析と運用情報取得で現状を把握し、SQL移植・バックアップ・冗長化・差分配信を目的別に参照してください。各DBの目次には配下の全章・節を掲載しています。

例示SQLは接続済みクライアントで実行します。`sql` / `javascript` / `text` のブロックはホストシェルのコマンドではありません。設定変更・バックアップ・復元・昇格・CDC作成は説明用の手順で、自動実行しません。権限や追加構成が必要な例は各章に記載します。

バックアップ例の `.local/` は利用者が作成する出力先です。事前にディレクトリを作り、毎回異なるファイル名を使用してください。復元は元DBを上書きせず隔離した別環境で行います。

「差分配信」は、更新ログやアプリケーションイベントを用いた変更データの継続配信を指します。物理レプリケーション、バックアップの増分/差分、アプリケーションCDCを分けて記述します。

## DB別の目次

| DB | 対象 | 現在のDatabaseLaboratory構成 |
| --- | --- | --- |
| [PostgreSQL](postgresql/README.md) | PostgreSQL 17 | 単体サーバー。pg_stat_statementsをプリロード。HA/論理配信は未構成。 |
| [MySQL](mysql/README.md) | MySQL 8.4 / InnoDB | 単体InnoDB。binlog/GTID/レプリカの設定は検証目的に合わせて追加。 |
| [MariaDB](mariadb/README.md) | MariaDB 11.4 / InnoDB | 単体サーバー。MySQLとは別のデータボリュームと初期化SQL。 |
| [SQL Server](sqlserver/README.md) | SQL Server 2022 Developer / Linux | 単体Developer版。Always On・SQL Server AgentのCDCジョブは未構成。 |
| [Oracle Database](oracle/README.md) | Oracle Free latest-lite / 実バージョンをV$VERSIONで確認 | 単体CDBとFREEPDB1。Data Guard/RAC/商用管理パックは構成しない。 |
| [IBM Db2](db2/README.md) | Db2 LUW Community 12.1.5.0 | 単体インスタンスdb2inst1とDBLAB DB。HADR/外部CDCは未構成。 |
| [MongoDB](mongodb/README.md) | MongoDB 8.0 / WiredTiger | 認証付きstandalone。replica set・change streams・分散transactionは未構成。 |
| [Redis](redis/README.md) | Redis 7.4 | 単体・認証あり・AOF有効。Sentinel/Cluster/永続CDC基盤は未構成。 |
| [ClickHouse](clickhouse/README.md) | ClickHouse 25.8 / MergeTree | 単体MergeTree。Keeper、ReplicatedMergeTree、外部CDCは未構成。 |
| [AlloyDB Omni](alloydb/README.md) | AlloyDB Omni 17.9.0 / PostgreSQL互換 | Omniサーバーと初期化用クライアント。マネージドAlloyDB/Operator/HAは未構成。 |
| [Google Cloud Spanner](spanner/README.md) | Spanner本番設計 / Emulator 1.5.41のGoogleSQLで機能検証 | インメモリエミュレーターとREST初期化。IAM/本番性能/本番HAは検証不可。 |
| [SQLite](sqlite/README.md) | 利用するPython/CLIに同梱されたSQLite 3 / sqlite_version()で確認 | Python標準ライブラリからローカルファイルを生成。サーバー/HA/CDC拡張は未構成。 |
| [DuckDB](duckdb/README.md) | インストールしたDuckDBの版 / version()で確認 | Python追加パッケージでローカルファイル生成。サーバー/HA/標準CDCなし。 |

## 共通の記録項目

| 観点 | 記録する内容 |
| --- | --- |
| 再現条件 | DB/クライアント/イメージの版、CPU、RAM、ディスク、設定、件数、索引、同時実行数 |
| 性能 | p50/p95/p99、スループット、エラー率、実行回数、CPU/IO/メモリ、待機、推定行数と実行行数 |
| 復旧 | 最終復元可能時刻、復元所要時間、ログ欠損、接続切り替え時間、件数/精度/制約の照合結果 |
| 差分 | 初期ロードの境界、保持期間、再開位置、遅延、重複、欠落、削除、スキーマ版 |

RPOは許容するデータ損失の時間、RTOは業務再開までの時間です。レプリカは誤更新も反映するため、バックアップの代わりにはなりません。

## 実装とドキュメントの境界

Composeは単体DBを起動する検証環境です。HAクラスタ、CDCブローカー、保管先、鍵管理、監視基盤は自動構築しません。これらの章は構成・検証の設計資料です。Spannerエミュレーターで本番性能・IAM・冗長化を評価しません。AlloyDB OmniとGoogle CloudのマネージドAlloyDBを混同しません。

[DB横断の比較表](comparison.md) · [実測記録](verification/README.md) · [検証環境の使い方](../README.md) · [取得元](../SOURCE.md)
