# SQL Server — バックアップと復旧

[DB別目次](README.md) · [全体目次](../README.md)

対象: SQL Server 2022 Developer / Linux / 確認日: 2026-10-26

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

FULL、DIFFERENTIAL、LOG backupと論理exportを区別します。バックアップにはDB以外にlogin、job、linked server、証明書/TDE鍵の復旧計画も必要です。

<a id="section-2"></a>

## 取得時の整合性と前提条件

BACKUP DATABASEで整合したバックアップを作り、CHECKSUMを利用します。COPY_ONLYのフルは通常の差分ベースを変更しない用途向けです。コンテナーの一時ファイルに保存しただけでは保管完了ではありません。

<a id="section-3"></a>

## 増分・差分・時点復旧

差分は直近の通常フル以降、ログは前のログバックアップ以降のログチェーンです。PITRにはFULL等の復旧モデル、最初のフル、連続したログとSTOPAT境界を管理します。

<a id="section-4"></a>

## 復元と切り戻しの手順

RESTORE HEADERONLY/FILELISTONLYで内容を確認し、別DBへMOVEして復元します。フル→必要な差分→ログをNORECOVERYで適用し、最後にRECOVERYします。

<a id="section-5"></a>

## 復旧訓練・保持・暗号化

VERIFYONLYだけで完全な復旧確認とはせず、実復元後にDBCC CHECKDB、件数・型・権限とアプリを照合します。鍵を別保管し、tail-log取得可否と復旧時間も測ります。

<a id="examples"></a>

## 確認用の例と検証手順

管理権限が必要です。既存バックアップと異なる一意のパスを指定します。

```sql
BACKUP DATABASE rava TO DISK='/var/opt/mssql/rava-copy-only.bak' WITH COPY_ONLY,CHECKSUM;
RESTORE VERIFYONLY FROM DISK='/var/opt/mssql/rava-copy-only.bak' WITH CHECKSUM;
```
`docker compose cp sqlserver:/var/opt/mssql/rava-copy-only.bak .local/` で取り出し、隔離した別インスタンスで実復元を試験します。

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: 単体Developer版。Always On・SQL Server AgentのCDCジョブは未構成。

[バックアップと復元](https://learn.microsoft.com/en-us/sql/relational-databases/backup-restore/back-up-and-restore-of-sql-server-databases?view=sql-server-ver16) · [ログバックアップ](https://learn.microsoft.com/en-us/sql/relational-databases/backup-restore/transaction-log-backups-sql-server?view=sql-server-ver16)
