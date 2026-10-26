# DuckDB — SQLの構文差異

[DB別目次](README.md) · [全体目次](../README.md)

対象: インストールしたDuckDBの版 / version()で確認 / 確認日: 2026-10-26

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

PostgreSQLに似たSQLですが完全互換ではありません。識別子の大小文字や暗黙castなど固有差を確認し、PostgreSQLのextension/catalogをそのまま要求しません。

<a id="section-2"></a>

## 型・精度・NULL・文字列

DECIMAL、HUGEINT、LIST/STRUCT/MAP、TIMESTAMP系を利用します。DECIMAL除算等で浮動小数へ変わる演算もあるため、結果型をtypeofで確認します。

<a id="section-3"></a>

## ページング・日付・集約

LIMIT/OFFSET、INTERVAL、window/QUALIFY、read_parquet/read_csv等を使います。ファイルglobやunion_by_nameのschema推論は固定schema読み取りと別に検証します。

<a id="section-4"></a>

## 更新・UPSERT・採番

ON CONFLICTや対応版のMERGE、SEQUENCE等を使います。データ取込はCOPY/INSERT SELECTを基本に、一行ずつ大量送信する方式と比較します。

<a id="section-5"></a>

## DDL・トランザクション・パラメーター

BEGIN/COMMIT/ROLLBACK、transaction conflictの再試行を管理します。?/$1等のbind形式はAPIごとに確認し、外部ファイル名やextension読込の入力検証も設けます。

<a id="examples"></a>

## 確認用の例と検証手順

```sql
SELECT typeof(amount),amount FROM exact_values;
SELECT CURRENT_DATE + INTERVAL '1 day';
SELECT order_id FROM orders ORDER BY order_id LIMIT 10 OFFSET 10;
```

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: Python追加パッケージでローカルファイル生成。サーバー/HA/標準CDCなし。

[PostgreSQLとの差異](https://duckdb.org/docs/stable/sql/dialect/postgresql_compatibility) · [SQL](https://duckdb.org/docs/stable/sql/introduction)
