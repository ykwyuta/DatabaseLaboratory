# IBM Db2 — バックアップと復旧

[DB別目次](README.md) · [全体目次](../README.md)

対象: Db2 LUW Community 12.1.5.0 / 確認日: 2026-10-26

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

BACKUP DATABASEで物理バックアップ、db2lookとEXPORT等で論理定義/データを取得します。DB設定・権限・OS認証・fenced routineなどDB外の資産も保護します。

<a id="section-2"></a>

## 取得時の整合性と前提条件

オンラインbackupにはログアーカイブ等の前提を確認します。Ravaの既定DBをオンライン/PITR可能と仮定せず、GET DB CFGでLOGARCHMETH1/2やpending状態を調べます。

<a id="section-3"></a>

## 増分・差分・時点復旧

incrementalは直近full以降、incremental deltaは直前backup以降を中心にチェーンを構成します。rollforwardには必要な連続ログと復旧目標を管理します。

<a id="section-4"></a>

## 復元と切り戻しの手順

別DB/別instanceへRESTORE DATABASEし、必要なログをROLLFORWARDして復旧を完了します。storage pathやtablespaceのredirect、所有者、接続認証を整えます。

<a id="section-5"></a>

## 復旧訓練・保持・暗号化

backup imageの検査と実復元、表件数・制約・package/統計・権限を照合します。復旧pendingの解除までをRTOに含め、アーカイブログ欠落を訓練します。

<a id="examples"></a>

## 確認用の例と検証手順

```text
db2 get db cfg for RAVA
db2 list history backup all for RAVA
```
方式例: `BACKUP DATABASE RAVA ONLINE TO <backup_dir> INCLUDE LOGS`。ログアーカイブ等の前提を満たす追加環境で使用し、別DBへRESTORE/ROLLFORWARDを試験します。

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: 単体インスタンスdb2inst1とRAVA DB。HADR/外部CDCは未構成。

[回復とHAガイド](https://public.dhe.ibm.com/ps/products/db2/info/vr121/pdf/en_US/db2_data_recov_ha_121.pdf)
