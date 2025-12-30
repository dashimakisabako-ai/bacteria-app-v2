import streamlit as st
import google.generativeai as genai
import os

# ---------------------------------------------------------
# デザイン設定
# ---------------------------------------------------------
st.set_page_config(page_title="BactoEtymology AI", page_icon="🧫", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #F0F4F8; }
    h1 { color: #2C3E50; font-family: 'Helvetica Neue', sans-serif; }
    .stTextInput > label { color: #16A085; font-weight: bold; }
    .stButton > button { background-color: #2980B9; color: white; border-radius: 5px; font-weight: bold; }
    .stSuccess { background-color: #D5F5E3; color: #1E8449; }
    </style>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# AI設定
# ---------------------------------------------------------
SYSTEM_PROMPT = """
あなたは細菌学と古典言語（ラテン語・ギリシャ語）の専門家です。
ユーザーが入力した「細菌名（学名）」に対して、以下の構造で解説を出力してください。

出力フォーマット:
## 1. 語源解剖 (Etymological Breakdown)
学名をパーツに分解し、それぞれのラテン語・ギリシャ語の語源と意味を箇条書きで解説してください。

## 2. 名前の意味 (Literal Meaning)
その名前が直訳するとどういう意味になるか。

## 3. 臨床的特徴のヒント (Clinical Context)
名前が示唆する菌の形態や特徴について簡潔に。

## 4. 豆知識 (Did you know?)
その菌に関する興味深い歴史的背景やトリビアを1つ。
"""

# APIキー読み込み
api_key = st.secrets.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# ---------------------------------------------------------
# アプリ画面
# ---------------------------------------------------------
st.title("🧫 Bacterial Nomenclature AI")
st.markdown("細菌名の**語源と由来**を解析する専門ツール")

# ★現在のAPIキーの先頭を表示して、更新されたか確認できるようにします
if api_key:
    st.caption(f"現在のキー: {api_key[:6]}... (Rebootで更新されます)")

bacterium_name = st.text_input("細菌名を入力 (例: Staphylococcus aureus)", "")

if st.button("由来を解析する (Analyze)"):
    if not api_key:
        st.error("APIキーが設定されていません。")
    elif not bacterium_name:
        st.warning("細菌名を入力してください。")
    else:
        # プロンプト結合
        full_prompt = SYSTEM_PROMPT + "\n\nユーザー入力: " + bacterium_name
        
        # ★エラー回避の「二段構え」ロジック
        try:
            with st.spinner("解析中 (Gemini 1.5 Flash)..."):
                # まずは最新のFlashでトライ
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(full_prompt)
                st.success("解析完了 (1.5 Flash)")
                st.markdown(response.text)

        except Exception as e_flash:
            # FlashがダメならProで再トライ（自動バックアップ）
            try:
                with st.spinner(f"Flashモデルが応答しないため、安定版(Pro)に切り替えています..."):
                    model = genai.GenerativeModel("gemini-pro")
                    response = model.generate_content(full_prompt)
                    st.success("解析完了 (Proモデルで実行)")
                    st.markdown(response.text)
            except Exception as e_pro:
                # どっちもダメならエラー表示
                st.error("エラーが発生しました。")
                st.write(f"詳細: {e_flash}")
                st.info("ヒント: Streamlit右上の『Reboot app』を必ず押してください。")
