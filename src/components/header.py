import streamlit as st
from pathlib import Path
import base64


def header_home():
    logo_path = Path(__file__).parent.parent / "img" / "app_logo.png"

    with open(logo_path, "rb") as f:
        logo = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <div style="
            display:flex;
            align-items:center;
            justify-content:center;
            gap:20px;
            margin-bottom:20px;
        ">
            <img src="data:image/png;base64,{logo}" width="100">
            <h1 style="
                color:#E0E3FF;
                margin:0;
                font-size:60px;
            ">
                SNAPCLASS
            </h1>
        </div>
        """,
        unsafe_allow_html=True
    )

def header_dashboard():

    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"

    st.markdown(f"""
        <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; margin-bottom:20px;">
            <img src='{logo_url}' style='height:85px;' />
            <h2 style='text-align:center; color:#5865F2'>SNAP<br/>CLASS</h1>
        </div>

        """, unsafe_allow_html=True)