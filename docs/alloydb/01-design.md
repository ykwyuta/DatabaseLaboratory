# AlloyDB Omni — 基本的な設計思想

[DB別目次](README.md) · [全体目次](../README.md)

対象: AlloyDB Omni 17.9.0 / PostgreSQL互換 / 確認日: 2026-10-26

## この章の目次

- [用途とワークロード](#section-1)
- [格納方式とアクセス経路](#section-2)
- [トランザクションと整合性](#section-3)
- [モデル設計と避けたい設計](#section-4)
- [DatabaseLaboratoryでの観察ポイント](#section-5)
- [確認用の例と検証手順](#examples)
- [公式資料と適用範囲](#sources)

<a id="section-1"></a>

## 用途とワークロード

GoogleのPostgreSQL互換DBを自己管理環境で動かす製品です。Omniは標準ファイルシステムを利用し、Google CloudマネージドAlloyDBのクラウドストレージや管理プレーンとは異なります。

<a id="section-2"></a>

## 格納方式とアクセス経路

PostgreSQL系の行ストアに列指向処理を組み合わせ、分析用の列を列ストアへ配置できます。列ストアの対象・メモリ・適用状態を確認し、存在するだけで全SQLが高速化すると仮定しません。

<a id="section-3"></a>

## トランザクションと整合性

PostgreSQLのMVCC/分離レベルを基本に、Google拡張と実装版の違いを確認します。PostgreSQLと接続互換でも拡張や物理バックアップ形式の完全互換を保証するものではありません。

<a id="section-4"></a>

## モデル設計と避けたい設計

業務制約や型はPostgreSQL相当を基本にします。大量scan/集約は列指向化の候補ですが、少量点検索・更新コスト・メモリ余裕と比較して選びます。

<a id="section-5"></a>

## DatabaseLaboratoryでの観察ポイント

DatabaseLaboratoryは共通受注モデルを作るだけで列指向チューニングを自動適用しません。PostgreSQLと同じSELECTを実行し、実際に列指向計画が選ばれたかを別途確認します。

<a id="examples"></a>

## 確認用の例と検証手順

```sql
SELECT version();
SELECT extname,extversion FROM pg_extension;
SELECT name,setting FROM pg_settings WHERE name LIKE 'google_%';
```

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: Omniサーバーと初期化用クライアント。マネージドAlloyDB/Operator/HAは未構成。

[Omni 17.9概要](https://docs.cloud.google.com/alloydb/omni/containers/17.9.0/docs/overview)
