# SQL Server — SQLの構文差異

[DB別目次](README.md) · [全体目次](../README.md)

対象: SQL Server 2022 Developer / Linux / 確認日: 2026-10-26

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

方言はT-SQL。schemaはdbo、識別子は[]または設定に応じ二重引用符です。GOはsqlcmd等のバッチ区切りで、DBサーバーが解釈するSQL文ではありません。

<a id="section-2"></a>

## 型・精度・NULL・文字列

BIT、DECIMAL、NVARCHAR、DATETIME2/DATETIMEOFFSET、UNIQUEIDENTIFIERを区別します。2022のJSONはNVARCHARとJSON関数が基本です。Unicode定数はNを付け、NULLと空文字を別に扱います。

<a id="section-3"></a>

## ページング・日付・集約

TOPまたはORDER BY ... OFFSET ... FETCH、DATEADD、STRING_AGGを使います。順序なしTOPは結果が安定しません。+連結のNULL挙動とCONCATを比較します。

<a id="section-4"></a>

## 更新・UPSERT・採番

IDENTITY/SEQUENCE、OUTPUT句を使います。MERGEは同時実行・重複入力を含め検証し、更新→挿入の別実装も比較します。SCOPE_IDENTITYと@@IDENTITYの取得範囲は異なります。

<a id="section-5"></a>

## DDL・トランザクション・パラメーター

BEGIN TRANSACTION、TRY/CATCH、XACT_ABORT、XACT_STATEで失敗時の状態を管理します。DDLの可逆性は文ごとに確認します。T-SQLの変数は@name、ドライバーbind形式とは分けます。

<a id="examples"></a>

## 確認用の例と検証手順

```sql
SELECT N'営業部',CAST('12345678901234567890123.12345678' AS decimal(31,8));
SELECT order_id FROM dbo.orders ORDER BY order_id OFFSET 10 ROWS FETCH NEXT 10 ROWS ONLY;
SELECT DATEADD(day,1,SYSDATETIME());
```

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: 単体Developer版。Always On・SQL Server AgentのCDCジョブは未構成。

[T-SQL](https://learn.microsoft.com/en-us/sql/t-sql/language-reference?view=sql-server-ver16) · [decimal](https://learn.microsoft.com/en-us/sql/t-sql/data-types/decimal-and-numeric-transact-sql?view=sql-server-ver16)
