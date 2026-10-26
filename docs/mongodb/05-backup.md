# MongoDB — バックアップと復旧

[DB別目次](README.md) · [全体目次](../README.md)

対象: MongoDB 8.0 / WiredTiger / 確認日: 2026-10-26

## この章の目次

- [保護対象と方式の選択](#section-1)
- [取得時の整合性と前提条件](#section-2)
- [増分・差分・時点復旧](#section-3)
- [復元と切り戻しの手順](#section-4)
- [復旧訓練・保持・暗号化](#section-5)
- [確認用の例と検証手順](#examples)
- [公式資料と適用範囲](#sources)

<a id="section-1"></a>

## 保護対象と方式の選択

mongodump/mongorestoreのBSONバックアップ、整合したファイルsnapshot、対応する管理製品を使い分けます。mongoexportのJSON/CSVは型やmetadataを完全保持するバックアップとは異なります。

<a id="section-2"></a>

## 取得時の整合性と前提条件

standaloneで更新中の複数collectionをmongodumpするとDB全体の単一時点整合性は保証できません。DatabaseLaboratoryでは書き込み停止中に取得するか、replica setへ拡張して--oplog条件を満たします。

<a id="section-3"></a>

## 増分・差分・時点復旧

PITRはsnapshotとoplogの継続取得等が必要です。--oplog/--oplogReplayの適用範囲やsharded clusterの制約を確認し、standaloneにoplogがあると仮定しません。

<a id="section-4"></a>

## 復元と切り戻しの手順

別のmongodへmongorestoreし、index/validator/認証情報とBSON型を検証します。sharded clusterはconfig serverとshard間の整合した復旧手順が必要です。

<a id="section-5"></a>

## 復旧訓練・保持・暗号化

件数だけでなくLong/Decimal128、null/欠落、unique index、TTL indexを検証します。バージョン互換性、FCV、暗号鍵、復元時の容量とindex構築時間を測ります。

<a id="examples"></a>

## 確認用の例と検証手順

書込みを止めたDatabaseLaboratoryでの例です。

```sh
docker compose exec -T mongo mongodump --username dblab --password 'DatabaseLaboratory_Test_2026!' --authenticationDatabase admin --db dblab --archive=/tmp/dblab.archive --gzip
docker compose cp mongo:/tmp/dblab.archive .local/dblab-mongo.archive
```
別mongodへ `mongorestore --archive=<path> --gzip` で復元し、認証先とnamespaceを確認します。

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: 認証付きstandalone。replica set・change streams・分散transactionは未構成。

[self-managed backup](https://www.mongodb.com/docs/manual/core/backups/)
