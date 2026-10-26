# MongoDB — 性能分析手法

[DB別目次](README.md) · [全体目次](../README.md)

対象: MongoDB 8.0 / WiredTiger / 確認日: 2026-10-26

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

query filter、projection、sort、collation、batch sizeとindexを固定します。返却件数が多い場合のネットワーク転送時間をサーバー処理と分けます。

<a id="section-2"></a>

## 実行計画の取得と読み方

explain("executionStats")でwinningPlan、IXSCAN/COLLSCAN、nReturned、totalKeysExamined、totalDocsExaminedを見ます。aggregationでは各stageとspillを確認し、実行付きexplainの負荷に注意します。

<a id="section-3"></a>

## SQL統計とボトルネックの特定

slow query log、currentOp、必要時のdatabase profilerを使います。profilerは書き込みと情報保存を伴うため、しきい値と期間を決めて有効化します。

<a id="section-4"></a>

## ロックと待機の分析

currentOpの待機、transaction継続、lock/ticket、write conflictを見ます。replica setならflow controlやmajority待ちも分け、standaloneの結果から推測しません。

<a id="section-5"></a>

## 資源と改善効果の確認

serverStatusのWiredTiger cache・eviction、IO、index sizeとworking setを比較します。索引追加で読取りが改善してもwrite amplificationと容量が増える点を測定します。

<a id="examples"></a>

## 確認用の例と検証手順

```javascript
db.orders.find({customer_id:1}).explain("executionStats");
db.orders.find({customer_id:3}).explain("executionStats");
```
走査件数と返却件数の比を比較します。

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: 認証付きstandalone。replica set・change streams・分散transactionは未構成。

[Explain](https://www.mongodb.com/docs/manual/reference/explain-results/) · [Profiler](https://www.mongodb.com/docs/manual/tutorial/manage-the-database-profiler/)
