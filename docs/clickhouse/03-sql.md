# ClickHouse — SQLの構文差異

[DB別目次](README.md) · [全体目次](../README.md)

対象: ClickHouse 25.8 / MergeTree / 確認日: 2026-10-26

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

方言はClickHouse SQLでtable engineの指定が重要です。databaseとtable、ORDER BYの格納順序とSELECTの出力順を区別します。

<a id="section-2"></a>

## 型・精度・NULL・文字列

UInt/Int、Decimal、DateTime64、Array/Tuple/Map、Nullable等を使います。未一致JOINの既定値とNULLはjoin_use_nullsに依存し、SUM/COUNTのNULL挙動を確認します。

<a id="section-3"></a>

## ページング・日付・集約

LIMIT、toDateTime64、date/time関数、countIf/sumIf等の集約combinator、arrayJoinが特徴です。ANSI SQLから移植する場合は暗黙変換と関数の引数順を確認します。

<a id="section-4"></a>

## 更新・UPSERT・採番

追記を基本とし、ReplacingMergeTree等はeventualな置換モデルです。FINALのコストやversion/delete列を考慮します。25.8のUPDATE方式の利用可否は設定・engineを確認し、古いALTER UPDATEだけとも決めつけません。

<a id="section-5"></a>

## DDL・トランザクション・パラメーター

DDLはengineとクラスタ伝播を意識します。通常の複数文をSQL transactionとして扱いません。typed query parameterは{param:Type}等で、文字列連結に頼りません。

<a id="examples"></a>

## 確認用の例と検証手順

```sql
SELECT customer_id,countIf(category='購入') FROM events GROUP BY customer_id;
SELECT toTypeName(amount),amount FROM exact_values;
```

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: 単体MergeTree。Keeper、ReplicatedMergeTree、外部CDCは未構成。

[SQL](https://clickhouse.com/docs/sql-reference) · [型](https://clickhouse.com/docs/sql-reference/data-types)
