# Oracle Database — バックアップと復旧

[DB別目次](README.md) · [全体目次](../README.md)

対象: Oracle Free latest-lite / 実バージョンをV$VERSIONで確認 / 確認日: 2026-10-26

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

Data Pumpはschema/table等の論理移行、RMANはdatafile/controlfile/archivelog等の物理回復です。PDB/CDBの保護単位、wallet、設定、パスワードファイルを別に整理します。

<a id="section-2"></a>

## 取得時の整合性と前提条件

Data Pumpの一貫した時点はFLASHBACK_TIME/SCN等を検討します。RMANのオンラインバックアップとPITRにはARCHIVELOG等の前提があり、Freeの現設定を確認してから実施します。

<a id="section-3"></a>

## 増分・差分・時点復旧

RMANのlevel 0/1、differential/cumulativeとarchivelogを組み合わせます。Data Pumpの差分移行をredoベースの時点復旧の代わりにはできません。

<a id="section-4"></a>

## 復元と切り戻しの手順

別の隔離環境でRMAN RESTORE→RECOVER→OPEN、またはData Pumpでremap schema/tablespaceを行います。制御ファイル・SCN・incarnationと接続サービスを確認します。

<a id="section-5"></a>

## 復旧訓練・保持・暗号化

RESTORE VALIDATEと実復元を分け、件数・制約・INVALIDオブジェクト・grant・PLSQL・NLSを照合します。鍵、wallet、外部ファイルも独立して保管します。

<a id="examples"></a>

## 確認用の例と検証手順

```text
-- 管理者接続のSQL*Plusで現状確認
ARCHIVE LOG LIST
-- RMANでの方式例。ARCHIVELOG/保管先/容量を準備してから実施
BACKUP DATABASE PLUS ARCHIVELOG;
RESTORE DATABASE VALIDATE;
```
Data Pumpはサーバー側DIRECTORYとREAD/WRITE権限を準備します。例は設計用で、自動構成しません。

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: 単体CDBとFREEPDB1。Data Guard/RAC/商用管理パックは構成しない。

[RMAN](https://docs.oracle.com/en/database/oracle/oracle-database/23/bradv/) · [Data Pump](https://docs.oracle.com/en/database/oracle/oracle-database/23/sutil/)
