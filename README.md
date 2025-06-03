# 🤖 AIストーリーテラー

## 概要

AIストーリーテラーは、Google Gemini APIを活用した対話型インタラクティブストーリーアプリケーションです。ユーザーは物語のジャンルとテーマを指定し、AIと協力して物語を作り上げることができます。

### 主な機能

- 🎲 ダイナミックなストーリー生成
- 🔀 ユーザー選択による物語の分岐
- 🤖 AIによる自然な物語展開
- 🌈 多様なジャンルとテーマのサポート
- 📖 物語のタイトル自動生成

## 新機能

- 全角コロン（：）の自動変換
- ストーリーの終盤と最終タイトル生成
- より柔軟な物語展開オプション

## 必要要件

- Python 3.9+
- Gemini API キー

## セットアップ手順

### 1. リポジトリのクローン

```bash
git clone https://github.com/kuroneko4423/Streamlit-Storyteller.git
cd ai-storyteller
```

### 2. 仮想環境の作成と有効化

```bash
python -m venv venv
source venv/bin/activate  # Windowsの場合: venv\Scripts\activate
```

### 3. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 4. 環境変数の設定

`.env.example` をコピーして `.env` ファイルを作成し、Gemini API キーを設定します：

```bash
cp .env.example .env
```

`.env` ファイルを編集：

```
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash-preview-05-20
```

## アプリケーションの実行

```bash
streamlit run src/main.py
```

## 使用方法

1. アプリを起動後、「ジャンル：テーマ」の形式で物語を開始します。
   - 例: `ファンタジー：森で迷った少女`

2. AIが物語の導入部を生成し、3つの選択肢を提示します。

3. 選択肢を選ぶことで、物語が展開されます。

4. ストーリーの終盤では、AIが自動的にタイトルを生成します。

## 設定のカスタマイズ

`config.yaml` で以下の項目をカスタマイズできます：
- アプリケーションタイトル
- 初期メッセージ
- エラーメッセージ
- プロンプトテンプレート

## 新しい入力形式

- 全角コロン（：）を使用した入力が可能
- 自動的に全角コロンに変換されます

## トラブルシューティング

- API キーが無効な場合、アプリケーションは起動しません。
- インターネット接続が必要です。
- Python と pip が正しくインストールされていることを確認してください。

## 今後の改善点

- [ ] 多言語サポート
- [ ] ストーリー保存機能
- [ ] テーマとジャンルのバリデーション
- [ ] よりインタラクティブな UI
- [ ] ストーリー分岐の詳細な制御

## ライセンス

MIT License

## 貢献

プルリクエストや機能提案を歓迎します。詳細は CONTRIBUTING.md を参照してください。

## 謝辞

- [Streamlit](https://streamlit.io/)
- [Google Generative AI](https://ai.google/tools/gemini/)