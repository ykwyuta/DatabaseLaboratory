# PostgreSQL — 差分配信方式

[DB別目次](README.md) · [全体目次](../README.md)

対象: PostgreSQL 17 / 確認日: 2026-10-26

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

WALをlogical decodingで行変更に変換し、publication/subscriptionまたは外部CDCへ配信します。物理レプリケーションと違ってテーブルを選べますが、DDLやsequenceの自動同期は前提にできません。

<a id="section-2"></a>

## 初期ロードと増分の境界

初期スナップショットとslotの開始LSNを整合させ、その間の変更を失わないようにします。wal_level=logical、slot数、sender数、権限、接続許可が必要で、DatabaseLaboratoryの既定設定では有効化していません。

<a id="section-3"></a>

## 順序・チェックポイント・再開

受信済みではなく配信先へ永続反映したLSNを再開位置として管理します。トランザクション境界とcommit順序を保持し、配信先停止でslotが保持するWALの容量を監視します。

<a id="section-4"></a>

## 削除・DDL・型変更への対応

UPDATE/DELETEには行識別用の主キーまたはREPLICA IDENTITYを決めます。DDL・列追加・型変更・TRUNCATEを配信対象として明示し、スキーマ適用順を管理します。

<a id="section-5"></a>

## 配信先の冪等性と監視

主キー+版/LSNでUPSERTを冪等化し、DELETEをtombstoneにする場合は保持期限も決めます。重複・遅延・slot失効・ログ欠落時には再スナップショットと件数照合を行います。

<a id="examples"></a>

## 確認用の例と検証手順

```sql
SHOW wal_level;
SELECT slot_name,slot_type,active,restart_lsn,confirmed_flush_lsn
FROM pg_replication_slots;
```
追加環境で `CREATE PUBLICATION dblab_pub FOR TABLE orders;` を作成し、スナップショット後のINSERT/UPDATE/DELETEと再開を確認します。slotはWALを保持するため終了後の管理対象にします。

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: 単体サーバー。pg_stat_statementsをプリロード。HA/論理配信は未構成。

[論理レプリケーション](https://www.postgresql.org/docs/17/logical-replication.html) · [Logical decoding](https://www.postgresql.org/docs/17/logicaldecoding.html)
