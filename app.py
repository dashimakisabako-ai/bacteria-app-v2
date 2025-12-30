import streamlit as st
import google.generativeai as genai

# ==========================================
# 【緊急対応】ここにAPIキーを直接貼ってください
# ※ "" の中にキーを入れます (例: "AIzaSy...")
# ==========================================
MY_DIRECT_KEY = "AIzaSyDh8o42DRYP4keFZxIC5zQlIGw0lij6KLQ" 

# ---------------------------------------------------------
# デザイン設定
# ---------------------------------------------------------
st.set_page_config(page_title="BactoEtymology AI", page_icon="🧫")
st.markdown("""<style>.stApp { background-color: #F0F4F8; } h1 { color: #2C3E50; }</style>""", unsafe_allow_html=True)
st.title("🧫 Bacterial Nomenclature AI")

# ---------------------------------------------------------
# 万能型AI接続ロジック（どれか一つでも動けばOK）
# ---------------------------------------------------------
if st.button("由来を解析する"):
    if "AIza" not in MY_DIRECT_KEY:
        st.error("⚠️ コード内の `MY_DIRECT_KEY` にキーが貼り付けられていません！")
    else:
        # キーを設定
        genai.configure(api_key=MY_DIRECT_KEY)
        
        # 入力がない場合はサンプルを使用
        target_name = st.text_input("細菌名", "Staphylococcus aureus")
        
        # 使えるモデルを総当たりで試すリスト
        models_to_test = [
            "gemini-1.5-flash", 
            "gemini-1.5-flash-001",
            "gemini-1.5-pro",
            "gemini-pro"
        ]
        
        success = False
        st.write("接続テストを開始します...")
        
        for model_name in models_to_test:
            try:
                # モデルを定義して通信トライ
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(f"細菌名「{target_name}」の語源を3行で解説して。")
                
                # 成功したら表示
                st.success(f"✅ 成功しました！ (使用モデル: {model_name})")
                st.info(response.text)
                success = True
                break # ループを抜ける
                
            except Exception as e:
                # 失敗したら次へ
                st.write(f"❌ {model_name} はダメでした...")
        
        if not success:
            st.error("全てのモデルで通信に失敗しました。APIキー自体が無効になっている可能性があります。")
