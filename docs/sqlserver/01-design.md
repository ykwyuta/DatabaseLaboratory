# SQL Server — 基本的な設計思想

[DB別目次](README.md) · [全体目次](../README.md)

対象: SQL Server 2022 Developer / Linux / 確認日: 2026-10-26

## この章の目次

- [用途とワークロード](#section-1)
- [格納方式とアクセス経路](#section-2)
- [トランザクションと整合性](#section-3)
- [モデル設計と避けたい設計](#section-4)
- [Ravaでの観察ポイント](#section-5)
- [確認用の例と検証手順](#examples)
- [公式資料と適用範囲](#sources)

<a id="section-1"></a>

## 用途とワークロード

業務トランザクション、T-SQL、運用ツールを統合したRDBMSです。Developer版は開発検証用で、本番ではエディション・OS・ライセンスに合わせて機能を選びます。

<a id="section-2"></a>

## 格納方式とアクセス経路

行指向のheap/clustered indexとnonclustered index、分析向けcolumnstoreを使い分けます。クラスタ化キーが二次索引の行識別にも影響し、索引数は更新コストを増やします。

<a id="section-3"></a>

## トランザクションと整合性

通常のREAD COMMITTEDはロックベースです。READ_COMMITTED_SNAPSHOTやSNAPSHOTは設定が必要で、Azureの既定値をオンプレ版へ当てはめません。tempdbのversion storeも容量管理します。

<a id="section-4"></a>

## モデル設計と避けたい設計

正確な金額はDECIMAL、UnicodeはNVARCHAR/Nリテラルを使います。parameter sniffing、互換性レベル、統計の変化で計画が変わるためデータの偏りを設計・検証に含めます。

<a id="section-5"></a>

## Ravaでの観察ポイント

顧客1と24の推定/実測計画、hash/sortのspill、exact_valuesの桁を比較します。-1E-8のような指数表記がFLOATになり、VALUES列全体の精度を変えるケースも確認します。

<a id="examples"></a>

## 確認用の例と検証手順

```sql
SELECT name,is_read_committed_snapshot_on,snapshot_isolation_state_desc FROM sys.databases WHERE name=DB_NAME();
SELECT name,type_desc FROM sys.indexes WHERE object_id=OBJECT_ID('dbo.orders');
```

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: 単体Developer版。Always On・SQL Server AgentのCDCジョブは未構成。

[ロックと行バージョニング](https://learn.microsoft.com/en-us/sql/relational-databases/sql-server-transaction-locking-and-row-versioning-guide?view=sql-server-ver16)
