import streamlit as st
import google.generativeai as genai
import os

# ---------------------------------------------------------
# 1. デザイン設定 (Clean Lab Aesthetic)
# ---------------------------------------------------------
st.set_page_config(
    page_title="BactoEtymology AI",
    page_icon="🧫",
    layout="centered"
)

# 清潔感のある「臨床検査室」風のデザイン
st.markdown("""
    <style>
    .stApp {
        background-color: #F0F4F8; /* 薄いグレーブルー */
    }
    h1 {
        color: #2C3E50; /* 濃いグレー */
        font-family: 'Helvetica Neue', sans-serif;
    }
    .stTextInput > label {
        color: #16A085; /* 落ち着いたグリーン */
        font-weight: bold;
    }
    .stButton > button {
        background-color: #2980B9; /* 濃い青 */
        color: white;
        border-radius: 5px;
        font-weight: bold;
    }
    .stMarkdown h2 {
        color: #27AE60; /* 緑 */
        border-bottom: 2px solid #BDC3C7;
        padding-bottom: 5px;
        margin-top: 20px;
    }
    .stSuccess {
        background-color: #D5F5E3;
        color: #1E8449;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. AIの設定 (あなたのAI Studio設定を完全再現)
# ---------------------------------------------------------
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
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    pass

# ---------------------------------------------------------
# 3. アプリ画面
# ---------------------------------------------------------
st.title("🧫 Bacterial Nomenclature AI")
st.markdown("細菌名の**語源と由来**を解析する専門ツール")

# 入力フォーム
bacterium_name = st.text_input("細菌名を入力してください (例: Staphylococcus aureus)", "")

# 実行ボタン
if st.button("由来を解析する (Analyze)"):
    if not bacterium_name:
        st.warning("まずは細菌名を入力してください。")
    else:
        try:
            # バージョン0.8.6なので、最新のFlashモデルが確実に使えます
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction=SYSTEM_PROMPT
            )
            
            with st.spinner("文献データベースと語源を照合中..."):
                response = model.generate_content(bacterium_name)
            
            # 結果表示
            st.success("解析完了")
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
            st.info("APIキーの権限や通信状態を確認してください。")

# フッター
st.markdown("---")
st.caption("Powered by Google Gemini 1.5 Flash | Designed for Clinical Laboratory Scientists")
