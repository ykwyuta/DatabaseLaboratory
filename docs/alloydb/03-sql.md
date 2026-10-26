# AlloyDB Omni — SQLの構文差異

[DB別目次](README.md) · [全体目次](../README.md)

対象: AlloyDB Omni 17.9.0 / PostgreSQL互換 / 確認日: 2026-10-26

## この章の目次

- [方言と識別子](#section-1)
- [型・精度・NULL・文字列](#section-2)
- [ページング・日付・集約](#section-3)
- [更新・UPSERT・採番](#section-4)
- [DDL・トランザクション・パラメーター](#section-5)
- [確認用の例と検証手順](#examples)
- [公式資料と適用範囲](#sources)

<a id="section-1"></a>

## 方言と識別子

SQLと接続はPostgreSQL互換を基本に、schema/search_pathと小文字への折り畳みを理解します。Google Cloud用の管理SQLやAPIをOmniの標準SQLと混同しません。

<a id="section-2"></a>

## 型・精度・NULL・文字列

NUMERIC、TIMESTAMPTZ、JSONB等を使い、Google独自extension/typeは存在と版を確認します。大きな整数・DECIMALをクライアントでdoubleに落とさないようにします。

<a id="section-3"></a>

## ページング・日付・集約

LIMIT/OFFSET、INTERVAL、ウィンドウ関数、||を基本に共通SQLを試します。SQL構文が同じでも列ストアが対応しない式で行実行へ戻る可能性を計画で確認します。

<a id="section-4"></a>

## 更新・UPSERT・採番

ON CONFLICT、IDENTITY/SEQUENCE、RETURNINGをPostgreSQLと同様に確認します。分析のための列ストア配置操作はデータ更新SQLと別の管理作業です。

<a id="section-5"></a>

## DDL・トランザクション・パラメーター

transaction内DDLの可否や$1形式のbindは対象版で確認します。拡張DDLやGoogle固有フラグは標準PostgreSQLのmigrationへ無条件に流さないよう分けます。

<a id="examples"></a>

## 確認用の例と検証手順

```sql
SELECT big_integer,amount FROM exact_values ORDER BY value_id;
SELECT CURRENT_TIMESTAMP + INTERVAL '1 day';
```
同じSQLをPostgreSQLへ実行して結果と計画を比較します。

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: Omniサーバーと初期化用クライアント。マネージドAlloyDB/Operator/HAは未構成。

[接続互換性](https://docs.cloud.google.com/alloydb/omni/containers/17.9.0/docs/run-connect) · [PostgreSQL SQL](https://www.postgresql.org/docs/17/sql.html)
