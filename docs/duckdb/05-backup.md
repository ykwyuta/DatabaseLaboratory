# DuckDB — バックアップと復旧

[DB別目次](README.md) · [全体目次](../README.md)

対象: インストールしたDuckDBの版 / version()で確認 / 確認日: 2026-10-26

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

EXPORT DATABASEによるschema/dataの論理保管、一貫した停止時のnative DBコピー、外部ファイル保管を使い分けます。外部ファイル参照がDBファイルだけに収まるとは仮定しません。

<a id="section-2"></a>

## 取得時の整合性と前提条件

稼働中のDB本体だけをコピーせず、書込み停止・CHECKPOINT・全接続close後のコピー、またはエンジンのEXPORTを使います。WALの未反映分を切り捨てないようにします。

<a id="section-3"></a>

## 増分・差分・時点復旧

標準native DuckDBはサーバー型のarchive log PITRや増分backupを提供する前提ではありません。差分Parquetを自作する場合はsnapshot世代・manifest・削除を管理します。

<a id="section-4"></a>

## 復元と切り戻しの手順

別の新規DBへIMPORT DATABASE、または停止時コピーを開きます。DuckDB/extensionの版互換性、schema、viewの外部パス、外部credentialを確認します。

<a id="section-5"></a>

## 復旧訓練・保持・暗号化

件数・DECIMAL・制約・view・外部scanと代表分析を照合します。temp不足、WALが残るcrash、外部ファイル欠落、拡張読込失敗、復元時間を試します。

<a id="examples"></a>

## 確認用の例と検証手順

```sql
EXPORT DATABASE '.local/duckdb-export' (FORMAT PARQUET);
```
新規DBで `IMPORT DATABASE '.local/duckdb-export';` を実行し、DECIMALと制約・viewを照合します。パスはDuckDBを実行しているプロセスから見た相対パスです。nativeコピーはCHECKPOINTして全接続を閉じてから取得します。

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: Python追加パッケージでローカルファイル生成。サーバー/HA/標準CDCなし。

[EXPORT/IMPORT](https://duckdb.org/docs/stable/sql/statements/export) · [CHECKPOINT](https://duckdb.org/docs/stable/sql/statements/checkpoint)
