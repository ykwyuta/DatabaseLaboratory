# Google Cloud Spanner — 基本的な設計思想

[DB別目次](README.md) · [全体目次](../README.md)

対象: Spanner本番設計 / Emulator 1.5.41のGoogleSQLで機能検証 / 確認日: 2026-10-26

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

分散RDBMSとして強い整合性と水平分散を両立する設計です。複製合意と時刻に基づく外部整合性を利用し、単体RDBMSの共有メモリ/ローカルディスク前提と分けます。

<a id="section-2"></a>

## 格納方式とアクセス経路

主キー順のkey rangeをsplitして配置します。単調増加キーやtimestamp先頭キーはhotspotを生み得るため、分散キーと読み取りlocalityを両立させます。

<a id="section-3"></a>

## トランザクションと整合性

read-write transactionの競合はABORTEDの再試行を想定します。strong readとstale readの選択、commit timestamp、複数splitをまたぐ更新のコストを設計します。

<a id="section-4"></a>

## モデル設計と避けたい設計

PK、secondary index、interleaving、FKをアクセス経路から選びます。index追加でwrite amplificationや分散transactionが増える点を測定します。

<a id="section-5"></a>

## Ravaでの観察ポイント

Ravaの連番PKは単純な機能fixtureで、本番分散キー設計の推奨ではありません。GoogleSQLとRESTのint64/NUMERICを文字列で送受信し、クライアント精度を確認します。

<a id="examples"></a>

## 確認用の例と検証手順

```sql
SELECT TABLE_NAME,COLUMN_NAME,SPANNER_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='';
SELECT customer_id,COUNT(*) FROM orders GROUP BY customer_id;
```
エミュレーターではAPI呼出しの成功と型を確認します。

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: インメモリエミュレーターとREST初期化。IAM/本番性能/本番HAは検証不可。

[概要](https://docs.cloud.google.com/spanner/docs/overview) · [schema設計](https://docs.cloud.google.com/spanner/docs/schema-design)
