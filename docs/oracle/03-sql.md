# Oracle Database — SQLの構文差異

[DB別目次](README.md) · [全体目次](../README.md)

対象: Oracle Free latest-lite / 実バージョンをV$VERSIONで確認 / 確認日: 2026-10-26

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

非引用識別子は大文字へ折り畳まれます。ユーザーとschemaは強く対応し、別ユーザー表はRAVA.ORDERSのように修飾します。SQL*Plusの/はPLSQLブロックの実行区切りです。

<a id="section-2"></a>

## 型・精度・NULL・文字列

NUMBER、VARCHAR2、CLOB/BLOB、DATE、TIMESTAMP系を使い分けます。DATEは時刻も持ち、空文字はNULLです。SQL BOOLEANなど新しい機能は取得したFreeイメージの実版で確認します。

<a id="section-3"></a>

## ページング・日付・集約

FETCH FIRST/OFFSET、ADD_MONTHS、INTERVAL、LISTAGG、||を使います。NLS依存の暗黙日付変換を避け、DATE/TIMESTAMPリテラルか明示的formatを指定します。

<a id="section-4"></a>

## 更新・UPSERT・採番

MERGE、SEQUENCE、IDENTITY、RETURNING INTOを使います。INSERT ALLと複数VALUESの対応は版で違うためRavaはINSERT ALLを使用します。sequenceの欠番を業務番号の連続性と混同しません。

<a id="section-5"></a>

## DDL・トランザクション・パラメーター

DDLは暗黙COMMITに注意します。bindは:name形式が一般的で、PLSQLとSQLの変数範囲は別です。SQL*PlusはWHENEVER SQLERROR/OSERRORで失敗を終了コードへ伝えます。

<a id="examples"></a>

## 確認用の例と検証手順

```sql
SELECT CASE WHEN '' IS NULL THEN 'NULL' ELSE 'EMPTY' END FROM dual;
SELECT order_id FROM orders ORDER BY order_id OFFSET 10 ROWS FETCH NEXT 10 ROWS ONLY;
SELECT DATE '2026-10-01' + 1 FROM dual;
```

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: 単体CDBとFREEPDB1。Data Guard/RAC/商用管理パックは構成しない。

[SQL Language Reference](https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/)
