# Google Cloud Spanner — SQLの構文差異

[DB別目次](README.md) · [全体目次](../README.md)

対象: Spanner本番設計 / Emulator 1.5.41のGoogleSQLで機能検証 / 確認日: 2026-10-26

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

GoogleSQLとPostgreSQL方言はDB作成時の選択で、完全なPostgreSQLサーバーではありません。RavaはGoogleSQLのみで、通常のpsql接続口やPGAdapterを用意していません。

<a id="section-2"></a>

## 型・精度・NULL・文字列

INT64、NUMERIC、STRING/BYTES、ARRAY、STRUCT、TIMESTAMP等を使います。GoogleSQL NUMERICはPostgreSQLの任意精度NUMERICと同じ上限ではなく、JSONの整数変換も精度を確認します。

<a id="section-3"></a>

## ページング・日付・集約

LIMIT/OFFSET、DATE_ADD/TIMESTAMP_ADD、UNNEST、ARRAY/STRUCTを使います。index hintやFORCE_INDEXは移植性と退行リスクを検討し、測定根拠を持って使用します。

<a id="section-4"></a>

## 更新・UPSERT・採番

DMLとmutation APIは呼出し方式が異なります。INSERT OR UPDATE mutationはSQL UPSERT構文そのものではありません。sequence/生成キーの対応を版・方言別に確認します。

<a id="section-5"></a>

## DDL・トランザクション・パラメーター

DDLはlong-running operationとして完了を待ちます。DML transactionとDDL変更を同一の原子操作とみなしません。GoogleSQL bindは@param、RESTのINT64は文字列で扱います。

<a id="examples"></a>

## 確認用の例と検証手順

```sql
SELECT order_id FROM orders ORDER BY order_id LIMIT 10 OFFSET 10;
SELECT DATE_ADD(DATE '2026-10-01',INTERVAL 1 DAY);
SELECT big_integer,amount FROM exact_values;
```
通常のSQLクライアントではなくSpanner SDK/RESTで実行します。

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: インメモリエミュレーターとREST初期化。IAM/本番性能/本番HAは検証不可。

[GoogleSQL](https://docs.cloud.google.com/spanner/docs/reference/standard-sql/overview) · [PostgreSQL方言](https://docs.cloud.google.com/spanner/docs/postgresql-interface)
