# ClickHouse — 基本的な設計思想

[DB別目次](README.md) · [全体目次](../README.md)

対象: ClickHouse 25.8 / MergeTree / 確認日: 2026-10-26

## この章の目次

- [用途とワークロード](#section-1)
- [格納方式とアクセス経路](#section-2)
- [トランザクションと整合性](#section-3)
- [モデル設計と避けたい設計](#section-4)
- [Ravaでの観察ポイント](#section-5)
- [確認用の例と検証手順](#examples)
- [公式資料と適用範囲](#sources)

<a id="section-1"></a>

## 用途とワークロード

列指向の分析DBで、大量の追記・集計・圧縮と並列scanを重視します。細かな単一行更新と強いトランザクション制約を中心にしたOLTPモデルとは分けて設計します。

<a id="section-2"></a>

## 格納方式とアクセス経路

MergeTreeはpartを作りバックグラウンドmergeします。ORDER BYの並びと疎なprimary indexで読み飛ばし、主キーは一般RDBMSの一意制約とは異なります。小さすぎるINSERTはpartを増やします。

<a id="section-3"></a>

## トランザクションと整合性

単一INSERTの可視性や複数表/複数shardの整合性は同じではありません。mutationは非同期の場合があり、OLTPの即時UPDATEや複数表transactionを想定しません。

<a id="section-4"></a>

## モデル設計と避けたい設計

ORDER BY、partition、TTL、LowCardinality、Nullable、Decimalをワークロードから選びます。高cardinalityの細かいpartitionやSELECT *を避け、必要列を絞ります。

<a id="section-5"></a>

## Ravaでの観察ポイント

Ravaのeventsはcustomer_id/occurred_at/event_id順です。特定顧客と全体集計、同じ件数でも走査列数を変えた性能を比較します。

<a id="examples"></a>

## 確認用の例と検証手順

```sql
SHOW CREATE TABLE events;
SELECT engine,sorting_key,primary_key FROM system.tables WHERE database='rava';
```

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: 単体MergeTree。Keeper、ReplicatedMergeTree、外部CDCは未構成。

[MergeTree](https://clickhouse.com/docs/engines/table-engines/mergetree-family/mergetree)
