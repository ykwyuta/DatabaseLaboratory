# Oracle Database — 運用観点の情報取得方法

[DB別目次](README.md) · [全体目次](../README.md)

対象: Oracle Free latest-lite / 実バージョンをV$VERSIONで確認 / 確認日: 2026-10-26

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

V$VERSION、SYS_CONTEXTのCON_NAME/SERVICE_NAME、V$PARAMETERを収集します。CDBルートとPDBで見える設定・権限・オブジェクトが異なります。

<a id="section-2"></a>

## セッション・処理・ロック

V$SESSION、V$SQL、V$LOCKで接続・実行中SQL・blocking sessionを確認します。必要なV_$ビューへのSELECTを付与し、日常確認をSYSDBAに依存させません。

<a id="section-3"></a>

## 容量・ログ・保持期間

DBA_DATA_FILES、DBA_FREE_SPACE、TEMP、undo、FRA/archived redoとalert logを確認します。autoextend上限とホスト容量は別に監視します。

<a id="section-4"></a>

## メタデータ・権限・セキュリティ

USER_/ALL_/DBA_ビューで取得範囲を分けます。DIRECTORYオブジェクト、DB link、scheduler、roleと直接権限、PDBサービスを復旧台帳に記録します。

<a id="section-5"></a>

## 定期取得と障害時の採取順序

接続PDBと時刻→session/SQL_ID→待機→表領域/redo/undo→alert/traceを保存します。商用診断機能を必要条件とせず、権限不足と情報なしを区別します。

<a id="examples"></a>

## 確認用の例と検証手順

```sql
SELECT banner_full FROM v$version;
SELECT sid,serial#,status,event,wait_class,blocking_session FROM v$session WHERE type='USER';
```
追加例は `sql/performance/oracle.sql` を参照します。

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: 単体CDBとFREEPDB1。Data Guard/RAC/商用管理パックは構成しない。

[Database Reference](https://docs.oracle.com/en/database/oracle/oracle-database/23/refrn/)
