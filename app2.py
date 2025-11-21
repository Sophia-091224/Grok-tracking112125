import streamlit as st
import pandas as pd
import yaml
import os
from agents.orchestrator import TraceabilityOrchestrator
from utils.llm import LLMProvider

st.set_page_config(page_title="🐔 食品溯源AI系統 v2.0", layout="wide")
st.title("🐔 食品溯源AI系統 - Food Traceability AI System")
st.markdown("### 台灣蛋品冷鏈完整追溯 · 31個專業AI代理協同分析")

# --- Sidebar 設定 ---
with st.sidebar:
    st.header("🔑 API Key 設定")
    openai_key = st.text_input("OpenAI API Key", type="password", value=os.getenv("OPENAI_API_KEY", ""))
    gemini_key = st.text_input("Gemini API Key", type="password", value=os.getenv("GEMINI_API_KEY", ""))
    groq_key = st.text_input("Grok API Key (groq)", type="password", value=os.getenv("GROQ_API_KEY", ""))
    
    st.header("⚙️ 模型選擇")
    default_model = st.selectbox("主力模型", ["gpt-4o", "gemini-1.5-pro", "grok-beta"], index=0)

    if openai_key or gemini_key or groq_key:
        st.success("API Key 已載入")

# 初始化 LLM
if openai_key or gemini_key or groq_key:
    llm = LLMProvider(openai_key, gemini_key, groq_key)

uploaded_file = st.file_uploader("上傳蛋品溯源資料（CSV / JSON）", type=["csv", "json"])

if uploaded_file and (openai_key or gemini_key or groq_key):
    # 讀取資料
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_json(uploaded_file)
    
    st.success(f"成功載入 {len(df)} 筆資料")
    st.dataframe(df.head(10), use_container_width=True)

    if st.button("🚀 啟動31個AI代理進行完整分析", type="primary", use_container_width=True):
        with st.spinner("Agent 031 協調員已啟動，正在調度31個專業代理..."):
            orchestrator = TraceabilityOrchestrator(df, llm, default_model)
            result = orchestrator.run_full_pipeline()
        
        # 顯示結果
        st.success("✅ 所有代理執行完畢！")
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("⚠️ 風險總評")
            st.metric("最高風險批次", result["highest_risk_batch"], 
                     delta=f"{result['risk_score']:.1f}/10")
            st.markdown(result["risk_summary"])
        
        with col2:
            st.subheader("📊 關鍵圖表")
            if "temp_heatmap" in result:
                st.plotly_chart(result["temp_heatmap"], use_container_width=True)
            if "timeline_chart" in result:
                st.plotly_chart(result["timeline_chart"], use_container_width=True)

        st.subheader("📄 AI生成完整報告")
        st.markdown(result["final_report"])

        # 下載報告
        st.download_button(
            label="⬇️ 下載完整分析報告 (Markdown)",
            data=result["final_report"],
            file_name=f"食品溯源報告_{pd.Timestamp.now().strftime('%Y%m%d')}.md",
            mime="text/markdown"
        )
else:
    st.info("👈 請上傳資料並填入至少一個API Key 即可開始使用")
    st.markdown("### 範例資料下載")
    sample_path = "data/sample_egg_traceability.csv"
    if os.path.exists(sample_path):
        with open(sample_path, "rb") as f:
            st.download_button("下載範例蛋品資料", f, "sample_egg_traceability.csv")
