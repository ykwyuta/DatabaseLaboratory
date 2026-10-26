# MariaDB — 差分配信方式

[DB別目次](README.md) · [全体目次](../README.md)

対象: MariaDB 11.4 / InnoDB / 確認日: 2026-10-26

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

binlogベースの行変更配信を使います。MariaDB GTIDはdomain_id-server_id-sequenceの体系で、MySQL GTIDと互換として扱えません。

<a id="section-2"></a>

## 初期ロードと増分の境界

snapshotとbinlog座標またはMariaDB GTIDを組にします。CDC製品がMariaDB 11.4のイベントと型をサポートするか確認します。

<a id="section-3"></a>

## 順序・チェックポイント・再開

適用済みGTIDとdomainごとの順序を保存します。multi-sourceではdomain間に単一の全順序があると仮定せず、依存するテーブルの配信単位を決めます。

<a id="section-4"></a>

## 削除・DDL・型変更への対応

ROWイベントとDDLの適用を分離し、JSON文字列、DECIMAL、unsigned整数、ゼロ日付をマッピングします。DELETE・TRUNCATE・列改名をケースに含めます。

<a id="section-5"></a>

## 配信先の冪等性と監視

キーと配信位置による冪等化、schema history保存、binlog保持量と遅延の監視が必要です。ログ欠落時に更新時刻だけで差分を再構築しないよう削除履歴も持ちます。

<a id="examples"></a>

## 確認用の例と検証手順

```sql
SHOW VARIABLES LIKE 'log_bin';
SHOW VARIABLES LIKE 'binlog_format';
SELECT @@gtid_current_pos,@@gtid_binlog_pos,@@gtid_slave_pos;
```
CDC追加環境でsnapshot境界・再送・削除を検証します。

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: 単体サーバー。MySQLとは別のデータボリュームと初期化SQL。

[GTID](https://mariadb.com/docs/server/ha-and-performance/standard-replication/gtid)
