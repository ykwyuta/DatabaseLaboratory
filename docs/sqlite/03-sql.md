# SQLite — SQLの構文差異

[DB別目次](README.md) · [全体目次](../README.md)

対象: 利用するPython/CLIに同梱されたSQLite 3 / sqlite_version()で確認 / 確認日: 2026-10-26

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

SQLite SQLとCLIのドットコマンドは別です。二重引用符を識別子、単一引用符を文字列に使い、寛容な旧式引用に依存しません。schemaはmain/temp/ATTACH先を表します。

<a id="section-2"></a>

## 型・精度・NULL・文字列

storage classはNULL/INTEGER/REAL/TEXT/BLOBです。DECIMAL宣言だけでは正確な小数演算を保証しません。BOOLEAN専用storage classもなく、DATEはTEXT/INTEGER/REAL等の規約で表します。

<a id="section-3"></a>

## ページング・日付・集約

LIMIT/OFFSET、date()/datetime()、group_concatを使います。日付関数の戻り型、UTC/localtime、文字列日付と他DB DATE型の違いを明示します。

<a id="section-4"></a>

## 更新・UPSERT・採番

INTEGER PRIMARY KEY、INSERT ... ON CONFLICT、RETURNINGを利用可能版で確認します。AUTOINCREMENTは再利用制限の意味があり、常に必要ではありません。REPLACEの削除動作にも注意します。

<a id="section-5"></a>

## DDL・トランザクション・パラメーター

BEGIN DEFERRED/IMMEDIATE/EXCLUSIVEでロック取得時機が変わります。ALTER TABLEは対応操作と版を確認します。?/?NNN/:name/@name等のbindを使用し、SQL文字列連結を避けます。

<a id="examples"></a>

## 確認用の例と検証手順

```sql
SELECT typeof(big_integer),typeof(amount),big_integer,amount FROM exact_values;
SELECT date('2026-10-01','+1 day');
```
amountのTEXT保持と、CASTした場合の精度を比較します。

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: Python標準ライブラリからローカルファイルを生成。サーバー/HA/CDC拡張は未構成。

[SQL](https://www.sqlite.org/lang.html) · [型](https://www.sqlite.org/datatype3.html)
