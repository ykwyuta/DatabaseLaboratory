# SQLite — 性能分析手法

[DB別目次](README.md) · [全体目次](../README.md)

対象: 利用するPython/CLIに同梱されたSQLite 3 / sqlite_version()で確認 / 確認日: 2026-10-26

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

ファイルサイズ、journal mode、synchronous、cache_size、SQLite版、compile optionsを記録します。単体処理と並行アクセスを分け、OS page cacheの温まりも考慮します。

<a id="section-2"></a>

## 実行計画の取得と読み方

EXPLAIN QUERY PLANでSCAN/SEARCH、covering index、一時B-treeを確認します。出力文字列は版で変わり得るため固定パーサーを前提にしません。これは実測行数の計画ではありません。

<a id="section-3"></a>

## SQL統計とボトルネックの特定

CLIの.timer/.stats、利用可能なsqlite3_stmt_status/scanstatus、アプリの処理時間を使います。全sessionの累積SQL統計を持つサーバーDMVはありません。

<a id="section-4"></a>

## ロックと待機の分析

SQLITE_BUSY/LOCKED、transaction時間、busy_timeout、WAL checkpointを確認します。待ちを無制限再試行で隠さず、トランザクションを短くする変更と比較します。

<a id="section-5"></a>

## 資源と改善効果の確認

page_count/freelist_count、cache hit、journal/WAL、IOを確認します。ANALYZE/PRAGMA optimizeの適用とindex増加の更新コストを記録します。

<a id="examples"></a>

## 確認用の例と検証手順

```sql
EXPLAIN QUERY PLAN SELECT * FROM orders WHERE customer_id=24;
PRAGMA page_count;
PRAGMA freelist_count;
```
CLIを利用する場合は.timer on/.stats onで補助します。

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: Python標準ライブラリからローカルファイルを生成。サーバー/HA/CDC拡張は未構成。

[Query planner](https://www.sqlite.org/queryplanner.html) · [EXPLAIN QUERY PLAN](https://www.sqlite.org/eqp.html)
