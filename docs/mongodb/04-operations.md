# MongoDB — 運用観点の情報取得方法

[DB別目次](README.md) · [全体目次](../README.md)

対象: MongoDB 8.0 / WiredTiger / 確認日: 2026-10-26

## この章の目次

- [接続先・バージョン・設定](#section-1)
- [セッション・処理・ロック](#section-2)
- [容量・ログ・保持期間](#section-3)
- [メタデータ・権限・セキュリティ](#section-4)
- [定期取得と障害時の採取順序](#section-5)
- [確認用の例と検証手順](#examples)
- [公式資料と適用範囲](#sources)

<a id="section-1"></a>

## 接続先・バージョン・設定

db.version()、hello、getParameter、buildInfoを取得します。standalone/replica set/mongosの役割と接続先DB/authSourceを明示します。

<a id="section-2"></a>

## セッション・処理・ロック

currentOp、serverStatus、connection数、必要時profilerで処理を見ます。clusterMonitor等の役割とアプリDBのreadWriteを分け、root常用を避けます。

<a id="section-3"></a>

## 容量・ログ・保持期間

dbStats/collStats、storageSize/indexSize、journal、replica setならoplog時間幅を監視します。logical sizeと圧縮後ディスク容量を分けます。

<a id="section-4"></a>

## メタデータ・権限・セキュリティ

listCollections/getIndexes、validator、usersInfoを取得します。認証DB、role、TLS、バックアップに含めるユーザー/roleの範囲を記録します。

<a id="section-5"></a>

## 定期取得と障害時の採取順序

接続先role→currentOp→slow query→cache/IO→replication→server logの順に保存します。オブジェクトをNumberへ変換せずBSON/Extended JSONの精度を保ちます。

<a id="examples"></a>

## 確認用の例と検証手順

```javascript
db.version();
db.adminCommand({hello:1});
db.serverStatus().connections;
db.orders.getIndexes();
```

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: 認証付きstandalone。replica set・change streams・分散transactionは未構成。

[監視](https://www.mongodb.com/docs/manual/administration/monitoring/)
