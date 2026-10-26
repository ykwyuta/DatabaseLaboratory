# IBM Db2 — 差分配信方式

[DB別目次](README.md) · [全体目次](../README.md)

対象: Db2 LUW Community 12.1.5.0 / 確認日: 2026-10-26

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

ログベースのSQL Replication/Q Replicationや外部CDCを使います。HADRの物理ログ配送と、異種DBへの行変更配信を区別します。製品・版の対応と追加構成が必要です。

<a id="section-2"></a>

## 初期ロードと増分の境界

DATA CAPTURE CHANGES等のログ拡張、archive保持、対象表のキーを設定します。整合した初期ロードとcapture開始位置を結び、LOADやNOT LOGGED操作の扱いを確認します。

<a id="section-3"></a>

## 順序・チェックポイント・再開

capture/applyの再開位置とcommit単位を保存します。分散した配信先で単一順序を仮定せず、トランザクション/表/キーの保証単位を決めます。

<a id="section-4"></a>

## 削除・DDL・型変更への対応

UPDATE/DELETEのbefore image、LOB、DDL、型変更、triggerの二重実行を検証します。DECIMALと文字コードを維持し、loggedでない一括投入を取りこぼさない手順を定めます。

<a id="section-5"></a>

## 配信先の冪等性と監視

キーとログ座標で冪等適用し、capture/apply lag、queue深度、ログ保持、再送回数を監視します。再開不能なら再初期化し、件数・集約値・削除を突合します。

<a id="examples"></a>

## 確認用の例と検証手順

```sql
SELECT TABSCHEMA,TABNAME,DATACAPTURE FROM SYSCAT.TABLES WHERE TABSCHEMA=CURRENT SCHEMA;
```
別のCDC用環境でログ拡張とcapture/applyを設定します。属性変更だけで外部へ自動配信されるわけではありません。

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: 単体インスタンスdb2inst1とRAVA DB。HADR/外部CDCは未構成。

[IBM replication components](https://www.ibm.com/docs/en/db2/11.5.x?topic=options-replication-tools-by-component) · [レプリケーション時の考慮点](https://www.ibm.com/docs/en/db2/12.1.x?topic=replication-workload-database-considerations)
