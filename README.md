# 🍆 New Dicks as a Service (DaaS)

[日本語](README.md) | [English](README_EN.md)

おちんぽ生成API。様々なカテゴリのASCIIアートおちんぽを提供します。
APIを通じて、アプリケーションに簡単に組み込むことができます。

## 🌟 Features

- 多様なカテゴリ（asian, black, white, random）
- 1リクエストで最大100個生成
- リアルタイム統計
- 美しいドキュメントページ

## 🚀 Quick Start

基本的な使用例:
```bash
curl "https://dick.frwi.net/dicks?category=random&count=5"
```

カテゴリ指定の例:
```bash
curl "https://dick.frwi.net/dicks?category=asian&count=3"
```

統計情報の取得:
```bash
curl "https://dick.frwi.net/stats"
```

## 📚 Documentation

詳細なAPIドキュメントは以下で確認できます：
https://dick.frwi.net/docs

## 🔧 Development

### Requirements
[ここ](requirements.txt)

### Setup
```bash
# リポジトリのクローン
git clone https://github.com/FreeWiFi7749/DaaS.git
cd [DaaS/の/パス]

# 仮想環境の作成と有効化
python -m venv .venv
source .venv/bin/activate

# 依存関係のインストール
pip install -r requirements.txt

# 開発サーバーの起動
uvicorn dick:app --reload

# 本番環境での起動
uvicorn dick:app --host 0.0.0.0 --port 8000
```

### Environment Variables
環境変数は`.env`ファイルで管理します：

```bash
# サーバー設定
HOST=0.0.0.0      # サーバーのホスト名
PORT=8000         # サーバーのポート番号
WORKERS=4         # ワーカープロセス数
```

`.env.example`をコピーして`.env`を作成し、適切な値を設定してください：
```bash
cp .env.example .env
```

## 📊 Available Categories

- **asian**: 3-7文字の控えめサイズ
- **black**: 8-15文字の迫力満点サイズ
- **white**: 5-10文字の標準サイズ
- **random**: 3-15文字のランダムサイズ

## 📝 License

[DICK License](LICENSE) (Based on MIT License)
