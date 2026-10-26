# MySQL — SQLの構文差異

[DB別目次](README.md) · [全体目次](../README.md)

対象: MySQL 8.4 / InnoDB / 確認日: 2026-10-26

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

識別子の引用はバッククォートが基本です。DBとschemaはほぼ同義です。lower_case_table_namesとOSでテーブル名の大小文字動作が変わるため、命名は小文字に統一します。

<a id="section-2"></a>

## 型・精度・NULL・文字列

BOOLEANはTINYINT(1)の別名で、CHECKなしで真偽値だけに限定されません。JSONは専用型、DECIMALは正確値です。SQL modeで変換エラーの扱いが変わり、空文字とNULLは別です。

<a id="section-3"></a>

## ページング・日付・集約

LIMIT件数 OFFSET位置、DATE_ADD、GROUP_CONCATを使います。文字列連結はCONCATで、||はSQL modeに依存します。ONLY_FULL_GROUP_BYを前提に曖昧なGROUP BYを避けます。

<a id="section-4"></a>

## 更新・UPSERT・採番

AUTO_INCREMENTとINSERT ... ON DUPLICATE KEY UPDATEを使います。重複判定は複数の一意索引に影響されるため対象行を検証します。REPLACEは削除+挿入となる場合がありUPSERTと同一視しません。

<a id="section-5"></a>

## DDL・トランザクション・パラメーター

多くのDDLは暗黙COMMITを伴います。atomic DDLがあってもユーザートランザクションで自由にROLLBACKできるという意味ではありません。prepared statementは?を使い、識別子をbindしません。

<a id="examples"></a>

## 確認用の例と検証手順

```sql
SELECT value_id,big_integer,amount,optional_text IS NULL FROM exact_values;
SELECT DATE_ADD(CURRENT_DATE, INTERVAL 1 DAY);
SELECT order_id FROM orders ORDER BY order_id LIMIT 10 OFFSET 10;
```

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: 単体InnoDB。binlog/GTID/レプリカの設定は検証目的に合わせて追加。

[SQL構文](https://dev.mysql.com/doc/refman/8.4/en/sql-statements.html) · [SQL mode](https://dev.mysql.com/doc/refman/8.4/en/sql-mode.html)
