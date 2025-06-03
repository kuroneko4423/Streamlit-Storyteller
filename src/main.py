import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import yaml
import json
import re
import random

# 環境変数の読み込み
load_dotenv()

# 設定ファイルの読み込み
def load_config(config_path='config.yaml'):
    """
    設定ファイルを読み込む
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        st.error(f"設定ファイル {config_path} が見つかりません。")
        return None
    except yaml.YAMLError as e:
        st.error(f"設定ファイルの読み込み中にエラーが発生しました: {e}")
        return None

# 設定の読み込み
config = load_config()

# Gemini APIの設定
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# モデルの初期化
model = genai.GenerativeModel(os.getenv('GEMINI_MODEL'))

def generate_response(prompt):
    """
    Gemini APIを使用してプロンプトに対する応答を生成
    """
    try:
        response = model.generate_content(prompt)
        # response.text が空または無効な場合のハンドリングを追加
        if not response.text.strip():
            st.error("AIからの応答が空でした。")
            return None
        # print(response.text)
        return response.text
    except Exception as e:
        st.error(f"APIリクエスト中にエラーが発生しました: {e}")
        return None

def check_colon_format(s: str) -> bool:
    """
    文字列が「〇〇：△△」の形式であるか（「：」が1つで、分割すると2つの要素になるか）をチェックします。
    """
    colon_count = s.count('：')
    if colon_count != 1:
        return False
    parts = s.split('：')
    if len(parts) == 2 and all(p.strip() for p in parts): # 各部分が空でないことも確認
        return True
    else:
        return False

def to_full_width_specific(text):
    """
    str.translate() を使って特定の半角文字（コロン）を全角に変換します。
    """
    translation_map = str.maketrans(":", "：")
    return text.translate(translation_map)

def extract_and_parse_json(input_string):
    """
    入力文字列からJSONデータを抽出し、Pythonオブジェクトにパースします。
    """
    markdown_match = re.search(r"```json\n(.*?)```", input_string, re.DOTALL)
    
    if markdown_match:
        json_to_parse = markdown_match.group(1).strip()
        # print("--- MarkdownコードブロックからJSONを抽出しました ---")
    else:
        json_to_parse = input_string.strip()
        # print("--- 純粋なJSON文字列として処理します ---")

    try:
        data = json.loads(json_to_parse)
        return data
    except json.JSONDecodeError as e:
        print(f"エラー: JSONのパースに失敗しました。詳細: {e}")
        return None
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e}")
        return None

def process_ai_response_and_update_history(response_text):
    """
    AIからの応答テキストを処理し、履歴を更新します。
    物語と選択肢を抽出し、セッションステートに保存します。
    """
    parsed_output = extract_and_parse_json(response_text)
    
    if parsed_output is None:
        st.error("AIからの応答がJSON形式ではありませんでした。")
        st.session_state.display_choices = False # 選択肢は表示しない
        return

    # 物語部分の処理
    story_content = parsed_output.get('物語')
    if story_content:
        st.session_state.messages.append({
            'role': 'assistant', 
            'content': story_content
        })
        st.session_state.story += story_content
    else:
        if st.session_state.title == False:
            st.error("AIの応答に「物語」のキーが見つかりませんでした。")
            st.session_state.display_choices = False
            return

    # 選択肢部分の処理
    choices_list = parsed_output.get('選択肢')
    if choices_list and isinstance(choices_list, list) and len(choices_list) >= 3:
        st.session_state.choices_to_display = choices_list[:3] # 最初の3つだけを保存
        st.session_state.display_choices = True # 選択肢を表示するフラグを立てる
        if 'climax' not in st.session_state:
            st.session_state.messages.append({
                'role': 'assistant', 
                'content': '次の行動を選択してください。'
            })
        else:
            st.session_state.messages.append({
                'role': 'assistant', 
                'content': '最後の行動を選択してください。'
            })
    else:
        if st.session_state.ending == False:
            st.error("AIの応答に有効な「選択肢」のリストが見つかりません。")
        st.session_state.display_choices = False # 選択肢は表示しない
    
    if st.session_state.title:
        title_content = parsed_output.get('title')
        if title_content:
            ending_message = config['message']['ending_message']
            message = ending_message.replace("｛タイトル｝", title_content)
            st.session_state.messages.append({
                'role': 'assistant', 
                'content': message
            })
        print(title_content)

def one_in_five_chance() -> bool:
    """
    1/5 (20%) の確率で True を、4/5 (80%) の確率で False を返します。
    """
    # random.random() は 0.0 以上 1.0 未満の浮動小数点数を返す
    # 0.0 から 0.2 (排他的) の範囲であれば True を返す
    return random.random() < 0.2

def main():
    st.title('🤖 AIストーリーテラー')
    st.write('Gemini APIを使用したインタラクティブストーリーテラー')


    if not config:
        st.stop() # 設定ファイルが読み込めなければアプリを停止

    # --- セッションステートの初期化 ---
    if 'messages' not in st.session_state:
        st.session_state.messages = []
        st.session_state.is_first_load = True
        st.session_state.story = ''
        st.session_state.waiting_for_ai_response = False
        st.session_state.display_choices = False # 選択肢を表示するかどうかのフラグ
        st.session_state.choices_to_display = [] # 表示する選択肢のリスト
        st.session_state.ending = False
        st.session_state.title = False
    
    # 初期メッセージの生成（最初の読み込み時のみ）
    if st.session_state.is_first_load and config:
        initial_message = config['message']['initial_message']
        st.session_state.messages.append({
            'role': 'assistant', 
            'content': initial_message
        })
        st.session_state.is_first_load = False
        st.rerun() # 初期メッセージを表示するために再実行

    # チャット履歴の表示
    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'])
    
    # --- AI応答生成トリガー ---
    # 履歴の最後のメッセージがユーザーからのものであり、
    # かつAIが現在応答を生成中でない場合
    if st.session_state.messages and \
       st.session_state.messages[-1]["role"] == "user" and \
       not st.session_state.waiting_for_ai_response:
        
        last_user_message = st.session_state.messages[-1]["content"]
        
        st.session_state.waiting_for_ai_response = True # AI応答待ちフラグを立てる
        st.session_state.display_choices = False # 新しいAI応答のために選択肢をリセット

        with st.chat_message('assistant'):
            with st.spinner('考え中...'):
                response_text = None
                
                # ストーリーがまだ始まっていない場合 (初回入力時)
                if not st.session_state.story:
                    if check_colon_format(last_user_message):
                        prompt = config['prompt']['intro_prompt']
                        parts = last_user_message.split('：')
                        genre = parts[0]
                        theme = parts[1]
                        prompt = prompt.replace("｛ジャンル｝", genre)
                        prompt = prompt.replace("｛テーマ｝", theme)
                        response_text = generate_response(prompt)
                    else:
                        error_message = config['message']['error_message']['input_error01']
                        st.markdown(error_message)
                        st.session_state.messages.append({
                            'role': 'assistant', 
                            'content': error_message
                        })
                        st.session_state.waiting_for_ai_response = False
                        st.rerun() # エラーメッセージを表示してUIを更新
                        return # ここで処理を終了

                else:
                    # ストーリーが進行中の場合 (選択肢による入力時)
                    # ここで、選択肢に応じた次のプロンプトを生成
                    # 例：現在のストーリーと選択された行動をAIに伝えるプロンプト
                    # 注意: 実際のプロンプトはAIの設計に合わせて調整してください
                    if 'climax' not in st.session_state:
                        if one_in_five_chance():
                            prompt = config['prompt']['climax_prompt']
                            st.session_state.climax = True
                        else:
                            prompt = config['prompt']['nomal_prompt']
                    else:
                        prompt = config['prompt']['ending_prompt']
                        st.session_state.ending = True
                    
                    prompt = prompt.replace("｛これまでのストーリー｝", st.session_state.story)
                    prompt = prompt.replace("｛ユーザーの選択｝", last_user_message)
                    # continue_prompt = f"現在の状況:\n{st.session_state.story}\n\nユーザーの選択: {last_user_message}\n\nこの選択に基づいて、物語の次の部分と3つの新しい選択肢を以下のJSON形式で提供してください。\n```json\n{{\n  \"物語\": \"物語の続きのテキスト\",\n  \"選択肢\": [\n    \"選択肢1のテキスト\",\n    \"選択肢2のテキスト\",\n    \"選択肢3のテキスト\"\n  ]\n}}\n```"
                    response_text = generate_response(prompt)

            # AI応答を処理し、履歴と選択肢を更新
            if response_text:
                process_ai_response_and_update_history(response_text)
            else:
                # AI応答がNoneの場合（APIエラーなど）
                st.session_state.display_choices = False # 選択肢は表示しない
            
            if st.session_state.ending:
                st.session_state.title = True
                prompt = config['prompt']['title_prompt']
                prompt = prompt.replace("｛物語の内容｝", st.session_state.story)
                response_text = generate_response(prompt)
                process_ai_response_and_update_history(response_text)

            st.session_state.waiting_for_ai_response = False # AI応答待ちフラグをリセット
            st.rerun() # AI応答が表示されたら再度実行してUIを更新 (ここで選択肢も描画される)

    # --- 選択肢ボタンの表示 ---
    # display_choices フラグがTrueの場合のみ表示
    if st.session_state.display_choices and st.session_state.choices_to_display:
        # st.markdown('次の行動を選択してください。') # 再表示されるため、必要であればコメントアウト
        cols = st.columns(len(st.session_state.choices_to_display))
        for i, choice in enumerate(st.session_state.choices_to_display):
            with cols[i]:
                if st.button(choice, key=f"choice_button_{i}"):
                    # ユーザーメッセージを履歴に追加
                    st.session_state.messages.append({
                        'role': 'user', 
                        'content': choice
                    })
                    st.session_state.display_choices = False # ボタンを押したら選択肢を一時的に非表示
                    st.session_state.choices_to_display = [] # 選択肢をクリア
                    st.rerun() # ボタンが押されたら再実行して表示を更新


    # ユーザー入力フィールド
    # AIが応答を生成中の場合は無効にする
    if not st.session_state.waiting_for_ai_response:
        # ユーザー入力。手動で入力された場合のみこのブロックに入る
        user_input_from_chat_input = st.chat_input('メッセージを入力してください', key="chat_input", disabled=st.session_state.ending)
        if user_input_from_chat_input:
            user_input_from_chat_input = to_full_width_specific(user_input_from_chat_input)
            # 手動で入力されたメッセージを履歴に追加
            st.session_state.messages.append({
                'role': 'user', 
                'content': user_input_from_chat_input
            })
            # UIに手動入力されたメッセージを表示 (chat_messageで表示されるので通常は不要だが、即時性を求めるなら)
            # with st.chat_message('user'):
            #     st.markdown(user_input_from_chat_input)
            st.rerun() # 新しい入力があったら再実行してAI応答をトリガー

if __name__ == '__main__':
    main()