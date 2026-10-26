# Redis — 差分配信方式

[DB別目次](README.md) · [全体目次](../README.md)

対象: Redis 7.4 / 確認日: 2026-10-26

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

keyspace notifications/PubSubはイベント通知ですが接続断で消えるため信頼できるCDC履歴ではありません。確実な配信はアプリがStreamsやoutboxへ変更イベントを書く設計を検討します。

<a id="section-2"></a>

## 初期ロードと増分の境界

初期SCANには更新中の完全snapshot保証がないため、書込み境界・版・停止時間を設計します。イベントにentity key、operation、version、payloadを含めてsnapshotと統合します。

<a id="section-3"></a>

## 順序・チェックポイント・再開

Streamsではconsumer group、pending entries、XACK、再配信とclaimを設計します。最後に読んだIDと処理成功は別で、永続反映後にackする順序を守ります。

<a id="section-4"></a>

## 削除・DDL・型変更への対応

DEL/期限切れ/evictionが通知される条件と通知遅延を考慮します。TTL消滅を業務削除イベントへ変換するなら、アプリが永続イベントを発行する設計を選びます。

<a id="section-5"></a>

## 配信先の冪等性と監視

イベントIDと業務版で冪等化し、pending、lag、retention/trim、DLQを監視します。Stream追記と業務キー更新のatomic性、クラスタのsame-slot制約を確認します。

<a id="examples"></a>

## 確認用の例と検証手順

```text
CONFIG GET notify-keyspace-events
```
通知を使う試験ではconsumer切断中の欠落を確認します。Streamsを使う場合はXINFO GROUPS/XPENDINGで未処理と再送を観測します。

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: 単体・認証あり・AOF有効。Sentinel/Cluster/永続CDC基盤は未構成。

[keyspace notifications](https://redis.io/docs/latest/develop/pubsub/keyspace-notifications/) · [Streams](https://redis.io/docs/latest/develop/data-types/streams/)
