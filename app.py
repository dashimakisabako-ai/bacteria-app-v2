import streamlit as st
import google.generativeai as genai
import os

# ---------------------------------------------------------
# 1. デザイン設定
# ---------------------------------------------------------
st.set_page_config(
    page_title="BactoEtymology AI",
    page_icon="🧫",
    layout="centered"
)

st.markdown("""
    <style>
    .stApp {
        background-color: #F0F4F8;
    }
    h1 {
        color: #2C3E50;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .stTextInput > label {
        color: #16A085;
        font-weight: bold;
    }
    .stButton > button {
        background-color: #2980B9;
        color: white;
        border-radius: 5px;
    }
    .stMarkdown h2 {
        color: #27AE60;
        border-bottom: 2px solid #BDC3C7;
        padding-bottom: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. AIの設定
# ---------------------------------------------------------
# システム指示
SYSTEM_PROMPT = """
あなたは細菌学と古典言語（ラテン語・ギリシャ語）の専門家です。
ユーザーが入力した「細菌名（学名）」に対して、以下の構造で解説を出力してください。
臨床検査技師にとって有益な、科学的かつ教育的なトーンを維持してください。

出力フォーマット:
## 1. 語源解剖 (Etymological Breakdown)
学名をパーツに分解し、それぞれのラテン語・ギリシャ語の語源と意味を箇条書きで解説してください。
（例：Staphylococcus -> Staphyle（ブドウの房）+ kokkos（球））

## 2. 名前の意味 (Literal Meaning)
その名前が直訳するとどういう意味になるか。

## 3. 臨床的特徴のヒント (Clinical Context)
名前が示唆する菌の形態や特徴について簡潔に。

## 4. 豆知識 (Did you know?)
その菌に関する興味深い歴史的背景やトリビアを1つ。
"""

# APIキーの読み込み
try:
    # Streamlit CloudのSecretsから読み込み
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except:
    pass

# ---------------------------------------------------------
# 3. アプリの画面構成
# ---------------------------------------------------------
st.title("🧫 Bacterial Nomenclature AI")
st.markdown("細菌名の**語源と由来**を解析する専門ツール")

bacterium_name = st.text_input("細菌名を入力 (例: Staphylococcus aureus)", "")

if st.button("由来を解析する"):
    if not bacterium_name:
        st.warning("細菌名を入力してください。")
    else:
        try:
            # 【修正点】モデルを安定版の 'gemini-pro' に変更
            model = genai.GenerativeModel("gemini-pro")
            
            # 【修正点】システム指示をプロンプト本文に結合して送信（これでエラー回避）
            full_prompt = SYSTEM_PROMPT + "\n\nユーザーの入力した菌名: " + bacterium_name
            
            with st.spinner("文献を検索中..."):
                response = model.generate_content(full_prompt)
            
            st.success("解析完了")
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
            st.info("APIキーの設定を確認してください。")
