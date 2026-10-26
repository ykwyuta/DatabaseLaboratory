# PostgreSQL — 性能分析手法

[DB別目次](README.md) · [全体目次](../README.md)

対象: PostgreSQL 17 / 確認日: 2026-10-26

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

同一データ・設定・同時実行数で、初回とウォーム実行を分けます。単発の最速値ではなく遅延分布と処理件数を保存し、統計情報の更新時刻も記録します。

<a id="section-2"></a>

## 実行計画の取得と読み方

EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)で推定行数とactual rows、loops、shared hit/read、Sortのspillを確認します。ANALYZE付きは実際に文を実行するため、まず読み取りSELECTで比較します。

<a id="section-3"></a>

## SQL統計とボトルネックの特定

pg_stat_statementsでcalls・total_exec_time・mean_exec_time・rowsを比較し、総時間が大きいSQLを優先します。値は累積なので2時点の差分を使い、リセットや再起動を検出します。

<a id="section-4"></a>

## ロックと待機の分析

pg_stat_activityのwait_event_typeとwait_event、pg_blocking_pids(pid)で待機とブロック元を調べます。SQLの遅さとロック待ちを分離し、長いトランザクションの開始時刻を残します。

<a id="section-5"></a>

## 資源と改善効果の確認

pg_stat_database、pg_stat_io、pg_stat_walとOSのCPU/IO/ディスク空きを合わせます。索引追加後は実行時間だけでなく更新コストとWAL増加も再測定します。

<a id="examples"></a>

## 確認用の例と検証手順

```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)
SELECT * FROM orders WHERE customer_id=24;
SELECT queryid,calls,total_exec_time,rows FROM pg_stat_statements
ORDER BY total_exec_time DESC LIMIT 10;
```
顧客1にも同じSQLを実行し、推定行数・バッファ・計画を比較します。

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: 単体サーバー。pg_stat_statementsをプリロード。HA/論理配信は未構成。

[EXPLAIN](https://www.postgresql.org/docs/17/using-explain.html) · [pg_stat_statements](https://www.postgresql.org/docs/17/pgstatstatements.html)
