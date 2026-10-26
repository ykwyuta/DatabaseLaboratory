# MariaDB — SQLの構文差異

[DB別目次](README.md) · [全体目次](../README.md)

対象: MariaDB 11.4 / InnoDB / 確認日: 2026-10-26

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

識別子はバッククォート、DBとschemaは同義です。SQL_MODE=ORACLEなど互換モードは独立した検証条件とし、既定SQLとの混在を避けます。

<a id="section-2"></a>

## 型・精度・NULL・文字列

JSONはMySQLのバイナリJSONと同じ格納型ではなく、MariaDBではLONGTEXTの別名です。DECIMALとDOUBLE、NULLと空文字、文字列照合順序を境界値で確認します。

<a id="section-3"></a>

## ページング・日付・集約

LIMIT/OFFSET、DATE_ADD、GROUP_CONCATを利用します。CTE・ウィンドウ関数・JSON関数の対応は個別に調べ、MySQL固有関数を機械的に置換しません。

<a id="section-4"></a>

## 更新・UPSERT・採番

AUTO_INCREMENT、INSERT ... ON DUPLICATE KEY UPDATE、SEQUENCEを用途に応じて使います。INSERT ... RETURNINGなどMariaDB固有の対応をMySQL側にもあると仮定しません。

<a id="section-5"></a>

## DDL・トランザクション・パラメーター

DDLの暗黙COMMITとエンジンごとのトランザクション対応に注意します。?パラメーターを使うprepared statementでも動的な表名は別に検証します。

<a id="examples"></a>

## 確認用の例と検証手順

```sql
SELECT JSON_VALID('{"region":"東京"}');
SELECT DATE_ADD(CURRENT_DATE,INTERVAL 1 DAY);
SELECT order_id FROM orders ORDER BY order_id LIMIT 10 OFFSET 10;
```

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: 単体サーバー。MySQLとは別のデータボリュームと初期化SQL。

[SQL statements](https://mariadb.com/docs/server/reference/sql-statements) · [JSON](https://mariadb.com/docs/server/reference/data-types/string-data-types/json)
