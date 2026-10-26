# SQL Server — 性能分析手法

[DB別目次](README.md) · [全体目次](../README.md)

対象: SQL Server 2022 Developer / Linux / 確認日: 2026-10-26

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

互換性レベル、SETオプション、bind型、MAXDOP、メモリ上限、統計をそろえます。計画キャッシュを消して測定する操作は共有検証環境で無断実行しません。

<a id="section-2"></a>

## 実行計画の取得と読み方

推定計画はSHOWPLAN_XML、実測はSTATISTICS XMLまたはクライアントのactual planで取得します。estimated/actual rows、logical reads、CPU、memory grant、spill、並列性を比較します。

<a id="section-3"></a>

## SQL統計とボトルネックの特定

Query Storeは計画と実行/待機統計の履歴、dm_exec_query_statsはキャッシュ内の累積値です。計画退行を時系列で追い、plan forcingは原因分析と解除条件を用意してから検討します。

<a id="section-4"></a>

## ロックと待機の分析

dm_exec_requestsのblocking_session_id/wait_typeとdm_os_waiting_tasksを使います。deadlockはExtended Eventsのグラフで解析し、LCK、PAGEIOLATCH、WRITELOG、メモリ待ちを区別します。

<a id="section-5"></a>

## 資源と改善効果の確認

STATISTICS IO/TIME、dm_io_virtual_file_stats、tempdb、ログ使用率を合わせます。並列化でCPUだけが増える場合やparameter別に計画が悪化する場合を再測定します。

<a id="examples"></a>

## 確認用の例と検証手順

```sql
SET STATISTICS IO ON;
SET STATISTICS TIME ON;
SELECT * FROM dbo.orders WHERE customer_id=24;
SET STATISTICS TIME OFF;
SET STATISTICS IO OFF;
```
実測計画は別途取得します。`sql/performance/sqlserver.sql` も参照してください。

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: 単体Developer版。Always On・SQL Server AgentのCDCジョブは未構成。

[Query Store](https://learn.microsoft.com/sql/relational-databases/performance/monitoring-performance-by-using-the-query-store) · [実行計画](https://learn.microsoft.com/en-us/sql/relational-databases/performance/execution-plans?view=sql-server-ver16)
