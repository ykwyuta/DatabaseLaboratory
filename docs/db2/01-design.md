# IBM Db2 — 基本的な設計思想

[DB別目次](README.md) · [全体目次](../README.md)

対象: Db2 LUW Community 12.1.5.0 / 確認日: 2026-10-26

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

LUW版の業務RDBMSとして、行指向、buffer pool、tablespace、静的/動的SQLとpackageを持ちます。z/OS版やDb2 Warehouseの機能・管理手順をそのまま適用しません。

<a id="section-2"></a>

## 格納方式とアクセス経路

instanceとdatabase、schema、tablespace、containerを分けます。RavaはBLUを有効化せず行指向で、Db2の列指向分析機能を評価した結果ではありません。

<a id="section-3"></a>

## トランザクションと整合性

分離レベルはUR/CS/RS/RRで表し、接続・packageで設定を確認します。CSを基本にcurrently committed、行/表ロック、lock escalation、長時間UOWを評価します。

<a id="section-4"></a>

## モデル設計と避けたい設計

DECIMAL(31,8)など桁数、文字コード、NULL、IDENTITY/SEQUENCEを明示します。RUNSTATSとアクセスパスの関係が強いため、データ増減後の統計管理を設計します。

<a id="section-5"></a>

## Ravaでの観察ポイント

RAVA DBのDB2INST1 schemaを使います。複合PK、自己参照FK、偏り、RUNSTATS後の計画を比較し、アプリの接続schemaの解決も確認します。

<a id="examples"></a>

## 確認用の例と検証手順

```sql
VALUES CURRENT SERVER;
VALUES CURRENT SCHEMA;
SELECT TABNAME,TBSPACE FROM SYSCAT.TABLES WHERE TABSCHEMA=CURRENT SCHEMA;
```

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: 単体インスタンスdb2inst1とRAVA DB。HADR/外部CDCは未構成。

[Db2 12.1ドキュメント](https://www.ibm.com/docs/en/db2/12.1.x)
