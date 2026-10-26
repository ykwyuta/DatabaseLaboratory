# Redis — 性能分析手法

[DB別目次](README.md) · [全体目次](../README.md)

対象: Redis 7.4 / 確認日: 2026-10-26

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

接続数、pipeline、payload、key分布、hit/miss、TTL、永続化設定を固定します。ネットワークRTTとサーバーコマンド時間を分けて測定します。

<a id="section-2"></a>

## 実行計画の取得と読み方

SQL実行計画はありません。SLOWLOG、INFO commandstats/latencystats、LATENCYを使い、O(N)コマンド、巨大キー、Lua、forkを調べます。

<a id="section-3"></a>

## SQL統計とボトルネックの特定

commandstatsのcalls/usecやerrorstatsを差分集計します。MONITORは全コマンド監視で負荷・機微情報が増えるため、通常監視の常時手段にはしません。

<a id="section-4"></a>

## ロックと待機の分析

ブロッキングList/Streamの待機は通常の処理待ちの場合があります。CLIENT LIST、blocked_clientsと、長いコマンドによる全体レイテンシを区別します。

<a id="section-5"></a>

## 資源と改善効果の確認

used_memory、RSS、fragmentation、evicted_keys、AOF rewrite、forkのcopy-on-writeとIOを確認します。最大メモリだけでなくfork時の余裕とpage faultも評価します。

<a id="examples"></a>

## 確認用の例と検証手順

```text
SLOWLOG GET 10
INFO commandstats
INFO latencystats
LATENCY LATEST
```
LATENCYの履歴は収集しきい値の設定に依存します。

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: 単体・認証あり・AOF有効。Sentinel/Cluster/永続CDC基盤は未構成。

[レイテンシ分析](https://redis.io/docs/latest/operate/oss_and_stack/management/optimization/latency/)
