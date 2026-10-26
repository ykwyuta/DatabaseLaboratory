# AlloyDB Omni — 運用観点の情報取得方法

[DB別目次](README.md) · [全体目次](../README.md)

対象: AlloyDB Omni 17.9.0 / PostgreSQL互換 / 確認日: 2026-10-26

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

version()、pg_settings、pg_extensionを収集し、Omniイメージタグ・PostgreSQLベース版・Google拡張を区別します。container構成とOperator管理構成の手順を分けます。

<a id="section-2"></a>

## セッション・処理・ロック

pg_stat_activity、blocking pid、必要なSQL統計で接続/処理を確認します。初期化サービスalloydbのhealthはサーバーへの問い合わせで、データサーバー本体はalloydb-serverです。

<a id="section-3"></a>

## 容量・ログ・保持期間

PGDATA、WAL、temporary、backup領域と列ストア関連のメモリを確認します。Dockerのmemory limitとshared memory上限を記録し、OOMとDB内メモリ待ちを区別します。

<a id="section-4"></a>

## メタデータ・権限・セキュリティ

PostgreSQL系catalog/roleに加えGoogle拡張の設定を台帳化します。マネージドサービスのIAMやCloud Monitoring自動統合が単体Omniにあると仮定しません。

<a id="section-5"></a>

## 定期取得と障害時の採取順序

接続/待機→SQL/plan→行/列メモリ→WAL/ディスク→alloydb-serverログを採取します。拡張列ストアの状態と設定変更履歴を性能記録へ添付します。

<a id="examples"></a>

## 確認用の例と検証手順

```sql
SELECT pid,state,wait_event_type,wait_event,pg_blocking_pids(pid) FROM pg_stat_activity;
SELECT pg_size_pretty(pg_database_size(current_database()));
```
サーバーログは `python tools/dblab.py logs alloydb` で取得します。

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: Omniサーバーと初期化用クライアント。マネージドAlloyDB/Operator/HAは未構成。

[Omni運用概要](https://docs.cloud.google.com/alloydb/omni/containers/17.9.0/docs/overview) · [PostgreSQL監視](https://www.postgresql.org/docs/17/monitoring-stats.html)
