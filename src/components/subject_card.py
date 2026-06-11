import streamlit as st
import streamlit.components.v1 as components

def subject_card(name, code, section, stats=None, footer_callback=None):

    stats_html = ""
    if stats:
        stats_html = '<div style="display:flex; gap:10px; flex-wrap:wrap; margin-top:8px;">'
        for icon, label, value in stats:
            stats_html += f"""
            <div style="background:#f5f3ff; padding:5px 14px; border-radius:20px; font-size:0.85rem; color:#4b5563;">
                {icon} <b>{value}</b> {label}
            </div>
            """
        stats_html += "</div>"

    html = f"""
    <div style="
        background: white;
        border-radius: 16px;
        padding: 24px 28px 16px 28px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.07);
        border: 1px solid #ede9f6;
        border-left: 6px solid #EB459E;
        font-family: sans-serif;
    ">
        <h3 style="margin: 0 0 8px 0; color: #1a1a2e; font-size: 1.25rem; font-weight: 700;">
            {name}
        </h3>
        <p style="color: #64748b; margin: 6px 0 12px 0; font-size: 0.95rem;">
            Code :&nbsp;
            <span style="background:#E0E3FF; color:#5865F2; padding:2px 10px; border-radius:6px; font-weight:600; font-size:0.85rem;">{code}</span>
            &nbsp;|&nbsp; Section : {section}
        </p>
        {stats_html}
    </div>
    """

    components.html(html, height=160, scrolling=False)

    if footer_callback:
        footer_callback()