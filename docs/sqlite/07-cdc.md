# SQLite — 差分配信方式

[DB別目次](README.md) · [全体目次](../README.md)

対象: 利用するPython/CLIに同梱されたSQLite 3 / sqlite_version()で確認 / 確認日: 2026-10-26

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

session extensionのchangeset/patchset、またはアプリのoutbox/triggerを使います。session extensionはbuild optionとAPIが必要で、標準Python sqlite3にAPIがあるとは限りません。

<a id="section-2"></a>

## 初期ロードと増分の境界

基準snapshotと変更収集開始をそろえ、表schemaとPKの互換性を維持します。update hookだけでは永続履歴、rollback後の正しい確定イベント、別connectionの変更を一括で扱えません。

<a id="section-3"></a>

## 順序・チェックポイント・再開

changesetの世代/順序と適用済みIDをアプリが保存します。session extensionがnetwork配送や自動checkpointを提供するわけではありません。

<a id="section-4"></a>

## 削除・DDL・型変更への対応

INSERT/UPDATE/DELETEの競合解決、PK変更、schema変更の先行適用を定めます。TEXTのDECIMAL、BLOB、NULL、WITHOUT ROWIDの対応を利用API/版で試験します。

<a id="section-5"></a>

## 配信先の冪等性と監視

配送IDを記録し、同じtransaction内で受信記録と適用を行う等の冪等化を設計します。競合・欠落・未確定変更・保持超過時の再snapshotをテストします。

<a id="examples"></a>

## 確認用の例と検証手順

```sql
PRAGMA compile_options;
```
ENABLE_SESSION等を確認し、対応APIを持つ追加環境でchangesetを取得/適用します。DatabaseLaboratoryはsession extensionや配信consumerを自動導入しません。

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: Python標準ライブラリからローカルファイルを生成。サーバー/HA/CDC拡張は未構成。

[Session extension](https://www.sqlite.org/sessionintro.html) · [update hook](https://www.sqlite.org/c3ref/update_hook.html)
