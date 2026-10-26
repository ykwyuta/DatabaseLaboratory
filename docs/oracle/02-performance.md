# Oracle Database — 性能分析手法

[DB別目次](README.md) · [全体目次](../README.md)

対象: Oracle Free latest-lite / 実バージョンをV$VERSIONで確認 / 確認日: 2026-10-26

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

SQL_ID、child number、bind値、NLS、統計、PDBを記録します。別child cursorの統計を同じSQLの単一値として扱いません。

<a id="section-2"></a>

## 実行計画の取得と読み方

EXPLAIN PLANは推定です。実行したcursorをDBMS_XPLAN.DISPLAY_CURSORで表示し、ALLSTATS LASTにはGATHER_PLAN_STATISTICS等の実測収集が必要です。A-Rows/E-Rows、Starts、Buffers、Tempを見ます。

<a id="section-3"></a>

## SQL統計とボトルネックの特定

V$SQL/V$SQLSTATSでelapsed/CPU/buffer gets/disk reads/executionsを差分集計します。AWR/ASH等は契約・エディション条件があるため、Free環境の標準手順は動的性能ビューを中心にします。

<a id="section-4"></a>

## ロックと待機の分析

V$SESSIONのevent/wait_class/blocking_sessionとV$LOCKを合わせます。CPU実行、IO、enq: TX、cursor競合を分け、待ちの累積と現在のwaitを混同しません。

<a id="section-5"></a>

## 資源と改善効果の確認

SGA/PGA、TEMP spill、undo、redo同期待ち、datafile IOを確認します。統計再収集や索引変更前後のcursorとbindを同条件で比較します。

<a id="examples"></a>

## 確認用の例と検証手順

```sql
SELECT /*+ GATHER_PLAN_STATISTICS */ * FROM orders WHERE customer_id=24;
SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY_CURSOR(NULL,NULL,'ALLSTATS LAST'));
```
同じsessionで実行し、必要な動的性能ビュー権限を確認します。

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: 単体CDBとFREEPDB1。Data Guard/RAC/商用管理パックは構成しない。

[DBMS_XPLAN](https://docs.oracle.com/en/database/oracle/oracle-database/23/arpls/DBMS_XPLAN.html)
