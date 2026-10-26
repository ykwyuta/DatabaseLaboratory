# DB横断の比較表

[総合目次](README.md)

対象の版と根拠となる公式資料は各DBの該当章を参照してください。ここでは設計上の違いを比較し、製品間の性能順位や全機能の互換性は示しません。

## 設計と実行モデル

| DB | 主な格納/実行モデル | 整合性・並行処理の着眼点 | 最初に見る性能情報 |
| --- | --- | --- | --- |
| [PostgreSQL](postgresql/01-design.md) | ヒープ+索引、MVCC、汎用RDBMS | 分離レベル、長いtransaction、VACUUM | EXPLAIN ANALYZE/BUFFERS、pg_stat_statements |
| [MySQL](mysql/01-design.md) | InnoDB、主キーによるクラスタ化 | RR、consistent/locking read、gap lock | EXPLAIN ANALYZE、Performance Schema |
| [MariaDB](mariadb/01-design.md) | InnoDB等、独自オプティマイザー | RR、engine/SQL mode差 | ANALYZE FORMAT=JSON、slow log |
| [SQL Server](sqlserver/01-design.md) | clustered/nonclustered、columnstore | locking RC、RCSI/SNAPSHOTの設定差 | actual plan、Query Store、wait stats |
| [Oracle](oracle/01-design.md) | CDB/PDB、redo/undo、汎用RDBMS | read consistency、undo保持、DDL commit | DBMS_XPLAN、V$SQL、V$SESSION |
| [Db2](db2/01-design.md) | instance/DB、package、buffer pool | UR/CS/RS/RR、UOWとlock escalation | EXPLAIN/db2exfmt、MON_GET_* |
| [MongoDB](mongodb/01-design.md) | BSON、WiredTiger、document | 単一document atomic、read/write concern | explain executionStats、currentOp、serverStatus |
| [Redis](redis/01-design.md) | メモリ上のキー/構造 | command atomic、TTL、eviction | SLOWLOG、INFO、LATENCY |
| [ClickHouse](clickhouse/01-design.md) | 列指向、MergeTree、part/merge | 非同期merge/mutation、重複/最新状態 | EXPLAIN、query_log、parts/merges |
| [AlloyDB Omni](alloydb/01-design.md) | PostgreSQL系の行処理+列指向 | 行/列メモリ、対応拡張、単体自己管理 | EXPLAIN、pg_stat_*、列指向設定 |
| [Spanner](spanner/01-design.md) | 分散key range、合意による複製 | 強整合性、transaction再試行、hotspot | 本番plan、SPANNER_SYS、Cloud Monitoring |
| [SQLite](sqlite/01-design.md) | embedded B-tree、ファイル | 単一writer、WAL、BUSY | EXPLAIN QUERY PLAN、PRAGMA、アプリ計測 |
| [DuckDB](duckdb/01-design.md) | embedded列指向、vectorized | 単一writerプロセス、楽観的競合 | EXPLAIN ANALYZE、profile、memory/spill |

## SQL移植で最初に比較する項目

| DB | ページング | 採番/変更行取得 | NULL/型での主な差 |
| --- | --- | --- | --- |
| PostgreSQL | LIMIT/OFFSET | IDENTITY/SEQUENCE、RETURNING | NUMERIC、JSONB、TIMESTAMPTZ、空文字≠NULL |
| MySQL | LIMIT/OFFSET | AUTO_INCREMENT、接続単位のID取得 | BOOLEANは別名、binary JSON、SQL mode |
| MariaDB | LIMIT/OFFSET | AUTO_INCREMENT/SEQUENCE、対応RETURNING | JSONはLONGTEXTの別名、MySQLとの関数差 |
| SQL Server | TOP / OFFSET FETCH | IDENTITY/SEQUENCE、OUTPUT | Nリテラル/NVARCHAR、DECIMALと指数FLOAT |
| Oracle | OFFSET FETCH | SEQUENCE/IDENTITY、RETURNING INTO | 空文字=NULL、DATEに時刻、NUMBER |
| Db2 | OFFSET FETCH | IDENTITY/SEQUENCE、FINAL TABLE等 | DECIMAL 31桁、schemaの大文字化 |
| MongoDB | sort/skip/limit、key範囲 | _id、findOneAndUpdate | BSON、nullと属性欠落、SQL APIではない |
| Redis | SCAN/構造ごとの範囲 | INCR等 | nil/未存在、空文字、64bit整数とLua精度 |
| ClickHouse | LIMIT/OFFSET | sourceで生成/追記、engineごとの置換 | Nullable、unsigned、JOIN未一致の既定値 |
| AlloyDB Omni | PostgreSQL相当 | PostgreSQL相当 | Google拡張や列指向対応は別確認 |
| Spanner GoogleSQL | LIMIT/OFFSET | mutation/対応SQLとsequenceを選定 | INT64/NUMERIC/ARRAY/STRUCT、REST型表現 |
| SQLite | LIMIT/OFFSET | INTEGER PRIMARY KEY、対応RETURNING | affinity、DECIMAL精度は宣言だけで保証しない |
| DuckDB | LIMIT/OFFSET | SEQUENCE/対応DML | DECIMAL演算の戻り型、LIST/STRUCT、cast差 |

