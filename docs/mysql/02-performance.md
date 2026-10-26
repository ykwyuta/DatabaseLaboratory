# MySQL — 性能分析手法

[DB別目次](README.md) · [全体目次](../README.md)

対象: MySQL 8.4 / InnoDB / 確認日: 2026-10-26

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

取得するSQL・bind値・同時接続数・buffer poolサイズを固定します。クライアント返却時間とサーバー実行時間を分け、DDLやANALYZE TABLEの実施を記録します。

<a id="section-2"></a>

## 実行計画の取得と読み方

EXPLAIN FORMAT=JSONでアクセス経路、EXPLAIN ANALYZEで実行行数・loopsを取得します。MySQL 8.4の実測計画はTREE形式を基本とし、JSON形式の推定計画と同一構造とは扱いません。

<a id="section-3"></a>

## SQL統計とボトルネックの特定

events_statements_summary_by_digestやsys.statement_analysisで累積時間・実行回数・走査行数を見ます。digestにまとめられたSQLではbind値の選択性差も別に測ります。

<a id="section-4"></a>

## ロックと待機の分析

performance_schema.data_locks/data_lock_waitsとsys.innodb_lock_waitsでブロック元を確認します。メタデータロック、行ロック、IO待ちを区別し、長いトランザクションを特定します。

<a id="section-5"></a>

## 資源と改善効果の確認

InnoDB buffer pool hit、redoの待ち、temp table、fsync、ディスク空きを確認します。Slow query logとPerformance Schemaのオーバーヘッドを測り、閾値を定めて使います。

<a id="examples"></a>

## 確認用の例と検証手順

```sql
EXPLAIN FORMAT=JSON SELECT * FROM orders WHERE customer_id=24;
EXPLAIN ANALYZE SELECT * FROM orders WHERE customer_id=24;
SELECT DIGEST_TEXT,COUNT_STAR,SUM_TIMER_WAIT FROM performance_schema.events_statements_summary_by_digest ORDER BY SUM_TIMER_WAIT DESC LIMIT 10;
```
タイマー単位を確認し、差分値で比較します。

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: 単体InnoDB。binlog/GTID/レプリカの設定は検証目的に合わせて追加。

[EXPLAIN ANALYZE](https://dev.mysql.com/doc/refman/8.4/en/explain.html) · [Performance Schema](https://dev.mysql.com/doc/refman/8.4/en/performance-schema.html)
