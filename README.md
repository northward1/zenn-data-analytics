# zenn-data-analytics

[2026年にZennに投稿された5.2万件の記事のデータ分析:アルゴリズム導入やPublicationによるLike数の変化など](https://zenn.dev/northward/articles/zenn-data-analysis-2026)で分析したデータや、記事中で貼った図や表を作成するためのスクリプトを置いています。

## 環境構築・スクリプトの実行手順

まず、[`uv`](https://docs.astral.sh/uv/)が使用可能な状態で、`uv sync`を実行します。

そのあと、`scripts/`にあるスクリプトを順に実行します。

### 各ディレクトリの役割

* `data.jsonl`: 匿名化処理を施したデータ
* `scripts/`: 図や表を生成するためのスクリプト
* `images/`: スクリプトを実行して生成された図が配置されているディレクトリ
