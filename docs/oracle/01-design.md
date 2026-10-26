# Oracle Database — 基本的な設計思想

[DB別目次](README.md) · [全体目次](../README.md)

対象: Oracle Free latest-lite / 実バージョンをV$VERSIONで確認 / 確認日: 2026-10-26

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

業務トランザクションと整合性を中心に、表領域、redo、undo、SQL/PLSQLの機能を統合します。Freeで学べる範囲とEnterprise専用の可用性・診断機能を分けます。

<a id="section-2"></a>

## 格納方式とアクセス経路

CDB/PDB、ユーザーとschema、tablespace/datafile、segmentを区別します。接続先サービスFREEPDB1とインスタンスSIDを同一視しません。

<a id="section-3"></a>

## トランザクションと整合性

redoで障害回復、undoでread consistencyを支え、既定はREAD COMMITTEDです。長時間readのundo不足、行ロック、DDLロックを考慮し、SERIALIZABLEの競合処理を設計します。

<a id="section-4"></a>

## モデル設計と避けたい設計

NUMBERの精度、VARCHAR2のbyte/char semantics、日付と時刻、空文字=NULLを仕様化します。ヒープ表とB-treeを基本に、partitioning等は版・エディション対応を確認します。

<a id="section-5"></a>

## DatabaseLaboratoryでの観察ポイント

DatabaseLaboratoryのDBLAB schemaを使用します。exact_valuesの空文字がNULLになる点、顧客偏りによる計画差、物理FKと論理関係を比較します。

<a id="examples"></a>

## 確認用の例と検証手順

```sql
SELECT SYS_CONTEXT('USERENV','CON_NAME'),SYS_CONTEXT('USERENV','CURRENT_SCHEMA') FROM dual;
SELECT * FROM exact_values ORDER BY value_id;
```

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: 単体CDBとFREEPDB1。Data Guard/RAC/商用管理パックは構成しない。

[Database Concepts](https://docs.oracle.com/en/database/oracle/oracle-database/23/cncpt/)
