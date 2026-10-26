# DuckDB — 運用観点の情報取得方法

[DB別目次](README.md) · [全体目次](../README.md)

対象: インストールしたDuckDBの版 / version()で確認 / 確認日: 2026-10-26

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

version()、duckdb_settings()/extensions()/databases()でDB・設定・拡張版を確認します。nativeファイルと外部Parquet/CSVの所在を別台帳にします。

<a id="section-2"></a>

## セッション・処理・ロック

処理管理はアプリのconnection/thread/taskが中心です。キャンセル、timeout、file lock、エラーをアプリ側で記録し、全接続セッションを管理するサーバーを仮定しません。

<a id="section-3"></a>

## 容量・ログ・保持期間

DB本体・WAL・temp directory・外部ファイル容量を監視します。memory_limit以外のプロセスメモリやOS page cacheもあり、RSSとDB内指標を併記します。

<a id="section-4"></a>

## メタデータ・権限・セキュリティ

duckdb_tables/columns/indexes/constraints、information_schemaで定義を取得します。標準的なサーバーrole/認証を仮定せず、OS権限・アプリ境界・外部credentialを保護します。

<a id="section-5"></a>

## 定期取得と障害時の採取順序

query/profile→memory/spill→IO/files→extension/setting→アプリエラーの順に採取します。外部ファイルの世代変更やschema推論変更を再現条件に含めます。

<a id="examples"></a>

## 確認用の例と検証手順

```sql
SELECT * FROM duckdb_databases();
SELECT * FROM duckdb_temporary_files();
SELECT table_name FROM information_schema.tables;
```

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: Python追加パッケージでローカルファイル生成。サーバー/HA/標準CDCなし。

[システム情報](https://duckdb.org/docs/stable/sql/meta/duckdb_table_functions) · [設定](https://duckdb.org/docs/stable/configuration/overview)
