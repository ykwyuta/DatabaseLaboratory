# DuckDB — 差分配信方式

[DB別目次](README.md) · [全体目次](../README.md)

対象: インストールしたDuckDBの版 / version()で確認 / 確認日: 2026-10-26

## この章の目次

- [差分の取得元と配信経路](#section-1)
- [初期ロードと増分の境界](#section-2)
- [順序・チェックポイント・再開](#section-3)
- [削除・DDL・型変更への対応](#section-4)
- [配信先の冪等性と監視](#section-5)
- [確認用の例と検証手順](#examples)
- [公式資料と適用範囲](#sources)

<a id="section-1"></a>

## 差分の取得元と配信経路

標準DuckDBに一般的な行変更CDCログ配信を期待せず、source CDCやアプリoutboxをParquet/イベントとして受け取ります。外部lakehouse extensionの機能はnative DBと区別します。

<a id="section-2"></a>

## 初期ロードと増分の境界

snapshot世代とsource offsetをmanifestに記録し、その後のdelta file集合をimmutableにします。更新時刻だけで増分抽出すると削除や同時更新を逃すためversion/deleteを持たせます。

<a id="section-3"></a>

## 順序・チェックポイント・再開

取り込みbatch IDとsource offsetを永続記録し、公開済み世代をatomicに切り替えます。途中再実行で二重集計しないよう、stagingと公開を分けます。

<a id="section-4"></a>

## 削除・DDL・型変更への対応

UPSERT/MERGEやlatest-by-key集約で更新・削除を反映します。列追加・型昇格・DECIMAL/timezoneとファイルschemaをversion管理します。

<a id="section-5"></a>

## 配信先の冪等性と監視

主キー+version/batchで冪等化し、未処理file、offset lag、欠落、重複、compactionとretentionを監視します。全件再構築と増分適用の結果を比較します。

<a id="examples"></a>

## 確認用の例と検証手順

取り込み用の追加fixtureにkey/version/deleted/batch_idを用意し、同じdeltaを2回・逆順に適用して最終値を確認します。MERGE対応版ではstagingから適用し、未対応なら置換表作成等を検討します。Ravaは外部CDC/manifest公開を自動構築しません。

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: Python追加パッケージでローカルファイル生成。サーバー/HA/標準CDCなし。

[MERGE](https://duckdb.org/docs/stable/sql/statements/merge_into) · [COPY](https://duckdb.org/docs/stable/sql/statements/copy)
