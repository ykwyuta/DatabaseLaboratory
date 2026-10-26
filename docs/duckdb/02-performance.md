# DuckDB — 性能分析手法

[DB別目次](README.md) · [全体目次](../README.md)

対象: インストールしたDuckDBの版 / version()で確認 / 確認日: 2026-10-26

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

threads、memory_limit、temp_directory、DuckDB/extension版、ファイル形式とcache条件を記録します。ホストPythonの処理・変換時間とDB内実行を分けます。

<a id="section-2"></a>

## 実行計画の取得と読み方

EXPLAINで推定、EXPLAIN ANALYZEでoperator別の実行時間・cardinalityを見ます。並列operatorの累積時間とwall clockは一致しない場合があり、単純合計で比較しません。

<a id="section-3"></a>

## SQL統計とボトルネックの特定

profilingのJSON出力などでoperator・CPU・scanを記録します。サーバー型の全session累積DMVを前提にせず、接続/クエリー単位のprofileをアプリのログへ結びます。

<a id="section-4"></a>

## ロックと待機の分析

楽観的競合、file lock、長いquery、memory不足を区別します。一般RDBMSの行lock waiter一覧を期待せず、例外とアプリthread/processの状態を採取します。

<a id="section-5"></a>

## 資源と改善効果の確認

duckdb_memory()/temporary_files()/settingsでメモリ・spill・threadsを確認します。列projectionとfilter pushdown、Parquet row group、join/aggregateのメモリ使用を比較します。

<a id="examples"></a>

## 確認用の例と検証手順

```sql
EXPLAIN ANALYZE SELECT customer_id,sum(total_amount) FROM orders GROUP BY customer_id;
SELECT * FROM duckdb_memory();
```
追加例は `sql/performance/duckdb.sql` を参照します。

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: Python追加パッケージでローカルファイル生成。サーバー/HA/標準CDCなし。

[EXPLAIN ANALYZE](https://duckdb.org/docs/stable/guides/meta/explain_analyze) · [profiling](https://duckdb.org/docs/stable/configuration/pragmas#profiling)
