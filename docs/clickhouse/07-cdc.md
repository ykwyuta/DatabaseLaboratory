# ClickHouse — 差分配信方式

[DB別目次](README.md) · [全体目次](../README.md)

対象: ClickHouse 25.8 / MergeTree / 確認日: 2026-10-26

## この章の目次

- [差分の取得元と配信経路](#section-1)
- [初期ロードと増分の境界](#section-2)
- [順序・チェックポイント・再開](#section-3)
- [削除・DDL・型変更への対応](#section-4)
- [配信先の冪等性と監視](#section-5)
- [確認用の例と検証手順](#examples)
- [公式資料と適用範囲](#sources)

<a id="section-1"></a>

## 差分の取得元と配信経路

主に外部RDBMSのCDCを受ける分析sinkとして、broker/connectorを経由して取り込みます。ClickHouseからの一般的な更新ログ配信を、replicaのpart配送だけで代替しません。

<a id="section-2"></a>

## 初期ロードと増分の境界

source snapshot境界とLSN/GTID等のoffsetを保持し、初期ロードと追記CDCを接続します。非同期INSERTのackと永続反映の意味、失敗時再送を設計します。

<a id="section-3"></a>

## 順序・チェックポイント・再開

主キー、version、operation/delete flag、source positionを取り込みます。ReplacingMergeTreeのmergeは即時ではなく、最新行を読む方法とFINAL/argMaxのコストを決めます。

<a id="section-4"></a>

## 削除・DDL・型変更への対応

DELETEを削除フラグ等で表現し、schema変更・精度・timestampのタイムゾーンを維持します。materialized viewは入力blockに反応するため、後の置換/mergeが過去集計を自動修正するとは仮定しません。

<a id="section-5"></a>

## 配信先の冪等性と監視

sink適用はキー+source versionで冪等化し、broker offset、insertエラー、重複、part/merge lag、削除反映を監視します。再投入が集約を二重計上しないかを試験します。

<a id="examples"></a>

## 確認用の例と検証手順

追加環境では同じ主キーをversion=1→2と配信し、DELETE、再送、順序逆転を試験します。

```sql
SELECT customer_id,count(),sum(amount) FROM events GROUP BY customer_id;
```
Ravaのeventsは追記データであり、CDCのversion/delete列を持つReplacingMergeTree構成ではありません。

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: 単体MergeTree。Keeper、ReplicatedMergeTree、外部CDCは未構成。

[ReplacingMergeTree](https://clickhouse.com/docs/engines/table-engines/mergetree-family/replacingmergetree) · [CDC](https://clickhouse.com/docs/integrations/data-ingestion/cdc)
