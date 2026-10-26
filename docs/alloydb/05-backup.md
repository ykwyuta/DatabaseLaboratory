# AlloyDB Omni — バックアップと復旧

[DB別目次](README.md) · [全体目次](../README.md)

対象: AlloyDB Omni 17.9.0 / PostgreSQL互換 / 確認日: 2026-10-26

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

小規模の論理dumpと、Omni対応のBarman/pgBackRestによる物理backupを使い分けます。通常のPostgreSQL物理backupをOmniへ無条件に流用しません。

<a id="section-2"></a>

## 取得時の整合性と前提条件

dumpは対応版クライアントと拡張の再作成可否を確認します。物理はGoogleの対象版の手順、archive/streaming設定、保管先権限、バックアップツールの対応をそろえます。

<a id="section-3"></a>

## 増分・差分・時点復旧

full/differential/incrementalと連続WALを設計します。PITRは保持windowとWALの欠落検知を必要とし、Ravaのvolume永続化だけでは提供しません。

<a id="section-4"></a>

## 復元と切り戻しの手順

別Omniインスタンスへ復元し、拡張、設定、schema/roleと業務データを照合します。行データ復旧後の列ストア再準備やwarm-upをサービス再開時間へ含めます。

<a id="section-5"></a>

## 復旧訓練・保持・暗号化

件数・DECIMAL・制約・権限・代表SQLと性能回復を確認します。backupチェーン欠落、保管先停止、WAL流量増加を試し、Operatorのbackup planと単体ツールを混在させません。

<a id="examples"></a>

## 確認用の例と検証手順

```sh
docker compose exec -T alloydb pg_dump -U rava -d rava -Fc -f /tmp/rava-omni.dump
docker compose cp alloydb:/tmp/rava-omni.dump .local/rava-omni.dump
```
別Omniでpg_restoreを行い、物理backup/PITRはBarmanまたはpgBackRestの追加構成で試験します。

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: Omniサーバーと初期化用クライアント。マネージドAlloyDB/Operator/HAは未構成。

[Omniバックアップ](https://docs.cloud.google.com/alloydb/omni/containers/17.9.0/docs/protect-data-using-backups)
