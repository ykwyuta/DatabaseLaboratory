# MongoDB — 基本的な設計思想

[DB別目次](README.md) · [全体目次](../README.md)

対象: MongoDB 8.0 / WiredTiger / 確認日: 2026-10-26

## この章の目次

- [用途とワークロード](#section-1)
- [格納方式とアクセス経路](#section-2)
- [トランザクションと整合性](#section-3)
- [モデル設計と避けたい設計](#section-4)
- [DatabaseLaboratoryでの観察ポイント](#section-5)
- [確認用の例と検証手順](#examples)
- [公式資料と適用範囲](#sources)

<a id="section-1"></a>

## 用途とワークロード

BSONドキュメントを単位に、読み取りパターンに合わせて埋め込みと参照を選びます。schemaを自由に変えられますが、validatorや型の規約なしに無制限なばらつきを許容する設計ではありません。

<a id="section-2"></a>

## 格納方式とアクセス経路

WiredTigerのcache・圧縮・journalとB-tree索引を使います。配列のmultikey索引、複合索引の順序、巨大配列や無制限に成長するドキュメントに注意します。

<a id="section-3"></a>

## トランザクションと整合性

単一ドキュメントの更新はatomicです。複数ドキュメントのtransactionはreplica set/sharded clusterが前提で、DatabaseLaboratoryのstandaloneでは評価しません。read concernとwrite concernは別に指定します。

<a id="section-4"></a>

## モデル設計と避けたい設計

一緒に更新する小さな要素は埋め込み、独立して増大する要素は参照を検討します。BSONのInt64/Decimal128をJavaScript Numberへ変換せず、必須属性とindexを設計します。

<a id="section-5"></a>

## DatabaseLaboratoryでの観察ポイント

customersのネスト・配列・null/欠落属性とordersの1200件・偏り、exact_valuesのLong/Decimal128を確認します。SQL表へ平坦化した場合の対応も記録します。

<a id="examples"></a>

## 確認用の例と検証手順

```javascript
db.customers.find({}, {name:1,tags:1,address:1,note:1});
db.exact_values.findOne({_id:1});
```

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: 認証付きstandalone。replica set・change streams・分散transactionは未構成。

[データモデル](https://www.mongodb.com/docs/manual/data-modeling/) · [WiredTiger](https://www.mongodb.com/docs/manual/core/wiredtiger/)
