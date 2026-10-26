# 起動・データ検証の実測記録

[総合目次](../README.md)

2026-10-26、WindowsのDocker Desktop / Linux containersで11種類のサーバーDBを起動し、共通ツールによる検証が成功しました。[機械可読レポート](2026-10-26.json)には時刻・使用イメージID・件数照合結果を保存しています。

| 対象 | 確認内容 |
| --- | --- |
| PostgreSQL / MySQL / MariaDB / SQL Server / Oracle / Db2 / AlloyDB Omni | 9表の件数、日本語、BIGINT、DECIMAL、データ偏り、NULL、ビュー、共通SELECTサンプル |
| MongoDB | 顧客3件、受注1200件、偏り、Long/Decimal128 |
| Redis | String/Hash/List/Set/Sorted Set、TTL、検証キーの後片付け |
| ClickHouse | イベント1200件、偏り、Int64/Decimal、準備完了マーカー |
| Spanner Emulator | 顧客3件、受注1200件、偏り、INT64/NUMERIC |

Spannerエミュレーターの再起動後のfixture再作成、AlloyDB OmniとSQL Serverの再起動後の永続データ再開も確認しました。Docker不要の11件のPythonテストではSQLiteのFK・件数・精度、生成SQL、区切りファイル、既存ファイル保護、誤った検証結果の拒否、Spannerの初期化処理などを確認しています。

SQL Serverでは取得元のサーバー権限付与先、起動時のDB回復待ち、DECIMAL値の指数表記によるFLOAT昇格を修正しています。MySQL系クライアントではUTF-8を明示して日本語を照合しました。

この記録は負荷ベンチマーク、HA、PITR、バックアップ復元、外部CDC、全ドキュメント掲載例の実行結果を意味しません。各DBの章にある追加構成手順は公式資料に基づく設計・検証手順として扱います。DuckDBのローカル生成はオプションで、利用者が選ぶパッケージ版で確認してください。

再確認:

```sh
python tools/rava.py up all
python tools/rava.py verify
python -m unittest discover -s tests -v
docker compose --profile "*" config --quiet
```
