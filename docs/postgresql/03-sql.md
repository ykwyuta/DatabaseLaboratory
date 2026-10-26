# PostgreSQL — SQLの構文差異

[DB別目次](README.md) · [全体目次](../README.md)

対象: PostgreSQL 17 / 確認日: 2026-10-26

## この章の目次

- [方言と識別子](#section-1)
- [型・精度・NULL・文字列](#section-2)
- [ページング・日付・集約](#section-3)
- [更新・UPSERT・採番](#section-4)
- [DDL・トランザクション・パラメーター](#section-5)
- [確認用の例と検証手順](#examples)
- [公式資料と適用範囲](#sources)

<a id="section-1"></a>

## 方言と識別子

非引用の識別子は小文字に折り畳まれます。大文字小文字を保持する名前は二重引用符が必要です。スキーマとDBは別の名前空間で、search_path依存を減らすため運用SQLはpublic.ordersのように修飾します。

<a id="section-2"></a>

## 型・精度・NULL・文字列

BOOLEAN、NUMERIC、TIMESTAMPTZ、JSONB、配列を使えます。NUMERICと浮動小数を分け、空文字とNULLを区別します。NULLとの比較はIS NULL、NULL安全な比較はIS DISTINCT FROMです。

<a id="section-3"></a>

## ページング・日付・集約

LIMIT/OFFSETを使えますが大量の深いページングは主キーによるseek方式を検討します。日付演算はINTERVAL、文字列連結は||、集約のFILTERやウィンドウ関数も利用できます。

<a id="section-4"></a>

## 更新・UPSERT・採番

INSERT ... ON CONFLICTで一意制約を指定してUPSERTします。GENERATED ... AS IDENTITYの採番は欠番を許容します。RETURNINGで変更行を取得でき、COPYは一括入出力用です。

<a id="section-5"></a>

## DDL・トランザクション・パラメーター

多くのDDLはトランザクション内でロールバックできますがCREATE DATABASEなどは例外です。PostgreSQLプロトコルのパラメーターは$1形式で、クライアントAPIのプレースホルダーとは区別します。

<a id="examples"></a>

## 確認用の例と検証手順

```sql
SELECT value_id,big_integer,amount,optional_text IS NULL FROM exact_values;
SELECT order_id FROM orders ORDER BY order_id LIMIT 10 OFFSET 10;
SELECT CURRENT_TIMESTAMP, CURRENT_DATE + INTERVAL '1 day';
```
数値を文字列化してクライアント側の丸めも確認します。

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: 単体サーバー。pg_stat_statementsをプリロード。HA/論理配信は未構成。

[SQL言語](https://www.postgresql.org/docs/17/sql.html) · [数値型](https://www.postgresql.org/docs/17/datatype-numeric.html)
