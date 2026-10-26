# MariaDB — 性能分析手法

[DB別目次](README.md) · [全体目次](../README.md)

対象: MariaDB 11.4 / InnoDB / 確認日: 2026-10-26

## この章の目次

- [測定条件と再現性](#section-1)
- [実行計画の取得と読み方](#section-2)
- [SQL統計とボトルネックの特定](#section-3)
- [ロックと待機の分析](#section-4)
- [資源と改善効果の確認](#section-5)
- [確認用の例と検証手順](#examples)
- [公式資料と適用範囲](#sources)

<a id="section-1"></a>

## 測定条件と再現性

接続・データ量・統計更新・buffer poolを固定して比較します。MySQLとの製品比較ではコンテナーの資源上限も同じにします。

<a id="section-2"></a>

## 実行計画の取得と読み方

EXPLAIN FORMAT=JSONは推定、ANALYZE FORMAT=JSONは実測です。r_rows、r_loops、r_total_time_msなどを参照し、MySQLのJSON計画フィールドと対応を決めてから可視化します。

<a id="section-3"></a>

## SQL統計とボトルネックの特定

slow query log、information_schema.PROCESSLIST、利用可能なPerformance Schemaのdigestを使います。performance_schemaの有効化と収集instrumentの設定を先に確認します。

<a id="section-4"></a>

## ロックと待機の分析

information_schema.INNODB_TRX/INNODB_LOCK_WAITSなど、対象版の表を使います。MySQL 8.4のdata_locks表をそのまま期待せず、行ロックとmetadata lockを分けます。

<a id="section-5"></a>

## 資源と改善効果の確認

buffer pool、undo/redo、temp、IO、ディスクを確認し、ANALYZE TABLEによる統計改善と索引変更の効果を別々に測ります。クエリーキャッシュの有無など構成差も記録します。

<a id="examples"></a>

## 確認用の例と検証手順

```sql
EXPLAIN FORMAT=JSON SELECT * FROM orders WHERE customer_id=24;
ANALYZE FORMAT=JSON SELECT * FROM orders WHERE customer_id=24;
```
ANALYZEはSELECTを実行します。推定rowsと実測r_rowsを比較します。

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: 単体サーバー。MySQLとは別のデータボリュームと初期化SQL。

[ANALYZE / EXPLAIN](https://mariadb.com/docs/server/reference/sql-statements/administrative-sql-statements/analyze-and-explain-statements)
