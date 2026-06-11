import streamlit as st

def style_background_home():

    st.markdown("""
    <style>
        .stApp{
                background:#5865F2 !important;
            }

    </style>
    """, unsafe_allow_html=True)

def style_background_dashboard():

    st.markdown("""
    <style>
        .stApp{
                background:#EBE3FF !important;
            }

    </style>
    """, unsafe_allow_html=True)

# import streamlit as st

def style_base_layout():

    st.markdown("""
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&display=swap');

    #MainMenu, footer, header {
        visibility: hidden;
    }

    .block-container {
        padding-top: 1.5rem !important;
    }

    h1 {
        font-family: 'Climate Crisis', sans-serif !important;
        font-size: 3.5rem !important;
        line-height: 1.1 !important;
        margin-bottom: 0rem !important;
    }
    h2 {
        font-family: 'Climate Crisis', sans-serif !important;
        font-size: 3.5rem !important;
        line-height: 1.1 !important;
        margin-bottom: 0rem !important;
    }

    /* ✅ INPUT LABELS */
    .stTextInput label p {
        font-family: 'Outfit', sans-serif !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
    }

    /* ✅ INPUT TYPED TEXT */
    .stTextInput input {
        font-family: 'Outfit', sans-serif !important;
        font-size: 1rem !important;
    }

    /* ✅ INPUT PLACEHOLDER TEXT */
    .stTextInput input::placeholder {
        font-family: 'Outfit', sans-serif !important;
        color: #aaa !important;
    }

    /* ✅ BUTTON TEXT */
    .stButton button {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 600 !important;
    }

    </style>
    """, unsafe_allow_html=True)