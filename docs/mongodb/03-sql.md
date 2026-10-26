# MongoDB — SQLの構文差異

[DB別目次](README.md) · [全体目次](../README.md)

対象: MongoDB 8.0 / WiredTiger / 確認日: 2026-10-26

## この章の目次

- [方言と識別子](#section-1)
- [型・精度・NULL・文字列](#section-2)
- [ページング・日付・集約](#section-3)
- [更新・UPSERT・採番](#section-4)
- [DDL・トランザクション・パラメーター](#section-5)
- [確認用の例と検証手順](#examples)
- [公式資料と適用範囲](#sources)

<a id="section-1"></a>

## 方言と識別子

標準接続はSQLではなくMongoDB Query APIとaggregation pipelineです。SQL互換層の有無を明示し、find/$match/$group/$lookupを結合・集計へ対応させます。

<a id="section-2"></a>

## 型・精度・NULL・文字列

BSONにはInt32/Int64/Double/Decimal128/Date等があります。nullと属性欠落は異なり、{field:null}は両方に一致する場合があります。$existsや型判定を併用します。

<a id="section-3"></a>

## ページング・日付・集約

sort/skip/limitは深いページングで高コストになり、安定したキーの範囲条件を検討します。日時はBSON Date、集計は$groupやwindow stageを使います。

<a id="section-4"></a>

## 更新・UPSERT・採番

updateOne/updateMany、$set/$inc、upsert、findOneAndUpdateを使います。replaceOneはドキュメント置換です。SQLの部分更新を置換で実装して他属性を消さないよう注意します。

<a id="section-5"></a>

## DDL・トランザクション・パラメーター

索引作成、validator、collection変更をDDL相当として管理します。driver APIのfilterを構築し、ユーザー入力を任意の演算子として注入しません。transaction利用条件も接続先に応じ確認します。

<a id="examples"></a>

## 確認用の例と検証手順

```javascript
db.customers.find({note: {$exists:false}});
db.customers.find({note: {$type:"null"}});
db.orders.aggregate([{$group:{_id:"$customer_id",count:{$sum:1}}}]);
```

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: 認証付きstandalone。replica set・change streams・分散transactionは未構成。

[CRUD](https://www.mongodb.com/docs/manual/crud/) · [Aggregation](https://www.mongodb.com/docs/manual/aggregation/)
