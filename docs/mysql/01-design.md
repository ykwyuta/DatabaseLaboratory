# MySQL — 基本的な設計思想

[DB別目次](README.md) · [全体目次](../README.md)

対象: MySQL 8.4 / InnoDB / 確認日: 2026-10-26

## この章の目次

- [用途とワークロード](#section-1)
- [格納方式とアクセス経路](#section-2)
- [トランザクションと整合性](#section-3)
- [モデル設計と避けたい設計](#section-4)
- [Ravaでの観察ポイント](#section-5)
- [確認用の例と検証手順](#examples)
- [公式資料と適用範囲](#sources)

<a id="section-1"></a>

## 用途とワークロード

InnoDBを用いた行単位の業務トランザクションが中心です。SQLレイヤーとストレージエンジンを分ける設計ですが、エンジンを変えるとトランザクションやロックの意味も変わります。

<a id="section-2"></a>

## 格納方式とアクセス経路

主キーがクラスタ化索引となり、二次索引の葉に主キーを保持します。長い主キーは二次索引も大きくします。ランダムなキーによるページ分割と、連番キーへの書き込み集中を比較します。

<a id="section-3"></a>

## トランザクションと整合性

MVCCとundoを使用し、既定の分離レベルはREPEATABLE READです。通常のconsistent readとFOR UPDATEのcurrent readは同じ意味ではありません。範囲更新ではnext-key/gap lockの影響を確認します。

<a id="section-4"></a>

## モデル設計と避けたい設計

utf8mb4と照合順序を明示し、大小文字・アクセント・末尾空白の比較を仕様化します。複合索引の列順を検索パターンから決め、低選択性列の索引追加だけで解決しようとしません。

<a id="section-5"></a>

## Ravaでの観察ポイント

ordersの顧客の偏り、複合索引、DECIMAL、自己参照FKを観察します。buffer poolとデータ量の比を固定して比較します。

<a id="examples"></a>

## 確認用の例と検証手順

```sql
SELECT @@transaction_isolation,@@innodb_buffer_pool_size;
SHOW CREATE TABLE orders;
```
主キーの長さを変えた別表で二次索引サイズを比較します。

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: 単体InnoDB。binlog/GTID/レプリカの設定は検証目的に合わせて追加。

[InnoDB](https://dev.mysql.com/doc/refman/8.4/en/innodb-storage-engine.html)
