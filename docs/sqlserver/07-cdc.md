# SQL Server — 差分配信方式

[DB別目次](README.md) · [全体目次](../README.md)

対象: SQL Server 2022 Developer / Linux / 確認日: 2026-10-26

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

CDCはログからchange tableへ更新前後イメージ等を取り込みます。Change Trackingは変更されたキーの検出が中心で、完全な変更履歴ではありません。transactional replicationとも目的が違います。

<a id="section-2"></a>

## 初期ロードと増分の境界

CDCの有効化、capture instance、SQL Server Agentのcapture/cleanupジョブ、保持期間を設定します。初期snapshotと取得開始LSNを整合させ、snapshot中の変更も取得します。

<a id="section-3"></a>

## 順序・チェックポイント・再開

from/to LSNとsequenceを保存し、次回は重複範囲を含めて再読可能にします。最小LSNがconsumerの位置を追い越したら欠落として再初期化します。

<a id="section-4"></a>

## 削除・DDL・型変更への対応

INSERT/DELETE、UPDATE前後、captured columns、DDLによるcapture instanceの移行を設計します。DECIMALやDATETIMEOFFSETを文字列へ雑に落とさず型を保持します。

<a id="section-5"></a>

## 配信先の冪等性と監視

キー+LSN/seqで冪等化し、captureとcleanupの進行・配信lag・ログ再利用待ちを監視します。AG切替時もジョブと接続先が追従するか試験します。

<a id="examples"></a>

## 確認用の例と検証手順

```sql
SELECT name,is_cdc_enabled FROM sys.databases WHERE name=DB_NAME();
SELECT name,is_tracked_by_cdc FROM sys.tables;
```
DatabaseLaboratoryはCDC未有効です。検証用の別構成でAgentを準備してからcapture/cleanupと再開LSNを確認します。

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: 単体Developer版。Always On・SQL Server AgentのCDCジョブは未構成。

[CDC](https://learn.microsoft.com/en-us/sql/relational-databases/track-changes/about-change-data-capture-sql-server?view=sql-server-ver16) · [Change Tracking](https://learn.microsoft.com/en-us/sql/relational-databases/track-changes/about-change-tracking-sql-server?view=sql-server-ver16)
