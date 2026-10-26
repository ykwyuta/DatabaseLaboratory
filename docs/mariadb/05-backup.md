# MariaDB — バックアップと復旧

[DB別目次](README.md) · [全体目次](../README.md)

対象: MariaDB 11.4 / InnoDB / 確認日: 2026-10-26

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

論理はmariadb-dump、オンライン物理はmariadb-backupを選びます。MySQL用の物理バックアップをMariaDBのデータディレクトリへ流用しません。

<a id="section-2"></a>

## 取得時の整合性と前提条件

--single-transactionはトランザクション対応表に限った整合性です。物理バックアップは取得後に--prepareで適用準備し、サーバーとツールの互換版をそろえます。

<a id="section-3"></a>

## 増分・差分・時点復旧

mariadb-backupの増分はbaseのLSNとチェーンを管理します。PITRはバックアップ境界とbinlog/GTIDを保存し、必要なログを期限前に別保管します。

<a id="section-4"></a>

## 復元と切り戻しの手順

物理復元は停止した別データディレクトリへprepare済みの一式を戻し、所有者・設定を整えて起動します。論理復元は制約・routine・event・ユーザーを照合します。

<a id="section-5"></a>

## 復旧訓練・保持・暗号化

復元後に件数・精度・照合順序とレプリケーション座標を確認します。暗号化表・鍵・圧縮・system versioningの再現を別ケースで試験します。

<a id="examples"></a>

## 確認用の例と検証手順

```sh
docker compose exec -T -e MYSQL_PWD=Rava_Test_2026! mariadb mariadb-dump -u root --single-transaction --routines --events --triggers --databases rava --result-file=/tmp/rava.sql
docker compose cp mariadb:/tmp/rava.sql .local/rava-mariadb.sql
```
隔離した別サーバーへ復元して照合します。物理バックアップ用ツールの同梱はこのComposeでは前提にしません。

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: 単体サーバー。MySQLとは別のデータボリュームと初期化SQL。

[mariadb-backup](https://mariadb.com/docs/server/server-usage/backup-and-restore/mariadb-backup/)
