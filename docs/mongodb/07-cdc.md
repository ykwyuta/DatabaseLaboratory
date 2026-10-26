# MongoDB — 差分配信方式

[DB別目次](README.md) · [全体目次](../README.md)

対象: MongoDB 8.0 / WiredTiger / 確認日: 2026-10-26

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

change streamsはreplica set/sharded clusterで利用し、oplog由来の変更イベントを取得します。Ravaのstandaloneではwatch()を前提にしません。

<a id="section-2"></a>

## 初期ロードと増分の境界

初期collection scanとchange stream開始位置を整合させます。scan開始前から変更を保持し、scan中の同一キー更新を配信先で上書きできる版管理を決めます。

<a id="section-3"></a>

## 順序・チェックポイント・再開

イベントのresume tokenを不透明な値として保存し、resumeAfter/startAfter等の用途を区別します。tokenがoplog範囲外なら再開不能として再snapshotします。

<a id="section-4"></a>

## 削除・DDL・型変更への対応

deleteのdocumentKey、updateDescription、fullDocument、pre/post images、rename/drop/invalidateを設計します。updateLookupは更新時の完全像と同一とは限らないため意味を確認します。

<a id="section-5"></a>

## 配信先の冪等性と監視

document key+tokenで冪等適用し、consumer lag、resume token保存、oplog時間幅、DLQを監視します。分割や再シャーディング時にも継続するか対応版で試験します。

<a id="examples"></a>

## 確認用の例と検証手順

```javascript
// replica setを準備した追加環境専用
const changes = db.orders.watch([], {fullDocument:"updateLookup"});
```
consumer停止→再開、DELETE、collection rename/dropを含め、resume tokenによる復帰を試験します。

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: 認証付きstandalone。replica set・change streams・分散transactionは未構成。

[Change streams](https://www.mongodb.com/docs/manual/changestreams/) · [oplog](https://www.mongodb.com/docs/manual/core/replica-set-oplog/)
