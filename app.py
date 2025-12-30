import streamlit as st
import google.generativeai as genai
import importlib.metadata

st.title("🛠 アプリ診断モード")

# 1. ライブラリのバージョン確認
try:
    version = importlib.metadata.version("google-generativeai")
    st.write(f"📦 インストールされているライブラリのバージョン: **{version}**")
    
    # バージョンが 0.3.0 などの古いものだと動きません。
    # 0.8.3 以上になっているか確認します。
    if version < "0.7.0":
        st.error("❌ バージョンが古すぎます。requirements.txt が正しく読み込まれていません。")
    else:
        st.success("✅ バージョンはOKです。")
        
except Exception as e:
    st.error(f"ライブラリのバージョン確認エラー: {e}")

# 2. APIキーの確認
api_key = st.secrets.get("GEMINI_API_KEY", "")
st.write("🔑 APIキーの状態確認:")
if not api_key:
    st.error("❌ APIキーが読み込めていません。Secretsの設定を確認してください。")
else:
    # キーの先頭5文字だけ表示して確認（全部は表示しません）
    mask_key = api_key[:5] + "..."
    st.info(f"読み込まれたキー: {mask_key} (文字数: {len(api_key)})")
    
    # キーの形式チェック
    if not api_key.startswith("AIza"):
        st.warning("⚠️ 注意: Google AI Studioのキーは通常 'AIza' で始まります。")

# 3. 使えるモデルの一覧を取得（これができれば通信成功）
if st.button("使用可能なモデル一覧を取得"):
    if api_key:
        genai.configure(api_key=api_key)
        try:
            st.write("通信テスト中...")
            models = genai.list_models()
            found_models = []
            for m in models:
                if 'generateContent' in m.supported_generation_methods:
                    found_models.append(m.name)
            
            st.success("✅ 通信成功！以下のモデルが使用可能です：")
            st.json(found_models)
            
        except Exception as e:
            st.error("❌ 通信エラー発生")
            st.code(e)
            st.write("↑このエラーメッセージが原因の正体です。")
    else:
        st.error("APIキーがないためテストできません。")
