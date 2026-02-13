import streamlit as st
import requests
import pandas as pd
from bs4 import BeautifulSoup

# import parser functions
from parser import parse_metric_cards_from_html

st.set_page_config(
    page_title="Universal Metrics Parser",
    page_icon="📊",
    layout="wide"
)

# ---------- HEADER ----------
st.markdown("""
<h1 style='text-align: center; color: #2E86C1;'>
🌍 Universal Military Metrics Parser
</h1>
<p style='text-align: center; font-size:18px;'>
Paste any metrics page URL → Get structured CSV instantly
</p>
""", unsafe_allow_html=True)

st.divider()

# ---------- INPUT SECTION ----------
url = st.text_input("🔗 Paste Metrics Page URL Here")

metric_name = st.text_input("📝 Metric Name (example: aircraft_carriers, tanks, gas_production)")

col1, col2 = st.columns([1,1])

with col1:
    parse_btn = st.button("🚀 Parse Data", use_container_width=True)

with col2:
    clear_btn = st.button("🧹 Clear", use_container_width=True)

st.divider()

# ---------- PARSING ----------
if parse_btn and url and metric_name:

    with st.spinner("Fetching and Parsing Data... Please wait ⏳"):
        try:
            response = requests.get(url, timeout=15)
            soup = BeautifulSoup(response.text, "html.parser")

            df = parse_metric_cards_from_html(soup, metric_name)

            st.success("✅ Data Parsed Successfully!")

            st.subheader("📋 Parsed Preview")
            st.dataframe(df, use_container_width=True)

            # ---------- DOWNLOAD CSV ----------
            csv = df.to_csv(index=False).encode('utf-8')

            st.download_button(
                label="⬇️ Download CSV",
                data=csv,
                file_name=f"{metric_name}.csv",
                mime="text/csv",
                use_container_width=True
            )

        except Exception as e:
            st.error(f"Error: {e}")

if clear_btn:
    st.experimental_rerun()
