# SQLite — バックアップと復旧

[DB別目次](README.md) · [全体目次](../README.md)

対象: 利用するPython/CLIに同梱されたSQLite 3 / sqlite_version()で確認 / 確認日: 2026-10-26

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

Online Backup API、CLI .backup、VACUUM INTO、一貫した停止時コピーを使い分けます。SQL dumpは移行用で、BLOBや型・schemaの復元も検証します。

<a id="section-2"></a>

## 取得時の整合性と前提条件

更新中やWAL modeでDB本体だけをコピーすると確定済みのWAL内容を失う恐れがあります。Backup APIで一貫したsnapshotを作り、稼働中の複数ファイルの個別コピーは避けます。

<a id="section-3"></a>

## 増分・差分・時点復旧

標準SQLiteには継続したarchive logベースの汎用PITRはありません。WALをそのまま外部CDC/増分保管へ流用せず、外部ツールの復旧保証と保持方式を別途評価します。

<a id="section-4"></a>

## 復元と切り戻しの手順

別パスへbackupを作成し、新しい接続で開いてintegrity_check/foreign_key_checkを行います。切り替え時は全接続を閉じ、旧ファイルを残したまま新パスへアプリを向けます。

<a id="section-5"></a>

## 復旧訓練・保持・暗号化

件数・大整数・小数TEXT・FK・view/trigger・application/user versionを照合します。file permission、ディスク満杯、WAL未checkpoint、途中中断と復元時間を試します。

<a id="examples"></a>

## 確認用の例と検証手順

Python標準APIの例です。出力先は新しいパスを用意し、既存ファイルへ上書きしません。

```python
import sqlite3
source = sqlite3.connect('file:.local/dblab.sqlite?mode=ro', uri=True)
target = sqlite3.connect('.local/dblab-copy.sqlite')
try:
    source.backup(target)
finally:
    target.close()
    source.close()
```
別接続でコピーを開き、PRAGMA integrity_checkとデータ照合を行います。

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: Python標準ライブラリからローカルファイルを生成。サーバー/HA/CDC拡張は未構成。

[Backup API](https://www.sqlite.org/backup.html) · [VACUUM INTO](https://www.sqlite.org/lang_vacuum.html)
