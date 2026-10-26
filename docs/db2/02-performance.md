# IBM Db2 — 性能分析手法

[DB別目次](README.md) · [全体目次](../README.md)

対象: Db2 LUW Community 12.1.5.0 / 確認日: 2026-10-26

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

database/member、package cache、bind、統計、buffer poolとデータ量を記録します。初回コンパイルと繰返し実行、package cache退去を分けて測定します。

<a id="section-2"></a>

## 実行計画の取得と読み方

EXPLAIN PLAN FORで推定計画、db2exfmtで書式化します。実測section情報を得るにはactivity/section actuals等の収集設定が必要で、EXPLAINだけで実測値が得られるとは扱いません。

<a id="section-3"></a>

## SQL統計とボトルネックの特定

MON_GET_PKG_CACHE_STMTのNUM_EXECUTIONS/TOTAL_ACT_TIME/TOTAL_CPU_TIME/ROWS_READ等を差分集計します。TOTAL_ACT_TIMEはCPU時間と同義ではなく、対象memberと単位を確認します。

<a id="section-4"></a>

## ロックと待機の分析

MON_GET_CONNECTION、MON_GET_APPL_LOCKWAIT、db2pdで待機を調べます。lock timeout/deadlock、log IO、buffer pool、sort overflowを別々に分析します。

<a id="section-5"></a>

## 資源と改善効果の確認

MON_GET_BUFFERPOOL、MON_GET_TABLESPACE、MON_GET_TRANSACTION_LOGとOS IOを合わせます。RUNSTATS/REORGや索引追加の負荷を含めて改善を評価します。

<a id="examples"></a>

## 確認用の例と検証手順

```sql
EXPLAIN PLAN FOR SELECT * FROM orders WHERE customer_id=24;
SELECT NUM_EXECUTIONS,TOTAL_ACT_TIME,ROWS_READ FROM TABLE(MON_GET_PKG_CACHE_STMT(NULL,NULL,NULL,-2)) AS S;
```
instance ownerのshellで `db2exfmt -d DBLAB -1 -o /tmp/dblab-plan.txt` を使います。

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: 単体インスタンスdb2inst1とDBLAB DB。HADR/外部CDCは未構成。

[パッケージキャッシュ統計](https://www.ibm.com/docs/en/db2/12.1.x?topic=mmr-mon-get-pkg-cache-stmt-table-function-get-package-cache-statement-metrics)
