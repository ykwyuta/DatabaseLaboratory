# MySQL — 運用観点の情報取得方法

[DB別目次](README.md) · [全体目次](../README.md)

対象: MySQL 8.4 / InnoDB / 確認日: 2026-10-26

## この章の目次

- [接続先・バージョン・設定](#section-1)
- [セッション・処理・ロック](#section-2)
- [容量・ログ・保持期間](#section-3)
- [メタデータ・権限・セキュリティ](#section-4)
- [定期取得と障害時の採取順序](#section-5)
- [確認用の例と検証手順](#examples)
- [公式資料と適用範囲](#sources)

<a id="section-1"></a>

## 接続先・バージョン・設定

VERSION()、@@sql_mode、@@transaction_isolation、@@character_set_server、@@collation_serverを収集します。コンテナーの版とMySQL実体の版を別に記録します。

<a id="section-2"></a>

## セッション・処理・ロック

SHOW PROCESSLIST、performance_schema.threads、events_statements_current、data_lock_waitsを取得します。監視権限はPROCESSや対象ビューへのSELECTに分けて付与します。

<a id="section-3"></a>

## 容量・ログ・保持期間

information_schema.tablesのサイズは見積もりとして扱い、実ファイル・redo・binlog容量を併記します。binlog_expire_logs_secondsと配信先の遅延を比較し、保持期限の超過を検知します。

<a id="section-4"></a>

## メタデータ・権限・セキュリティ

information_schemaで表・列・制約、SHOW CREATE TABLEで実DDL、SHOW GRANTSで権限を確認します。アプリ用アカウントと管理用rootを分け、ホスト制限とTLSを点検します。

<a id="section-5"></a>

## 定期取得と障害時の採取順序

接続枯渇→ロック待ち→高負荷digest→IO/redo→ログの順に採取します。再起動・FLUSH/RESETで消える統計を先に保存し、監視自体の全表走査を避けます。

<a id="examples"></a>

## 確認用の例と検証手順

```sql
SELECT VERSION(),@@sql_mode,@@character_set_server;
SHOW GLOBAL STATUS LIKE 'Threads_connected';
SELECT * FROM performance_schema.data_lock_waits;
```
追加例は `sql/performance/mysql.sql` を参照します。

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: 単体InnoDB。binlog/GTID/レプリカの設定は検証目的に合わせて追加。

[sys schema](https://dev.mysql.com/doc/refman/8.4/en/sys-schema.html) · [Server status](https://dev.mysql.com/doc/refman/8.4/en/server-status-variables.html)
