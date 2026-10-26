# PostgreSQL — 基本的な設計思想

[DB別目次](README.md) · [全体目次](../README.md)

対象: PostgreSQL 17 / 確認日: 2026-10-26

## この章の目次

- [用途とワークロード](#section-1)
- [格納方式とアクセス経路](#section-2)
- [トランザクションと整合性](#section-3)
- [モデル設計と避けたい設計](#section-4)
- [DatabaseLaboratoryでの観察ポイント](#section-5)
- [確認用の例と検証手順](#examples)
- [公式資料と適用範囲](#sources)

<a id="section-1"></a>

## 用途とワークロード

汎用の行指向RDBMSとして、OLTP・複雑な結合・分析を同じSQLとトランザクションで扱います。拡張機能や型の豊富さを活用できますが、大規模分析の列指向専用エンジンとは読み取りコストの構造が違います。

<a id="section-2"></a>

## 格納方式とアクセス経路

ヒープと索引を分離し、B-treeに加えてGIN・GiST・BRINなどを選択します。索引で絞ってもヒープアクセスが残る場合があり、可視性マップとIndex Only Scanを合わせて読みます。更新で生まれる不要タプルの回収にはVACUUMが必要です。

<a id="section-3"></a>

## トランザクションと整合性

MVCCにより読み取りスナップショットを作ります。既定はREAD COMMITTEDで文ごとにスナップショットが変わり、REPEATABLE READやSERIALIZABLEでは競合時の再試行を設計します。長いトランザクションは回収を妨げます。

<a id="section-4"></a>

## モデル設計と避けたい設計

主キー・FK・CHECKで整合性を保ち、JSONBは柔軟な属性に限定します。増え続ける索引、巨大な一括更新、idle in transactionを避け、時系列の分割キーと保持期限を決めます。

<a id="section-5"></a>

## DatabaseLaboratoryでの観察ポイント

ordersの顧客1と顧客24で選択性を比較します。employeesの自己参照FK、order_itemsの複合PK、exact_valuesのDECIMALを確認し、autovacuumと更新頻度の関係を考察します。

<a id="examples"></a>

## 確認用の例と検証手順

```sql
SHOW default_transaction_isolation;
SELECT relname, n_live_tup, n_dead_tup FROM pg_stat_user_tables;
```
SELECTで確認した後、別接続で更新を行い、文単位スナップショットと長いトランザクションの違いを観察します。

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: 単体サーバー。pg_stat_statementsをプリロード。HA/論理配信は未構成。

[同時実行制御](https://www.postgresql.org/docs/17/mvcc.html) · [インデックス](https://www.postgresql.org/docs/17/indexes.html)
