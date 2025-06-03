# AIチャットボット with Streamlit and Gemini API

## 必要条件
- Python 3.8+
- pip

## セットアップ

1. リポジトリをクローン
```bash
git clone https://github.com/kuroneko4423/Streamlit-Storyteller.git
cd streamlit-gemini-chatbot
```

2. 仮想環境の作成と有効化（推奨）
```bash
python -m venv venv
source venv/bin/activate  # Windowsの場合: venv\Scripts\activate
```

3. 依存関係のインストール
```bash
pip install -r requirements.txt
```

4. 環境変数の設定
`.env`ファイルを作成し、以下の内容を追加
```
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash-preview-05-20
```

## APIキーの取得
1. [Google AI Studio](https://makersuite.google.com/app/apikey)にアクセス
2. 新しいAPIキーを生成
3. `.env`ファイルに貼り付け

## 実行方法
```bash
streamlit run src/main.py
```

## 機能
- Gemini APIを使用したインタラクティブストーリーテリングチャットボット
- ジャンルとテーマに基づく物語生成
- 動的な選択肢による物語の展開
- チャット履歴の保持
- エラーハンドリング

## 注意
- APIキーは機密情報です。絶対に公開しないでください
- `.env`ファイルは`.gitignore`に追加されています

## トラブルシューティング
- 依存関係のインストールに失敗した場合は、pipを最新版に更新してください
  ```bash
  pip install --upgrade pip
  ```
- APIキーが正しく設定されていることを確認してください
- `config.yaml`ファイルが正しく設定されていることを確認してください

## ライセンス
[適切なライセンスを追加]