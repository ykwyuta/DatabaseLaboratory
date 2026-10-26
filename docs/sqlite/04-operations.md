# SQLite — 運用観点の情報取得方法

[DB別目次](README.md) · [全体目次](../README.md)

対象: 利用するPython/CLIに同梱されたSQLite 3 / sqlite_version()で確認 / 確認日: 2026-10-26

## この章の目次

- [接続先・バージョン・設定](#section-1)
- [セッション・処理・ロック](#section-2)
- [容量・ログ・保持期間](#section-3)
- [メタデータ・権限・セキュリティ](#section-4)
- [定期取得と障害時の採取順序](#section-5)
- [確認用の例と検証手順](#examples)
- [公式資料と適用範囲](#sources)

<a id="section-1"></a>

## 接続先・バージョン・設定

sqlite_version()、PRAGMA compile_options/database_list/journal_mode/synchronous/foreign_keysを取得します。Python sqlite3の版とSQLite実体の版を分けます。

<a id="section-2"></a>

## セッション・処理・ロック

サーバーセッション一覧はなく、接続の管理はアプリ責任です。transaction時間、エラーコード、開いているfile handle、busy再試行をアプリログへ記録します。

<a id="section-3"></a>

## 容量・ログ・保持期間

DB本体、-wal、-shm、temporary、page_count/freelist_countを確認します。長いreaderがWALを保持する場合と、削除済み空きページがファイルへ残る場合を区別します。

<a id="section-4"></a>

## メタデータ・権限・セキュリティ

sqlite_schema、PRAGMA table_xinfo/index_list/foreign_key_listで定義を取得します。認証はOSファイル権限やアプリ境界で管理し、標準SQLiteのDBユーザー管理を仮定しません。

<a id="section-5"></a>

## 定期取得と障害時の採取順序

ファイル/接続元→BUSYとtransaction→journal/WAL→容量→integrity_checkの順に確認します。integrity_checkは負荷があるため状況に応じquick_checkと使い分けます。

<a id="examples"></a>

## 確認用の例と検証手順

```sql
PRAGMA database_list;
PRAGMA compile_options;
PRAGMA table_xinfo('orders');
PRAGMA foreign_key_check;
```

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: Python標準ライブラリからローカルファイルを生成。サーバー/HA/CDC拡張は未構成。

[PRAGMA](https://www.sqlite.org/pragma.html) · [WAL](https://www.sqlite.org/wal.html)
