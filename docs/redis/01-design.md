# Redis — 基本的な設計思想

[DB別目次](README.md) · [全体目次](../README.md)

対象: Redis 7.4 / 確認日: 2026-10-26

## この章の目次

- [用途とワークロード](#section-1)
- [格納方式とアクセス経路](#section-2)
- [トランザクションと整合性](#section-3)
- [モデル設計と避けたい設計](#section-4)
- [Ravaでの観察ポイント](#section-5)
- [確認用の例と検証手順](#examples)
- [公式資料と適用範囲](#sources)

<a id="section-1"></a>

## 用途とワークロード

メモリ上のキーとデータ構造を低遅延で操作します。キャッシュと、永続性を要求する正本データでは必要なRPOや設定が違います。SQLのFK・joinを備えるRDBMSとしては扱いません。

<a id="section-2"></a>

## 格納方式とアクセス経路

String/Hash/List/Set/Sorted Set/Stream等を用途に応じ選びます。巨大キー、長いLua、全キー走査は他処理も遅くし、データ構造の計算量が性能を左右します。

<a id="section-3"></a>

## トランザクションと整合性

コマンドはatomicですがMULTI/EXECは一般的なSQLトランザクションのrollbackと同じではありません。WATCHは楽観的競合検出、Luaはatomicな複数操作に使います。

<a id="section-4"></a>

## モデル設計と避けたい設計

キー規約、TTL、maxmemoryとeviction方針を決めます。大整数は文字列として保持し、Lua/クライアントの浮動小数による2^53超の丸めを避けます。

<a id="section-5"></a>

## Ravaでの観察ポイント

Ravaは空DBで起動します。verifyは専用ランダムキーで各構造とTTLを試して消すため、実データがない状態を初期化失敗とはみなしません。

<a id="examples"></a>

## 確認用の例と検証手順

```text
INFO memory
CONFIG GET maxmemory
CONFIG GET maxmemory-policy
```
redis-cliはCompose内のREDISCLI_AUTHで認証します。

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: 単体・認証あり・AOF有効。Sentinel/Cluster/永続CDC基盤は未構成。

[データ型](https://redis.io/docs/latest/develop/data-types/)
