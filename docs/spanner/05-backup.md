# Google Cloud Spanner — バックアップと復旧

[DB別目次](README.md) · [全体目次](../README.md)

対象: Spanner本番設計 / Emulator 1.5.41のGoogleSQLで機能検証 / 確認日: 2026-10-26

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

本番ではサービスのbackup、backup schedule、PITR、Cloud Storageへのexportを使い分けます。サービスbackupと分析用exportは復元範囲・時間・型の保持が異なります。

<a id="section-2"></a>

## 取得時の整合性と前提条件

backupの対象時点・retention・CMEK・権限とoperation完了を確認します。ローカルエミュレーターの状態をDocker volumeへ保存できると仮定しません。

<a id="section-3"></a>

## 増分・差分・時点復旧

PITRのearliest version timeとretention範囲、バックアップ方式ごとのチェーン/期限を管理します。version retentionだけで全期間のバックアップがあるとはみなしません。

<a id="section-4"></a>

## 復元と切り戻しの手順

別databaseへrestoreし、DDL、index、FK、IAM、アプリ接続先を照合します。誤削除前の時刻からbackupを作る方法など、利用可能な復旧経路を選びます。

<a id="section-5"></a>

## 復旧訓練・保持・暗号化

件数・NUMERIC・index/constraint・読書きと切替時間を検証します。region障害、鍵/権限欠落、期限切れ、restore operation失敗を訓練します。

<a id="examples"></a>

## 確認用の例と検証手順

本番でbackup scheduleとretentionを設定し、別databaseへのrestoreを訓練します。Ravaでは再起動後にfixtureを再生成するだけで、変更済みデータをバックアップ/復元する機能はありません。

```sh
python tools/rava.py verify spanner
```
この成功をバックアップ復旧試験の成功と混同しません。

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: インメモリエミュレーターとREST初期化。IAM/本番性能/本番HAは検証不可。

[backup](https://docs.cloud.google.com/spanner/docs/backup) · [PITR](https://docs.cloud.google.com/spanner/docs/pitr)
