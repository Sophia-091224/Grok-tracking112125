# app.py - Ultimate Food Traceability Visualizer + Multi-Agent GenAI Dashboard
# Deploy instantly on Hugging Face Spaces (Streamlit + Plotly + PyVis + OpenAI/Gemini/Grok)

import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import networkx as nx
from pyvis.network import Network
import yaml
import os
import requests
from openai import OpenAI
import google.generativeai as genai
from datetime import datetime

# ========================= CONFIG =========================
st.set_page_config(
    page_title="EggTrace AI - Food Traceability Dashboard",
    page_icon="🥚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for pro look
st.markdown("""
<style>
    .main-header {font-size: 3rem !important; text-align: center; color: #1e3d59;}
    .subtitle {text-align: center; color: #556b2f; font-size: 1.3rem;}
    .stTabs [data-baseweb="tab-list"] {gap: 20px;}
    .stTabs [data-baseweb="tab"] {font-size: 18px; font-weight: bold;}
    .success-box {padding: 1rem; border-radius: 10px; background: #f0fff0; border-left: 6px solid #00ab00;}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>🥚 EggTrace AI</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Next-Gen Food Traceability • Powered by GenAI • One Scan → Full Journey</p>", unsafe_allow_html=True)

# ========================= SIDEBAR =========================
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/egg.png", width=100)
    st.header("⚙️ Configuration")

    with st.expander("🔑 API Keys", expanded=True):
        openai_key = st.text_input("OpenAI API Key", type="password", help="gpt-4o, gpt-4-turbo")
        gemini_key = st.text_input("Google Gemini API Key", type="password")
        xai_key = st.text_input("xAI Grok API Key", type="password", help="https://x.ai/api")

    st.subheader("🤖 AI Agent")
    provider = st.selectbox("Provider", ["OpenAI", "Google Gemini", "xAI Grok"])
    
    model_map = {
        "OpenAI": ["gpt-4o", "gpt-4-turbo-2024-04-09", "gpt-4", "gpt-3.5-turbo"],
        "Google Gemini": ["gemini-1.5-pro", "gemini-1.5-flash", "gemini-pro"],
        "xai_key": ["grok-beta", "grok-2"]
    }
    selected_model = st.selectbox("Model", model_map[provider])

    col1, col2 = st.columns(2)
    with col1:
        temperature = st.slider("Creativity", 0.0, 1.0, 0.3)
    with col2:
        max_tokens = st.slider("Max Tokens", 256, 8192, 2048, 256)

    st.subheader("Prompt Template")
    templates = {
        "Default Traceability Analyst": """You are a senior food safety auditor with 20 years at USDA & EFSA.
Analyze the egg traceability dataset and return in Markdown:

## Top 3 Risks
## Bottlenecks & Delays
## Recall Readiness Score: /10
## Executive Summary
## Recommended Actions""",

        "Recall Commander": """SIMULATE A RECALL.
Batch affected? List ALL retailers, dates, quantities.
Generate recall notice draft + contact list.
Prioritize by risk level.""",

        "Consumer QR Explainer": """Turn this data into a friendly consumer story:
From which farm? → How many days old? → Was it always cold? 
Write like a story for the egg carton QR code."""
    }
    chosen_template = st.selectbox("Quick Template", list(templates.keys()))
    custom_prompt = st.text_area("Edit Prompt", value=templates[chosen_template], height=300)

# ========================= MAIN APP =========================
uploaded_file = st.file_uploader("Upload Traceability JSON (use the 3 mock datasets!)", type=["json"])

if uploaded_file:
    data = json.load(uploaded_file)
    st.success("Dataset loaded successfully!")

    # Auto-detect type
    if isinstance(data, list) and len(data) > 0 and "batch_id" in data[0]:
        dataset_type = "batch_list"
        df = pd.json_normalize(data)
        df['laying_date'] = pd.to_datetime(df.get('laying_date', ''))
        df['packing_date'] = pd.to_datetime(df.get('packing_date', ''))
        df['distribution_date'] = pd.to_datetime(df.get('distribution_date', ''))
        df['delivery_date'] = pd.to_datetime(df.get('delivery_date', ''))

    elif isinstance(data, dict) and "traceability_chain" in str(data):
        dataset_type = "hierarchical"
    elif isinstance(data, dict) and "nodes" in data and "links" in data:
        dataset_type = "sankey"
    else:
        dataset_type = "unknown"

    # ========================= TABS =========================
    tab_overview, tab_sankey, tab_gantt, tab_tree, tab_geo, tab_ai = st.tabs([
        "Overview", "Sankey Flow", "Timeline", "Sunburst Tree", "Map Route", "AI Agent"
    ])

    # ── Overview ──
    with tab_overview:
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.metric("Batches", len(df) if dataset_type == "batch_list" else "1")
        with col2: st.metric("Total Cartons", f"{df['quantity_cartons'].sum():,}" if 'quantity_cartons' in df.columns else "N/A")
        with col3: st.metric("Farms", df['farm_name'].nunique() if 'farm_name' in df.columns else "1")
        with col4: st.metric("Retailers", df['retailer'].nunique() if 'retailer' in df.columns else "1")
        st.dataframe(df if 'df' in locals() else pd.json_normalize([data]), use_container_width=True)

    # ── Sankey ──
    with tab_sankey:
        if dataset_type == "sankey":
            fig = go.Figure(go.Sankey(
                node=dict(pad=20, thickness=30, line=dict(color="black", width=1),
                          label=[n["id"] for n in data["nodes"]],
                          color="#2E8B57"),
                link=dict(
                    source=[next(i for i, n in enumerate(data["nodes"]) if n["id"] == l["source"]) for l in data["links"]],
                    target=[next(i for i, n in enumerate(data["nodes"]) if n["id"] == l["target"]) for l in data["links"]],
                    value=[l["value"] for l in data["links"]],
                    color="rgba(46,139,87,0.4)"
                )
            ))
            fig.update_layout(title="Supply Chain Flow (Cartons)", font_size=14, height=700)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Auto-generating Sankey from batch list...")
            # Auto Sankey from batch_list
            nodes = pd.unique(df[['farm_name','packing_facility','distributor','retailer']].values.ravel('K'))
            node_map = {name: i for i, name in enumerate(nodes)}
            links = []
            for _, r in df.iterrows():
                links.extend([
                    dict(source=node_map[r['farm_name']], target=node_map[r['packing_facility']], value=r['quantity_cartons']),
                    dict(source=node_map[r['packing_facility']], target=node_map[r['distributor']], value=r['quantity_cartons']),
                    dict(source=node_map[r['distributor']], target=node_map[r['retailer']], value=r['quantity_cartons']),
                ])
            fig = go.Figure(go.Sankey(node=dict(label=list(nodes), color="#4682B4"), link=links))
            st.plotly_chart(fig, use_container_width=True)

    # ── Timeline Gantt ──
    with tab_gantt:
        if dataset_type == "batch_list":
            gantt_df = df.melt(id_vars=["batch_id"], value_vars=["laying_date", "packing_date", "distribution_date", "delivery_date"],
                               var_name="Stage", value_name="Date").dropna()
            gantt_df = gantt_df.sort_values(["batch_id", "Date"])
            fig = px.timeline(gantt_df, x_start="Date", x_end="Date", y="batch_id", color="Stage",
                              color_discrete_sequence=["#228B22", "#FFD700", "#FF6347", "#4169E1"])
            fig.update_yaxes(autorange="reversed")
            fig.update_layout(height=600, title="Batch Journey Timeline")
            st.plotly_chart(fig, use_container_width=True)

    # ── Sunburst ──
    with tab_tree:
        if dataset_type == "hierarchical":
            labels, parents, values = [], [], []
            for i, stage in enumerate(data["traceability_chain"]):
                label = f"{stage['stage']}: {stage['name']}"
                labels.append(label); parents.append(""); values.append(1)
            fig = go.Figure(go.Sunburst(labels=labels, parents=parents, values=values, branchvalues="total"))
            fig.update_layout(margin=dict(t=0,l=0,r=0,b=0), height=700)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Upload hierarchical dataset for sunburst view")

    # ── Geo Map ──
    with tab_geo:
        st.markdown("### Example Route (Mock Coordinates)")
        locations = {
            "Fresno, California, USA": (36.7378, -119.7871),
            "Lancaster, Pennsylvania, USA": (40.0379, -76.3055),
            "Portland, Oregon, USA": (45.5152, -122.6784),
            "Tracy, CA DC": (37.7397, -121.4252),
            "San Francisco, CA": (37.7749, -122.4194)
        }
        # Take first batch as example
        if dataset_type == "batch_list" and len(df) > 0:
            row = df.iloc[0]
            points = [locations.get(row['farm_location'], (0,0)), (37.8, -122), locations.get("San Francisco, CA", (0,0))]
            lats, lons = zip(*points)
            fig = go.Figure(go.Scattergeo(lat=lats, lon=lons, mode='lines+markers', line=dict(width=6, color='#FF4500'),
                                          marker=dict(size=12)))
            fig.update_geos(scope="usa", showland=True, landcolor="#f0f0f0")
            st.plotly_chart(fig, use_container_width=True)

    # ── AI Agent Tab ──
    with tab_ai:
        st.markdown("### Run Custom AI Agent")
        if st.write(f"**Model:** `{selected_model}` • **Temp:** {temperature} • **Max tokens:** {max_tokens}")

        if st.button("Run Agent Now", type="primary", use_container_width=True):
            with st.spinner(f"Contacting {provider}..."):
                data_str = json.dumps(data, indent=2)
                if len(data_str) > 60000:
                    data_str = data_str[:60000] + "\n...[TRUNCATED]"
                full_prompt = custom_prompt + "\n\nDATASET:\n" + data_str

                try:
                    if provider == "OpenAI":
                        client = OpenAI(api_key=openai_key)
                        resp = client.chat.completions.create(
                            model=selected_model,
                            messages=[{"role": "user", "content": full_prompt}],
                            max_tokens=max_tokens,
                            temperature=temperature
                        )
                        result = resp.choices[0].message.content
                    elif provider == "Google Gemini":
                        genai.configure(api_key=gemini_key)
                        model = genai.GenerativeModel(selected_model)
                        resp = model.generate_content(full_prompt,
                            generation_config=genai.types.GenerationConfig(max_output_tokens=max_tokens, temperature=temperature))
                        result = resp.text
                    elif provider == "xAI Grok":
                        resp = requests.post("https://api.x.ai/v1/chat/completions",
                            headers={"Authorization": f"Bearer {xai_key}"},
                            json={"model": selected_model, "messages": [{"role": "user", "content": full_prompt}],
                                  "max_tokens": max_tokens, "temperature": temperature})
                        result = resp.json()['choices'][0]['message']['content'] if resp.ok else resp.text

                    st.markdown("### Agent Report")
                    st.markdown(result)

                    st.download_button("Download Report", result, f"traceability_report_{datetime.now().strftime('%Y%m%d')}.md")

                except Exception as e:
                    st.error(f"Error: {e}")

else:
    st.info("Upload one of the 3 mock JSON datasets to unlock full power!")

# ========================= FOOTER =========================
st.markdown("---")
st.markdown("""
**Built with ❤️ using Streamlit • Plotly • OpenAI • Gemini • Grok**  
Deployed on Hugging Face Spaces — Nov 21, 2025  
Ready for production use by egg producers worldwide.
""")

# Bonus: Auto-included agents.yaml
agents_yaml = """
traceability_analyst:
  role: "Senior Food Safety Expert"
  goal: "Detect risks, delays, recall readiness"
recall_coordinator:
  role: "Recall Manager"
  goal: "Generate instant recall plans"
consumer_qr_agent:
  role: "Storyteller"
  goal: "Turn data into consumer-friendly journey"
"""
with st.expander("agents.yaml – Ready for CrewAI/LangGraph"):
    st.code(agents_yaml, language="yaml")
