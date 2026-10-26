# IBM Db2 — 運用観点の情報取得方法

[DB別目次](README.md) · [全体目次](../README.md)

対象: Db2 LUW Community 12.1.5.0 / 確認日: 2026-10-26

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

db2level、GET DBM CFG、GET DB CFG、CURRENT SERVER/SCHEMAを収集します。instance環境とDB設定の変更反映条件を確認します。

<a id="section-2"></a>

## セッション・処理・ロック

MON_GET_CONNECTION/UNIT_OF_WORK、MON_GET_APPL_LOCKWAIT、db2pd -applications/-locksで確認します。SYSADM常用を避け、必要なMONITOR/SELECT系権限を設計します。

<a id="section-3"></a>

## 容量・ログ・保持期間

tablespace容量、log used、log archiveの成否、active log保持、temporary tablespaceを監視します。未完了UOWやHADR/CDCがログ削除を妨げる条件を確認します。

<a id="section-4"></a>

## メタデータ・権限・セキュリティ

SYSCAT.TABLES/COLUMNS/INDEXES/REFERENCES、SYSCAT.TABAUTH等を収集します。Db2 instance ownerはOSユーザーとも関係するためOSの認証・権限も台帳に含めます。

<a id="section-5"></a>

## 定期取得と障害時の採取順序

接続/UOW→待機→package統計→tablespace/log→db2diag.logの順に取得します。MON関数の対象member=-1/-2の意味をそろえて差分を保存します。

<a id="examples"></a>

## 確認用の例と検証手順

```text
db2level
db2 get db cfg for DBLAB
db2pd -db DBLAB -applications
```
container内のinstance ownerで実行します。SQL例は `sql/performance/db2.sql` を参照します。

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: 単体インスタンスdb2inst1とDBLAB DB。HADR/外部CDCは未構成。

[監視](https://www.ibm.com/docs/en/db2/12.1.x?topic=performance-monitoring-database)
