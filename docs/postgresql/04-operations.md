# PostgreSQL — 運用観点の情報取得方法

[DB別目次](README.md) · [全体目次](../README.md)

対象: PostgreSQL 17 / 確認日: 2026-10-26

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

SELECT version()、SHOW server_version、pg_settingsで実効設定と設定元を確認します。pg_conf_load_time()、postmaster開始時刻、拡張の版を記録します。

<a id="section-2"></a>

## セッション・処理・ロック

pg_stat_activity・pg_locks・pg_blocking_pidsで接続数、長時間SQL、idle in transactionを追跡します。監視ユーザーには必要に応じpg_read_all_stats等を付与し、不要なsuperuserを避けます。

<a id="section-3"></a>

## 容量・ログ・保持期間

pg_database_size、pg_total_relation_size、WALディレクトリ容量、replication slotのrestart_lsnを確認します。autovacuum遅延・dead tuples・凍結年齢・WALアーカイブ失敗は容量事故の前兆です。

<a id="section-4"></a>

## メタデータ・権限・セキュリティ

information_schemaとpg_catalogを使い分け、pg_roles、pg_auth_members、テーブル権限を収集します。接続許可はpg_hba.confとTLS設定で別に管理します。

<a id="section-5"></a>

## 定期取得と障害時の採取順序

障害時は時刻→接続/待機→SQL統計→サイズ/WAL→サーバーログ→OS資源の順に取得します。監視で統計リセットや重い全表走査を行わず、収集間隔と保存期間を固定します。

<a id="examples"></a>

## 確認用の例と検証手順

```sql
SELECT version();
SELECT pid,state,wait_event_type,wait_event,pg_blocking_pids(pid)
FROM pg_stat_activity WHERE datname=current_database();
SELECT pg_size_pretty(pg_database_size(current_database()));
```
詳しい読み取り例は `sql/performance/postgres.sql` にあります。

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: 単体サーバー。pg_stat_statementsをプリロード。HA/論理配信は未構成。

[統計情報](https://www.postgresql.org/docs/17/monitoring-stats.html) · [運用設定](https://www.postgresql.org/docs/17/runtime-config.html)
