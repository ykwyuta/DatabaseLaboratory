# SQLite — 基本的な設計思想

[DB別目次](README.md) · [全体目次](../README.md)

対象: 利用するPython/CLIに同梱されたSQLite 3 / sqlite_version()で確認 / 確認日: 2026-10-26

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

アプリ内に組み込む単一ファイルのDBで、サーバープロセスやネットワーク認証を必要としません。端末・テスト・小規模ローカルデータに向き、複数ホストの多数writerを前提にしません。

<a id="section-2"></a>

## 格納方式とアクセス経路

B-treeとページ、rowidまたはWITHOUT ROWID表を使います。INTEGER PRIMARY KEYとrowidの関係、複合主キーの格納、索引数とファイルサイズを比較します。

<a id="section-3"></a>

## トランザクションと整合性

同時に書けるwriterは基本1つです。WALはreaderとwriterの並行性を改善しますが、多数writerを並列化する機能ではありません。長いreadがcheckpointを妨げる場合があります。

<a id="section-4"></a>

## モデル設計と避けたい設計

型affinityとSTRICT表を区別し、FKは接続ごとのPRAGMA foreign_keysで有効化します。NUMERIC affinityを任意精度小数と誤認せず、Ravaのexact_values.amountはTEXTで桁を保ちます。

<a id="section-5"></a>

## Ravaでの観察ポイント

ローカルSQLiteファイルを作成し、FK・自己参照・複合PK・大整数・小数TEXTを確認します。別接続で短い書込みと長いreadを行いBUSYとjournal modeを観察します。

<a id="examples"></a>

## 確認用の例と検証手順

```sql
SELECT sqlite_version();
PRAGMA journal_mode;
PRAGMA foreign_keys;
```
アプリの接続初期化でforeign_keys=ONを設定し、無効なFK挿入を試験します。

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: Python標準ライブラリからローカルファイルを生成。サーバー/HA/CDC拡張は未構成。

[SQLiteの用途](https://www.sqlite.org/whentouse.html) · [分離](https://www.sqlite.org/isolation.html)
