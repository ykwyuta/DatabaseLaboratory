# MariaDB — 基本的な設計思想

[DB別目次](README.md) · [全体目次](../README.md)

対象: MariaDB 11.4 / InnoDB / 確認日: 2026-10-26

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

MySQLから派生した汎用RDBMSですが、オプティマイザー、SQL、JSON、GTID、管理ツールは独自に発展しています。MySQL互換という理由だけで同一の運用手順を適用しません。

<a id="section-2"></a>

## 格納方式とアクセス経路

DatabaseLaboratoryではInnoDBの主キーによるクラスタ化を使います。MariaDBには複数のエンジンがあり、エンジンごとのロック・永続化・バックアップ対応を確認します。

<a id="section-3"></a>

## トランザクションと整合性

既定のInnoDB分離レベルはREPEATABLE READです。consistent readとlocking read、gap lock、長いトランザクションのundo保持を分けて検証します。

<a id="section-4"></a>

## モデル設計と避けたい設計

文字コード・照合順序・sql_modeをMySQLと明示的に比較します。MySQLのutf8mb4_0900_ai_ciをこの構成へそのまま持ち込まず、DatabaseLaboratoryはutf8mb4_unicode_ciを指定します。

<a id="section-5"></a>

## DatabaseLaboratoryでの観察ポイント

MySQLと同じ受注データで計画・型・NULL・制約を比較します。結果件数が同じでも暗黙変換と実行計画が同じとは限りません。

<a id="examples"></a>

## 確認用の例と検証手順

```sql
SELECT VERSION(),@@tx_isolation,@@collation_server;
SHOW CREATE TABLE exact_values;
```

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: 単体サーバー。MySQLとは別のデータボリュームと初期化SQL。

[ストレージエンジン](https://mariadb.com/docs/server/server-usage/storage-engines/innodb)
