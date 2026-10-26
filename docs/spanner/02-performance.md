# Google Cloud Spanner — 性能分析手法

[DB別目次](README.md) · [全体目次](../README.md)

対象: Spanner本番設計 / Emulator 1.5.41のGoogleSQLで機能検証 / 確認日: 2026-10-26

## この章の目次

- [測定条件と再現性](#section-1)
- [実行計画の取得と読み方](#section-2)
- [SQL統計とボトルネックの特定](#section-3)
- [ロックと待機の分析](#section-4)
- [資源と改善効果の確認](#section-5)
- [確認用の例と検証手順](#examples)
- [公式資料と適用範囲](#sources)

<a id="section-1"></a>

## 測定条件と再現性

本番ではinstance構成、processing units/nodes、地域、データ分布、session poolを記録します。エミュレーターは本番の性能・スケーラビリティ・実行計画の評価には使いません。

<a id="section-2"></a>

## 実行計画の取得と読み方

本番のquery planとPROFILE統計でdistributed scan/join、remote calls、返却行数を読みます。エミュレーターのPLAN/PROFILEが空でも本番で計画がないという意味ではありません。

<a id="section-3"></a>

## SQL統計とボトルネックの特定

SPANNER_SYS.QUERY_STATS_TOP_*、Query InsightsでCPU、latency、rows scannedを追います。正規化queryやtime windowごとの統計として比較し、単発queryと区別します。

<a id="section-4"></a>

## ロックと待機の分析

LOCK_STATS、TXN_STATS、abort/retry、lock waitを分析します。アプリ側のtransaction再試行を含めた遅延と、サーバーの単一試行時間を分けます。

<a id="section-5"></a>

## 資源と改善効果の確認

CPU/ストレージ、split hotspot、leader配置、client/network/session poolを観測します。キー分散やindex変更後に分散呼出し数・書込みコストも再測定します。

<a id="examples"></a>

## 確認用の例と検証手順

```sql
-- 本番向け。エミュレーターでは統計・計画を評価しない
SELECT * FROM SPANNER_SYS.QUERY_STATS_TOP_MINUTE ORDER BY INTERVAL_END DESC LIMIT 10;
```
client retryを含むp95/p99とサーバー指標を別に保存します。

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: インメモリエミュレーターとREST初期化。IAM/本番性能/本番HAは検証不可。

[クエリー統計](https://docs.cloud.google.com/spanner/docs/introspection/query-statistics) · [hotspot](https://docs.cloud.google.com/spanner/docs/find-hotspots-in-database)
