# MariaDB — 運用観点の情報取得方法

[DB別目次](README.md) · [全体目次](../README.md)

対象: MariaDB 11.4 / InnoDB / 確認日: 2026-10-26

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

VERSION()、@@version_comment、@@sql_mode、@@tx_isolation、文字コードと照合順序を取得します。MariaDB用の変数名・コマンド名を台帳に保存します。

<a id="section-2"></a>

## セッション・処理・ロック

SHOW FULL PROCESSLIST、INNODB_TRX、INNODB_LOCK_WAITSで待機とトランザクションを見ます。監視アカウントにPROCESSや必要なSELECTを付与します。

<a id="section-3"></a>

## 容量・ログ・保持期間

データ・binlog・relay log・一時領域・undoの容量を分けます。長時間トランザクションとレプリカ遅延による保持増加を監視します。

<a id="section-4"></a>

## メタデータ・権限・セキュリティ

SHOW CREATE TABLE、information_schema、SHOW GRANTSで実定義と権限を確認します。system-versioned tableなど固有機能をバックアップ対象へ含めるか判断します。

<a id="section-5"></a>

## 定期取得と障害時の採取順序

接続→ブロック元→高負荷SQL→資源→error logの順で採取します。設定やステータスの名前がMySQLと一致するか確認し、未知の指標を0として処理しません。

<a id="examples"></a>

## 確認用の例と検証手順

```sql
SHOW FULL PROCESSLIST;
SHOW GLOBAL STATUS LIKE 'Threads_connected';
SELECT * FROM information_schema.INNODB_TRX;
```
権限不足と0件を区別してレポートします。

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: 単体サーバー。MySQLとは別のデータボリュームと初期化SQL。

[情報スキーマ](https://mariadb.com/docs/server/reference/system-tables/information-schema)
