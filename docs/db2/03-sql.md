# IBM Db2 — SQLの構文差異

[DB別目次](README.md) · [全体目次](../README.md)

対象: Db2 LUW Community 12.1.5.0 / 確認日: 2026-10-26

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

非引用識別子は大文字です。CURRENT SCHEMAとCURRENT PATH、接続DBを確認します。CLPの行終端とSQL文の終端、プロシージャ用の別terminatorを区別します。

<a id="section-2"></a>

## 型・精度・NULL・文字列

BIGINT、DECIMAL最大31桁、VARCHAR/CLOB、DATE/TIMESTAMP等を使います。2^53超の整数をアプリの浮動小数へ変換せず、NULLと空文字を区別します。

<a id="section-3"></a>

## ページング・日付・集約

FETCH FIRST/OFFSET、日付+1 DAY、LISTAGG、||を使います。SYSIBM.SYSDUMMY1やVALUESで単一式を評価でき、Oracleのdual依存を移植時に見直します。

<a id="section-4"></a>

## 更新・UPSERT・採番

MERGE、GENERATED ... AS IDENTITY、SEQUENCEを使います。FINAL TABLE/OLD TABLEなどdata change table referenceで更新結果を取得する方式を検討します。

<a id="section-5"></a>

## DDL・トランザクション・パラメーター

CLPのautocommitとCOMMIT/ROLLBACKを意識します。WITH URは読取整合性を緩める指定で、単なる高速化ヒントとして使いません。prepared parameter markerは?です。

<a id="examples"></a>

## 確認用の例と検証手順

```sql
VALUES CURRENT DATE + 1 DAY;
SELECT order_id FROM orders ORDER BY order_id OFFSET 10 ROWS FETCH NEXT 10 ROWS ONLY;
SELECT big_integer,amount FROM exact_values ORDER BY value_id;
```

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: 単体インスタンスdb2inst1とDBLAB DB。HADR/外部CDCは未構成。

[SQL](https://www.ibm.com/docs/en/db2/12.1.x?topic=reference-sql)
