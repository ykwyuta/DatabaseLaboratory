# SQL Server — 運用観点の情報取得方法

[DB別目次](README.md) · [全体目次](../README.md)

対象: SQL Server 2022 Developer / Linux / 確認日: 2026-10-26

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

@@VERSION、SERVERPROPERTY、sys.databasesのcompatibility_level/recovery_model_descを取得します。OS、CU、edition、DBオプションをセットで記録します。

<a id="section-2"></a>

## セッション・処理・ロック

sys.dm_exec_sessions/requests、dm_tran_locks、dm_os_waiting_tasksで接続と待機を確認します。2022では用途に応じVIEW SERVER PERFORMANCE STATE等の監視権限が必要です。

<a id="section-3"></a>

## 容量・ログ・保持期間

sys.database_files、dm_db_log_space_usage、tempdb使用量、ログ再利用待ち理由を採取します。データ増加とログバックアップ不足、CDC/AG遅延によるログ保持を分けます。

<a id="section-4"></a>

## メタデータ・権限・セキュリティ

sys.tables/columns/indexes/foreign_keys、sys.database_permissions、server/database principalを収集します。saは日常監視に使わず、master権限とユーザーDB権限を区別します。

<a id="section-5"></a>

## 定期取得と障害時の採取順序

接続/待機→SQLとplan handle→Query Store→tempdb/IO/ログ→errorlogとExtended Eventsの順に保存します。再起動やキャッシュ退去で消える情報を優先します。

<a id="examples"></a>

## 確認用の例と検証手順

```sql
SELECT @@VERSION;
SELECT session_id,status,wait_type,blocking_session_id FROM sys.dm_exec_requests;
SELECT name,recovery_model_desc,log_reuse_wait_desc FROM sys.databases;
```

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: 単体Developer版。Always On・SQL Server AgentのCDCジョブは未構成。

[動的管理ビュー](https://learn.microsoft.com/en-us/sql/relational-databases/system-dynamic-management-views/system-dynamic-management-views?view=sql-server-ver16)
