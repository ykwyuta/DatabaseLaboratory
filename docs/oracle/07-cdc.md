# Oracle Database — 差分配信方式

[DB別目次](README.md) · [全体目次](../README.md)

対象: Oracle Free latest-lite / 実バージョンをV$VERSIONで確認 / 確認日: 2026-10-26

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

redo/archived redoをLogMiner等で読み、外部CDCまたは対応するレプリケーション製品へ渡します。GoldenGate/XStream等の利用条件と対応版を個別に確認します。

<a id="section-2"></a>

## 初期ロードと増分の境界

SCNで一貫した初期ロード境界を決め、必要なredoを保持します。supplemental logging、ARCHIVELOG、主キー、権限、対象PDBを設定し、ログ量増加を評価します。

<a id="section-3"></a>

## 順序・チェックポイント・再開

commit SCNとトランザクション境界・ログ位置を保存します。SCNだけで複数イベントの一意性を決めず、再開後の重複を吸収します。古いcontinuous_mineを前提にしません。

<a id="section-4"></a>

## 削除・DDL・型変更への対応

DELETE/LOB/DDL/型変更の対応はCDC製品ごとに検証します。NUMBERのscale、DATEの時刻、TIMESTAMP WITH TIME ZONE、空文字=NULLを配信仕様へ反映します。

<a id="section-5"></a>

## 配信先の冪等性と監視

キー+イベント位置で冪等化し、ログ保持・capture lag・long transaction・schema historyを監視します。必要なarchivelogが欠落した場合はsnapshotからやり直します。

<a id="examples"></a>

## 確認用の例と検証手順

```sql
SELECT supplemental_log_data_min,log_mode FROM v$database;
```
追加のCDC環境でSCN境界、削除、DDL、長時間トランザクションとconsumer停止を試験します。

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: 単体CDBとFREEPDB1。Data Guard/RAC/商用管理パックは構成しない。

[LogMiner](https://docs.oracle.com/en/database/oracle/oracle-database/21/sutil/oracle-logminer-utility.html) · [ユーティリティ](https://docs.oracle.com/en/database/oracle/oracle-database/23/sutil/)
