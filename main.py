"""
このファイルは、Webアプリのメイン処理が記述されたファイルです。
"""

############################################################
# 1. ライブラリの読み込み
############################################################
# 「.env」ファイルから環境変数を読み込むための関数
from dotenv import load_dotenv
# ログ出力を行うためのモジュール
import logging
# streamlitアプリの表示を担当するモジュール
import streamlit as st
# （自作）画面表示以外の様々な関数が定義されているモジュール
import utils
# （自作）アプリ起動時に実行される初期化処理が記述された関数
from initialize import initialize
# （自作）画面表示系の関数が定義されているモジュール
import components as cn
# （自作）変数（定数）がまとめて定義・管理されているモジュール
import constants as ct


############################################################
# 2. 設定関連
############################################################
# ブラウザタブの表示文言を設定
st.set_page_config(
    page_title=ct.APP_NAME if hasattr(ct, "APP_NAME") else "社内情報特化型生成AI検索アプリ",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ログ出力を行うためのロガーの設定
logger = logging.getLogger(ct.LOGGER_NAME)


############################################################
# 3. 初期化処理
############################################################
try:
    # 初期化処理（「initialize.py」の「initialize」関数を実行）
    initialize()
except Exception as e:
    # エラーログの出力
    logger.error(f"{ct.INITIALIZE_ERROR_MESSAGE}\n{e}")
    # エラーメッセージの画面表示
    st.error(utils.build_error_message(ct.INITIALIZE_ERROR_MESSAGE), icon=ct.ERROR_ICON)
    # 後続の処理を中断
    st.stop()

# アプリ起動時のログファイルへの出力
if not "initialized" in st.session_state:
    st.session_state.initialized = True
    logger.info(ct.APP_BOOT_MESSAGE)


############################################################
# 4. 初期表示
############################################################

# タイトル（画像と同じ大見出し）
st.title("社内情報特化型生成AI検索アプリ")

# サイドバー：利用目的＋説明カード＋入力例（重複なし、選択時は緑）
with st.sidebar:
    st.header("利用目的")

    # ラジオで選択（内部モードの同期のみ行い、ここでは説明を描画しない）
    mode_choice = st.radio("モード選択", ["社内文書検索", "社内問い合わせ"], index=0, key="mode_radio", label_visibility="collapsed")
    if mode_choice == "社内文書検索":
        st.session_state.mode = getattr(ct, "ANSWER_MODE_1", "社内文書検索")
    else:
        st.session_state.mode = getattr(ct, "ANSWER_MODE_2", "社内問い合わせ")

    # 常時2つの説明カードを表示し、選択中のみ緑（success）
    # --- 社内文書検索 ---
    st.markdown("**『社内文書検索』を選択した場合**")
    if mode_choice == "社内文書検索":
        st.success("入力内容と関連性が高い社内文書のありかを検索できます。")
    else:
        st.info("入力内容と関連性が高い社内文書のありかを検索できます。")
    st.caption("【入力例】\n社員の育成方針に関するMTGの議事録")

    # --- 社内問い合わせ ---
    st.markdown("**『社内問い合わせ』を選択した場合**")
    if mode_choice == "社内問い合わせ":
        st.success("質問・要望に対して、社内文書の情報をもとに回答を得られます。")
    else:
        st.info("質問・要望に対して、社内文書の情報をもとに回答を得られます。")
    st.caption("【入力例】\n人事部に所属している従業員情報を一覧化して")


# 中央の緑・黄メッセージ
st.success(
    "こんにちは。私は社内文書の情報をもとに回答する生成AIチャットボットです。"
    "サイドバーで利用目的を選択し、画面下部のチャット欄からメッセージを送信してください。"
)
st.warning("具体的に入力したほうが期待通りの回答を得やすいです。")


############################################################
# 5. 会話ログの表示
############################################################
try:
    # 会話ログの表示
    cn.display_conversation_log()
except Exception as e:
    # エラーログの出力
    logger.error(f"{ct.CONVERSATION_LOG_ERROR_MESSAGE}\n{e}")
    # エラーメッセージの画面表示
    st.error(utils.build_error_message(ct.CONVERSATION_LOG_ERROR_MESSAGE), icon=ct.ERROR_ICON)
    # 後続の処理を中断
    st.stop()


############################################################
# 6. チャット入力の受け付け
############################################################
chat_placeholder = "こちらからメッセージを送信してください。"
helper_text = getattr(ct, "CHAT_INPUT_HELPER_TEXT", chat_placeholder)
chat_message = st.chat_input(helper_text or chat_placeholder)


############################################################
# 7. チャット送信時の処理
############################################################
if chat_message:
    # ==========================================
    # 7-1. ユーザーメッセージの表示
    # ==========================================
    # ユーザーメッセージのログ出力
    logger.info({"message": chat_message, "application_mode": st.session_state.mode})

    # ユーザーメッセージを表示
    with st.chat_message("user"):
        st.markdown(chat_message)

    # ==========================================
    # 7-2. LLMからの回答取得
    # ==========================================
    # 「st.spinner」でグルグル回っている間、表示の不具合が発生しないよう空のエリアを表示
    res_box = st.empty()
    # LLMによる回答生成（回答生成が完了するまでグルグル回す）
    with st.spinner(ct.SPINNER_TEXT):
        try:
            # 画面読み込み時に作成したRetrieverを使い、Chainを実行
            llm_response = utils.get_llm_response(chat_message)
        except Exception as e:
            # エラーログの出力
            logger.error(f"{ct.GET_LLM_RESPONSE_ERROR_MESSAGE}\n{e}")
            # エラーメッセージの画面表示
            st.error(utils.build_error_message(ct.GET_LLM_RESPONSE_ERROR_MESSAGE), icon=ct.ERROR_ICON)
            # 後続の処理を中断
            st.stop()
    
    # ==========================================
    # 7-3. LLMからの回答表示
    # ==========================================
    with st.chat_message("assistant"):
        try:
            # ==========================================
            # モードが「社内文書検索」の場合
            # ==========================================
            if st.session_state.mode == ct.ANSWER_MODE_1:
                # 入力内容と関連性が高い社内文書のありかを表示
                content = cn.display_search_llm_response(llm_response)

            # ==========================================
            # モードが「社内問い合わせ」の場合
            # ==========================================
            elif st.session_state.mode == ct.ANSWER_MODE_2:
                # 入力に対しての回答と、参照した文書のありかを表示
                content = cn.display_contact_llm_response(llm_response)
            
            # AIメッセージのログ出力
            logger.info({"message": content, "application_mode": st.session_state.mode})
        except Exception as e:
            # エラーログの出力
            logger.error(f"{ct.DISP_ANSWER_ERROR_MESSAGE}\n{e}")
            # エラーメッセージの画面表示
            st.error(utils.build_error_message(ct.DISP_ANSWER_ERROR_MESSAGE), icon=ct.ERROR_ICON)
            # 後続の処理を中断
            st.stop()

    # ==========================================
    # 7-4. 会話ログへの追加
    # ==========================================
    # 表示用の会話ログにユーザーメッセージを追加
    st.session_state.messages.append({"role": "user", "content": chat_message})
    # 表示用の会話ログにAIメッセージを追加
    st.session_state.messages.append({"role": "assistant", "content": content})