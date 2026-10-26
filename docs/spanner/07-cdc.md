# Google Cloud Spanner — 差分配信方式

[DB別目次](README.md) · [全体目次](../README.md)

対象: Spanner本番設計 / Emulator 1.5.41のGoogleSQLで機能検証 / 確認日: 2026-10-26

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

change streamで対象table/columnの変更を記録し、Dataflow等や対応consumerへ配信します。物理replicaとは別で、履歴保持・配信先反映を設計します。

<a id="section-2"></a>

## 初期ロードと増分の境界

stream作成/保持開始と一貫snapshotのread timestampを合わせ、snapshot中の変更を保持します。短すぎるretentionで初期ロード中に変更が失効しないよう見積もります。

<a id="section-3"></a>

## 順序・チェックポイント・再開

partition token、child partition、commit timestamp、record sequenceを管理します。partitionの分割・heartbeatsとcheckpointを扱い、全partitionに単一の全順序があると仮定しません。

<a id="section-4"></a>

## 削除・DDL・型変更への対応

capture type、primary key、old/new values、DELETE、schema evolutionと列型情報を設計します。streamのDROPは履歴削除につながるため変更管理します。

<a id="section-5"></a>

## 配信先の冪等性と監視

partition/record識別子と業務キーで冪等化し、watermark/lag・retention・consumer失敗を監視します。エミュレーターのchange stream対応は版の制限を確認し、本番の配信性能/保持保証は本番検証で評価します。

<a id="examples"></a>

## 確認用の例と検証手順

```sql
-- 本番/対応する追加検証環境向けのDDL例。DatabaseLaboratoryでは未作成
CREATE CHANGE STREAM dblab_orders FOR orders OPTIONS (retention_period='1d');
```
作成operation完了後、snapshot境界、partitionの増減、consumer停止/再開、DELETEとDDLを試験します。

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: インメモリエミュレーターとREST初期化。IAM/本番性能/本番HAは検証不可。

[change streams](https://docs.cloud.google.com/spanner/docs/change-streams) · [records/partitions](https://docs.cloud.google.com/spanner/docs/change-streams/details)
