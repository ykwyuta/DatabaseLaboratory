# MySQL — 差分配信方式

[DB別目次](README.md) · [全体目次](../README.md)

対象: MySQL 8.4 / InnoDB / 確認日: 2026-10-26

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

ROW binlogを外部CDCやレプリカが読みます。GTIDはトランザクション識別、file/positionはログ座標です。binlog_row_imageで更新前後の列情報が変わります。

<a id="section-2"></a>

## 初期ロードと増分の境界

一貫したsnapshotとGTID/file-positionを組にし、読み取り中に発生した更新をbinlogから追いつかせます。PK欠落表、巨大トランザクション、DDL並行を初期ロード試験に含めます。

<a id="section-3"></a>

## 順序・チェックポイント・再開

配信先反映済みのGTID/offsetを永続化し、再起動後の重複を許容します。並列配信では表をまたぐトランザクションと順序を保証する単位を決めます。

<a id="section-4"></a>

## 削除・DDL・型変更への対応

ROWイベントのINSERT/UPDATE/DELETEとDDLイベントは別に処理します。unsigned BIGINT、DECIMAL、zero date、JSON、charsetを配信先型へ変換するルールを持ちます。

<a id="section-5"></a>

## 配信先の冪等性と監視

主キーとイベント座標で冪等適用し、削除イベントも保存します。source保持期間・最古の未反映座標・lag・schema historyを監視し、binlog欠落時は再ロードを行います。

<a id="examples"></a>

## 確認用の例と検証手順

```sql
SHOW VARIABLES WHERE Variable_name IN ('log_bin','binlog_format','binlog_row_image','gtid_mode','binlog_expire_logs_seconds');
SHOW BINARY LOG STATUS;
```
MySQL 8.4では旧称SHOW MASTER STATUSを使わず、実際のログ座標を記録します。

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: 単体InnoDB。binlog/GTID/レプリカの設定は検証目的に合わせて追加。

[binary log](https://dev.mysql.com/doc/refman/8.4/en/binary-log.html) · [行ベースレプリケーション](https://dev.mysql.com/doc/refman/8.4/en/replication-rbr.html)
