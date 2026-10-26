# AlloyDB Omni — 差分配信方式

[DB別目次](README.md) · [全体目次](../README.md)

対象: AlloyDB Omni 17.9.0 / PostgreSQL互換 / 確認日: 2026-10-26

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

WALのlogical decodingや対応するpglogical等で外部へ配信します。Omniの行変更配信と、standbyへの物理複製、マネージドAlloyDBの移行サービスは別の方式です。

<a id="section-2"></a>

## 初期ロードと増分の境界

wal_level、preload extension、slot/sender、権限を対象版の手順に合わせます。snapshotと開始LSNを整合させ、Ravaの既定OmniではCDC設定済みと扱いません。

<a id="section-3"></a>

## 順序・チェックポイント・再開

永続反映済みLSNとtransaction境界を保存します。slotのWAL保持と無効化条件、HA昇格時のslot継続可否を対応製品/版で試験します。

<a id="section-4"></a>

## 削除・DDL・型変更への対応

PK/replica identity、UPDATE/DELETE、DDL、sequence、Google独自型/拡張の配信範囲を定めます。schema変更は別pipelineで順序を合わせます。

<a id="section-5"></a>

## 配信先の冪等性と監視

キー+LSN/業務versionで冪等化し、slot lag・WAL容量・consumer errorを監視します。停止が保持期間を超えたら再snapshotし、件数・集約・削除を照合します。

<a id="examples"></a>

## 確認用の例と検証手順

```sql
SHOW wal_level;
SELECT slot_name,active,restart_lsn,confirmed_flush_lsn FROM pg_replication_slots;
```
Google拡張と論理レプリケーション方式を選定した追加環境で設定・再開試験を行います。

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: Omniサーバーと初期化用クライアント。マネージドAlloyDB/Operator/HAは未構成。

[Omni論理配信例](https://docs.cloud.google.com/alloydb/omni/containers/17.10.0/docs/replicate-data-alloydb-omni)（17.10版。対象17.9で利用可否を確認） · [PostgreSQL論理配信](https://www.postgresql.org/docs/17/logical-replication.html)
