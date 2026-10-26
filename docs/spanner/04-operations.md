# Google Cloud Spanner — 運用観点の情報取得方法

[DB別目次](README.md) · [全体目次](../README.md)

対象: Spanner本番設計 / Emulator 1.5.41のGoogleSQLで機能検証 / 確認日: 2026-10-26

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

project/instance/database、SQL方言、instance configuration、processing unitsと地域を台帳化します。DatabaseLaboratoryではdblab-local/dblab/dblabとSPANNER_EMULATOR_HOSTを使用します。

<a id="section-2"></a>

## セッション・処理・ロック

session pool、active query、transaction/lock statsを確認します。IAMとDB fine-grained accessは本番側の設計で、認証なしエミュレーターの結果を権限制御の検証としません。

<a id="section-3"></a>

## 容量・ログ・保持期間

database/index size、CPU、version retention、backup容量、change stream保持を監視します。ファイルパスやWALディレクトリをホストから監視する方式ではありません。

<a id="section-4"></a>

## メタデータ・権限・セキュリティ

INFORMATION_SCHEMAでtable/column/index/constraint/change streamを取得します。DDL履歴とlong-running operationsの失敗を管理し、regionやedition条件も保存します。

<a id="section-5"></a>

## 定期取得と障害時の採取順序

client error/retry→query/transaction stats→hotspot/CPU→schema/operation→Cloud Monitoring/Loggingの順に採取します。エミュレーターではschemaと機能の範囲に限定します。

<a id="examples"></a>

## 確認用の例と検証手順

```sql
SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='';
SELECT INDEX_NAME,TABLE_NAME FROM INFORMATION_SCHEMA.INDEXES WHERE TABLE_SCHEMA='';
```
DatabaseLaboratory初期化/検証は `docker/spanner.py` のREST APIで実装しています。

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: インメモリエミュレーターとREST初期化。IAM/本番性能/本番HAは検証不可。

[監視指標](https://docs.cloud.google.com/spanner/docs/metrics) · [information schema](https://docs.cloud.google.com/spanner/docs/information-schema)
