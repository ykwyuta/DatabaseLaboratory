# IBM Db2

[全DBの目次](../README.md)

対象: Db2 LUW Community 12.1.5.0。確認日: 2026-10-26。

DatabaseLaboratory構成: 単体インスタンスdb2inst1とDBLAB DB。HADR/外部CDCは未構成。

## 起動と接続

```sh
python tools/dblab.py up db2
python tools/dblab.py verify db2
```

接続先・ポート・公開された検証用資格情報は[ルートREADME](../../README.md#接続先)を参照してください。

## 詳細目次

### 1. [基本的な設計思想](01-design.md)

- [1.1 用途とワークロード](01-design.md#section-1)
- [1.2 格納方式とアクセス経路](01-design.md#section-2)
- [1.3 トランザクションと整合性](01-design.md#section-3)
- [1.4 モデル設計と避けたい設計](01-design.md#section-4)
- [1.5 DatabaseLaboratoryでの観察ポイント](01-design.md#section-5)
- [1.6 確認用の例と検証手順](01-design.md#examples)
- [1.7 公式資料と適用範囲](01-design.md#sources)

### 2. [性能分析手法](02-performance.md)

- [2.1 測定条件と再現性](02-performance.md#section-1)
- [2.2 実行計画の取得と読み方](02-performance.md#section-2)
- [2.3 SQL統計とボトルネックの特定](02-performance.md#section-3)
- [2.4 ロックと待機の分析](02-performance.md#section-4)
- [2.5 資源と改善効果の確認](02-performance.md#section-5)
- [2.6 確認用の例と検証手順](02-performance.md#examples)
- [2.7 公式資料と適用範囲](02-performance.md#sources)

### 3. [SQLの構文差異](03-sql.md)

- [3.1 方言と識別子](03-sql.md#section-1)
- [3.2 型・精度・NULL・文字列](03-sql.md#section-2)
- [3.3 ページング・日付・集約](03-sql.md#section-3)
- [3.4 更新・UPSERT・採番](03-sql.md#section-4)
- [3.5 DDL・トランザクション・パラメーター](03-sql.md#section-5)
- [3.6 確認用の例と検証手順](03-sql.md#examples)
- [3.7 公式資料と適用範囲](03-sql.md#sources)

### 4. [運用観点の情報取得方法](04-operations.md)

- [4.1 接続先・バージョン・設定](04-operations.md#section-1)
- [4.2 セッション・処理・ロック](04-operations.md#section-2)
- [4.3 容量・ログ・保持期間](04-operations.md#section-3)
- [4.4 メタデータ・権限・セキュリティ](04-operations.md#section-4)
- [4.5 定期取得と障害時の採取順序](04-operations.md#section-5)
- [4.6 確認用の例と検証手順](04-operations.md#examples)
- [4.7 公式資料と適用範囲](04-operations.md#sources)

### 5. [バックアップと復旧](05-backup.md)

- [5.1 保護対象と方式の選択](05-backup.md#section-1)
- [5.2 取得時の整合性と前提条件](05-backup.md#section-2)
- [5.3 増分・差分・時点復旧](05-backup.md#section-3)
- [5.4 復元と切り戻しの手順](05-backup.md#section-4)
- [5.5 復旧訓練・保持・暗号化](05-backup.md#section-5)
- [5.6 確認用の例と検証手順](05-backup.md#examples)
- [5.7 公式資料と適用範囲](05-backup.md#sources)

### 6. [冗長化と障害復旧](06-ha.md)

- [6.1 構成と障害ドメイン](06-ha.md#section-1)
- [6.2 同期方式と読み取り整合性](06-ha.md#section-2)
- [6.3 昇格・接続先切り替え・再参加](06-ha.md#section-3)
- [6.4 遅延監視とスプリットブレイン対策](06-ha.md#section-4)
- [6.5 RPO・RTOと障害試験](06-ha.md#section-5)
- [6.6 確認用の例と検証手順](06-ha.md#examples)
- [6.7 公式資料と適用範囲](06-ha.md#sources)

### 7. [差分配信方式](07-cdc.md)

- [7.1 差分の取得元と配信経路](07-cdc.md#section-1)
- [7.2 初期ロードと増分の境界](07-cdc.md#section-2)
- [7.3 順序・チェックポイント・再開](07-cdc.md#section-3)
- [7.4 削除・DDL・型変更への対応](07-cdc.md#section-4)
- [7.5 配信先の冪等性と監視](07-cdc.md#section-5)
- [7.6 確認用の例と検証手順](07-cdc.md#examples)
- [7.7 公式資料と適用範囲](07-cdc.md#sources)
