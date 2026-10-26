# MySQL — バックアップと復旧

[DB別目次](README.md) · [全体目次](../README.md)

対象: MySQL 8.4 / InnoDB / 確認日: 2026-10-26

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

小規模の論理バックアップはmysqldump、物理バックアップは対応版の専用ツールを選びます。データ以外にユーザー、routine、event、trigger、設定、タイムゾーンの扱いを決めます。

<a id="section-2"></a>

## 取得時の整合性と前提条件

InnoDBの--single-transactionは一貫した論理スナップショットを取得しますが、並行DDLや非トランザクション表を同様に保護しません。ログ座標を記録する場合は権限・ロック条件を確認します。

<a id="section-3"></a>

## 増分・差分・時点復旧

フルバックアップ後のbinlogをmysqlbinlogで再生してPITRを行います。フルと差分配信の境界をGTIDまたはfile/positionで保存し、保持期限による欠落を防ぎます。

<a id="section-4"></a>

## 復元と切り戻しの手順

別インスタンスへschema→data→routine/権限を復元し、必要なbinlogを停止位置まで再生します。誤更新の直前を目標にし、同じ誤更新を再適用しない境界を検証します。

<a id="section-5"></a>

## 復旧訓練・保持・暗号化

件数・一意性・FK・照合順序・精度・AUTO_INCREMENT次値を照合します。復元先でアプリケーションを実行し、暗号鍵・GTID・タイムゾーン・保管先障害も試験します。

<a id="examples"></a>

## 確認用の例と検証手順

コンテナー内で取得し、シェルの文字コード変換を避けてコピーします。

```sh
docker compose exec -T -e MYSQL_PWD=DatabaseLaboratory_Test_2026! mysql mysqldump -u root --single-transaction --routines --events --triggers --databases dblab --result-file=/tmp/dblab.sql
docker compose cp mysql:/tmp/dblab.sql .local/dblab-mysql.sql
```
このdumpはCREATE DATABASE/USEを含むため、別の隔離したサーバーへ復元します。

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: 単体InnoDB。binlog/GTID/レプリカの設定は検証目的に合わせて追加。

[バックアップ](https://dev.mysql.com/doc/refman/8.4/en/backup-and-recovery.html)
