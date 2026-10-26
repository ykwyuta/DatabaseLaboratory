# AlloyDB Omni — 性能分析手法

[DB別目次](README.md) · [全体目次](../README.md)

対象: AlloyDB Omni 17.9.0 / PostgreSQL互換 / 確認日: 2026-10-26

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

PostgreSQLとの比較ではCPU/RAM/IO、同時実行数、統計、列ストアのwarm-upと対象列をそろえます。小さな1200件のfixtureから製品の最大性能を判断しません。

<a id="section-2"></a>

## 実行計画の取得と読み方

EXPLAIN (ANALYZE,BUFFERS)でscan/join/aggregateとGoogle拡張nodeを確認します。列指向へ移った範囲、行数推定、fallbackの理由を実効設定と合わせて調べます。

<a id="section-3"></a>

## SQL統計とボトルネックの特定

pg_stat_activityや利用可能なSQL統計拡張を確認します。RavaのOmni初期化SQLはpg_stat_statementsを作成しないので、必要なら対応拡張とpreload設定を先に準備します。

<a id="section-4"></a>

## ロックと待機の分析

PostgreSQL系のwait_eventとblocking pidを確認し、行ロック、IO、列ストア準備/更新の負荷を分けます。大きな分析SQLがOLTPのp99を悪化させないか評価します。

<a id="section-5"></a>

## 資源と改善効果の確認

行buffer、列ストアメモリ、PGA相当ではなくPostgreSQLのwork_mem等、temporary spill、CPU/IOを観測します。列対象を増やしたときのメモリ圧迫と更新負荷も測ります。

<a id="examples"></a>

## 確認用の例と検証手順

```sql
EXPLAIN (ANALYZE,BUFFERS) SELECT customer_id,sum(total_amount) FROM orders GROUP BY customer_id;
```
列指向設定を変える前後で、plan・CPU・read量・メモリを同じデータで比較します。

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: Omniサーバーと初期化用クライアント。マネージドAlloyDB/Operator/HAは未構成。

[列指向エンジン](https://docs.cloud.google.com/alloydb/omni/containers/17.5.0/docs/columnar-engine/overview) · [PostgreSQL EXPLAIN](https://www.postgresql.org/docs/17/using-explain.html)（列指向資料は17.5版。17.9の設定と照合）
