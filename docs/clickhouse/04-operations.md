# ClickHouse — 運用観点の情報取得方法

[DB別目次](README.md) · [全体目次](../README.md)

対象: ClickHouse 25.8 / MergeTree / 確認日: 2026-10-26

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

version()、system.settings、SHOW CREATE TABLE、system.build_optionsを記録します。serverの設定とsession/query設定を分けます。

<a id="section-2"></a>

## セッション・処理・ロック

system.processes、query_log、part_logで現在処理と履歴を確認します。監視権限とKILL/MUTATION等の変更権限を分離します。

<a id="section-3"></a>

## 容量・ログ・保持期間

system.parts、disks、merges、mutations、detached_partsで容量と未処理を確認します。active partだけでなくdetached/一時backupも容量へ含めます。

<a id="section-4"></a>

## メタデータ・権限・セキュリティ

system.tables/columns/users/roles/grantsで定義とRBACを収集します。接続口HTTP/native、TLS、ユーザープロファイル、quota、行policyを管理します。

<a id="section-5"></a>

## 定期取得と障害時の採取順序

query_idとerror→実行中→read量/メモリ→part/merge/mutation→ディスク/ログの順に採取します。systemログ自体のTTL・保持容量も設定します。

<a id="examples"></a>

## 確認用の例と検証手順

```sql
SELECT version();
SELECT database,table,count(),sum(bytes_on_disk) FROM system.parts WHERE active GROUP BY database,table;
SELECT * FROM system.mutations WHERE NOT is_done;
```

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: 単体MergeTree。Keeper、ReplicatedMergeTree、外部CDCは未構成。

[system tables](https://clickhouse.com/docs/operations/system-tables)
