# 社内検索アプリケーション

このアプリケーションは、社内文書の検索とQ&Aを行うためのStreamlitベースのWebアプリケーションです。OpenAI APIとLangChainを使用してRAG（Retrieval-Augmented Generation）機能を実装しています。

## 機能

### 1. 社内文書検索
- 入力したクエリに関連する社内文書を検索
- 関連度の高い文書の場所と内容を表示

### 2. 社内問い合わせ
- 自然言語での質問に対して、社内文書を参照した回答を生成
- 参照した文書の詳細情報も合わせて表示

## 技術スタック

- **フロントエンド**: Streamlit
- **AI/機械学習**: OpenAI API, LangChain
- **ベクトルデータベース**: ChromaDB
- **文書処理**: python-docx, lxml, beautifulsoup4
- **その他**: python-dotenv, logging

## セットアップ

### 1. 環境の準備

```bash
# 仮想環境の作成
python -m venv env

# 仮想環境の有効化 (Windows)
env\Scripts\activate

# 仮想環境の有効化 (Mac/Linux)
source env/bin/activate
```

### 2. 依存関係のインストール

```bash
# Windows
pip install -r requirements_windows.txt

# Mac
pip install -r requirements_mac.txt
```

### 3. 環境変数の設定

`.env`ファイルを作成し、OpenAI APIキーを設定してください：

```
OPENAI_API_KEY=your_openai_api_key_here
```

### 4. アプリケーションの起動

```bash
streamlit run main.py
```

アプリケーションは `http://localhost:8501` で利用できます。

## ファイル構成

```
company_inner_search_app/
├── main.py                 # メインアプリケーション
├── initialize.py           # 初期化処理
├── components.py          # UI コンポーネント
├── utils.py               # ユーティリティ関数
├── constants.py           # 定数定義
├── requirements_windows.txt # Windows用依存関係
├── requirements_mac.txt   # Mac用依存関係
├── .env                   # 環境変数（GitHubには含めない）
├── .gitignore            # Git除外設定
└── data/                 # 社内文書データ
    ├── MTG議事録/
    ├── サービスについて/
    ├── 会社について/
    ├── 顧客について/
    └── 社員について/
```

## 使用方法

1. アプリケーションを起動後、ブラウザでアクセス
2. 画面上部でモードを選択：
   - **社内文書検索**: 関連文書の検索
   - **社内問い合わせ**: Q&A形式での問い合わせ
3. チャット入力欄に質問や検索クエリを入力
4. AIが社内文書を参照して回答を生成

## 注意事項

- OpenAI APIキーが必要です
- 初回起動時に文書の前処理が実行されるため、起動に時間がかかる場合があります
- `data/`フォルダ内の文書が検索対象となります

## ライセンス

このプロジェクトは社内利用を目的としています。