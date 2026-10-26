# DuckDB — 基本的な設計思想

[DB別目次](README.md) · [全体目次](../README.md)

対象: インストールしたDuckDBの版 / version()で確認 / 確認日: 2026-10-26

## この章の目次

- [用途とワークロード](#section-1)
- [格納方式とアクセス経路](#section-2)
- [トランザクションと整合性](#section-3)
- [モデル設計と避けたい設計](#section-4)
- [Ravaでの観察ポイント](#section-5)
- [確認用の例と検証手順](#examples)
- [公式資料と適用範囲](#sources)

<a id="section-1"></a>

## 用途とワークロード

プロセスに組み込む分析用の列指向DBです。CSV/Parquet等を直接読む分析とローカル集計に適し、多数クライアントが高頻度で行更新するサーバーOLTPとは役割を分けます。

<a id="section-2"></a>

## 格納方式とアクセス経路

列指向・vectorized execution・parallel scanで必要列を処理します。row group/統計による読み飛ばしや圧縮を利用し、ART索引を行指向DBの全用途のB-tree代替とは考えません。

<a id="section-3"></a>

## トランザクションと整合性

単一プロセス内でMVCCと楽観的同時実行を使います。複数プロセスから同じnative DBへ同時書込みするサーバーモデルは既定ではなく、writer所有権をアプリ側で管理します。

<a id="section-4"></a>

## モデル設計と避けたい設計

分析対象を列・型・partition・ファイル配置から設計します。正確なDECIMALとHUGEINT等の範囲、external file schema、NULLとtimezoneを仕様化します。

<a id="section-5"></a>

## Ravaでの観察ポイント

Ravaの共通受注モデルを生成SQLから作ります。小規模fixtureは型と構文検証に用い、Parquetや大量scanの性能は別の拡大データで評価します。

<a id="examples"></a>

## 確認用の例と検証手順

```sql
SELECT version();
SELECT * FROM duckdb_settings() WHERE name IN ('threads','memory_limit','temp_directory');
```

<a id="sources"></a>

## 公式資料と適用範囲

現在の検証環境: Python追加パッケージでローカルファイル生成。サーバー/HA/標準CDCなし。

[概要](https://duckdb.org/docs/stable/) · [同時実行](https://duckdb.org/docs/stable/connect/concurrency)
