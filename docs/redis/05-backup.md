# Redis — バックアップと復旧

[DB別目次](README.md) · [全体目次](../README.md)

対象: Redis 7.4 / 確認日: 2026-10-26

## この章の目次

- [保護対象と方式の選択](#section-1)
- [取得時の整合性と前提条件](#section-2)
- [増分・差分・時点復旧](#section-3)
- [復元と切り戻しの手順](#section-4)
- [復旧訓練・保持・暗号化](#section-5)
- [確認用の例と検証手順](#examples)
- [公式資料と適用範囲](#sources)

<a id="section-1"></a>

## 保護対象と方式の選択

RDBは時点snapshot、AOFはコマンドの永続ログです。AOF有効化は外部バックアップの代わりになりません。Ravaはappendonly yesで、fsyncの実効値も確認します。

<a id="section-2"></a>

## 取得時の整合性と前提条件

BGSAVEの完了をINFO persistenceで確認してからRDBを保管します。fork/IO負荷を考慮し、multipart AOFはmanifestと全構成ファイルを一貫して保護します。

<a id="section-3"></a>

## 増分・差分・時点復旧

RDBだけなら最後のsnapshot以降を失い得ます。AOFのeverysec/always等は損失と性能のトレードオフで、AOF rewriteとバックアップの増分を同一視しません。標準AOFだけで任意時点PITRを保証しません。

<a id="section-4"></a>

## 復元と切り戻しの手順

別のRedisを停止状態で用意し、保存形式と版を確認してRDB/AOFを配置します。両方存在する場合の起動時選択、所有者、ACL/config、データディレクトリを確認します。

<a id="section-5"></a>

## 復旧訓練・保持・暗号化

key数・TYPE・値・TTL・Stream consumer group状態を照合します。過去時点へ戻すと有効期限切れキーが消える点、AOF破損、鍵、誤FLUSHの復旧も試します。

<a id="examples"></a>

## 確認用の例と検証手順

```text
BGSAVE
INFO persistence
CONFIG GET dir
CONFIG GET dbfilename
```
rdb_bgsave_in_progress=0とlast_bgsave_statusを確認後、生成したRDBをコンテナー外へコピーします。AOFの保管時はappenddirname/manifest一式と書込み整合性を確認します。

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: 単体・認証あり・AOF有効。Sentinel/Cluster/永続CDC基盤は未構成。

[永続化](https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/)
