# ClickHouse — バックアップと復旧

[DB別目次](README.md) · [全体目次](../README.md)

対象: ClickHouse 25.8 / MergeTree / 確認日: 2026-10-26

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

ネイティブBACKUP/RESTOREや整合したpart snapshotを使い、schema・data・RBAC/設定・Keeper metadataの保護範囲を決めます。レプリカに誤DELETEが伝播するためbackupは別に必要です。

<a id="section-2"></a>

## 取得時の整合性と前提条件

バックアップ先Disk/S3等の設定と権限を準備します。稼働中のデータディレクトリを単純コピーせず、partとmetadataの整合した方式を使います。

<a id="section-3"></a>

## 増分・差分・時点復旧

base_backupを参照する増分はベースの保持が必要です。part差分は業務行のCDCではなく、ログ連続再生型の任意時点PITRと同じではありません。

<a id="section-4"></a>

## 復元と切り戻しの手順

別DB名・別ノードへRESTOREし、engine、partition、materialized view、dictionary、権限を確認します。外部ストレージ依存やreplica識別も切り離してから起動します。

<a id="section-5"></a>

## 復旧訓練・保持・暗号化

件数だけでなくSUM/重複/最新version/delete行、part状態と再実行結果を照合します。backup status、破損、保管先credential、base欠落、復旧時間を試験します。

<a id="examples"></a>

## 確認用の例と検証手順

```sql
-- backup先Diskの許可設定がある追加環境向けの方式例
BACKUP DATABASE rava TO Disk('backups','rava-full.zip');
SELECT id,status,error FROM system.backups;
```
Rava既定にはbackupsディスクを設定していません。別DB/ノードへのRESTOREまで設計してから設定を追加します。

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: 単体MergeTree。Keeper、ReplicatedMergeTree、外部CDCは未構成。

[backup/restore](https://clickhouse.com/docs/operations/backup)
