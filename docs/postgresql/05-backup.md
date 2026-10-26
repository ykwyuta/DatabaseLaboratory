# PostgreSQL — バックアップと復旧

[DB別目次](README.md) · [全体目次](../README.md)

対象: PostgreSQL 17 / 確認日: 2026-10-26

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

小規模移行はpg_dump/pg_restore、クラスタ復旧は物理ベースバックアップを選びます。ロール・tablespaceはpg_dump単体に入らないためpg_dumpall --globals-onlyを別に保管します。

<a id="section-2"></a>

## 取得時の整合性と前提条件

pg_dumpは一貫したスナップショットを取得しますが、長時間実行によるVACUUMへの影響やDDLとの競合を観測します。稼働中のPGDATAを単純コピーしたものを一貫したバックアップとは扱いません。

<a id="section-3"></a>

## 増分・差分・時点復旧

PITRはベースバックアップと連続したWALアーカイブを組み合わせます。17の物理増分バックアップはサマリー設定とpg_combinebackupを含む復旧チェーンの設計が必要です。論理dumpはWALの代わりになりません。

<a id="section-4"></a>

## 復元と切り戻しの手順

元DBを上書きせず別インスタンスへ復元し、拡張・ロール・照合順序をそろえてからpg_restoreします。PITRでは復旧目標とtimelineを明示し、昇格とアプリ接続切り替えを別工程にします。

<a id="section-5"></a>

## 復旧訓練・保持・暗号化

件数・精度・制約・権限・アプリ読書きを照合し、復旧時間を測ります。アーカイブ欠落、鍵の紛失、破損したdumpを想定し、保管先をDBと別の障害ドメインに配置します。

<a id="examples"></a>

## 確認用の例と検証手順

DatabaseLaboratoryのコンテナー内にdumpを作り、ホストへコピーする例です。既存ファイルを上書きしない一意の名前を使います。

```sh
docker compose exec -T postgres pg_dump -U dblab -d dblab -Fc -f /tmp/dblab-backup.dump
docker compose cp postgres:/tmp/dblab-backup.dump .local/dblab-backup.dump
```
復元先には別DBを作成し、`pg_restore --exit-on-error --no-owner -d <restore_db> <dump>` を実行します。roles/拡張を先に準備し、復元後に照合します。

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: 単体サーバー。pg_stat_statementsをプリロード。HA/論理配信は未構成。

[バックアップ](https://www.postgresql.org/docs/17/backup.html) · [WALアーカイブとPITR](https://www.postgresql.org/docs/17/continuous-archiving.html)
