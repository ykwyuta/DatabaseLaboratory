# Redis — 運用観点の情報取得方法

[DB別目次](README.md) · [全体目次](../README.md)

対象: Redis 7.4 / 確認日: 2026-10-26

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

INFO server、CONFIG GET、ROLEでversion・port・実効設定・役割を確認します。requirepass/ACLとアプリ接続認証を区別し、設定ファイルの永続化も管理します。

<a id="section-2"></a>

## セッション・処理・ロック

CLIENT LIST、INFO clients、SLOWLOG GETで長い処理や接続枯渇を確認します。ACLでCONFIG/FLUSH/DEBUG等の強い操作を制限し、監視用権限を分けます。

<a id="section-3"></a>

## 容量・ログ・保持期間

INFO memory/persistence/replication、DBSIZE、AOF/RDB容量を確認します。evictionはキャッシュなら仕様、正本ならデータ損失になるため指標の重要度が変わります。

<a id="section-4"></a>

## メタデータ・権限・セキュリティ

キーの型はTYPE、寿命はTTL/PTTL、サイズはMEMORY USAGEで調べます。KEYS *の代わりにSCANを使い、ACLユーザー、TLS、接続元制限を台帳化します。

<a id="section-5"></a>

## 定期取得と障害時の採取順序

role→latency/slowlog→memory/eviction→persistence→replicationの順で採取します。時刻と累積counter差分を保存し、CONFIG RESETSTAT等で根拠を消さないようにします。

<a id="examples"></a>

## 確認用の例と検証手順

```sh
docker compose exec -T redis redis-cli INFO server
docker compose exec -T redis redis-cli INFO persistence
docker compose exec -T redis redis-cli INFO replication
```

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: 単体・認証あり・AOF有効。Sentinel/Cluster/永続CDC基盤は未構成。

[INFO](https://redis.io/docs/latest/commands/info/) · [ACL](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/)