同じ列名・同じ件数でも、丸め、NULL、時刻帯、照合順序、文字数/バイト数、暗黙cast、DDLのCOMMIT境界を比較します。詳細は各DBの `03-sql.md` にあります。

## 保護・可用性・差分配信

| DB | バックアップ/復旧 | 主な冗長化 | 行変更配信/差分 |
| --- | --- | --- | --- |
| PostgreSQL | pg_dump、物理base+WAL、PITR | streaming standby+昇格管理 | logical decoding、publication/subscription |
| MySQL | mysqldump、対応物理backup、binlog PITR | source/replica、Group Replication | ROW binlog、GTID/座標 |
| MariaDB | mariadb-dump、mariadb-backup、binlog | 標準replication、Galera | MariaDB binlog/GTID。MySQLと同一視しない |
| SQL Server | full/differential/log、復旧モデル | AG/FCI、OS/cluster設計 | CDC、CT、transactional replicationを区別 |
| Oracle | Data Pump、RMAN+archivelog | Data Guard/RAC、対応editionが必要 | LogMiner等、SCN、supplemental logging |
| Db2 | BACKUP/RESTORE/ROLLFORWARD | HADR、同期modeとcluster管理 | SQL/Q Replication等、ログ拡張とcapture/apply |
| MongoDB | BSON dump、整合snapshot+oplog等 | replica set、shardごとの複製 | change stream、resume token、oplog window |
| Redis | RDB/AOF、外部保管 | replica+Sentinel、Cluster | 通知は欠落あり。Streams/outboxを別設計 |
| ClickHouse | native BACKUP、part差分とbase保持 | ReplicatedMergeTree+Keeper | 主に外部CDCのsink、version/deleteの適用 |
| AlloyDB Omni | dump、Omni対応Barman/pgBackRest+WAL | 対応するOmni HA/DR構成 | 対応logical replication、slot/LSN |
| Spanner | サービスbackup/PITR/export | regional/multi-region構成 | change streams、partition/record/checkpoint |
| SQLite | Backup API/.backup/VACUUM INTO | アプリ/外部の所有権・複製設計 | session changeset、outbox等。標準配信サーバーなし |
| DuckDB | EXPORT/IMPORT、一貫した停止時コピー | アプリ/ジョブ/immutable世代配布 | source CDC→delta適用。nativeの汎用CDCを仮定しない |

物理レプリケーションは誤削除も複製します。復旧用バックアップは独立した保管先と復旧時点を持ちます。CDCはさらに初期snapshot境界、再開offset、重複/削除、schema変更、配信先の冪等性が必要です。

## 比較試験の進め方

1. バージョン・文字コード・timezone・分離レベル・データ件数・索引を固定する。
2. 接続、境界値、NULL、集計、更新、DDL rollbackの結果をDB別に記録する。
3. 同じ業務要求に対する最適なSQLを用意し、計画・scan量・待機・p95/p99を採取する。
4. 別環境へバックアップ復元し、アプリケーションが再開できるまでを測る。
5. 冗長化環境で停止/分断/遅延を試し、確定済みの書込みと二重writer防止を確認する。
6. CDCの停止/再送/順序逆転/DELETE/DDL/ログ保持超過で、配信先とsourceを突合する。

DatabaseLaboratoryの単体Composeで確認済みなのは、起動、初期投入、基本SQL/型とfixtureの照合です。複数ノードのHA、バックアップからの実復元、外部CDCの配信保証は、追加構成で実施する試験として記録してください。
