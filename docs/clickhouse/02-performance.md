# ClickHouse — 性能分析手法

[DB別目次](README.md) · [全体目次](../README.md)

対象: ClickHouse 25.8 / MergeTree / 確認日: 2026-10-26

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

max_threads、メモリ上限、part数、merge進行、cache、入力列数を記録します。バックグラウンドmergeが測定中に影響するため複数回比較します。

<a id="section-2"></a>

## 実行計画の取得と読み方

EXPLAIN indexes=1とPIPELINEで絞り込みと並列処理を確認します。selected parts/granulesとread_rows/read_bytesを見て、返却行数だけで評価しません。

<a id="section-3"></a>

## SQL統計とボトルネックの特定

system.query_logのQueryFinishをquery_idで対応させ、query_duration_ms/read_rows/read_bytes/memory_usage/ProfileEventsを保存します。logは非同期で反映される点を考慮します。

<a id="section-4"></a>

## ロックと待機の分析

system.processes、merges、mutations、replication_queueで現在の処理を確認します。mutation未完了、merge過多、replica遅延をSQLのscan時間と分けます。

<a id="section-5"></a>

## 資源と改善効果の確認

system.parts/disks/metrics/asynchronous_metricsでpart増加、空き、memoryを確認します。ORDER BY変更やbatch INSERTで読取量とmergeコストがどう変わるか測定します。

<a id="examples"></a>

## 確認用の例と検証手順

```sql
EXPLAIN indexes=1 SELECT count() FROM events WHERE customer_id=1;
SELECT query_id,query_duration_ms,read_rows,read_bytes,memory_usage FROM system.query_log WHERE type='QueryFinish' ORDER BY event_time DESC LIMIT 10;
```
query_logの反映待ちと対象query_idを考慮します。

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: 単体MergeTree。Keeper、ReplicatedMergeTree、外部CDCは未構成。

[EXPLAIN](https://clickhouse.com/docs/sql-reference/statements/explain) · [query_log](https://clickhouse.com/docs/operations/system-tables/query_log)
