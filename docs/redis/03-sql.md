# Redis — SQLの構文差異

[DB別目次](README.md) · [全体目次](../README.md)

対象: Redis 7.4 / 確認日: 2026-10-26

## この章の目次

- [方言と識別子](#section-1)
- [型・精度・NULL・文字列](#section-2)
- [ページング・日付・集約](#section-3)
- [更新・UPSERT・採番](#section-4)
- [DDL・トランザクション・パラメーター](#section-5)
- [確認用の例と検証手順](#examples)
- [公式資料と適用範囲](#sources)

<a id="section-1"></a>

## 方言と識別子

SQLは使わずRESPとRedisコマンドを使います。DB番号、キーprefix、Cluster hash slotは別概念です。Redis ClusterではDB 0のみを使う制約にも注意します。

<a id="section-2"></a>

## 型・精度・NULL・文字列

Stringはバイト列で、文字列/整数としての操作はコマンド次第です。NULL相当は未存在やnil応答で、空文字やTTL消滅とは区別します。INCRは64bit整数範囲を持ちます。

<a id="section-3"></a>

## ページング・日付・集約

ページングはSCAN/SSCAN/HSCAN/ZSCANやsorted set範囲で実装します。SCANは重複・変更中の見え方があり、DBスナップショットの代わりにしません。時刻はepoch等の規約を決めます。

<a id="section-4"></a>

## 更新・UPSERT・採番

SET NX/XX、HSET、INCR、ZADD、Luaを使い分けます。SETのTTL保持/更新や、構造の型が違うWRONGTYPEを試験します。採番キーの障害復帰・欠番も仕様化します。

<a id="section-5"></a>

## DDL・トランザクション・パラメーター

MULTI/EXECとWATCHの再試行を明示します。Clusterでは複数キー操作が同じslotに必要な場合がありhash tagを設計します。引数はクライアントAPIから渡し文字列連結しません。

<a id="examples"></a>

## 確認用の例と検証手順

```text
TYPE dblab:example
PTTL dblab:example
SCAN 0 MATCH dblab:* COUNT 100
```
未存在キーのTYPE/TTL応答を空値と区別します。

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: 単体・認証あり・AOF有効。Sentinel/Cluster/永続CDC基盤は未構成。

[コマンド](https://redis.io/docs/latest/commands/) · [transaction](https://redis.io/docs/latest/develop/using-commands/transactions/)
