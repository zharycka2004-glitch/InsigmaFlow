"""
╔══════════════════════════════════════════════════════════════════════════════╗
║   SISTEMA DE CONTROL ESTADÍSTICO DE PROCESOS (CEP)                         ║
║   Empresa Manufacturera de Bloques de Concreto                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║   Archivo único : app.py                                                    ║
║   Ejecución     : streamlit run app.py                                      ║
║   Estructura    :                                                            ║
║     1. Configuración de página                                              ║
║     2. Estilos CSS globales                                                 ║
║     3. Inicialización del estado de sesión                                  ║
║     4. Componentes HTML reutilizables                                       ║
║     5. Secciones 1–12                                                       ║
║     6. Sidebar + enrutador principal                                        ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import io
import warnings

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import streamlit as st
from matplotlib.gridspec import GridSpec
from scipy import stats as sp_stats

warnings.filterwarnings("ignore")          # suprimir avisos de pandas/numpy en consola

# Estilo global de matplotlib (fondo oscuro coherente con la UI)
plt.rcParams.update({
    "figure.facecolor":  "#FFFFFF",
    "axes.facecolor":    "#FAFBFC",
    "axes.edgecolor":    "#E5E7EB",
    "axes.labelcolor":   "#374151",
    "axes.titlecolor":   "#111827",
    "xtick.color":       "#6B7280",
    "ytick.color":       "#6B7280",
    "text.color":        "#111827",
    "grid.color":        "#F3F4F6",
    "grid.linestyle":    "--",
    "grid.alpha":        0.8,
    "font.family":       "sans-serif",
    "figure.dpi":        130,
    "axes.spines.top":   False,
    "axes.spines.right": False,
})

# ══════════════════════════════════════════════════════════════════════════════
# 1. CONFIGURACIÓN DE PÁGINA
# ══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="CEP – Bloques de Concreto",
    page_icon="🧱",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ══════════════════════════════════════════════════════════════════════════════
# 2. ESTILOS CSS GLOBALES
# ══════════════════════════════════════════════════════════════════════════════

def aplicar_estilos():
    """Inyecta el sistema de diseño CSS premium v2 en la aplicación Streamlit.

    Principios de diseño:
    - Tema oscuro industrial inspirado en Minitab + Power BI.
    - Variables CSS centralizadas para coherencia total entre módulos.
    - Micro-interacciones (hover, transition) para fluidez visual.
    - Tipografía dual: Inter para texto, JetBrains Mono para valores numéricos.
    - Jerarquía visual clara: sección > bloque > tarjeta > dato.
    """
    st.markdown(
        """
        <style>
        /* ═══════════════════════════════════════════════════════════════════════
           FUENTES — Inter + JetBrains Mono
        ═══════════════════════════════════════════════════════════════════════ */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

        :root {
            --bg:        #F5F7FA;
            --surface:   #FFFFFF;
            --surface2:  #F9FAFB;
            --surface3:  #F3F4F6;
            --border:    #E5E7EB;
            --border2:   #D1D5DB;
            --primary:   #2563EB;
            --primary-l: #3B82F6;
            --primary-d: #1D4ED8;
            --primary-bg: rgba(37,99,235,.06);
            --primary-bg2: rgba(37,99,235,.10);
            --success:   #10B981;
            --success-l: #34D399;
            --success-bg: rgba(16,185,129,.07);
            --warning:   #F59E0B;
            --warning-l: #FBBF24;
            --warning-bg: rgba(245,158,11,.07);
            --danger:    #EF4444;
            --danger-l:  #F87171;
            --danger-bg: rgba(239,68,68,.07);
            --text:      #111827;
            --text-2:    #374151;
            --text-3:    #6B7280;
            --muted:     #9CA3AF;
            --dim:       #D1D5DB;
            --font:      'Inter', system-ui, -apple-system, sans-serif;
            --mono:      'JetBrains Mono', 'Courier New', monospace;
            --shadow-xs: 0 1px 2px rgba(0,0,0,.05);
            --shadow-sm: 0 1px 3px rgba(0,0,0,.08), 0 1px 2px rgba(0,0,0,.04);
            --shadow:    0 4px 6px rgba(0,0,0,.07), 0 2px 4px rgba(0,0,0,.04);
            --shadow-md: 0 8px 16px rgba(0,0,0,.08), 0 2px 4px rgba(0,0,0,.04);
            --shadow-lg: 0 16px 32px rgba(0,0,0,.10), 0 4px 8px rgba(0,0,0,.05);
            --shadow-blue: 0 4px 14px rgba(37,99,235,.15);
            --r-xs: 4px; --r-sm: 8px; --r: 12px; --r-lg: 16px; --r-xl: 20px; --r-2xl: 24px;
            --t: .16s ease; --t-md: .22s ease;
        }

        html, body, [class*="css"],
        .stApp, .stMarkdown, p, span, div {
            font-family: var(--font) !important;
            -webkit-font-smoothing: antialiased;
        }
        .stApp { background: var(--bg) !important; color: var(--text) !important; }

        ::-webkit-scrollbar { width: 5px; height: 5px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: var(--dim); border-radius: 10px; }
        ::-webkit-scrollbar-thumb:hover { background: var(--primary); }

        /* SIDEBAR */
        [data-testid="stSidebar"] {
            background: #FFFFFF !important;
            border-right: 1px solid var(--border) !important;
            box-shadow: 2px 0 12px rgba(0,0,0,.04) !important;
        }
        [data-testid="stSidebar"] > div:first-child { padding: 0 !important; }

        .sb-brand {
            display: flex; align-items: center; gap: 11px;
            padding: 22px 18px 18px;
            border-bottom: 1px solid var(--border);
        }
        .sb-logo-img { width: 52px; height: auto; flex-shrink: 0; display: flex; align-items: center; }
        .sb-logo-img img { width: 100%; height: auto; object-fit: contain; }
        .sb-logo {
            width: 36px; height: 36px; background: var(--primary);
            border-radius: var(--r-sm); display: flex; align-items: center; justify-content: center;
            font-size: 1.1rem; box-shadow: var(--shadow-blue); flex-shrink: 0;
        }
        .sb-title { font-size: .9rem; font-weight: 700; color: var(--text); letter-spacing: -.02em; line-height: 1.2; }
        .sb-sub { font-size: .63rem; color: var(--muted); letter-spacing: .06em; text-transform: uppercase; margin-top: 2px; }
        .sb-divider { border: none; border-top: 1px solid var(--border); margin: 0; }
        .sb-nav-lbl {
            font-size: .6rem; color: var(--muted); letter-spacing: .12em;
            text-transform: uppercase; padding: 16px 18px 6px; font-weight: 600; margin: 0;
        }

        div[data-testid="stRadio"] > div { gap: 1px !important; padding: 0 10px !important; }
        div[data-testid="stRadio"] label {
            font-size: .82rem !important; color: var(--text-3) !important;
            padding: 8px 12px !important; border-radius: var(--r-sm) !important;
            transition: background var(--t), color var(--t) !important;
            cursor: pointer !important; font-weight: 500 !important;
            display: flex !important; align-items: center !important;
            width: 100% !important; letter-spacing: -.01em !important;
        }
        div[data-testid="stRadio"] label:hover {
            background: var(--primary-bg) !important; color: var(--primary) !important;
        }
        div[data-testid="stRadio"] [data-baseweb="radio"] > div:first-child { display: none !important; }

        .sb-status-panel {
            margin: 10px 12px 8px; background: var(--surface2);
            border: 1px solid var(--border); border-radius: var(--r); padding: 13px 15px;
        }
        .sb-status-title {
            font-size: .58rem; color: var(--muted); letter-spacing: .12em;
            text-transform: uppercase; font-weight: 700; margin-bottom: 10px;
        }
        .sb-kpi-row {
            display: flex; justify-content: space-between; align-items: center;
            padding: 5px 0; border-bottom: 1px solid var(--border);
        }
        .sb-kpi-row:last-child { border-bottom: none; }
        .sb-kpi-lbl { font-size: .71rem; color: var(--text-3); font-weight: 500; }
        .sb-kpi-val { font-family: var(--mono); font-size: .76rem; font-weight: 600; }

        .sb-data-pill {
            display: flex; align-items: center; gap: 7px;
            margin: 8px 12px 4px; padding: 7px 12px;
            border-radius: 20px; font-size: .72rem; font-weight: 600;
        }
        .sb-data-pill.ok  { background: var(--success-bg); color: #059669; border: 1px solid rgba(16,185,129,.2); }
        .sb-data-pill.nok { background: rgba(245,158,11,.07); color: #D97706; border: 1px solid rgba(245,158,11,.2); }
        .sb-pulse { width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0; animation: pulse 2.2s infinite; }
        .ok  .sb-pulse { background: var(--success); }
        .nok .sb-pulse { background: var(--warning); }
        @keyframes pulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:.5;transform:scale(.85)} }

        .sb-footer {
            font-size: .61rem; color: var(--muted); text-align: center;
            padding: 12px 16px 18px; border-top: 1px solid var(--border);
            margin-top: 8px; letter-spacing: .02em;
        }
        .sb-ver { color: var(--primary); font-weight: 700; }

        /* SECTION HEADER */
        .sec-hdr {
            position: relative; padding: 22px 26px 20px 28px; margin: 0 0 28px;
            background: var(--surface); border: 1px solid var(--border);
            border-left: 3px solid var(--primary); border-radius: var(--r-xl);
            box-shadow: var(--shadow-sm);
        }
        .sec-hdr-inner { display: flex; align-items: flex-start; gap: 16px; }
        .sec-hdr-ico {
            width: 42px; height: 42px; background: var(--primary-bg2);
            border-radius: var(--r); display: flex; align-items: center; justify-content: center;
            font-size: 1.3rem; flex-shrink: 0;
        }
        .sec-hdr h1 {
            font-size: 1.4rem !important; font-weight: 700 !important; color: var(--text) !important;
            margin: 0 0 4px !important; letter-spacing: -.03em !important; line-height: 1.2 !important;
        }
        .sec-hdr p {
            font-size: .83rem !important; color: var(--text-3) !important;
            margin: 0 !important; line-height: 1.55 !important;
        }
        .sec-hdr-badge {
            position: absolute; top: 16px; right: 16px;
            font-size: .58rem; font-weight: 700; letter-spacing: .1em; text-transform: uppercase;
            padding: 3px 10px; border-radius: 20px; background: var(--primary-bg2);
            color: var(--primary); border: 1px solid rgba(37,99,235,.2);
        }

        /* METRIC CARDS */
        .m-card {
            background: var(--surface); border: 1px solid var(--border);
            border-radius: var(--r-lg); padding: 20px 22px; text-align: center;
            transition: transform var(--t-md), border-color var(--t), box-shadow var(--t-md);
            margin-bottom: 12px; box-shadow: var(--shadow-sm); position: relative; overflow: hidden;
        }
        .m-card::after {
            content:''; position:absolute; top:0; left:0; right:0; height:2px;
            background: linear-gradient(90deg,var(--primary),var(--primary-l),transparent);
            opacity:0; transition:opacity var(--t-md);
        }
        .m-card:hover { transform:translateY(-2px); border-color:var(--primary-l); box-shadow:var(--shadow-md),var(--shadow-blue); }
        .m-card:hover::after { opacity:1; }
        .m-lbl { font-size:.6rem; color:var(--muted); letter-spacing:.12em; text-transform:uppercase; margin-bottom:10px; font-weight:700; }
        .m-val { font-family:var(--mono); font-size:1.6rem; font-weight:600; color:var(--primary); line-height:1; letter-spacing:-.03em; }
        .m-note { font-size:.71rem; color:var(--text-3); margin-top:7px; line-height:1.45; }

        /* KPI CARD */
        .kpi-card {
            background: var(--surface); border: 1px solid var(--border); border-radius: var(--r-lg);
            padding: 17px 20px; display: flex; align-items: center; gap: 14px;
            transition: transform var(--t-md), box-shadow var(--t-md), border-color var(--t);
            margin-bottom: 10px; box-shadow: var(--shadow-sm);
        }
        .kpi-card:hover { transform:translateY(-1px); box-shadow:var(--shadow-md); border-color:var(--border2); }
        .kpi-icon { width:42px; height:42px; border-radius:var(--r); display:flex; align-items:center; justify-content:center; font-size:1.2rem; flex-shrink:0; }
        .kpi-body { flex:1; min-width:0; }
        .kpi-lbl { font-size:.62rem; color:var(--muted); letter-spacing:.1em; text-transform:uppercase; font-weight:700; }
        .kpi-val { font-family:var(--mono); font-size:1.35rem; font-weight:700; color:var(--text); line-height:1.15; }
        .kpi-sub { font-size:.7rem; color:var(--text-3); margin-top:2px; }

        /* ALERT BOXES */
        .box-i,.box-w,.box-s,.box-e {
            display:flex; align-items:flex-start; gap:12px; border-radius:var(--r);
            padding:13px 16px; margin:10px 0; font-size:.85rem; color:var(--text-2);
            line-height:1.6; border-left-width:3px; border-left-style:solid;
        }
        .box-ico { font-size:.95rem; flex-shrink:0; margin-top:2px; }
        .box-i { background:rgba(37,99,235,.04); border:1px solid rgba(37,99,235,.15); border-left-color:var(--primary); }
        .box-w { background:var(--warning-bg); border:1px solid rgba(245,158,11,.2); border-left-color:var(--warning); }
        .box-s { background:var(--success-bg); border:1px solid rgba(16,185,129,.2); border-left-color:var(--success); }
        .box-e { background:var(--danger-bg); border:1px solid rgba(239,68,68,.2); border-left-color:var(--danger); }

        /* COMING SOON */
        .coming { background:var(--surface); border:1.5px dashed var(--border2); border-radius:var(--r-xl); padding:48px 36px; text-align:center; margin:16px 0; }
        .coming .ci { font-size:2.5rem; margin-bottom:14px; opacity:.4; }
        .coming h3 { color:var(--text-3); font-weight:600; margin:0 0 6px; font-size:1rem; }
        .coming p  { color:var(--muted); font-size:.82rem; margin:0; }

        /* BADGES */
        .bdg { display:inline-flex; align-items:center; gap:4px; padding:3px 10px; border-radius:20px; font-size:.63rem; font-weight:700; letter-spacing:.06em; text-transform:uppercase; }
        .bdg-blue   { background:rgba(37,99,235,.08);  color:var(--primary); border:1px solid rgba(37,99,235,.2); }
        .bdg-green  { background:var(--success-bg);    color:#059669;        border:1px solid rgba(16,185,129,.25); }
        .bdg-yellow { background:var(--warning-bg);    color:#D97706;        border:1px solid rgba(245,158,11,.25); }
        .bdg-red    { background:var(--danger-bg);     color:#DC2626;        border:1px solid rgba(239,68,68,.2); }
        .bdg-gray   { background:var(--surface3);      color:var(--text-3);  border:1px solid var(--border); }
        .bdg-purple { background:rgba(124,58,237,.07); color:#6D28D9;        border:1px solid rgba(124,58,237,.2); }

        /* STATUS ROW */
        .srow {
            display:flex; justify-content:space-between; align-items:center;
            padding:11px 16px; background:var(--surface); border-radius:var(--r);
            border:1px solid var(--border); margin-bottom:6px; transition:border-color var(--t),box-shadow var(--t);
        }
        .srow:hover { border-color:var(--primary-l); box-shadow:var(--shadow-xs); }
        .srow s { font-size:.86rem; color:var(--text-2); font-weight:500; text-decoration:none; }

        /* FLOW STEPS */
        .fstep {
            display:flex; align-items:flex-start; gap:14px; margin:7px 0; padding:13px 16px;
            background:var(--surface); border-radius:var(--r); border:1px solid var(--border);
            border-left:3px solid var(--primary); box-shadow:var(--shadow-xs);
            transition:box-shadow var(--t),transform var(--t);
        }
        .fstep:hover { box-shadow:var(--shadow-sm); transform:translateX(2px); }
        .fstep-ico  { font-size:1.1rem; flex-shrink:0; margin-top:1px; }
        .fstep-name { font-weight:600; color:var(--text); font-size:.88rem; letter-spacing:-.01em; }
        .fstep-desc { color:var(--text-3); font-size:.78rem; margin:2px 0 0; line-height:1.45; }

        /* PHVA / PDCA */
        .pdca {
            display:flex; gap:14px; padding:14px 18px; background:var(--surface);
            border-radius:var(--r); border:1px solid var(--border); margin-bottom:7px;
            box-shadow:var(--shadow-xs); transition:transform var(--t),box-shadow var(--t);
        }
        .pdca:hover { transform:translateX(3px); box-shadow:var(--shadow-sm); }
        .pdca-t { font-weight:700; white-space:nowrap; font-size:.88rem; color:var(--text); }
        .pdca-d { font-size:.82rem; color:var(--text-3); line-height:1.5; }

        /* SEPARATOR */
        .sep { border:none; border-top:1px solid var(--border); margin:28px 0; opacity:.8; }

        /* STREAMLIT OVERRIDES */
        .main .block-container { padding:2rem 2.5rem 2rem !important; max-width:1400px !important; }

        [data-testid="stMetricValue"] { font-family:var(--mono) !important; font-size:1.55rem !important; font-weight:700 !important; color:var(--text) !important; }
        [data-testid="stMetricLabel"] { font-size:.7rem !important; color:var(--muted) !important; text-transform:uppercase !important; letter-spacing:.09em !important; font-weight:700 !important; }
        [data-testid="stMetricDelta"] { font-size:.77rem !important; font-weight:600 !important; }
        [data-testid="metric-container"] { background:var(--surface) !important; border:1px solid var(--border) !important; border-radius:var(--r-lg) !important; padding:18px 22px !important; box-shadow:var(--shadow-sm) !important; transition:box-shadow var(--t),transform var(--t-md) !important; }
        [data-testid="metric-container"]:hover { box-shadow:var(--shadow-md) !important; transform:translateY(-1px) !important; }

        [data-testid="stDataFrame"] { border-radius:var(--r-lg) !important; overflow:hidden !important; border:1px solid var(--border) !important; box-shadow:var(--shadow-sm) !important; }

        .stButton>button {
            background:var(--primary) !important; color:#FFFFFF !important; border:none !important;
            border-radius:var(--r-sm) !important; font-family:var(--font) !important; font-weight:600 !important;
            font-size:.84rem !important; padding:9px 22px !important; letter-spacing:-.01em !important;
            transition:background var(--t),transform var(--t),box-shadow var(--t) !important; box-shadow:var(--shadow-blue) !important;
        }
        .stButton>button:hover { background:var(--primary-d) !important; transform:translateY(-1px) !important; box-shadow:0 6px 18px rgba(37,99,235,.25) !important; }
        button[kind="secondary"] { background:var(--surface) !important; border:1px solid var(--border) !important; color:var(--text-2) !important; box-shadow:var(--shadow-xs) !important; }
        button[kind="secondary"]:hover { background:var(--surface3) !important; border-color:var(--border2) !important; }

        .stTextInput input,.stNumberInput input,.stTextArea textarea {
            background:var(--surface) !important; border:1px solid var(--border) !important;
            border-radius:var(--r-sm) !important; color:var(--text) !important;
            font-family:var(--font) !important; font-size:.875rem !important;
            transition:border-color var(--t),box-shadow var(--t) !important; box-shadow:var(--shadow-xs) !important;
        }
        .stTextInput input:focus,.stNumberInput input:focus,.stTextArea textarea:focus {
            border-color:var(--primary) !important; box-shadow:0 0 0 3px rgba(37,99,235,.12) !important; outline:none !important;
        }
        .stSelectbox>div>div { background:var(--surface) !important; border:1px solid var(--border) !important; border-radius:var(--r-sm) !important; color:var(--text) !important; }
        .stSelectbox>div>div:focus-within { border-color:var(--primary) !important; box-shadow:0 0 0 3px rgba(37,99,235,.12) !important; }

        .stTextInput label,.stNumberInput label,.stSelectbox label,.stTextArea label,.stSlider label,.stFileUploader label {
            font-size:.78rem !important; font-weight:600 !important; color:var(--text-2) !important; letter-spacing:-.01em !important;
        }

        [data-testid="stExpander"] { background:var(--surface) !important; border:1px solid var(--border) !important; border-radius:var(--r-lg) !important; box-shadow:var(--shadow-xs) !important; transition:box-shadow var(--t) !important; }
        [data-testid="stExpander"]:hover { border-color:var(--border2) !important; box-shadow:var(--shadow-sm) !important; }
        [data-testid="stExpander"] summary { font-weight:600 !important; font-size:.86rem !important; color:var(--text-2) !important; padding:14px 18px !important; }

        .stTabs [data-baseweb="tab-list"] { background:transparent !important; border-bottom:2px solid var(--border) !important; gap:0 !important; padding:0 !important; }
        .stTabs [data-baseweb="tab"] { background:transparent !important; color:var(--muted) !important; font-weight:600 !important; font-size:.82rem !important; padding:10px 18px !important; border-bottom:2px solid transparent !important; margin-bottom:-2px !important; transition:color var(--t),border-color var(--t) !important; letter-spacing:-.01em !important; }
        .stTabs [data-baseweb="tab"]:hover { color:var(--text-2) !important; }
        .stTabs [aria-selected="true"] { color:var(--primary) !important; border-bottom-color:var(--primary) !important; background:transparent !important; }
        .stTabs [data-baseweb="tab-panel"] { background:transparent !important; border:none !important; padding:20px 0 !important; }

        [data-testid="stSlider"] .st-ae { background:var(--primary) !important; }
        .stAlert { border-radius:var(--r) !important; border:none !important; box-shadow:var(--shadow-sm) !important; }

        [data-testid="stFileUploader"] { background:var(--surface) !important; border:1.5px dashed var(--border2) !important; border-radius:var(--r-lg) !important; padding:8px !important; transition:border-color var(--t) !important; }
        [data-testid="stFileUploader"]:hover { border-color:var(--primary) !important; }

        .stCheckbox label,.stRadio label { font-size:.84rem !important; color:var(--text-2) !important; font-weight:500 !important; }

        .section-block { background:var(--surface); border:1px solid var(--border); border-radius:var(--r-xl); padding:24px 26px; margin-bottom:18px; box-shadow:var(--shadow-sm); }

        .stMarkdown h2 { font-size:1.1rem !important; font-weight:700 !important; color:var(--text) !important; letter-spacing:-.02em !important; margin-top:1.5rem !important; margin-bottom:.6rem !important; }
        .stMarkdown h3 { font-size:.97rem !important; font-weight:600 !important; color:var(--text-2) !important; letter-spacing:-.015em !important; margin-top:1.2rem !important; margin-bottom:.5rem !important; }

        .text-muted { color:var(--muted) !important; font-size:.82rem; }
        .text-mono  { font-family:var(--mono) !important; }
        .text-center { text-align:center !important; }

        [data-testid="stImage"] img { border-radius:var(--r-lg) !important; border:1px solid var(--border) !important; box-shadow:var(--shadow-sm) !important; }

        .stDownloadButton>button { background:var(--surface) !important; color:var(--primary) !important; border:1px solid rgba(37,99,235,.3) !important; box-shadow:none !important; font-weight:600 !important; }
        .stDownloadButton>button:hover { background:var(--primary-bg) !important; border-color:var(--primary) !important; }

        [data-testid="column"] { padding:0 8px !important; }

        </style>
        """,
        unsafe_allow_html=True,
    )

# ══════════════════════════════════════════════════════════════════════════════
# 3. INICIALIZACIÓN DEL ESTADO DE SESIÓN
# ══════════════════════════════════════════════════════════════════════════════

def inicializar_estado():
    """Crea en st.session_state todas las claves necesarias (solo si no existen)."""

    defaults = {
        # ── Módulo Ingreso de datos ────────────────────────────────────────────
        "datos_cargados":     False,    # True cuando df_raw es válido y mapeado
        "df_raw":             None,     # DataFrame original (tal como llega del archivo)
        "df_subgrupos":       None,     # DataFrame reorganizado con columna 'subgrupo'
        "col_resistencia":    None,     # Nombre de la columna de resistencia mapeada
        "col_absorcion":      None,     # Nombre de la columna de absorción mapeada
        "col_subgrupo":       None,     # Columna que identifica el subgrupo (si existe)
        "errores_carga":      [],       # Errores fatales de validación
        "advertencias_carga": [],       # Advertencias no fatales

        # ── Configuración del proceso ──────────────────────────────────────────
        "config_proceso": {
            "variable":          "Resistencia a compresión (kg/cm²)",
            "lsl_res":           130.0,
            "usl_res":           160.0,
            "target_res":        145.0,
            "lsl_abs":           0.0,
            "usl_abs":           10.0,
            "tamano_subgrupo":   5,
            "n_subgrupos_min":   25,
            "frecuencia":        "Por turno",
        },

        # ── Validación estadística ─────────────────────────────────────────────
        "validacion": {
            "normalidad_ok": None,
            "outliers":      [],
            "estadisticos":  {},
        },

        # ── Fase 1 – Estabilización ────────────────────────────────────────────
        "fase1": {
            "limites_xbar":          {},
            "limites_r":             {},
            "limites_s":             {},
            "puntos_fuera":          [],
            "proceso_estable":       None,
            "subgrupos_excluidos":   [],
            "historial_exclusiones": [],
        },
        # Estado interno del modulo de causas especiales (no se resetea con datos)
        "f1_eliminados": [],   # historial de exclusiones con justificacion
        "f1_excluidos":  set(), # set de IDs de subgrupo actualmente excluidos

        # ── Fase 2 – Monitoreo ─────────────────────────────────────────────────
        "fase2": {
            "alertas":            [],
            "ultimas_mediciones": [],
        },

        "capacidad": {"cp": None, "cpk": None, "pp": None, "ppk": None},
        "muestreo":  {"plan": {}, "curva_co": []},
    }

    for clave, valor in defaults.items():
        if clave not in st.session_state:
            st.session_state[clave] = valor


# ══════════════════════════════════════════════════════════════════════════════
# 4. COMPONENTES HTML REUTILIZABLES
# ══════════════════════════════════════════════════════════════════════════════

def encabezado(icono: str, titulo: str, desc: str = "", badge_txt: str = "CEP"):
    """Encabezado premium de sección con gradiente, ícono filtrado y badge."""
    badge_html = (
        f'<span class="sec-hdr-badge">{badge_txt}</span>'
        if badge_txt else ""
    )
    desc_html = f'<p>{desc}</p>' if desc else ""
    st.markdown(
        f"""
        <div class="sec-hdr">
            {badge_html}
            <div class="sec-hdr-inner">
                <div class="sec-hdr-ico">{icono}</div>
                <div>
                    <h1>{titulo}</h1>
                    {desc_html}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def tarjeta(label: str, valor: str, nota: str = "", color: str = ""):
    """Tarjeta de métrica con hover premium y color opcional para el valor."""
    val_style = f"color:{color};" if color else ""
    nota_html = f'<div class="m-note">{nota}</div>' if nota else ""
    st.markdown(
        f"""
        <div class="m-card">
            <div class="m-lbl">{label}</div>
            <div class="m-val" style="{val_style}">{valor}</div>
            {nota_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def kpi_card(icono: str, label: str, valor: str, sub: str = "",
             color: str = "#3b82f6"):
    """Tarjeta KPI horizontal con ícono coloreado, valor y subtítulo."""
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon" style="background:{color}18;color:{color}">{icono}</div>
            <div class="kpi-body">
                <div class="kpi-lbl">{label}</div>
                <div class="kpi-val" style="color:{color}">{valor}</div>
                {"<div class='kpi-sub'>" + sub + "</div>" if sub else ""}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def caja(mensaje: str, tipo: str = "info"):
    """Caja de mensaje con borde lateral de color y ícono.

    tipo: 'info' | 'warning' | 'success' | 'error'
    """
    meta = {
        "info":    ("box-i", "ℹ️"),
        "warning": ("box-w", "⚠️"),
        "success": ("box-s", "✅"),
        "error":   ("box-e", "❌"),
    }
    cls, ico = meta.get(tipo, ("box-i", "ℹ️"))
    st.markdown(
        f"""
        <div class="{cls}">
            <span class="box-ico">{ico}</span>
            <span>{mensaje}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def proximamente(titulo: str = "En desarrollo",
                 desc: str = "Esta sección se habilitará próximamente."):
    """Bloque visual placeholder con diseño premium."""
    st.markdown(
        f"""
        <div class="coming">
            <div class="ci">🔧</div>
            <h3>{titulo}</h3>
            <p>{desc}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def sep():
    """Separador visual sutil entre bloques de contenido."""
    st.markdown("<hr class='sep'/>", unsafe_allow_html=True)


def badge(texto: str, color: str = "blue"):
    """Badge de estado inline."""
    st.markdown(
        f'<span class="bdg bdg-{color}">{texto}</span>',
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
# 5. SECCIONES (1–12)
# ══════════════════════════════════════════════════════════════════════════════

# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 1 – Introducción + Calidad y Costos
# ─────────────────────────────────────────────────────────────────────────────
def seccion_introduccion():
    encabezado(
        "🏠", "Introducción & Calidad",
        "Sistema de Control Estadístico de Procesos para manufactura de bloques de concreto",
    )

    col_txt, col_vis = st.columns([3, 2], gap="large")

    with col_txt:
        st.markdown("### ¿Qué es este sistema?")
        st.markdown(
            """
            Esta aplicación implementa herramientas de **Control Estadístico de Procesos (CEP)**
            para monitorear y mejorar la calidad productiva de bloques de concreto.

            El CEP distingue entre **causas comunes** (variación inherente) y **causas especiales**
            (eventos anómalos), evitando el sobreajuste del proceso (*tampering*) y reduciendo costos.
            """
        )

        st.markdown("### Flujo del sistema")
        pasos = [
            ("📥", "Ingreso de datos",        "Carga de mediciones por subgrupo"),
            ("🔍", "Validación estadística",  "Normalidad, outliers y descriptivos"),
            ("📊", "Fase 1 – Estabilización", "Cálculo de límites de control"),
            ("📈", "Fase 2 – Monitoreo",      "Vigilancia continua del proceso"),
            ("⚙️", "Capacidad del proceso",   "Índices Cp, Cpk, Pp, Ppk"),
            ("💡", "Recomendaciones",          "Acciones de mejora priorizadas"),
        ]
        for ico, nom, desc in pasos:
            st.markdown(
                f"""<div class="fstep">
                    <span class="fstep-ico">{ico}</span>
                    <div>
                        <div class="fstep-name">{nom}</div>
                        <div class="fstep-desc">{desc}</div>
                    </div>
                </div>""",
                unsafe_allow_html=True,
            )

    with col_vis:
        st.markdown("### Variable principal")
        for lbl, val in [
            ("Variable de control",  "Resistencia a compresión"),
            ("Límite inferior (LSL)", "130 kg/cm²"),
            ("Límite superior (USL)", "160 kg/cm²"),
            ("Valor objetivo",        "145 kg/cm²"),
        ]:
            tarjeta(lbl, val)

    sep()

    st.markdown("### 💰 Relación Calidad – Costos")
    caja(
        "La mala calidad no solo genera rechazos: impacta costos de reproceso, garantías, "
        "pérdida de clientes y reputación. El CEP reduce costos interviniendo antes de producir defectos.",
        tipo="info",
    )
    cols = st.columns(4)
    for c, (ico, nom, desc) in zip(cols, [
        ("🔄", "Reproceso",        "Lotes fuera de especificación reworkeados"),
        ("🗑️", "Scrap",            "Material desechado sin recuperación"),
        ("🔎", "Inspección 100 %", "Recursos en verificación total de piezas"),
        ("📉", "Pérdida cliente",  "Devoluciones y penalizaciones contractuales"),
    ]):
        with c:
            st.markdown(
                f"""<div class="m-card">
                    <div style="font-size:1.5rem;margin-bottom:8px">{ico}</div>
                    <div class="m-lbl">{nom}</div>
                    <div class="m-note">{desc}</div>
                </div>""",
                unsafe_allow_html=True,
            )

    sep()

    st.markdown("### 📚 Normas y referencias")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Normas de producto**")
        for n in ["NTC 4026 – Bloques de concreto", "ASTM C90 – Unit masonry", "ASTM C140 – Sampling & testing"]:
            badge(n, "blue"); st.write("")
    with c2:
        st.markdown("**Normas de proceso**")
        for n in ["ISO 9001:2015 – SGC", "AIAG SPC Manual 2nd Ed.", "ASTM E2281 – Process Capability"]:
            badge(n, "green"); st.write("")


# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 2 – Ingreso de datos
# ─────────────────────────────────────────────────────────────────────────────

# ── Constantes del módulo ─────────────────────────────────────────────────────

# Nombres canónicos que el sistema reconoce automáticamente al detectar columnas.
# Cualquier nombre que contenga alguna de estas cadenas (en minúsculas) se mapea
# a la variable correspondiente.
ALIAS_RESISTENCIA = ["resist", "compres", "mpa", "kg/cm", "f'c", "fc"]
ALIAS_ABSORCION   = ["absorc", "absorb", "agua", "water"]
ALIAS_SUBGRUPO    = ["subgrupo", "lote", "muestra", "grupo", "batch", "turno", "sg"]

# Rangos físicamente plausibles para detectar datos corruptos o unidades erróneas
RANGO_RESISTENCIA = (50.0,  400.0)   # kg/cm²  (mín y máx aceptables)
RANGO_ABSORCION   = (0.0,   25.0)    # %  (porcentaje de absorción)

# Límites de especificación predeterminados (NTC 4026 bloque tipo A)
LSL_RES_DEFAULT  = 130.0
USL_RES_DEFAULT  = 160.0
TARGET_RES_DEFAULT = 145.0
LSL_ABS_DEFAULT  = 0.0
USL_ABS_DEFAULT  = 10.0


# ── Funciones auxiliares del módulo ──────────────────────────────────────────

def _limpiar_estado_datos():
    """Restablece todas las claves de datos al estado inicial.
    Se llama cuando el usuario sube un archivo nuevo o limpia la carga."""
    st.session_state.datos_cargados     = False
    st.session_state.df_raw             = None
    st.session_state.df_subgrupos       = None
    st.session_state.col_resistencia    = None
    st.session_state.col_absorcion      = None
    st.session_state.col_subgrupo       = None
    st.session_state.errores_carga      = []
    st.session_state.advertencias_carga = []


def _detectar_columna(columnas: list[str], alias: list[str]) -> str | None:
    """Busca en la lista de columnas alguna que contenga uno de los alias.
    Devuelve el nombre original de la columna o None si no hay coincidencia.

    Args:
        columnas: nombres de columna del DataFrame (tal como vienen del archivo).
        alias: lista de subcadenas que indican la variable buscada.

    Returns:
        Primer nombre de columna que coincide, o None.
    """
    for col in columnas:
        col_lower = col.lower().strip()
        if any(a in col_lower for a in alias):
            return col
    return None


def _parsear_archivo(archivo) -> pd.DataFrame | None:
    """Lee un archivo CSV o Excel subido por el usuario y devuelve un DataFrame.

    Intenta múltiples encodings para CSV.  Devuelve None si ocurre un error
    irrecuperable y deja el mensaje en st.session_state.errores_carga.
    """
    nombre = archivo.name.lower()
    try:
        if nombre.endswith(".csv"):
            # Intentar encodings comunes en archivos de laboratorio latinoamericanos
            for enc in ("utf-8", "latin-1", "cp1252"):
                try:
                    archivo.seek(0)
                    return pd.read_csv(archivo, encoding=enc)
                except UnicodeDecodeError:
                    continue
            st.session_state.errores_carga.append(
                "No se pudo decodificar el CSV. Guárdelo con codificación UTF-8."
            )
            return None
        elif nombre.endswith((".xlsx", ".xls")):
            archivo.seek(0)
            return pd.read_excel(archivo)
        else:
            st.session_state.errores_carga.append("Formato de archivo no soportado.")
            return None
    except Exception as exc:
        st.session_state.errores_carga.append(f"Error al leer el archivo: {exc}")
        return None


def _validar_dataframe(df: pd.DataFrame) -> bool:
    """Ejecuta todas las validaciones estructurales sobre el DataFrame cargado.

    Llena st.session_state.errores_carga y .advertencias_carga.
    Retorna True si el DataFrame puede usarse (aunque con advertencias).
    """
    errores = st.session_state.errores_carga
    warns   = st.session_state.advertencias_carga

    # ── 1. El archivo no puede estar vacío ────────────────────────────────────
    if df.empty:
        errores.append("El archivo está vacío (0 filas).")
        return False

    # ── 2. Debe tener al menos 2 columnas ─────────────────────────────────────
    if df.shape[1] < 2:
        errores.append(
            f"El archivo tiene solo {df.shape[1]} columna(s). "
            "Se requieren al menos 2 (resistencia y absorción)."
        )
        return False

    # ── 3. Detectar columnas obligatorias ─────────────────────────────────────
    cols = df.columns.tolist()

    col_res = _detectar_columna(cols, ALIAS_RESISTENCIA)
    col_abs = _detectar_columna(cols, ALIAS_ABSORCION)

    if col_res is None:
        errores.append(
            "No se encontró una columna de **resistencia a compresión**. "
            "Renombre la columna incluyendo alguna de estas palabras: "
            + ", ".join(ALIAS_RESISTENCIA) + "."
        )
    if col_abs is None:
        errores.append(
            "No se encontró una columna de **absorción**. "
            "Renombre la columna incluyendo alguna de estas palabras: "
            + ", ".join(ALIAS_ABSORCION) + "."
        )

    if errores:        # Si faltó alguna columna obligatoria, detenerse aquí
        return False

    # ── 4. Las columnas detectadas deben ser numéricas ─────────────────────────
    for col, nombre in [(col_res, "resistencia"), (col_abs, "absorción")]:
        if not pd.api.types.is_numeric_dtype(df[col]):
            # Intentar conversión forzada antes de declarar error
            convertida = pd.to_numeric(df[col], errors="coerce")
            pct_nulos  = convertida.isna().mean()
            if pct_nulos > 0.5:
                errores.append(
                    f"La columna '{col}' ({nombre}) no es numérica "
                    f"({pct_nulos*100:.0f} % de valores no convertibles)."
                )
            else:
                warns.append(
                    f"La columna '{col}' ({nombre}) tenía valores no numéricos "
                    f"que fueron eliminados ({int(pct_nulos*len(df))} filas)."
                )

    if errores:
        return False

    # ── 5. Verificar valores mínimos después de limpiar nulos ─────────────────
    df_clean = df[[col_res, col_abs]].apply(pd.to_numeric, errors="coerce").dropna()
    if len(df_clean) < 10:
        errores.append(
            f"Después de limpiar valores no numéricos quedan solo {len(df_clean)} filas. "
            "Se requieren al menos 10 observaciones."
        )
        return False

    # ── 6. Validar rangos plausibles ──────────────────────────────────────────
    rmin_r, rmax_r = RANGO_RESISTENCIA
    fuera_res = (~df_clean[col_res].between(rmin_r, rmax_r)).sum()
    if fuera_res > 0:
        warns.append(
            f"{fuera_res} valor(es) de resistencia están fuera del rango esperado "
            f"[{rmin_r} – {rmax_r} kg/cm²]. Verifique las unidades."
        )

    rmin_a, rmax_a = RANGO_ABSORCION
    fuera_abs = (~df_clean[col_abs].between(rmin_a, rmax_a)).sum()
    if fuera_abs > 0:
        warns.append(
            f"{fuera_abs} valor(es) de absorción están fuera del rango esperado "
            f"[{rmin_a} – {rmax_a} %]. Verifique las unidades."
        )

    # ── 7. Detectar columna de subgrupo (opcional) ────────────────────────────
    col_sg = _detectar_columna(cols, ALIAS_SUBGRUPO)
    if col_sg:
        warns.append(
            f"Se detectó automáticamente la columna de subgrupo: **'{col_sg}'**."
        )

    # ── Guardar resultados en session_state ───────────────────────────────────
    st.session_state.col_resistencia = col_res
    st.session_state.col_absorcion   = col_abs
    st.session_state.col_subgrupo    = col_sg

    return True


def _construir_subgrupos(df: pd.DataFrame, col_res: str, col_abs: str,
                          col_sg: str | None, n: int) -> pd.DataFrame:
    """Agrega una columna 'subgrupo' al DataFrame limpio.

    Si el archivo ya tiene una columna de subgrupo, la usa.
    De lo contrario, asigna subgrupos consecutivos de tamaño n.

    Returns:
        DataFrame limpio con columnas numéricas y columna 'subgrupo' (int).
    """
    tiene_sg_valido = (
        col_sg is not None
        and col_sg in df.columns
        and col_sg != col_res
        and col_sg != col_abs
    )

    # Seleccionar solo las columnas que usaremos
    cols_usar = [col_res, col_abs]
    if tiene_sg_valido:
        cols_usar.append(col_sg)

    df_work = df[cols_usar].copy()
    df_work[col_res] = pd.to_numeric(df_work[col_res], errors="coerce")
    df_work[col_abs] = pd.to_numeric(df_work[col_abs], errors="coerce")
    df_work = df_work.dropna(subset=[col_res, col_abs]).reset_index(drop=True)

    if tiene_sg_valido:
        # Extraer serie de subgrupo ANTES de renombrar para evitar confusión de nombres
        serie_sg = df_work[col_sg].copy()
        df_work = df_work.drop(columns=[col_sg])
        # Re-encodificar a enteros secuenciales (1, 2, 3…)
        unicos   = serie_sg.unique()
        mapa_sg  = {v: i + 1 for i, v in enumerate(unicos)}
        df_work["subgrupo"] = serie_sg.map(mapa_sg).astype(int)
    else:
        # Asignar subgrupos consecutivos según el tamaño n configurado
        df_work["subgrupo"] = (df_work.index // n) + 1

    # Renombrar a nombres canónicos para el resto de la aplicación
    df_work = df_work.rename(columns={col_res: "resistencia", col_abs: "absorcion"})

    # Ordenar columnas de forma consistente
    return df_work[["subgrupo", "resistencia", "absorcion"]]


def _generar_datos_ejemplo(n_subgrupos: int = 30, n: int = 5,
                            seed: int = 42) -> pd.DataFrame:
    """Genera un dataset sintético realista de bloques de concreto.

    Simula un proceso con pequeña deriva positiva en resistencia y
    dos subgrupos con causas especiales (para que las cartas tengan señales).

    Args:
        n_subgrupos: Número de subgrupos a generar.
        n: Tamaño de cada subgrupo.
        seed: Semilla para reproducibilidad.

    Returns:
        DataFrame con columnas: subgrupo, medicion, resistencia, absorcion.
    """
    rng       = np.random.default_rng(seed)
    filas     = []
    media_res = 144.0          # Media del proceso (ligeramente bajo el target 145)
    sigma_res = 3.5            # Desviación estándar del proceso
    media_abs = 5.5            # Media de absorción (%)
    sigma_abs = 0.8

    for sg in range(1, n_subgrupos + 1):
        # Simular pequeña deriva en resistencia (causas comunes graduales)
        deriva = 0.05 * (sg - 1)

        for obs in range(1, n + 1):
            res = rng.normal(media_res + deriva, sigma_res)
            ab  = rng.normal(media_abs,          sigma_abs)

            # Introducir causas especiales en subgrupos 12 y 22
            if sg == 12:
                res -= 12.0   # Caída brusca (materia prima deficiente)
            if sg == 22:
                res += 10.0   # Pico alto (cambio de operario sin calibrar)

            filas.append({
                "subgrupo":    sg,
                "medicion":    obs,
                "resistencia": round(float(res), 2),
                "absorcion":   round(max(0.1, float(ab)), 2),
            })

    return pd.DataFrame(filas)


def _estadisticos_rapidos(df_sg: pd.DataFrame) -> dict:
    """Calcula estadísticos descriptivos básicos para la vista previa.

    Args:
        df_sg: DataFrame con columnas 'resistencia' y 'absorcion'.

    Returns:
        Diccionario con estadísticos por variable.
    """
    stats = {}
    for col in ["resistencia", "absorcion"]:
        s = df_sg[col]
        stats[col] = {
            "n":       len(s),
            "media":   round(s.mean(), 3),
            "std":     round(s.std(ddof=1), 3),
            "min":     round(s.min(), 3),
            "max":     round(s.max(), 3),
            "cv":      round(s.std(ddof=1) / s.mean() * 100, 2) if s.mean() != 0 else None,
        }
    return stats


# ── Panel principal de la sección ─────────────────────────────────────────────

def seccion_ingreso_datos():
    """Módulo completo de ingreso de datos del sistema CEP.

    Flujo interno:
    1. Panel de configuración del proceso (especificaciones y muestreo).
    2. Selección de fuente de datos (archivo / datos de ejemplo).
    3. Carga y parseo del archivo.
    4. Detección y mapeo de columnas.
    5. Validación estructural y de rangos.
    6. Configuración de subgrupos.
    7. Vista previa con estadísticos y tabla interactiva.
    8. Opción de descarga del dataset procesado.
    """
    encabezado(
        "📥", "Ingreso de datos",
        "Carga, validación y configuración de mediciones del proceso productivo",
    )

    # ══════════════════════════════════════════════════════════════════════════
    # BLOQUE A – Configuración del proceso
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("### ⚙️ Configuración del proceso")
    caja(
        "Defina los límites de especificación y los parámetros de muestreo antes de cargar datos. "
        "Estos valores se usarán en todas las secciones del sistema.",
        tipo="info",
    )

    with st.expander("📐 Especificaciones y muestreo", expanded=True):

        # ── Fila 1: Resistencia ───────────────────────────────────────────────
        st.markdown("**Resistencia a compresión (kg/cm²)**")
        c1, c2, c3 = st.columns(3)
        with c1:
            lsl_res = st.number_input(
                "LSL – Límite inferior de especificación",
                value=float(st.session_state.config_proceso.get("lsl_res", LSL_RES_DEFAULT)),
                step=0.5, format="%.1f", key="cfg_lsl_res",
                help="Valor mínimo aceptable de resistencia según norma NTC 4026.",
            )
        with c2:
            usl_res = st.number_input(
                "USL – Límite superior de especificación",
                value=float(st.session_state.config_proceso.get("usl_res", USL_RES_DEFAULT)),
                step=0.5, format="%.1f", key="cfg_usl_res",
                help="Valor máximo aceptable de resistencia.",
            )
        with c3:
            target_res = st.number_input(
                "Target – Valor nominal objetivo",
                value=float(st.session_state.config_proceso.get("target_res", TARGET_RES_DEFAULT)),
                step=0.5, format="%.1f", key="cfg_target_res",
                help="Centro del diseño. Idealmente (LSL + USL) / 2.",
            )

        # Validación inline LSL < Target < USL
        if not (lsl_res < target_res < usl_res):
            caja("⚠️ Verifique: debe cumplirse LSL < Target < USL para la resistencia.", tipo="warning")

        st.markdown("<div style='margin-top:14px'></div>", unsafe_allow_html=True)

        # ── Fila 2: Absorción ──────────────────────────────────────────────────
        st.markdown("**Absorción de agua (%)**")
        c4, c5 = st.columns(2)
        with c4:
            lsl_abs = st.number_input(
                "LSL – Mínimo de absorción",
                value=float(st.session_state.config_proceso.get("lsl_abs", LSL_ABS_DEFAULT)),
                step=0.1, format="%.1f", key="cfg_lsl_abs",
                help="Generalmente 0. Un valor muy bajo puede indicar bloques impermeabilizados.",
            )
        with c5:
            usl_abs = st.number_input(
                "USL – Máximo de absorción",
                value=float(st.session_state.config_proceso.get("usl_abs", USL_ABS_DEFAULT)),
                step=0.1, format="%.1f", key="cfg_usl_abs",
                help="NTC 4026 establece máximo 10 % de absorción para bloque tipo A.",
            )

        st.markdown("<div style='margin-top:14px'></div>", unsafe_allow_html=True)

        # ── Fila 3: Muestreo ──────────────────────────────────────────────────
        st.markdown("**Parámetros de muestreo**")
        c6, c7, c8 = st.columns(3)
        with c6:
            n_muestra = st.number_input(
                "Tamaño de subgrupo (n)",
                value=int(st.session_state.config_proceso.get("tamano_subgrupo", 5)),
                min_value=2, max_value=25, step=1, key="cfg_n",
                help="Número de piezas medidas por subgrupo racional. Recomendado: 4–6.",
            )
        with c7:
            n_min_sg = st.number_input(
                "N° mínimo de subgrupos para Fase 1",
                value=int(st.session_state.config_proceso.get("n_subgrupos_min", 25)),
                min_value=10, max_value=100, step=1, key="cfg_sg_min",
                help="Se recomiendan al menos 25 subgrupos para estimar límites de control confiables.",
            )
        with c8:
            frecuencia = st.selectbox(
                "Frecuencia de muestreo",
                ["Por turno", "Por hora", "Por lote", "Diaria", "Semanal", "Personalizada"],
                index=["Por turno", "Por hora", "Por lote", "Diaria", "Semanal", "Personalizada"]
                      .index(st.session_state.config_proceso.get("frecuencia", "Por turno")),
                key="cfg_frec",
                help="Define cada cuánto tiempo / lotes se toma un subgrupo.",
            )

        # Guardar configuración actualizada en session_state
        st.session_state.config_proceso.update({
            "lsl_res":         lsl_res,
            "usl_res":         usl_res,
            "target_res":      target_res,
            "lsl_abs":         lsl_abs,
            "usl_abs":         usl_abs,
            "tamano_subgrupo": n_muestra,
            "n_subgrupos_min": n_min_sg,
            "frecuencia":      frecuencia,
        })

    sep()

    # ══════════════════════════════════════════════════════════════════════════
    # BLOQUE B – Fuente de datos
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("### 📂 Fuente de datos")

    metodo = st.radio(
        "Seleccione la fuente:",
        ["📁 Cargar archivo (CSV / Excel)", "🎲 Datos de ejemplo (simulados)"],
        horizontal=True,
        key="metodo_carga",
    )

    # ── Fuente 1: Archivo del usuario ─────────────────────────────────────────
    if metodo == "📁 Cargar archivo (CSV / Excel)":
        caja(
            "El archivo debe contener al menos una columna de **resistencia a compresión** "
            "y una de **absorción de agua**. Puede incluir también una columna de subgrupo o lote.",
            tipo="info",
        )

        with st.expander("📋 Formato esperado del archivo", expanded=False):
            st.markdown(
                """
                **Nombres de columna sugeridos** (el sistema los detecta automáticamente):

                | Variable | Ejemplos de nombre válido |
                |----------|--------------------------|
                | Resistencia | `resistencia`, `compresion`, `fc`, `mpa`, `kg/cm2` |
                | Absorción | `absorcion`, `absorb`, `agua` |
                | Subgrupo | `subgrupo`, `lote`, `turno`, `batch` |

                **Tipos de archivo soportados:** `.csv`, `.xlsx`, `.xls`

                **Estructura mínima esperada (una fila = una medición):**
                ```
                subgrupo, resistencia, absorcion
                1, 141.2, 5.4
                1, 138.9, 5.7
                2, 143.0, 5.1
                ...
                ```
                """
            )

        uploaded = st.file_uploader(
            "Arrastre su archivo aquí o haga clic para seleccionar",
            type=["csv", "xlsx", "xls"],
            key="file_uploader",
            label_visibility="collapsed",
        )

        if uploaded is not None:
            # Si es un archivo nuevo, limpiar estado anterior
            clave_archivo = f"{uploaded.name}_{uploaded.size}"
            if st.session_state.get("_ultimo_archivo") != clave_archivo:
                _limpiar_estado_datos()
                st.session_state["_ultimo_archivo"] = clave_archivo

            # Procesar si aún no está cargado
            if not st.session_state.datos_cargados:
                with st.spinner("Leyendo y validando el archivo…"):
                    df_leido = _parsear_archivo(uploaded)

                if df_leido is not None:
                    valido = _validar_dataframe(df_leido)

                    if valido:
                        # Construir DataFrame de subgrupos con la config actual
                        n_sg = st.session_state.config_proceso["tamano_subgrupo"]
                        df_sg = _construir_subgrupos(
                            df_leido,
                            st.session_state.col_resistencia,
                            st.session_state.col_absorcion,
                            st.session_state.col_subgrupo,
                            n_sg,
                        )
                        st.session_state.df_raw       = df_leido
                        st.session_state.df_subgrupos = df_sg
                        st.session_state.datos_cargados = True

    # ── Fuente 2: Datos de ejemplo ────────────────────────────────────────────
    else:
        n_sg_ej = st.session_state.config_proceso.get("tamano_subgrupo", 5)
        st.markdown(
            f"""
            <div class="m-card" style="text-align:left;padding:20px 24px">
                <div class="m-lbl" style="margin-bottom:10px">Dataset sintético – NTC 4026</div>
                <p style="font-size:.88rem;color:var(--text);margin:0 0 8px">
                    Genera <strong>30 subgrupos × {n_sg_ej} observaciones</strong> de resistencia a compresión
                    y absorción de agua con las siguientes características:
                </p>
                <ul style="font-size:.84rem;color:var(--muted);margin:0;padding-left:20px">
                    <li>Proceso centrado en <strong>144 kg/cm²</strong> (σ = 3.5)</li>
                    <li>Absorción media <strong>5.5 %</strong> (σ = 0.8)</li>
                    <li>Causas especiales simuladas en subgrupos <strong>12</strong> y <strong>22</strong></li>
                    <li>Pequeña deriva positiva a lo largo del tiempo</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("⚡ Generar y cargar datos de ejemplo", type="primary"):
            _limpiar_estado_datos()
            with st.spinner("Generando datos sintéticos…"):
                df_ejemplo = _generar_datos_ejemplo(
                    n_subgrupos=30,
                    n=n_sg_ej,
                )
            # Los datos de ejemplo ya tienen columnas estándar
            st.session_state.df_raw           = df_ejemplo
            st.session_state.df_subgrupos     = df_ejemplo[["subgrupo", "resistencia", "absorcion"]]
            st.session_state.col_resistencia  = "resistencia"
            st.session_state.col_absorcion    = "absorcion"
            st.session_state.col_subgrupo     = "subgrupo"
            st.session_state.datos_cargados   = True
            caja(f"Datos de ejemplo generados: {len(df_ejemplo)} observaciones en 30 subgrupos.", tipo="success")

    sep()

    # ══════════════════════════════════════════════════════════════════════════
    # BLOQUE C – Mensajes de validación
    # ══════════════════════════════════════════════════════════════════════════
    errores = st.session_state.get("errores_carga", [])
    warns   = st.session_state.get("advertencias_carga", [])

    if errores:
        st.markdown("### ❌ Errores de validación")
        for err in errores:
            caja(err, tipo="warning")
        caja(
            "Corrija los errores indicados y vuelva a cargar el archivo.",
            tipo="warning",
        )
        return   # No mostrar nada más si hay errores fatales

    for w in warns:
        caja(w, tipo="warning")

    # ══════════════════════════════════════════════════════════════════════════
    # BLOQUE D – Vista previa (solo si hay datos válidos)
    # ══════════════════════════════════════════════════════════════════════════
    if not st.session_state.get("datos_cargados") or st.session_state.df_subgrupos is None:
        st.markdown("### 👁️ Vista previa de datos")
        proximamente(
            "Esperando datos",
            "Cargue un archivo CSV / Excel o genere los datos de ejemplo para continuar.",
        )
        return

    df_sg   = st.session_state.df_subgrupos
    n_obs   = len(df_sg)
    n_sgs   = df_sg["subgrupo"].nunique()
    n_tam   = st.session_state.config_proceso["tamano_subgrupo"]
    stats   = _estadisticos_rapidos(df_sg)

    # ── Tarjetas de resumen ────────────────────────────────────────────────────
    st.markdown("### ✅ Resumen de la carga")

    c1, c2, c3, c4 = st.columns(4)
    with c1: tarjeta("Total observaciones", str(n_obs))
    with c2: tarjeta("Subgrupos",           str(n_sgs),  f"n = {n_tam} por subgrupo")
    with c3: tarjeta("Col. resistencia",    st.session_state.col_resistencia or "—")
    with c4: tarjeta("Col. absorción",      st.session_state.col_absorcion   or "—")

    # Verificar si hay suficientes subgrupos para Fase 1
    n_min = st.session_state.config_proceso.get("n_subgrupos_min", 25)
    if n_sgs < n_min:
        caja(
            f"Se tienen **{n_sgs} subgrupos** pero se recomiendan al menos **{n_min}** "
            f"para construir límites de control confiables en Fase 1.",
            tipo="warning",
        )
    else:
        caja(
            f"✔ El dataset contiene {n_sgs} subgrupos (≥ {n_min} recomendados). "
            "Puede proceder a la validación estadística.",
            tipo="success",
        )

    sep()

    # ── Estadísticos rápidos ───────────────────────────────────────────────────
    st.markdown("### 📐 Estadísticos descriptivos rápidos")

    col_res_s = stats["resistencia"]
    col_abs_s = stats["absorcion"]

    # Resistencia
    st.markdown("**Resistencia a compresión (kg/cm²)**")
    cr1, cr2, cr3, cr4, cr5 = st.columns(5)
    lbl_vals = [
        ("Media (x̄)",    f"{col_res_s['media']:.2f}"),
        ("Desv. Est. (s)", f"{col_res_s['std']:.2f}"),
        ("Mínimo",        f"{col_res_s['min']:.2f}"),
        ("Máximo",        f"{col_res_s['max']:.2f}"),
        ("CV (%)",        f"{col_res_s['cv']:.1f}" if col_res_s['cv'] else "—"),
    ]
    for col_ui, (lbl, val) in zip([cr1, cr2, cr3, cr4, cr5], lbl_vals):
        with col_ui: tarjeta(lbl, val)

    # Verificar si la media está dentro de especificaciones
    media_res = col_res_s["media"]
    lsl_r = st.session_state.config_proceso["lsl_res"]
    usl_r = st.session_state.config_proceso["usl_res"]
    if lsl_r <= media_res <= usl_r:
        caja(f"La media de resistencia ({media_res:.2f}) está dentro de las especificaciones [{lsl_r} – {usl_r}].", tipo="success")
    else:
        caja(f"⚠️ La media de resistencia ({media_res:.2f}) está **fuera** de las especificaciones [{lsl_r} – {usl_r}].", tipo="warning")

    st.markdown("<div style='margin-top:16px'></div>", unsafe_allow_html=True)

    # Absorción
    st.markdown("**Absorción de agua (%)**")
    ca1, ca2, ca3, ca4, ca5 = st.columns(5)
    lbl_vals_abs = [
        ("Media (x̄)",    f"{col_abs_s['media']:.2f}"),
        ("Desv. Est. (s)", f"{col_abs_s['std']:.2f}"),
        ("Mínimo",        f"{col_abs_s['min']:.2f}"),
        ("Máximo",        f"{col_abs_s['max']:.2f}"),
        ("CV (%)",        f"{col_abs_s['cv']:.1f}" if col_abs_s['cv'] else "—"),
    ]
    for col_ui, (lbl, val) in zip([ca1, ca2, ca3, ca4, ca5], lbl_vals_abs):
        with col_ui: tarjeta(lbl, val)

    # Verificar si la media de absorción está dentro de spec
    media_abs = col_abs_s["media"]
    usl_a = st.session_state.config_proceso["usl_abs"]
    if media_abs <= usl_a:
        caja(f"La media de absorción ({media_abs:.2f} %) cumple el máximo especificado ({usl_a} %).", tipo="success")
    else:
        caja(f"⚠️ La media de absorción ({media_abs:.2f} %) **excede** el máximo especificado ({usl_a} %).", tipo="warning")

    sep()

    # ── Mapeo de columnas (revisión manual) ───────────────────────────────────
    st.markdown("### 🗺️ Mapeo de columnas")
    caja(
        "El sistema detectó automáticamente las columnas. Si la asignación no es correcta, "
        "ajústela manualmente en los selectores y pulse **Aplicar mapeo**.",
        tipo="info",
    )

    cols_disponibles = st.session_state.df_raw.columns.tolist()
    cm1, cm2, cm3 = st.columns(3)
    with cm1:
        nueva_col_res = st.selectbox(
            "Columna → Resistencia (kg/cm²)",
            options=cols_disponibles,
            index=cols_disponibles.index(st.session_state.col_resistencia)
                  if st.session_state.col_resistencia in cols_disponibles else 0,
            key="map_resistencia",
        )
    with cm2:
        nueva_col_abs = st.selectbox(
            "Columna → Absorción (%)",
            options=cols_disponibles,
            index=cols_disponibles.index(st.session_state.col_absorcion)
                  if st.session_state.col_absorcion in cols_disponibles else 0,
            key="map_absorcion",
        )
    with cm3:
        cols_sg_opts = ["— Ninguna (asignar automáticamente) —"] + cols_disponibles
        idx_sg = (
            cols_sg_opts.index(st.session_state.col_subgrupo)
            if st.session_state.col_subgrupo in cols_sg_opts else 0
        )
        nueva_col_sg_raw = st.selectbox(
            "Columna → Subgrupo / Lote (opcional)",
            options=cols_sg_opts,
            index=idx_sg,
            key="map_subgrupo",
        )

    nueva_col_sg = None if nueva_col_sg_raw.startswith("—") else nueva_col_sg_raw

    # Advertir si resistencia y absorción apuntan a la misma columna
    if nueva_col_res == nueva_col_abs:
        caja("Resistencia y absorción no pueden apuntar a la misma columna.", tipo="warning")
    else:
        if st.button("✅ Aplicar mapeo", type="secondary"):
            # Reconstruir subgrupos con el nuevo mapeo
            n_sg = st.session_state.config_proceso["tamano_subgrupo"]
            df_sg_nuevo = _construir_subgrupos(
                st.session_state.df_raw,
                nueva_col_res,
                nueva_col_abs,
                nueva_col_sg,
                n_sg,
            )
            st.session_state.col_resistencia  = nueva_col_res
            st.session_state.col_absorcion    = nueva_col_abs
            st.session_state.col_subgrupo     = nueva_col_sg
            st.session_state.df_subgrupos     = df_sg_nuevo
            caja("Mapeo aplicado correctamente.", tipo="success")
            st.rerun()

    sep()

    # ── Tabla de datos procesados ──────────────────────────────────────────────
    st.markdown("### 📋 Tabla de datos procesados")

    vista = st.radio(
        "Mostrar:",
        ["Vista por observación", "Vista por subgrupo (resumen)"],
        horizontal=True,
        key="vista_tabla",
    )

    if vista == "Vista por observación":
        # Mostrar primeras 100 filas para no sobrecargar el navegador
        df_mostrar = df_sg.head(100).copy()
        df_mostrar.index = range(1, len(df_mostrar) + 1)

        # Columnas de estado (sin applymap ni format condicional CSS)
        lsl_r = st.session_state.config_proceso["lsl_res"]
        usl_r = st.session_state.config_proceso["usl_res"]
        usl_a = st.session_state.config_proceso["usl_abs"]

        df_vista = df_mostrar[["subgrupo", "resistencia", "absorcion"]].copy()
        df_vista["resistencia"] = df_vista["resistencia"].round(2)
        df_vista["absorcion"]   = df_vista["absorcion"].round(2)

        # Indica si cada medición está dentro o fuera de especificación
        def _estado_res(v):
            if pd.isna(v):
                return "—"
            return "✅ OK" if lsl_r <= v <= usl_r else "❌ Fuera spec"

        def _estado_abs(v):
            if pd.isna(v):
                return "—"
            return "✅ OK" if v <= usl_a else "⚠️ Excede USL"

        df_vista["estado_resistencia"] = df_vista["resistencia"].apply(_estado_res)
        df_vista["estado_absorcion"]   = df_vista["absorcion"].apply(_estado_abs)

        st.dataframe(df_vista, use_container_width=True, height=380)

        if n_obs > 100:
            caja(f"Mostrando las primeras 100 de {n_obs} observaciones.", tipo="info")

    else:
        # Vista resumen: una fila por subgrupo con media, rango, desv. est.
        resumen = (
            df_sg.groupby("subgrupo")
            .agg(
                n_obs        =("resistencia", "count"),
                media_res    =("resistencia", "mean"),
                rango_res    =("resistencia", lambda x: x.max() - x.min()),
                std_res      =("resistencia", "std"),
                media_abs    =("absorcion",   "mean"),
                rango_abs    =("absorcion",   lambda x: x.max() - x.min()),
            )
            .round(3)
            .reset_index()
        )
        resumen.columns = [
            "Subgrupo", "n", "X̄ Resist.", "R Resist.", "S Resist.",
            "X̄ Absorc.", "R Absorc.",
        ]
        st.dataframe(resumen, use_container_width=True, height=380)
        caja(f"Resumen de {n_sgs} subgrupos · {n_obs} observaciones totales.", tipo="info")

    sep()

    # ── Descarga del dataset procesado ────────────────────────────────────────
    st.markdown("### 💾 Descargar datos procesados")

    c_dl1, c_dl2, _ = st.columns([1, 1, 2])

    with c_dl1:
        csv_bytes = df_sg.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Descargar CSV",
            data=csv_bytes,
            file_name="datos_cep_procesados.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with c_dl2:
        # Generar Excel en memoria usando openpyxl a través de pandas
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df_sg.to_excel(writer, sheet_name="Observaciones", index=False)
            # Hoja adicional con resumen por subgrupo
            resumen_dl = (
                df_sg.groupby("subgrupo")
                .agg(
                    n         =("resistencia", "count"),
                    media_res =("resistencia", "mean"),
                    rango_res =("resistencia", lambda x: x.max() - x.min()),
                    std_res   =("resistencia", "std"),
                    media_abs =("absorcion",   "mean"),
                )
                .round(3)
                .reset_index()
            )
            resumen_dl.to_excel(writer, sheet_name="Resumen subgrupos", index=False)
        buffer.seek(0)
        st.download_button(
            label="⬇️ Descargar Excel",
            data=buffer,
            file_name="datos_cep_procesados.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )

    caja(
        "Los datos descargados incluyen columnas estándar **subgrupo · resistencia · absorcion** "
        "listas para ser importadas directamente en otras secciones del sistema.",
        tipo="info",
    )


# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 3 – Validación estadística
# ─────────────────────────────────────────────────────────────────────────────

# ── Constantes del módulo ─────────────────────────────────────────────────────

# Umbral de significancia para pruebas de normalidad
ALPHA = 0.05

# Límite de tamaño muestral para Shapiro-Wilk (máx. 5 000 obs.)
SW_MAX_N = 5_000

# Colores corporativos para gráficos
C_PRIMARY  = "#3b82f6"   # azul principal
C_ACCENT   = "#f59e0b"   # naranja/advertencia
C_SUCCESS  = "#22c55e"   # verde OK
C_DANGER   = "#ef4444"   # rojo falla
C_MUTED    = "#64748b"   # gris apagado
C_SURFACE  = "#1a1d27"   # fondo tarjeta
C_NORMAL   = "#818cf8"   # violeta para curva normal


# ── Funciones de análisis estadístico ────────────────────────────────────────

def _shapiro_wilk(datos: np.ndarray) -> dict:
    """Ejecuta la prueba Shapiro-Wilk y devuelve un diccionario con resultados.

    Si n > SW_MAX_N se aplica K-S (Kolmogorov-Smirnov) contra normal como
    alternativa, ya que scipy.stats.shapiro no acepta más de 5 000 obs.

    Returns:
        dict con claves: stat, p_value, normal (bool), metodo, interpretacion.
    """
    n = len(datos)

    if n < 3:
        return {
            "stat": None, "p_value": None, "normal": None,
            "metodo": "—",
            "interpretacion": "Se necesitan al menos 3 observaciones.",
        }

    if n <= SW_MAX_N:
        stat, p = sp_stats.shapiro(datos)
        metodo = "Shapiro-Wilk"
    else:
        # Normalizar y aplicar KS contra N(0,1)
        z = (datos - datos.mean()) / datos.std(ddof=1)
        stat, p = sp_stats.kstest(z, "norm")
        metodo = "Kolmogorov-Smirnov (n > 5 000)"

    normal = bool(p > ALPHA)
    if normal:
        interp = (
            f"p = {p:.4f} > α = {ALPHA}  →  No se rechaza H₀. "
            "Los datos son **consistentes con una distribución normal**."
        )
    else:
        interp = (
            f"p = {p:.4f} ≤ α = {ALPHA}  →  Se rechaza H₀. "
            "Los datos **no siguen una distribución normal** con este nivel de significancia."
        )

    return {
        "stat": round(float(stat), 6),
        "p_value": round(float(p), 6),
        "normal": normal,
        "metodo": metodo,
        "interpretacion": interp,
    }


def _estadisticos_descriptivos(datos: np.ndarray) -> dict:
    """Calcula un conjunto completo de estadísticos descriptivos.

    Returns:
        dict con n, media, mediana, std, var, cv, min, max, rango,
        q1, q3, iqr, asimetria, curtosis.
    """
    n    = len(datos)
    med  = float(np.mean(datos))
    mdn  = float(np.median(datos))
    std  = float(np.std(datos, ddof=1))
    var  = float(np.var(datos, ddof=1))
    cv   = std / med * 100 if med != 0 else None
    q1   = float(np.percentile(datos, 25))
    q3   = float(np.percentile(datos, 75))
    asi  = float(sp_stats.skew(datos))
    kurt = float(sp_stats.kurtosis(datos))   # exceso de curtosis (normal = 0)

    return {
        "n":        n,
        "media":    round(med,  4),
        "mediana":  round(mdn,  4),
        "std":      round(std,  4),
        "var":      round(var,  4),
        "cv":       round(cv,   2) if cv is not None else None,
        "min":      round(float(datos.min()), 4),
        "max":      round(float(datos.max()), 4),
        "rango":    round(float(datos.max() - datos.min()), 4),
        "q1":       round(q1,   4),
        "q3":       round(q3,   4),
        "iqr":      round(q3 - q1, 4),
        "asimetria": round(asi, 4),
        "curtosis":  round(kurt, 4),
    }


def _interpretar_asimetria(valor: float) -> tuple[str, str]:
    """Devuelve (etiqueta, color) según el coeficiente de asimetría."""
    if abs(valor) < 0.5:
        return "Simétrica", C_SUCCESS
    if abs(valor) < 1.0:
        lab = "Asimetría moderada"
    else:
        lab = "Asimetría pronunciada"
    dir_ = "positiva (cola derecha)" if valor > 0 else "negativa (cola izquierda)"
    return f"{lab} {dir_}", C_ACCENT


def _interpretar_curtosis(valor: float) -> tuple[str, str]:
    """Devuelve (etiqueta, color) según el exceso de curtosis."""
    if abs(valor) < 0.5:
        return "Mesocúrtica (normal)", C_SUCCESS
    if valor > 0.5:
        return f"Leptocúrtica (colas pesadas, K={valor:.2f})", C_ACCENT
    return f"Platicúrtica (colas ligeras, K={valor:.2f})", C_ACCENT


# ── Funciones de graficación ──────────────────────────────────────────────────

def _fig_histograma(datos: np.ndarray, variable: str,
                    lsl: float, usl: float, target: float,
                    sw: dict) -> plt.Figure:
    """Genera el histograma con curva normal superpuesta y líneas de spec.

    Args:
        datos:    array 1-D de observaciones.
        variable: nombre de la variable (para título).
        lsl, usl, target: límites de especificación.
        sw:       resultado de _shapiro_wilk (para anotar en el gráfico).

    Returns:
        Figura matplotlib lista para st.pyplot().
    """
    fig, ax = plt.subplots(figsize=(8, 4.2))

    n    = len(datos)
    mean = datos.mean()
    std  = datos.std(ddof=1)

    # ── Histograma ──────────────────────────────────────────────────────
    # Número de bins por regla de Sturges ajustada
    bins = max(10, int(1 + 3.322 * np.log10(n)))
    counts, edges, patches = ax.hist(
        datos, bins=bins,
        color=C_PRIMARY, alpha=0.75, edgecolor="#0f1117", linewidth=0.6,
        zorder=2,
    )

    # Colorear barras fuera de especificación en rojo
    for patch, left, right in zip(patches, edges[:-1], edges[1:]):
        if right <= lsl or left >= usl:
            patch.set_facecolor(C_DANGER)
            patch.set_alpha(0.85)

    # ── Curva normal teórica superpuesta ────────────────────────────────
    x_curve = np.linspace(datos.min() - 2 * std, datos.max() + 2 * std, 300)
    y_curve = sp_stats.norm.pdf(x_curve, mean, std)
    # Escalar la densidad al conteo del histograma
    bin_width = edges[1] - edges[0]
    ax.plot(x_curve, y_curve * n * bin_width,
            color=C_NORMAL, linewidth=2, label="Dist. normal teórica", zorder=4)

    # ── Líneas de especificación ─────────────────────────────────────────
    ax.axvline(lsl,    color=C_DANGER,  linewidth=1.6, linestyle="--",
               label=f"LSL = {lsl}", zorder=5)
    ax.axvline(usl,    color=C_DANGER,  linewidth=1.6, linestyle="--",
               label=f"USL = {usl}", zorder=5)
    ax.axvline(target, color=C_ACCENT,  linewidth=1.4, linestyle=":",
               label=f"Target = {target}", zorder=5)
    ax.axvline(mean,   color=C_SUCCESS, linewidth=1.4, linestyle="-.",
               label=f"X̄ = {mean:.2f}", zorder=5)

    # ── Anotación del resultado SW ───────────────────────────────────────
    if sw["p_value"] is not None:
        color_txt = C_SUCCESS if sw["normal"] else C_DANGER
        ax.text(
            0.98, 0.97,
            f"{sw['metodo']}\nW = {sw['stat']:.4f}   p = {sw['p_value']:.4f}",
            transform=ax.transAxes, fontsize=7.5, color=color_txt,
            va="top", ha="right",
            bbox=dict(boxstyle="round,pad=0.35", facecolor="#0f1117",
                      edgecolor=color_txt, alpha=0.85),
        )

    ax.set_title(f"Histograma – {variable}", fontsize=11, fontweight="bold", pad=10)
    ax.set_xlabel(variable, fontsize=9)
    ax.set_ylabel("Frecuencia", fontsize=9)
    ax.legend(fontsize=7.5, loc="upper left",
              facecolor="#0f1117", edgecolor="#2a2d3e")
    ax.grid(True, axis="y")
    fig.tight_layout()
    return fig


def _fig_qq(datos: np.ndarray, variable: str, sw: dict) -> plt.Figure:
    """Genera el gráfico Q-Q (cuantil-cuantil) frente a la distribución normal.

    Los puntos se colorean verde si la prueba indica normalidad, rojo si no.
    Se dibuja la banda de confianza del 95 % usando la aproximación de Filliben.

    Returns:
        Figura matplotlib lista para st.pyplot().
    """
    fig, ax = plt.subplots(figsize=(5.5, 4.2))

    n    = len(datos)
    mean = datos.mean()
    std  = datos.std(ddof=1)

    # ── Cuantiles observados y teóricos (método de scipy) ────────────────
    (osm, osr), (slope, intercept, r) = sp_stats.probplot(datos, dist="norm")

    color_pts = C_SUCCESS if (sw.get("normal") is True) else (
        C_DANGER if (sw.get("normal") is False) else C_PRIMARY
    )

    ax.scatter(osm, osr, color=color_pts, s=22, alpha=0.80,
               edgecolors="none", zorder=3, label="Observaciones")

    # ── Línea de referencia (distribución normal perfecta) ───────────────
    x_line = np.array([osm.min(), osm.max()])
    ax.plot(x_line, slope * x_line + intercept,
            color=C_MUTED, linewidth=1.5, linestyle="--",
            label="Línea de referencia", zorder=2)

    # ── Banda de confianza del 95 % (bootstrap aproximado) ───────────────
    ci = 1.96 * std * np.sqrt(
        sp_stats.norm.pdf(osm) ** (-2) * (
            sp_stats.norm.cdf(osm) * (1 - sp_stats.norm.cdf(osm)) / n
        )
    )
    ax.fill_between(
        osm,
        slope * osm + intercept - ci,
        slope * osm + intercept + ci,
        color=C_PRIMARY, alpha=0.12, label="IC 95 %",
    )

    # ── Anotación R² ─────────────────────────────────────────────────────
    ax.text(
        0.04, 0.96, f"R² = {r**2:.4f}",
        transform=ax.transAxes, fontsize=8, color=C_ACCENT,
        va="top",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="#0f1117",
                  edgecolor=C_ACCENT, alpha=0.85),
    )

    ax.set_title(f"Gráfico Q-Q – {variable}", fontsize=11, fontweight="bold", pad=10)
    ax.set_xlabel("Cuantiles teóricos (Normal)", fontsize=9)
    ax.set_ylabel("Cuantiles observados", fontsize=9)
    ax.legend(fontsize=7.5, facecolor="#0f1117", edgecolor="#2a2d3e")
    ax.grid(True)
    fig.tight_layout()
    return fig


def _fig_boxplot(datos_res: np.ndarray, datos_abs: np.ndarray) -> plt.Figure:
    """Boxplot lado a lado de resistencia y absorción para detección visual de outliers.

    Returns:
        Figura matplotlib.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3.8))

    kw = dict(
        vert=True, patch_artist=True, widths=0.45,
        medianprops=dict(color=C_ACCENT, linewidth=2),
        flierprops=dict(marker="o", markerfacecolor=C_DANGER,
                        markersize=5, linestyle="none", alpha=0.8),
        whiskerprops=dict(color=C_MUTED),
        capprops=dict(color=C_MUTED),
    )

    bp1 = ax1.boxplot(datos_res, **kw)
    bp1["boxes"][0].set_facecolor(C_PRIMARY + "55")
    ax1.set_title("Resistencia (kg/cm²)", fontsize=10, fontweight="bold")
    ax1.set_xticks([])
    ax1.grid(True, axis="y")

    bp2 = ax2.boxplot(datos_abs, **kw)
    bp2["boxes"][0].set_facecolor(C_SUCCESS + "55")
    ax2.set_title("Absorción (%)", fontsize=10, fontweight="bold")
    ax2.set_xticks([])
    ax2.grid(True, axis="y")

    fig.suptitle("Diagrama de caja – detección visual de outliers",
                 fontsize=10, color="#e2e8f0", y=1.01)
    fig.tight_layout()
    return fig


# ── Panel de decisión automática ─────────────────────────────────────────────

def _panel_decision(sw_res: dict, sw_abs: dict, est_res: dict, est_abs: dict):
    """Renderiza el bloque de decisión y recomendaciones de herramientas CEP.

    La lógica determina qué tipo de carta de control y qué análisis es más
    adecuado según la normalidad de cada variable.
    """
    ambas_normales  = sw_res["normal"] and sw_abs["normal"]
    alguna_normal   = sw_res["normal"] or  sw_abs["normal"]
    ninguna_normal  = not sw_res["normal"] and not sw_abs["normal"]

    # ── Veredicto global ──────────────────────────────────────────────────
    if ambas_normales:
        color_v, icono_v, titulo_v = "#22c55e", "✅", "Ambas variables siguen distribución normal"
        msg_v = (
            "Los supuestos de normalidad se cumplen para resistencia y absorción. "
            "Puede proceder con las **cartas de control X̄-R / X̄-S** y los "
            "**índices de capacidad Cp/Cpk** con plena validez estadística."
        )
    elif alguna_normal:
        color_v, icono_v, titulo_v = "#f59e0b", "⚠️", "Una variable no sigue distribución normal"
        msg_v = (
            "Solo una variable cumple normalidad. Las cartas de control siguen siendo "
            "robustas para tamaños de subgrupo n ≥ 4 (Teorema Central del Límite). "
            "Interprete los índices Cpk con precaución para la variable no normal."
        )
    else:
        color_v, icono_v, titulo_v = "#ef4444", "❌", "Ninguna variable sigue distribución normal"
        msg_v = (
            "Los datos no cumplen el supuesto de normalidad. Considere: "
            "(1) verificar si existen causas especiales que distorsionen la distribución, "
            "(2) aplicar transformación Box-Cox, o "
            "(3) usar cartas de control no paramétricas."
        )

    st.markdown(
        f"""
        <div style="background:#0f1117;border:2px solid {color_v};border-radius:12px;
                    padding:20px 24px;margin:10px 0">
            <div style="font-size:1.15rem;font-weight:700;color:{color_v};margin-bottom:8px">
                {icono_v} {titulo_v}
            </div>
            <p style="font-size:.88rem;color:#e2e8f0;margin:0">{msg_v}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    sep()

    # ── Tabla de decisión por variable ────────────────────────────────────
    st.markdown("#### 📋 Decisión por variable")
    cols = st.columns(2)
    for col_ui, nombre_var, sw, est, lbl_unidad in [
        (cols[0], "Resistencia", sw_res, est_res, "kg/cm²"),
        (cols[1], "Absorción",   sw_abs, est_abs, "%"),
    ]:
        with col_ui:
            normal = sw["normal"]
            c_borde = C_SUCCESS if normal else C_DANGER
            estado  = "Normal ✅" if normal else "No normal ❌"
            asi_lbl, _   = _interpretar_asimetria(est["asimetria"])
            kurt_lbl, _  = _interpretar_curtosis(est["curtosis"])

            st.markdown(
                f"""
                <div style="background:{C_SURFACE};border:1px solid {c_borde};
                            border-radius:10px;padding:16px 18px">
                    <div style="font-weight:700;font-size:1rem;
                                color:{c_borde};margin-bottom:10px">
                        {nombre_var} ({lbl_unidad})
                    </div>
                    <table style="width:100%;font-size:.82rem;border-collapse:collapse">
                        <tr><td style="color:#64748b;padding:3px 0">Distribución</td>
                            <td style="color:{c_borde};text-align:right;font-weight:600">{estado}</td></tr>
                        <tr><td style="color:#64748b;padding:3px 0">p-value</td>
                            <td style="color:#e2e8f0;text-align:right">
                                {f"{sw['p_value']:.4f}" if sw['p_value'] is not None else '—'}
                            </td></tr>
                        <tr><td style="color:#64748b;padding:3px 0">Asimetría</td>
                            <td style="color:#e2e8f0;text-align:right">{est['asimetria']:.3f} · {asi_lbl}</td></tr>
                        <tr><td style="color:#64748b;padding:3px 0">Curtosis (exc.)</td>
                            <td style="color:#e2e8f0;text-align:right">{est['curtosis']:.3f} · {kurt_lbl}</td></tr>
                        <tr><td style="color:#64748b;padding:3px 0">CV (%)</td>
                            <td style="color:#e2e8f0;text-align:right">
                                {f"{est['cv']:.2f}" if est['cv'] is not None else '—'}
                            </td></tr>
                    </table>
                </div>
                """,
                unsafe_allow_html=True,
            )

    sep()

    # ── Recomendaciones de herramientas ───────────────────────────────────
    st.markdown("#### 🔧 Herramientas CEP recomendadas")
    herramientas = [
        (
            "Cartas X̄-R / X̄-S",
            "Robustas por el TCL para n ≥ 4. Aplicables aunque los individuales no sean normales.",
            C_SUCCESS if True else C_DANGER,
            "✅ Aplicable",
        ),
        (
            "Índices Cp / Cpk",
            "Requieren normalidad estricta. Use con precaución si alguna variable no es normal.",
            C_SUCCESS if ambas_normales else C_ACCENT,
            "✅ Aplicable" if ambas_normales else "⚠️ Con precaución",
        ),
        (
            "Transformación Box-Cox",
            "Recomendada si los datos no son normales y la asimetría supera ±1.",
            C_ACCENT if ninguna_normal else C_MUTED,
            "⚠️ Considerar" if ninguna_normal else "— No necesaria",
        ),
        (
            "Prueba de runs / rachas",
            "Complementaria para detectar patrones no aleatorios independientemente de la distribución.",
            C_PRIMARY,
            "ℹ️ Complementaria",
        ),
    ]

    for nom, desc, color, estado_h in herramientas:
        st.markdown(
            f"""
            <div style="display:flex;justify-content:space-between;align-items:center;
                        padding:10px 15px;background:{C_SURFACE};border-radius:8px;
                        border-left:3px solid {color};margin-bottom:7px">
                <div>
                    <span style="font-size:.9rem;font-weight:600;color:#e2e8f0">{nom}</span>
                    <span style="font-size:.78rem;color:#64748b;margin-left:10px">{desc}</span>
                </div>
                <span style="font-size:.78rem;color:{color};white-space:nowrap;margin-left:12px">{estado_h}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ── Función principal de la sección ──────────────────────────────────────────

def seccion_validacion():
    """Módulo completo de validación estadística del sistema CEP.

    Flujo interno:
    1. Verificar que haya datos cargados.
    2. Selector de variable a analizar.
    3. Estadísticos descriptivos completos.
    4. Prueba Shapiro-Wilk con interpretación.
    5. Histograma + curva normal superpuesta.
    6. Gráfico Q-Q con banda de confianza.
    7. Boxplot para detección visual de outliers.
    8. Panel de decisión automática y recomendaciones.
    9. Guardar resultados en st.session_state.validacion.
    """
    encabezado(
        "🔍", "Validación estadística",
        "Verificación del supuesto de normalidad antes de construir las cartas de control",
    )

    # ── Requisito previo: datos cargados ─────────────────────────────────────
    if not st.session_state.get("datos_cargados") or st.session_state.df_subgrupos is None:
        caja(
            "Cargue o genere datos en la sección **📥 Ingreso de datos** para habilitar este módulo.",
            tipo="warning",
        )
        return

    df_sg = st.session_state.df_subgrupos
    cfg   = st.session_state.config_proceso

    # Arrays de observaciones individuales (todas, sin agrupar)
    datos_res = df_sg["resistencia"].dropna().to_numpy()
    datos_abs = df_sg["absorcion"].dropna().to_numpy()

    # ══════════════════════════════════════════════════════════════════════════
    # BLOQUE A – Selector de variable y contexto
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("### 🎛️ Variable a analizar")
    c_sel, c_ctx = st.columns([1, 3])
    with c_sel:
        variable = st.radio(
            "Variable:",
            ["Resistencia", "Absorción", "Ambas"],
            key="val_variable",
        )
    with c_ctx:
        n_total  = len(datos_res)
        n_sgs    = df_sg["subgrupo"].nunique()
        n_tam    = cfg.get("tamano_subgrupo", 5)
        caja(
            f"Dataset activo: **{n_total} observaciones** · **{n_sgs} subgrupos** · "
            f"n = {n_tam} por subgrupo. "
            f"Umbral de significancia α = **{ALPHA}**.",
            tipo="info",
        )

    sep()

    # ══════════════════════════════════════════════════════════════════════════
    # BLOQUE B – Estadísticos descriptivos
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("### 📐 Estadísticos descriptivos")

    est_res = _estadisticos_descriptivos(datos_res)
    est_abs = _estadisticos_descriptivos(datos_abs)

    # Seleccionar cuáles mostrar según la variable elegida
    vars_mostrar = []
    if variable in ("Resistencia", "Ambas"):
        vars_mostrar.append(("Resistencia (kg/cm²)", est_res,
                              cfg["lsl_res"], cfg["usl_res"]))
    if variable in ("Absorción", "Ambas"):
        vars_mostrar.append(("Absorción (%)", est_abs,
                              cfg["lsl_abs"], cfg["usl_abs"]))

    for nombre_v, est, lsl_v, usl_v in vars_mostrar:
        st.markdown(f"**{nombre_v}**")

        # Fila 1: métricas de posición
        c1, c2, c3, c4, c5 = st.columns(5)
        for col_ui, lbl, val in [
            (c1, "n",           str(est["n"])),
            (c2, "Media (x̄)",  f"{est['media']:.3f}"),
            (c3, "Mediana",     f"{est['mediana']:.3f}"),
            (c4, "Desv. Est.", f"{est['std']:.3f}"),
            (c5, "CV (%)",      f"{est['cv']:.2f}" if est["cv"] else "—"),
        ]:
            with col_ui: tarjeta(lbl, val)

        # Fila 2: métricas de dispersión y forma
        c6, c7, c8, c9, c10 = st.columns(5)
        asi_lbl, asi_color = _interpretar_asimetria(est["asimetria"])
        kurt_lbl, kurt_color = _interpretar_curtosis(est["curtosis"])
        for col_ui, lbl, val in [
            (c6,  "Mínimo",       f"{est['min']:.3f}"),
            (c7,  "Máximo",       f"{est['max']:.3f}"),
            (c8,  "IQR",          f"{est['iqr']:.3f}"),
            (c9,  "Asimetría",    f"{est['asimetria']:.3f}"),
            (c10, "Curtosis exc.", f"{est['curtosis']:.3f}"),
        ]:
            with col_ui: tarjeta(lbl, val)

        # Interpretación de forma
        st.markdown(
            f"""
            <div style="display:flex;gap:10px;margin:6px 0 16px">
                <span style="font-size:.8rem;color:{asi_color};
                             background:{asi_color}22;padding:3px 10px;border-radius:20px">
                    {asi_lbl}
                </span>
                <span style="font-size:.8rem;color:{kurt_color};
                             background:{kurt_color}22;padding:3px 10px;border-radius:20px">
                    {kurt_lbl}
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    sep()

    # ══════════════════════════════════════════════════════════════════════════
    # BLOQUE C – Prueba Shapiro-Wilk
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("### 🔔 Prueba de normalidad – Shapiro-Wilk")
    caja(
        "**H₀:** Los datos provienen de una distribución normal.  "
        "**H₁:** Los datos no siguen distribución normal.  "
        f"Se rechaza H₀ si p-value ≤ α = {ALPHA}.",
        tipo="info",
    )

    sw_res = _shapiro_wilk(datos_res)
    sw_abs = _shapiro_wilk(datos_abs)

    sw_mostrar = []
    if variable in ("Resistencia", "Ambas"):
        sw_mostrar.append(("Resistencia (kg/cm²)", sw_res))
    if variable in ("Absorción", "Ambas"):
        sw_mostrar.append(("Absorción (%)", sw_abs))

    for nombre_v, sw in sw_mostrar:
        normal     = sw["normal"]
        c_borde    = C_SUCCESS if normal else C_DANGER
        icono_res  = "✅" if normal else "❌"
        estado_txt = "NORMAL" if normal else "NO NORMAL"

        # Tarjeta de resultado SW
        st.markdown(
            f"""
            <div style="background:#0f1117;border:1.5px solid {c_borde};
                        border-radius:10px;padding:18px 22px;margin:10px 0">
                <div style="display:flex;justify-content:space-between;align-items:center">
                    <span style="font-size:1rem;font-weight:700;color:#e2e8f0">{nombre_v}</span>
                    <span style="font-size:.85rem;font-weight:700;color:{c_borde};
                                 background:{c_borde}22;padding:4px 14px;border-radius:20px">
                        {icono_res} {estado_txt}
                    </span>
                </div>
                <div style="display:flex;gap:32px;margin-top:12px">
                    <div>
                        <div style="font-size:.68rem;color:#64748b;letter-spacing:.08em;
                                    text-transform:uppercase">Método</div>
                        <div style="font-size:.9rem;color:#e2e8f0;margin-top:2px">{sw['metodo']}</div>
                    </div>
                    <div>
                        <div style="font-size:.68rem;color:#64748b;letter-spacing:.08em;
                                    text-transform:uppercase">Estadístico W</div>
                        <div style="font-family:monospace;font-size:.9rem;
                                    color:#e2e8f0;margin-top:2px">{f"{sw['stat']:.6f}" if sw['stat'] is not None else '—'}</div>
                    </div>
                    <div>
                        <div style="font-size:.68rem;color:#64748b;letter-spacing:.08em;
                                    text-transform:uppercase">p-value</div>
                        <div style="font-family:monospace;font-size:.9rem;
                                    color:{c_borde};font-weight:700;margin-top:2px">
                            {f"{sw['p_value']:.6f}" if sw['p_value'] is not None else '—'}
                        </div>
                    </div>
                    <div>
                        <div style="font-size:.68rem;color:#64748b;letter-spacing:.08em;
                                    text-transform:uppercase">α</div>
                        <div style="font-family:monospace;font-size:.9rem;
                                    color:#e2e8f0;margin-top:2px">{ALPHA}</div>
                    </div>
                </div>
                <p style="font-size:.83rem;color:#94a3b8;margin:12px 0 0">
                    {sw['interpretacion']}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    sep()

    # ══════════════════════════════════════════════════════════════════════════
    # BLOQUE D – Histograma
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("### 📊 Histograma con curva normal teórica")
    caja(
        "Las barras **rojas** representan observaciones fuera de los límites de especificación. "
        "La curva violeta muestra la distribución normal teórica ajustada a media y desviación del proceso.",
        tipo="info",
    )

    if variable == "Ambas":
        c_h1, c_h2 = st.columns(2)
        with c_h1:
            fig_h_res = _fig_histograma(
                datos_res, "Resistencia (kg/cm²)",
                cfg["lsl_res"], cfg["usl_res"], cfg["target_res"], sw_res,
            )
            st.pyplot(fig_h_res, use_container_width=True)
            plt.close(fig_h_res)
        with c_h2:
            fig_h_abs = _fig_histograma(
                datos_abs, "Absorción (%)",
                cfg["lsl_abs"], cfg["usl_abs"],
                (cfg["lsl_abs"] + cfg["usl_abs"]) / 2, sw_abs,
            )
            st.pyplot(fig_h_abs, use_container_width=True)
            plt.close(fig_h_abs)

    elif variable == "Resistencia":
        fig_h = _fig_histograma(
            datos_res, "Resistencia (kg/cm²)",
            cfg["lsl_res"], cfg["usl_res"], cfg["target_res"], sw_res,
        )
        st.pyplot(fig_h, use_container_width=True)
        plt.close(fig_h)

    else:  # Absorción
        fig_h = _fig_histograma(
            datos_abs, "Absorción (%)",
            cfg["lsl_abs"], cfg["usl_abs"],
            (cfg["lsl_abs"] + cfg["usl_abs"]) / 2, sw_abs,
        )
        st.pyplot(fig_h, use_container_width=True)
        plt.close(fig_h)

    sep()

    # ══════════════════════════════════════════════════════════════════════════
    # BLOQUE E – Gráfico Q-Q
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("### 📈 Gráfico Q-Q (cuantil-cuantil)")
    caja(
        "Si los puntos siguen la línea de referencia y permanecen dentro de la **banda de confianza al 95 %**, "
        "los datos son consistentes con una distribución normal. "
        "Desviaciones en los extremos indican colas pesadas o asimetría.",
        tipo="info",
    )

    if variable == "Ambas":
        c_q1, c_q2 = st.columns(2)
        with c_q1:
            fig_q_res = _fig_qq(datos_res, "Resistencia (kg/cm²)", sw_res)
            st.pyplot(fig_q_res, use_container_width=True)
            plt.close(fig_q_res)
        with c_q2:
            fig_q_abs = _fig_qq(datos_abs, "Absorción (%)", sw_abs)
            st.pyplot(fig_q_abs, use_container_width=True)
            plt.close(fig_q_abs)

    elif variable == "Resistencia":
        fig_q = _fig_qq(datos_res, "Resistencia (kg/cm²)", sw_res)
        st.pyplot(fig_q, use_container_width=True)
        plt.close(fig_q)

    else:
        fig_q = _fig_qq(datos_abs, "Absorción (%)", sw_abs)
        st.pyplot(fig_q, use_container_width=True)
        plt.close(fig_q)

    sep()

    # ══════════════════════════════════════════════════════════════════════════
    # BLOQUE F – Boxplot (outliers visuales)
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("### 📦 Diagrama de caja – Detección visual de outliers")
    caja(
        "Los **puntos rojos** son outliers según la regla de Tukey (IQR × 1.5). "
        "La línea naranja es la mediana; la caja contiene el 50 % central de los datos.",
        tipo="info",
    )

    fig_box = _fig_boxplot(datos_res, datos_abs)
    st.pyplot(fig_box, use_container_width=True)
    plt.close(fig_box)

    # Conteo de outliers (IQR rule)
    def _contar_outliers_iqr(arr: np.ndarray) -> int:
        q1, q3 = np.percentile(arr, [25, 75])
        iqr    = q3 - q1
        return int(((arr < q1 - 1.5 * iqr) | (arr > q3 + 1.5 * iqr)).sum())

    n_out_res = _contar_outliers_iqr(datos_res)
    n_out_abs = _contar_outliers_iqr(datos_abs)

    col_or, col_oa = st.columns(2)
    with col_or:
        tipo_out = "warning" if n_out_res > 0 else "success"
        caja(
            f"Resistencia: **{n_out_res} outlier(s)** detectados por regla de Tukey "
            f"({n_out_res / len(datos_res) * 100:.1f} % de las observaciones).",
            tipo=tipo_out,
        )
    with col_oa:
        tipo_out = "warning" if n_out_abs > 0 else "success"
        caja(
            f"Absorción: **{n_out_abs} outlier(s)** detectados por regla de Tukey "
            f"({n_out_abs / len(datos_abs) * 100:.1f} % de las observaciones).",
            tipo=tipo_out,
        )

    sep()

    # ══════════════════════════════════════════════════════════════════════════
    # BLOQUE G – Panel de decisión automática
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("### 🧭 Decisión automática y recomendaciones")
    _panel_decision(sw_res, sw_abs, est_res, est_abs)

    # ── Guardar resultados en session_state para que otras secciones los lean
    st.session_state.validacion = {
        "normalidad_ok":      sw_res["normal"] and sw_abs["normal"],
        "sw_resistencia":     sw_res,
        "sw_absorcion":       sw_abs,
        "est_resistencia":    est_res,
        "est_absorcion":      est_abs,
        "outliers_res":       n_out_res,
        "outliers_abs":       n_out_abs,
    }


# ─────────────────────────────────────────────────────────────────────────────
# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 4 – Fase 1: Estabilización
# ─────────────────────────────────────────────────────────────────────────────

# ── Constantes SPC (AIAG SPC Manual 2nd Ed., Appendix VI) ────────────────────
# Índice = tamaño de subgrupo n. Índices 0 y 1 no se usan (n mínimo = 2).

_A2 = [None, None, 1.880, 1.023, 0.729, 0.577, 0.483, 0.419, 0.373, 0.337, 0.308,
       0.285, 0.266, 0.249, 0.235, 0.223, 0.212, 0.203, 0.194, 0.187, 0.180,
       0.173, 0.167, 0.162, 0.157, 0.153]

_D3 = [None, None, 0,     0,     0,     0,     0,     0.076, 0.136, 0.184, 0.223,
       0.256, 0.283, 0.307, 0.328, 0.347, 0.363, 0.378, 0.391, 0.403, 0.415,
       0.425, 0.434, 0.443, 0.451, 0.459]

_D4 = [None, None, 3.267, 2.574, 2.282, 2.115, 2.004, 1.924, 1.864, 1.816, 1.777,
       1.744, 1.717, 1.693, 1.672, 1.653, 1.637, 1.622, 1.608, 1.597, 1.585,
       1.575, 1.566, 1.557, 1.548, 1.541]

_A3 = [None, None, 2.659, 1.954, 1.628, 1.427, 1.287, 1.182, 1.099, 1.032, 0.975,
       0.927, 0.886, 0.850, 0.817, 0.789, 0.763, 0.739, 0.718, 0.698, 0.680,
       0.663, 0.647, 0.633, 0.619, 0.606]

_B3 = [None, None, 0,     0,     0,     0,     0.030, 0.118, 0.185, 0.239, 0.284,
       0.321, 0.354, 0.382, 0.406, 0.428, 0.448, 0.466, 0.482, 0.497, 0.510,
       0.523, 0.534, 0.545, 0.555, 0.565]

_B4 = [None, None, 3.267, 2.568, 2.266, 2.089, 1.970, 1.882, 1.815, 1.761, 1.716,
       1.679, 1.646, 1.618, 1.594, 1.572, 1.552, 1.534, 1.518, 1.503, 1.490,
       1.477, 1.466, 1.455, 1.445, 1.435]

# d2 para estimar sigma desde el rango medio (n=2..10)
_d2 = [None, None, 1.128, 1.693, 2.059, 2.326, 2.534, 2.704, 2.847, 2.970, 3.078]


# ── Funciones de calculo SPC ──────────────────────────────────────────────────

def _calcular_limites_xbar_r(xbar: np.ndarray, R: np.ndarray, n: int,
                             k: float = 3.0) -> dict:
    """Calcula limites de control para carta X-barra R.

    Args:
        xbar: array de medias por subgrupo.
        R:    array de rangos por subgrupo.
        n:    tamaño del subgrupo.
        k:    multiplicador sigma para los limites (default 3.0).

    Returns:
        dict con ucl, cl, lcl para xbar y para R.
    """
    xbar_bar = float(xbar.mean())
    R_bar    = float(R.mean())
    d2_n     = _d2[n] if n <= 10 else _d2[10]
    sigma_e  = R_bar / d2_n

    # X-barra: X̄ ± k·σ/√n
    ucl_x = xbar_bar + k * sigma_e / np.sqrt(n)
    lcl_x = xbar_bar - k * sigma_e / np.sqrt(n)

    # Rango: CL_R ± k·d3·σ  (d3 es la desv. est. del rango relativa a sigma)
    _d3_tbl = [None, None, 0.853, 0.888, 0.880, 0.864, 0.848, 0.833, 0.820, 0.808, 0.797]
    d3_n    = _d3_tbl[n] if 2 <= n <= 10 else 0.797
    ucl_r   = R_bar + k * d3_n * sigma_e
    lcl_r   = max(0.0, R_bar - k * d3_n * sigma_e)

    return {
        "xbar": {"ucl": ucl_x, "cl": xbar_bar, "lcl": lcl_x},
        "disp": {"ucl": ucl_r, "cl": R_bar,    "lcl": lcl_r},
        "tipo": "R",
        "sigma_est": sigma_e,
    }


def _calcular_limites_xbar_s(xbar: np.ndarray, S: np.ndarray, n: int,
                             k: float = 3.0) -> dict:
    """Calcula limites de control para carta X-barra S.

    Args:
        xbar: array de medias por subgrupo.
        S:    array de desviaciones estandar por subgrupo.
        n:    tamaño del subgrupo.
        k:    multiplicador sigma para los limites (default 3.0).

    Returns:
        dict con ucl, cl, lcl para xbar y para S.
    """
    import math as _math
    xbar_bar = float(xbar.mean())
    S_bar    = float(S.mean())

    # c4 calculado analiticamente
    c4_n = _math.sqrt(2 / (n - 1)) * (
        _math.gamma(n / 2) / _math.gamma((n - 1) / 2)
    )
    sigma_e = S_bar / c4_n

    # X-barra: X̄ ± k·σ/√n
    ucl_x = xbar_bar + k * sigma_e / _math.sqrt(n)
    lcl_x = xbar_bar - k * sigma_e / _math.sqrt(n)

    # S: CL_S ± k·sqrt(1-c4²)·σ
    ucl_s = S_bar + k * _math.sqrt(1 - c4_n**2) * sigma_e
    lcl_s = max(0.0, S_bar - k * _math.sqrt(1 - c4_n**2) * sigma_e)

    return {
        "xbar": {"ucl": ucl_x, "cl": xbar_bar, "lcl": lcl_x},
        "disp": {"ucl": ucl_s, "cl": S_bar,    "lcl": lcl_s},
        "tipo": "S",
        "sigma_est": sigma_e,
    }


def _calcular_limites_imr(individ: np.ndarray, k: float = 3.0) -> dict:
    """Calcula limites de control para carta I-MR (individuales - rango movil).

    Args:
        individ: array de observaciones individuales.
        k:       multiplicador sigma para los limites (default 3.0).

    Returns:
        dict con ucl, cl, lcl para I y para MR.
    """
    MR      = np.abs(np.diff(individ))
    MR_bar  = float(MR.mean())
    x_bar   = float(individ.mean())
    sigma   = MR_bar / 1.128          # d2 para n=2

    ucl_i  = x_bar  + k * sigma
    lcl_i  = x_bar  - k * sigma
    # Limites MR: D4/D3 para n=2 escalados con k
    # D4(n=2,k=3)=3.267 → 1 + k·d3/d2 = 1 + 3·0.853/1.128
    ucl_mr = MR_bar * (1 + k * 0.853 / 1.128)
    lcl_mr = max(0.0, MR_bar * (1 - k * 0.853 / 1.128))

    return {
        "xbar": {"ucl": ucl_i,  "cl": x_bar,  "lcl": lcl_i},
        "disp": {"ucl": ucl_mr, "cl": MR_bar, "lcl": lcl_mr},
        "tipo": "MR",
        "sigma_est": sigma,
    }


def _aplicar_reglas_we(
    serie: np.ndarray,
    ucl: float, cl: float, lcl: float,
    sigma_est: float,
    reglas: list,
) -> list:
    """Aplica las Reglas de Western Electric seleccionadas.

    Devuelve lista de indices (0-based) de subgrupos que violan alguna regla.

    Reglas implementadas:
      1. Punto mas alla de +/-3 sigma (UCL/LCL).
      2. 9 puntos consecutivos al mismo lado de la linea central.
      3. 6 puntos consecutivos en tendencia estrictamente monotonica.
      4. 14 puntos alternando arriba/abajo de la CL.
      5. 2 de 3 puntos en zona A (mas alla de +/-2 sigma, mismo lado).
      6. 4 de 5 puntos en zona B o mas alla (mas alla de +/-1 sigma, mismo lado).
      7. 15 puntos consecutivos dentro de la zona C (+/-1 sigma).
      8. 8 puntos consecutivos fuera de zona C (ninguno dentro de +/-1 sigma).

    Args:
        serie:     array de estadistico de subgrupo (Xbar o R/S/MR).
        ucl/cl/lcl: limites de control.
        sigma_est: estimacion de sigma del proceso para zonas A/B/C.
        reglas:    lista de enteros [1..8] indicando que reglas activar.

    Returns:
        Lista ordenada sin duplicados de indices infractores.
    """
    n   = len(serie)
    # Calcular sigma desde los limites (mas robusto que sigma_est para las zonas)
    sig = (ucl - cl) / 3.0 if (ucl - cl) != 0 else sigma_est
    infractores = set()

    # Regla 1: punto fuera de +/-3 sigma
    if 1 in reglas:
        for i, v in enumerate(serie):
            if v > ucl or v < lcl:
                infractores.add(i)

    # Regla 2: 9 consecutivos mismo lado de CL
    if 2 in reglas:
        for lado in [1, -1]:
            count = 0
            run   = []
            for i, v in enumerate(serie):
                if (lado == 1 and v > cl) or (lado == -1 and v < cl):
                    count += 1
                    run.append(i)
                else:
                    count = 0
                    run   = []
                if count >= 9:
                    infractores.update(run)

    # Regla 3: 6 puntos en tendencia monotonica
    if 3 in reglas:
        for i in range(n - 5):
            sub = serie[i:i + 6]
            if all(sub[j] < sub[j + 1] for j in range(5)) or \
               all(sub[j] > sub[j + 1] for j in range(5)):
                infractores.update(range(i, i + 6))

    # Regla 4: 14 alternando arriba/abajo
    if 4 in reglas:
        for i in range(n - 13):
            sub = serie[i:i + 14]
            alt = all((sub[j] > cl) != (sub[j + 1] > cl) for j in range(13))
            if alt:
                infractores.update(range(i, i + 14))

    # Regla 5: 2 de 3 en zona A mismo lado (>2 sigma)
    if 5 in reglas:
        zona_a_pos = serie > (cl + 2 * sig)
        zona_a_neg = serie < (cl - 2 * sig)
        for i in range(n - 2):
            if sum(zona_a_pos[i:i + 3]) >= 2 or sum(zona_a_neg[i:i + 3]) >= 2:
                infractores.update(range(i, i + 3))

    # Regla 6: 4 de 5 en zona B o mas alla mismo lado (>1 sigma)
    if 6 in reglas:
        zona_b_pos = serie > (cl + sig)
        zona_b_neg = serie < (cl - sig)
        for i in range(n - 4):
            if sum(zona_b_pos[i:i + 5]) >= 4 or sum(zona_b_neg[i:i + 5]) >= 4:
                infractores.update(range(i, i + 5))

    # Regla 7: 15 consecutivos en zona C (dentro de +/-1 sigma)
    if 7 in reglas:
        zona_c = (serie > (cl - sig)) & (serie < (cl + sig))
        count  = 0
        run    = []
        for i, v in enumerate(zona_c):
            if v:
                count += 1
                run.append(i)
            else:
                count = 0
                run   = []
            if count >= 15:
                infractores.update(run)

    # Regla 8: 8 consecutivos fuera de zona C
    if 8 in reglas:
        fuera_c = (serie > (cl + sig)) | (serie < (cl - sig))
        count   = 0
        run     = []
        for i, v in enumerate(fuera_c):
            if v:
                count += 1
                run.append(i)
            else:
                count = 0
                run   = []
            if count >= 8:
                infractores.update(run)

    return sorted(infractores)


def _fig_carta_control(
    serie: np.ndarray,
    ucl: float, cl: float, lcl: float,
    infractores: list,
    titulo: str,
    ylabel: str,
    sigma_est: float,
    lsl=None,
    usl=None,
    etiquetas_sg=None,
    ajustado=False,
) -> plt.Figure:
    """Genera una carta de control con zonas A/B/C, senales y leyenda.

    Args:
        serie:         estadistico por subgrupo.
        ucl/cl/lcl:    limites de control.
        infractores:   indices de subgrupos en senal (base-0).
        titulo:        titulo del grafico.
        ylabel:        etiqueta eje Y.
        sigma_est:     sigma estimado (para zonas A/B/C).
        lsl/usl:       limites de especificacion opcionales.
        etiquetas_sg:  lista de IDs reales de subgrupo para etiquetar el eje X.
                       Si es None se usan 1, 2, 3...
        ajustado:      si True, añade sello visual de grafico ajustado.

    Returns:
        Figura matplotlib.
    """
    fig, ax = plt.subplots(figsize=(11, 3.8))
    k       = len(serie)
    x       = np.arange(1, k + 1)
    sig     = (ucl - cl) / 3.0 if (ucl - cl) != 0 else sigma_est

    # Zonas A / B / C (bandas de fondo)
    zona_kw = dict(alpha=0.06, linewidth=0)
    ax.fill_between(x, cl + 2 * sig, ucl,          color="#ef4444", **zona_kw)
    ax.fill_between(x, lcl,          cl - 2 * sig, color="#ef4444", **zona_kw)
    ax.fill_between(x, cl + sig,     cl + 2 * sig, color="#f59e0b", **zona_kw)
    ax.fill_between(x, cl - 2 * sig, cl - sig,     color="#f59e0b", **zona_kw)
    ax.fill_between(x, cl - sig,     cl + sig,     color="#22c55e", **zona_kw)

    # Limites de especificacion opcionales
    if lsl is not None:
        ax.axhline(lsl, color="#94a3b8", linewidth=1.0, linestyle=":",
                   alpha=0.65, label=f"LSL={lsl}")
    if usl is not None:
        ax.axhline(usl, color="#94a3b8", linewidth=1.0, linestyle=":",
                   alpha=0.65, label=f"USL={usl}")

    # Lineas de control
    ax.axhline(ucl, color="#ef4444", linewidth=1.5, linestyle="--",
               label=f"UCL = {ucl:.4f}")
    ax.axhline(cl,  color="#22c55e", linewidth=1.8, linestyle="-",
               label=f"CL  = {cl:.4f}")
    ax.axhline(lcl, color="#ef4444", linewidth=1.5, linestyle="--",
               label=f"LCL = {lcl:.4f}")

    # Serie principal
    ax.plot(x, serie, color="#3b82f6", linewidth=1.3, zorder=3,
            marker="o", markersize=4, markerfacecolor="#3b82f6")

    # Senales (resaltadas en rojo con borde blanco)
    if infractores:
        xi = np.array([i + 1 for i in infractores])
        yi = serie[list(infractores)]
        ax.scatter(xi, yi, color="#ef4444", s=70, zorder=5,
                   label=f"Senal ({len(infractores)} pto.)",
                   edgecolors="white", linewidths=0.8)
        # Anotar el ID real del subgrupo sobre cada senal
        if etiquetas_sg is not None:
            for idx, yv in zip(infractores, yi):
                sg_id = etiquetas_sg[idx] if idx < len(etiquetas_sg) else idx + 1
                ax.annotate(
                    f"SG{sg_id}",
                    xy=(idx + 1, yv),
                    xytext=(0, 9),
                    textcoords="offset points",
                    ha="center",
                    fontsize=6.5,
                    color="#ef4444",
                )

    # Etiquetas de limites al borde derecho
    for val, lbl, color in [
        (ucl, "UCL", "#ef4444"),
        (cl,  "CL",  "#22c55e"),
        (lcl, "LCL", "#ef4444"),
    ]:
        ax.text(k + 0.3, val, f" {lbl}", va="center", fontsize=7.5, color=color)

    # Eje X con IDs de subgrupo reales (si hay pocos mostramos todos; si no, cada 5)
    if etiquetas_sg is not None and len(etiquetas_sg) == k:
        paso = 1 if k <= 30 else 5
        ticks_pos = x[::paso]
        ticks_lbl = [str(etiquetas_sg[i - 1]) for i in ticks_pos]
        ax.set_xticks(ticks_pos)
        ax.set_xticklabels(ticks_lbl, fontsize=7)

    ax.set_title(titulo, fontsize=10.5, fontweight="bold", pad=8)
    ax.set_xlabel("Subgrupo (ID)", fontsize=9)
    ax.set_ylabel(ylabel, fontsize=9)
    ax.set_xlim(0.5, k + 1.5)
    ax.legend(fontsize=7, loc="upper right",
              facecolor="#0f1117", edgecolor="#2a2d3e", ncol=2)
    ax.grid(True, axis="y")

    # Sello visual cuando el grafico usa limites ajustados (causas especiales removidas)
    # El parametro ajustado=True lo pasa seccion_fase1 cuando hay subgrupos excluidos
    if ajustado:
        ax.text(
            0.01, 0.97, "LIMITES AJUSTADOS",
            transform=ax.transAxes,
            fontsize=7.5, color="#22c55e", alpha=0.80,
            va="top", ha="left",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#0d1f17",
                      edgecolor="#22c55e", alpha=0.90),
        )

    fig.tight_layout()
    return fig


def _tabla_limites(lim: dict, carta: str) -> pd.DataFrame:
    """Construye DataFrame con tabla de limites para mostrar en UI.

    Args:
        lim:   resultado de _calcular_limites_*.
        carta: etiqueta de carta ('X-R', 'X-S', 'I-MR').

    Returns:
        DataFrame con columnas Carta, Estadistico, UCL, CL, LCL.
    """
    tipo_disp = lim["tipo"]

    # Formateo seguro: construir strings con is not None
    def fmt4(v):
        return f"{v:.4f}" if v is not None else "---"

    rows = [
        {
            "Carta":         carta,
            "Estadistico":   "X-barra (media)",
            "UCL":           fmt4(lim["xbar"]["ucl"]),
            "CL":            fmt4(lim["xbar"]["cl"]),
            "LCL":           fmt4(lim["xbar"]["lcl"]),
        },
        {
            "Carta":         carta,
            "Estadistico":   f"{tipo_disp} (dispersion)",
            "UCL":           fmt4(lim["disp"]["ucl"]),
            "CL":            fmt4(lim["disp"]["cl"]),
            "LCL":           fmt4(lim["disp"]["lcl"]),
        },
    ]
    return pd.DataFrame(rows)


def _tabla_senales(
    infractores_x: list,
    infractores_d: list,
    xbar: np.ndarray,
    disp: np.ndarray,
    tipo_disp: str,
    subgrupo_ids: list = None,
) -> pd.DataFrame:
    """Construye tabla de senales detectadas para mostrar en la UI.

    Args:
        infractores_x: indices (base-0) de xbar en senal.
        infractores_d: indices (base-0) de dispersion en senal.
        xbar:          array de medias por subgrupo.
        disp:          array de dispersion por subgrupo.
        tipo_disp:     etiqueta del estadistico de dispersion ('R','S','MR').
        subgrupo_ids:  lista de IDs reales de subgrupo; si None usa i+1.

    Returns:
        DataFrame con: Subgrupo, Carta, Valor, Tipo senal.
    """
    def _sg_id(i):
        # Obtener ID real del subgrupo de forma segura
        if subgrupo_ids is not None and i < len(subgrupo_ids):
            return subgrupo_ids[i]
        return i + 1

    rows = []
    todos = set(infractores_x) | set(infractores_d)
    for i in sorted(todos):
        if i in infractores_x:
            val_x = f"{float(xbar[i]):.4f}" if i < len(xbar) else "---"
            rows.append({
                "Subgrupo":   _sg_id(i),
                "Carta":      "X-barra",
                "Valor":      val_x,
                "Tipo senal": "Fuera de limites / regla WE",
            })
        if i in infractores_d and i < len(disp):
            val_d = f"{float(disp[i]):.4f}"
            rows.append({
                "Subgrupo":   _sg_id(i),
                "Carta":      tipo_disp,
                "Valor":      val_d,
                "Tipo senal": "Fuera de limites / regla WE",
            })
    if not rows:
        return pd.DataFrame(columns=["Subgrupo", "Carta", "Valor", "Tipo senal"])
    return pd.DataFrame(rows)


def _panel_veredicto(n_senales: int, n_subgrupos: int, sigma_est: float,
                     tipo_carta: str):
    """Renderiza el bloque visual de veredicto de estabilidad del proceso.

    Args:
        n_senales:   total de subgrupos en senal (sin duplicados).
        n_subgrupos: total de subgrupos analizados.
        sigma_est:   sigma estimado del proceso.
        tipo_carta:  etiqueta de la carta usada.
    """
    pct = (n_senales / n_subgrupos * 100) if n_subgrupos > 0 else 0.0

    if n_senales == 0:
        color  = "#22c55e"
        icono  = "OK"
        estado = "PROCESO BAJO CONTROL ESTADÍSTICO"
        msg    = (
            "No se detectaron señales de causas especiales. "
            "El proceso opera de forma estable y predecible. "
            "Puede proceder a calcular los índices de capacidad con los límites actuales."
        )
        recom = [
            "Proceda a la sección Capacidad del proceso para calcular Cp y Cpk.",
            "Documente los límites de control como referencia para Fase 2.",
            "Establezca la frecuencia de muestreo para el monitoreo continuo.",
        ]
    elif pct <= 10:
        color  = "#f59e0b"
        icono  = "ADVERTENCIA"
        estado = "PROCESO MARGINALMENTE ESTABLE"
        msg    = (
            f"Se detectaron {n_senales} subgrupo(s) con señales ({pct:.1f} % del total). "
            "El proceso muestra indicios de inestabilidad menor. "
            "Investigue las causas antes de calcular la capacidad."
        )
        recom = [
            "Identifique y elimine las causas especiales de los subgrupos señalados.",
            "Recalcule los límites excluyendo los subgrupos con causa asignada.",
            "Repita el análisis hasta alcanzar estabilidad completa.",
        ]
    else:
        color  = "#ef4444"
        icono  = "ALERTA"
        estado = "PROCESO FUERA DE CONTROL ESTADÍSTICO"
        msg    = (
            f"Se detectaron {n_senales} subgrupo(s) con señales ({pct:.1f} % del total). "
            "El proceso presenta variación por causas especiales. "
            "Los límites actuales NO son válidos para monitoreo ni capacidad."
        )
        recom = [
            "Realice análisis de causas raíz en todos los subgrupos señalados.",
            "Corrija las causas especiales identificadas antes de continuar.",
            "Recolecter nuevos datos luego de la mejora y repita la Fase 1.",
        ]

    # Construir strings seguros (sin f-strings condicionales en una sola línea)
    pct_str   = f"{pct:.1f}%"
    sigma_str = f"{sigma_est:.4f}"

    st.markdown(
        f"""
        <div style="background:#0f1117;border:2px solid {color};border-radius:12px;
                    padding:22px 26px;margin:12px 0">
            <div style="font-size:1.2rem;font-weight:700;color:{color};margin-bottom:10px">
                {icono} &nbsp; {estado}
            </div>
            <p style="font-size:.88rem;color:#e2e8f0;margin:0 0 14px">{msg}</p>
            <div style="display:flex;gap:28px;flex-wrap:wrap">
                <div>
                    <div style="font-size:.65rem;color:#64748b;letter-spacing:.1em;
                                text-transform:uppercase">Subgrupos analizados</div>
                    <div style="font-family:monospace;font-size:1.4rem;
                                color:#e2e8f0;font-weight:700">{n_subgrupos}</div>
                </div>
                <div>
                    <div style="font-size:.65rem;color:#64748b;letter-spacing:.1em;
                                text-transform:uppercase">Señales detectadas</div>
                    <div style="font-family:monospace;font-size:1.4rem;
                                color:{color};font-weight:700">{n_senales}</div>
                </div>
                <div>
                    <div style="font-size:.65rem;color:#64748b;letter-spacing:.1em;
                                text-transform:uppercase">% en señal</div>
                    <div style="font-family:monospace;font-size:1.4rem;
                                color:{color};font-weight:700">{pct_str}</div>
                </div>
                <div>
                    <div style="font-size:.65rem;color:#64748b;letter-spacing:.1em;
                                text-transform:uppercase">sigma estimado</div>
                    <div style="font-family:monospace;font-size:1.4rem;
                                color:#3b82f6;font-weight:700">{sigma_str}</div>
                </div>
                <div>
                    <div style="font-size:.65rem;color:#64748b;letter-spacing:.1em;
                                text-transform:uppercase">Tipo de carta</div>
                    <div style="font-size:1rem;color:#e2e8f0;font-weight:600;
                                margin-top:4px">{tipo_carta}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Recomendaciones
    st.markdown("#### Recomendaciones")
    for rec in recom:
        st.markdown(
            f"""
            <div style="display:flex;gap:10px;align-items:flex-start;
                        padding:9px 14px;background:#1a1d27;border-radius:8px;
                        border-left:3px solid {color};margin-bottom:7px">
                <span style="font-size:.88rem;color:#e2e8f0">{rec}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )


def seccion_fase1():
    """Modulo Fase 1 - Estabilizacion del sistema CEP.

    Flujo completo:
    1.  Verificar prerequisitos (datos cargados).
    2.  Selector de variable, tipo de carta y reglas WE.
    3.  Calculo de estadisticos por subgrupo (Xbar, R/S/MR).
    4.  Calculo de limites de control con constantes AIAG.
    5.  Aplicacion de Reglas de Western Electric.
    6.  KPIs de limites calculados.
    7.  Carta X-barra con señales, zonas A/B/C y limites spec.
    8.  Carta R / S / MR con señales.
    9.  Tablas de limites y señales.
    10. MODULO CAUSAS ESPECIALES:
        - Seleccion de subgrupo en señal para analizar.
        - Justificacion obligatoria + confirmacion + accion correctiva.
        - Validacion: solo elimina con justificacion confirmada.
        - Recalculo automatico tras eliminacion.
        - Historial de eliminaciones.
    11. Veredicto automatico de estabilidad (original + recalculado).
    12. Guardar resultados en st.session_state.fase1.
    """
    encabezado(
        "📊", "Fase 1 – Estabilización",
        "Construcción de cartas de control con datos históricos para establecer los límites naturales",
    )

    # ── Prerequisito ─────────────────────────────────────────────────────────
    if not st.session_state.get("datos_cargados") or st.session_state.df_subgrupos is None:
        caja(
            "Cargue o genere datos en la sección 📥 Ingreso de datos para habilitar este módulo.",
            tipo="warning",
        )
        return

    # ── Inicializar estado interno de este modulo si es la primera vez ────────
    if "f1_eliminados" not in st.session_state:
        st.session_state.f1_eliminados = []     # lista de dicts {subgrupo, razon, accion, ts}
    if "f1_excluidos" not in st.session_state:
        st.session_state.f1_excluidos = set()   # set de IDs de subgrupo excluidos

    df_sg  = st.session_state.df_subgrupos
    cfg    = st.session_state.config_proceso
    n_tam  = int(cfg.get("tamano_subgrupo", 5))

    # ══════════════════════════════════════════════════════════════════════════
    # BLOQUE A - Configuracion del analisis
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("### ⚙️ Configuración del análisis")

    col_var, col_tipo, col_reg, col_sigma = st.columns(4)

    with col_var:
        variable = st.selectbox(
            "Variable a analizar",
            ["Resistencia (kg/cm²)", "Absorción (%)"],
            key="f1_variable",
            help="Variable de proceso a controlar.",
        )

    with col_tipo:
        opciones_carta = [
            "X-R  (recomendado n <= 10)",
            "X-S  (recomendado n > 10)",
            "I-MR  (observaciones individuales)",
        ]
        idx_sug = 0 if n_tam <= 10 else 1
        tipo_carta_raw = st.selectbox(
            "Tipo de carta de control",
            opciones_carta,
            index=idx_sug,
            key="f1_tipo_carta",
            help="X-R es mas eficiente para subgrupos pequeños (n <= 10).",
        )

    with col_reg:
        opciones_reglas = [
            "Regla 1 solo: puntos fuera de limites",
            "4 Reglas basicas (1, 2, 3, 5)",
            "8 Reglas Western Electric (completo)",
        ]
        reglas_sel = st.selectbox(
            "Reglas de detección",
            opciones_reglas,
            index=1,
            key="f1_reglas",
            help="Mas reglas = mayor sensibilidad, pero mas falsas alarmas.",
        )

    with col_sigma:
        k_sigma = st.number_input(
            "Límites (± k·σ)",
            min_value=1.0,
            max_value=6.0,
            value=3.0,
            step=0.5,
            key="f1_k_sigma",
            help=(
                "Número de desviaciones estándar para los límites de control. "
                "El estándar Shewhart es ±3σ. Valores menores (ej. 2σ) aumentan "
                "la sensibilidad pero generan más falsas alarmas; valores mayores "
                "reducen falsas alarmas pero pueden ocultar causas especiales."
            ),
        )

    # Mapear seleccion a lista de reglas
    if "solo" in reglas_sel.lower():
        reglas_activas = [1]
    elif "4 Reglas" in reglas_sel:
        reglas_activas = [1, 2, 3, 5]
    else:
        reglas_activas = [1, 2, 3, 4, 5, 6, 7, 8]

    if "X-R" in tipo_carta_raw:
        tipo_carta = "X-R"
    elif "X-S" in tipo_carta_raw:
        tipo_carta = "X-S"
    else:
        tipo_carta = "I-MR"

    col_datos = "resistencia" if "Resisten" in variable else "absorcion"
    lsl_v     = cfg["lsl_res"] if "Resisten" in variable else cfg["lsl_abs"]
    usl_v     = cfg["usl_res"] if "Resisten" in variable else cfg["usl_abs"]

    # Aplicar exclusiones activas al dataframe de trabajo
    excluidos   = st.session_state.f1_excluidos
    df_activo   = df_sg[~df_sg["subgrupo"].isin(excluidos)].copy()
    n_excluidos = len(excluidos)

    n_sgs = df_activo["subgrupo"].nunique()

    info_base = (
        f"Carta: **{tipo_carta}** | Variable: **{variable}** | "
        f"Subgrupos activos: **{n_sgs}**"
    )
    if n_excluidos > 0:
        info_base += f" | Subgrupos excluidos: **{n_excluidos}**"
    info_base += f" | n = **{n_tam}** | Reglas: **{reglas_activas}** | Límites: **±{k_sigma}σ**"
    caja(info_base, tipo="info")

    sep()

    # ══════════════════════════════════════════════════════════════════════════
    # BLOQUE B - Calculo de estadisticos y limites (sobre datos activos)
    # ══════════════════════════════════════════════════════════════════════════
    grupos       = df_activo.groupby("subgrupo")[col_datos].apply(list)
    n_valido     = int(grupos.apply(len).min()) if len(grupos) > 0 else n_tam
    n_real       = min(n_tam, n_valido)
    subgrupo_ids = sorted(df_activo["subgrupo"].unique())

    if len(subgrupo_ids) < 2:
        caja(
            "Quedan menos de 2 subgrupos activos tras las exclusiones. "
            "Restaure subgrupos desde el historial de eliminaciones.",
            tipo="warning",
        )
        return

    if tipo_carta == "I-MR":
        individ  = df_activo.sort_values("subgrupo")[col_datos].to_numpy(dtype=float)
        MR_arr   = np.abs(np.diff(individ))
        lim      = _calcular_limites_imr(individ, k_sigma)
        xbar_arr = individ
        disp_arr = np.append(MR_arr, MR_arr[-1] if len(MR_arr) > 0 else 0.0)
        ylabel_d = "Rango movil (MR)"
    else:
        xbar_arr = np.array([
            float(np.mean(grupos[sg][:n_real])) for sg in subgrupo_ids
        ])
        if tipo_carta == "X-R":
            disp_arr = np.array([
                float(max(grupos[sg][:n_real]) - min(grupos[sg][:n_real]))
                for sg in subgrupo_ids
            ])
            lim      = _calcular_limites_xbar_r(xbar_arr, disp_arr, n_real, k_sigma)
            ylabel_d = "Rango (R)"
        else:
            disp_arr = np.array([
                float(np.std(grupos[sg][:n_real], ddof=1)) for sg in subgrupo_ids
            ])
            lim      = _calcular_limites_xbar_s(xbar_arr, disp_arr, n_real, k_sigma)
            ylabel_d = "Desv. estándar (S)"

    sigma_est = lim["sigma_est"]
    tipo_disp = lim["tipo"]
    disp_plot = disp_arr[:-1] if tipo_carta == "I-MR" else disp_arr

    # Detectar señales con reglas WE
    inf_x = _aplicar_reglas_we(
        xbar_arr,
        lim["xbar"]["ucl"], lim["xbar"]["cl"], lim["xbar"]["lcl"],
        sigma_est, reglas_activas,
    )
    inf_d = _aplicar_reglas_we(
        disp_plot,
        lim["disp"]["ucl"], lim["disp"]["cl"], lim["disp"]["lcl"],
        sigma_est, reglas_activas,
    )

    n_senales_total = len(set(inf_x) | set(inf_d))
    n_subgrupos     = len(xbar_arr)

    # ══════════════════════════════════════════════════════════════════════════
    # ══════════════════════════════════════════════════════════════════════════
    # BLOQUE C - KPIs de limites (actuales)
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("### 📐 Límites de control calculados")

    # ── Construir strings seguros (nunca f-string condicional en una sola linea) ──
    ucl_x_str = f"{lim['xbar']['ucl']:.4f}"
    cl_x_str  = f"{lim['xbar']['cl']:.4f}"
    lcl_x_str = f"{lim['xbar']['lcl']:.4f}"
    ucl_d_str = f"{lim['disp']['ucl']:.4f}"
    cl_d_str  = f"{lim['disp']['cl']:.4f}"
    sig_str   = f"{sigma_est:.4f}"

    # Bandera visual cuando los limites ya son ajustados
    if n_excluidos > 0:
        st.markdown(
            "<div style='display:inline-block;background:rgba(34,197,94,.15);"
            "border:1px solid #22c55e;border-radius:20px;padding:3px 14px;"
            "font-size:.78rem;color:#22c55e;margin-bottom:10px'>"
            "✅ Límites ajustados tras eliminar causas especiales</div>",
            unsafe_allow_html=True,
        )

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1: tarjeta("Gran media (X=)",   cl_x_str,  "Media de subgrupos")
    with c2: tarjeta("UCL  X-barra",      ucl_x_str, "Limite superior")
    with c3: tarjeta("LCL  X-barra",      lcl_x_str, "Limite inferior")
    with c4: tarjeta(f"CL  {tipo_disp}",  cl_d_str,  "Linea central dispersion")
    with c5: tarjeta(f"UCL  {tipo_disp}", ucl_d_str, "Limite superior dispersion")
    with c6: tarjeta("sigma estimado",    sig_str,   "Desv. estandar del proceso")

    sep()

    # ══════════════════════════════════════════════════════════════════════════
    # BLOQUE C2 – Rango/Desviación por subgrupo y σ̂ del proceso
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("### 📊 Estadísticos por subgrupo y desviación estándar del proceso")
    caja(
        "Para cada subgrupo se calcula su rango (R) o desviación estándar (S). "
        "El promedio de todos esos estadísticos (R̄ o S̄) permite estimar la "
        "desviación estándar **propia del proceso** (σ̂) mediante las constantes "
        "AIAG: σ̂ = R̄/d₂ (cartas X-R e I-MR) o σ̂ = S̄/c₄ (carta X-S).",
        tipo="info",
    )

    # ── Construir tabla de estadísticos por subgrupo ──────────────────────────
    if tipo_carta == "I-MR":
        # Para I-MR: cada observación es un punto individual;
        # el rango móvil = |X_i − X_{i-1}| entre observaciones consecutivas.
        MR_vals = np.abs(np.diff(xbar_arr))
        filas_sg = []
        for i, sg_id in enumerate(subgrupo_ids):
            mr_i = float(MR_vals[i - 1]) if i > 0 else float("nan")
            filas_sg.append({
                "Subgrupo":         sg_id,
                "Valor (X)":        round(float(xbar_arr[i]), 4),
                "Rango Móvil (MR)": round(mr_i, 4) if not np.isnan(mr_i) else "—",
            })
        df_sg_stats = pd.DataFrame(filas_sg)

        # ── Fila PROMEDIOS ────────────────────────────────────────────────────
        x_bar_val  = float(xbar_arr.mean())            # X̄ general
        MR_bar_val = float(np.nanmean(MR_vals))        # MR̄
        fila_prom  = pd.DataFrame([{
            "Subgrupo":         "PROMEDIOS",
            "Valor (X)":        round(x_bar_val,  4),
            "Rango Móvil (MR)": round(MR_bar_val, 4),
        }])
        df_sg_stats = pd.concat([df_sg_stats, fila_prom], ignore_index=True)

        d2_imr     = 1.128                             # d2 para n=2
        sigma_proc = MR_bar_val / d2_imr

        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            tarjeta("X̄ general", f"{x_bar_val:.4f}",
                    "Promedio de todas las observaciones individuales")
        with col_m2:
            tarjeta("MR̄  (Rango Móvil Promedio)", f"{MR_bar_val:.4f}",
                    "Promedio de todos los rangos móviles")
        with col_m3:
            tarjeta("d₂  (n = 2)", f"{d2_imr:.3f}",
                    "Constante AIAG para I-MR")
        with col_m4:
            tarjeta("σ̂ = MR̄ / d₂", f"{sigma_proc:.4f}",
                    f"Desv. estándar del proceso — {variable}")

        st.markdown(
            f"<div style='background:var(--primary-bg,#eff6ff);border:1px solid #93c5fd;"
            f"border-radius:10px;padding:12px 18px;margin:10px 0;font-size:.88rem'>"
            f"<b>Fórmula aplicada (I-MR):</b> &nbsp; σ̂ = MR̄ / d₂ = "
            f"{MR_bar_val:.4f} / {d2_imr:.3f} = <b style='color:#1d4ed8'>{sigma_proc:.4f}</b>"
            f"&nbsp;&nbsp;·&nbsp;&nbsp;Variable: <b>{variable}</b></div>",
            unsafe_allow_html=True,
        )

    elif tipo_carta == "X-R":
        # ── Calcular X̄, máx, mín y R para cada subgrupo ─────────────────────
        filas_sg = []
        for i, sg_id in enumerate(subgrupo_ids):
            vals_sg = [float(v) for v in grupos[sg_id][:n_real]]
            xbar_i  = float(np.mean(vals_sg))
            max_i   = float(np.max(vals_sg))
            min_i   = float(np.min(vals_sg))
            rango_i = max_i - min_i          # R = máx − mín  (definición exacta)
            filas_sg.append({
                "Subgrupo":    sg_id,
                "X̄ subgrupo": round(xbar_i,  4),
                "Máx":         round(max_i,   4),
                "Mín":         round(min_i,   4),
                "Rango (R)":   round(rango_i, 4),
            })
        df_sg_stats = pd.DataFrame(filas_sg)

        # ── Fila PROMEDIOS ────────────────────────────────────────────────────
        xbar_bar_val = float(xbar_arr.mean())          # X̄ general (promedio de promedios)
        R_bar_val    = float(disp_arr.mean())           # R̄ = suma(R_i) / k
        fila_prom = pd.DataFrame([{
            "Subgrupo":    "PROMEDIOS",
            "X̄ subgrupo": round(xbar_bar_val, 4),
            "Máx":         "—",
            "Mín":         "—",
            "Rango (R)":   round(R_bar_val, 4),
        }])
        df_sg_stats = pd.concat([df_sg_stats, fila_prom], ignore_index=True)

        d2_n       = _d2[n_real] if n_real <= 10 else _d2[10]
        sigma_proc = R_bar_val / d2_n

        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            tarjeta("X̄ general (X̿)", f"{xbar_bar_val:.4f}",
                    "Promedio de los X̄ de todos los subgrupos")
        with col_m2:
            tarjeta("R̄  (Rango Promedio)", f"{R_bar_val:.4f}",
                    "Promedio de los rangos de todos los subgrupos")
        with col_m3:
            tarjeta(f"d₂  (n = {n_real})", f"{d2_n:.3f}",
                    "Constante AIAG para el tamaño de subgrupo")
        with col_m4:
            tarjeta("σ̂ = R̄ / d₂", f"{sigma_proc:.4f}",
                    f"Desv. estándar del proceso — {variable}")

        st.markdown(
            f"<div style='background:var(--primary-bg,#eff6ff);border:1px solid #93c5fd;"
            f"border-radius:10px;padding:12px 18px;margin:10px 0;font-size:.88rem'>"
            f"<b>Fórmula aplicada (X̄–R):</b> &nbsp; σ̂ = R̄ / d₂ = "
            f"{R_bar_val:.4f} / {d2_n:.3f} = <b style='color:#1d4ed8'>{sigma_proc:.4f}</b>"
            f"&nbsp;&nbsp;·&nbsp;&nbsp;Variable: <b>{variable}</b> &nbsp;|&nbsp; "
            f"R_i = máx(subgrupo) − mín(subgrupo)</div>",
            unsafe_allow_html=True,
        )

    else:  # X-S
        # ── Calcular X̄ y S para cada subgrupo ────────────────────────────────
        import math as _math
        c4_n = _math.sqrt(2 / (n_real - 1)) * (
            _math.gamma(n_real / 2) / _math.gamma((n_real - 1) / 2)
        )

        filas_sg = []
        for i, sg_id in enumerate(subgrupo_ids):
            vals_sg = [float(v) for v in grupos[sg_id][:n_real]]
            xbar_i  = float(np.mean(vals_sg))
            s_i     = float(np.std(vals_sg, ddof=1))   # S con n-1
            filas_sg.append({
                "Subgrupo":        sg_id,
                "X̄ subgrupo":     round(xbar_i, 4),
                "Desv. Est. (S)": round(s_i,    4),
            })
        df_sg_stats = pd.DataFrame(filas_sg)

        # ── Fila PROMEDIOS ────────────────────────────────────────────────────
        xbar_bar_val = float(xbar_arr.mean())
        S_bar_val    = float(disp_arr.mean())           # S̄ = suma(S_i) / k
        fila_prom = pd.DataFrame([{
            "Subgrupo":        "PROMEDIOS",
            "X̄ subgrupo":     round(xbar_bar_val, 4),
            "Desv. Est. (S)": round(S_bar_val,    4),
        }])
        df_sg_stats = pd.concat([df_sg_stats, fila_prom], ignore_index=True)

        sigma_proc = S_bar_val / c4_n

        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            tarjeta("X̄ general (X̿)", f"{xbar_bar_val:.4f}",
                    "Promedio de los X̄ de todos los subgrupos")
        with col_m2:
            tarjeta("S̄  (Desv. Promedio)", f"{S_bar_val:.4f}",
                    "Promedio de las desviaciones de todos los subgrupos")
        with col_m3:
            tarjeta(f"c₄  (n = {n_real})", f"{c4_n:.4f}",
                    "Constante AIAG para el tamaño de subgrupo")
        with col_m4:
            tarjeta("σ̂ = S̄ / c₄", f"{sigma_proc:.4f}",
                    f"Desv. estándar del proceso — {variable}")

        st.markdown(
            f"<div style='background:var(--primary-bg,#eff6ff);border:1px solid #93c5fd;"
            f"border-radius:10px;padding:12px 18px;margin:10px 0;font-size:.88rem'>"
            f"<b>Fórmula aplicada (X̄–S):</b> &nbsp; σ̂ = S̄ / c₄ = "
            f"{S_bar_val:.4f} / {c4_n:.4f} = <b style='color:#1d4ed8'>{sigma_proc:.4f}</b>"
            f"&nbsp;&nbsp;·&nbsp;&nbsp;Variable: <b>{variable}</b></div>",
            unsafe_allow_html=True,
        )

    # ── Tabla detallada por subgrupo (expandible) ─────────────────────────────
    with st.expander("📋 Ver tabla detallada por subgrupo", expanded=False):
        st.dataframe(df_sg_stats, use_container_width=True, hide_index=True)

    sep()

    # ══════════════════════════════════════════════════════════════════════════
    # BLOQUE D - Carta de medias (X-barra o I)
    # ══════════════════════════════════════════════════════════════════════════
    # Titulo indica si el grafico usa limites originales o ajustados
    sufijo_ajuste = " [AJUSTADO]" if n_excluidos > 0 else ""
    titulo_x = (
        f"Carta I (individuales) — {variable}{sufijo_ajuste}"
        if tipo_carta == "I-MR"
        else f"Carta X-barra — {variable} [{tipo_carta}]{sufijo_ajuste}"
    )
    st.markdown(f"### 📉 {titulo_x}")
    caja(
        "Puntos rojos = subgrupos con señal según las reglas activas. "
        "Bandas: zona C verde (±1σ), zona B naranja (±2σ), zona A roja (±3σ)."
        + (" Los límites muestran el proceso **después de eliminar causas especiales**." if n_excluidos > 0 else ""),
        tipo="info",
    )

    fig_x = _fig_carta_control(
        xbar_arr,
        lim["xbar"]["ucl"], lim["xbar"]["cl"], lim["xbar"]["lcl"],
        inf_x, titulo_x, ylabel=variable,
        sigma_est=sigma_est, lsl=lsl_v, usl=usl_v,
        etiquetas_sg=subgrupo_ids,
        ajustado=(n_excluidos > 0),
    )
    st.pyplot(fig_x, use_container_width=True)
    plt.close(fig_x)

    sep()

    # ══════════════════════════════════════════════════════════════════════════
    # BLOQUE E - Carta de dispersion (R / S / MR)
    # ══════════════════════════════════════════════════════════════════════════
    titulo_d = f"Carta {tipo_disp} — {variable} [{tipo_carta}]{sufijo_ajuste}"
    st.markdown(f"### 📉 {titulo_d}")

    fig_d = _fig_carta_control(
        disp_plot,
        lim["disp"]["ucl"], lim["disp"]["cl"], lim["disp"]["lcl"],
        inf_d, titulo_d, ylabel=ylabel_d,
        sigma_est=sigma_est,
        etiquetas_sg=subgrupo_ids,
        ajustado=(n_excluidos > 0),
    )
    st.pyplot(fig_d, use_container_width=True)
    plt.close(fig_d)

    sep()

    # ══════════════════════════════════════════════════════════════════════════
    # BLOQUE F - Tablas de limites y señales
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("### 📋 Tablas de resultados")
    col_tab1, col_tab2 = st.columns([1, 2])

    with col_tab1:
        st.markdown("**Límites de control**")
        df_lim = _tabla_limites(lim, tipo_carta)
        st.dataframe(df_lim, use_container_width=True, hide_index=True)

    with col_tab2:
        n_sen_str = str(len(set(inf_x) | set(inf_d)))
        st.markdown(f"**Subgrupos con señal** ({n_sen_str} total)")
        df_sen = _tabla_senales(inf_x, inf_d, xbar_arr, disp_plot, tipo_disp,
                                subgrupo_ids)
        if df_sen.empty:
            caja("No se detectaron señales. El proceso parece estable.", tipo="success")
        else:
            st.dataframe(df_sen, use_container_width=True, hide_index=True)

    sep()

    # ══════════════════════════════════════════════════════════════════════════
    # BLOQUE F2 - GRAFICO DE CONTROL AJUSTADO (solo cuando hay exclusiones)
    # Muestra en tabs: carta original vs carta ajustada con mensajes de
    # interpretacion claros y datos filtrados + limites recalculados.
    # ══════════════════════════════════════════════════════════════════════════
    if n_excluidos > 0:
        st.markdown("### 📊 Gráfico de control ajustado")

        # Mensaje de contexto obligatorio
        st.markdown(
            """
            <div style="background:#0d1f17;border:1.5px solid #22c55e;
                        border-radius:10px;padding:14px 20px;margin:8px 0 16px">
                <div style="font-size:.94rem;font-weight:700;color:#22c55e;margin-bottom:5px">
                    ✅ Gráfico de control ajustado — proceso sin causas especiales
                </div>
                <ul style="font-size:.83rem;color:#e2e8f0;margin:0;padding-left:18px">
                    <li>Se eliminaron las causas especiales justificadas y documentadas.</li>
                    <li>Los límites de control fueron recalculados con los datos filtrados.</li>
                    <li>Este gráfico representa el proceso ajustado y estable.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Recuperar datos originales para la pestaña "Antes"
        lim_orig_snap = st.session_state.get("f1_limites_originales")

        # Pestanas: Original | Ajustado | Comparacion de limites
        if lim_orig_snap is not None:
            tab_orig, tab_adj, tab_cmp = st.tabs([
                "📉 Original (con causas especiales)",
                "✅ Ajustado (sin causas especiales)",
                "📋 Comparación de límites",
            ])
        else:
            tab_adj, tab_cmp = st.tabs([
                "✅ Ajustado (sin causas especiales)",
                "📋 Comparación de límites",
            ])
            tab_orig = None

        # ── Pestaña ORIGINAL ──────────────────────────────────────────────────
        if tab_orig is not None and lim_orig_snap is not None:
            with tab_orig:
                caja(
                    "Gráfico con **todos los subgrupos** incluidos (antes de eliminar "
                    "causas especiales). Los puntos rojos eran las señales detectadas.",
                    tipo="warning",
                )
                # Reconstruir arrays originales desde session_state
                xbar_orig_arr = np.array(lim_orig_snap["xbar_arr"])
                disp_orig_arr = np.array(lim_orig_snap["disp_arr"])
                sg_ids_orig   = lim_orig_snap["sg_ids"]
                inf_x_orig    = lim_orig_snap["inf_x"]
                inf_d_orig    = lim_orig_snap["inf_d"]

                titulo_orig_x = (
                    f"Carta X-barra ORIGINAL — {lim_orig_snap['variable']} "
                    f"[{lim_orig_snap['tipo']}] (con causas especiales)"
                )
                fig_orig_x = _fig_carta_control(
                    xbar_orig_arr,
                    lim_orig_snap["ucl_x"],
                    lim_orig_snap["cl_x"],
                    lim_orig_snap["lcl_x"],
                    inf_x_orig,
                    titulo_orig_x,
                    ylabel=lim_orig_snap["variable"],
                    sigma_est=lim_orig_snap["sigma"],
                    lsl=lim_orig_snap["lsl_v"],
                    usl=lim_orig_snap["usl_v"],
                    etiquetas_sg=sg_ids_orig,
                    ajustado=False,
                )
                st.pyplot(fig_orig_x, use_container_width=True)
                plt.close(fig_orig_x)

                titulo_orig_d = (
                    f"Carta {lim_orig_snap['tipo']} ORIGINAL — "
                    f"{lim_orig_snap['variable']} (con causas especiales)"
                )
                fig_orig_d = _fig_carta_control(
                    disp_orig_arr,
                    lim_orig_snap["ucl_d"],
                    lim_orig_snap["cl_d"],
                    lim_orig_snap["lcl_d"],
                    inf_d_orig,
                    titulo_orig_d,
                    ylabel=lim_orig_snap["ylabel_d"],
                    sigma_est=lim_orig_snap["sigma"],
                    etiquetas_sg=sg_ids_orig,
                    ajustado=False,
                )
                st.pyplot(fig_orig_d, use_container_width=True)
                plt.close(fig_orig_d)

        # ── Pestaña AJUSTADA ──────────────────────────────────────────────────
        with tab_adj:
            caja(
                f"Gráfico con **{n_sgs} subgrupos activos** "
                f"({n_excluidos} excluidos por causa especial documentada). "
                "Los límites de control son los **recalculados** con los datos filtrados.",
                tipo="success",
            )

            titulo_adj_x = (
                f"Carta X-barra AJUSTADA — {variable} [{tipo_carta}]  "
                f"[{n_excluidos} causa(s) especial(es) eliminada(s)]"
            )
            fig_adj_x = _fig_carta_control(
                xbar_arr,
                lim["xbar"]["ucl"], lim["xbar"]["cl"], lim["xbar"]["lcl"],
                inf_x,
                titulo_adj_x,
                ylabel=variable,
                sigma_est=sigma_est,
                lsl=lsl_v,
                usl=usl_v,
                etiquetas_sg=subgrupo_ids,
                ajustado=True,
            )
            st.pyplot(fig_adj_x, use_container_width=True)
            plt.close(fig_adj_x)

            titulo_adj_d = (
                f"Carta {tipo_disp} AJUSTADA — {variable} [{tipo_carta}]  "
                f"[Límites recalculados]"
            )
            fig_adj_d = _fig_carta_control(
                disp_plot,
                lim["disp"]["ucl"], lim["disp"]["cl"], lim["disp"]["lcl"],
                inf_d,
                titulo_adj_d,
                ylabel=ylabel_d,
                sigma_est=sigma_est,
                etiquetas_sg=subgrupo_ids,
                ajustado=True,
            )
            st.pyplot(fig_adj_d, use_container_width=True)
            plt.close(fig_adj_d)

            # Interpretacion del estado post-ajuste
            if n_senales_total == 0:
                st.markdown(
                    """
                    <div style="background:#0d1f17;border:2px solid #22c55e;
                                border-radius:10px;padding:14px 18px;margin:12px 0">
                        <span style="font-size:.92rem;font-weight:700;color:#22c55e">
                            ✅ El proceso está bajo control estadístico con los datos ajustados
                        </span>
                        <p style="font-size:.83rem;color:#e2e8f0;margin:6px 0 0">
                            Ningún subgrupo activo viola las reglas de detección.
                            Este gráfico es válido como referencia para Fase 2 – Monitoreo.
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                n_sen_str_adj = str(n_senales_total)
                caja(
                    f"Aún se detectan **{n_sen_str_adj} señal(es)** con los datos ajustados. "
                    "Analice si corresponden a causas especiales adicionales o a causas comunes.",
                    tipo="warning",
                )

        # ── Pestaña COMPARACION ───────────────────────────────────────────────
        with tab_cmp:
            if lim_orig_snap is not None:
                st.markdown("##### Parámetros antes y después de la eliminación de causas especiales")

                def _ds(v):
                    """Delta string seguro."""
                    if v is None:
                        return "—"
                    sign = "+" if v > 0 else ""
                    return f"{sign}{v:.4f}"

                df_cmp = pd.DataFrame([
                    {
                        "Parámetro":  "UCL  X-barra",
                        "Original":   f"{lim_orig_snap['ucl_x']:.4f}",
                        "Ajustado":   f"{lim['xbar']['ucl']:.4f}",
                        "Delta":      _ds(lim["xbar"]["ucl"] - lim_orig_snap["ucl_x"]),
                    },
                    {
                        "Parámetro":  "CL  X-barra",
                        "Original":   f"{lim_orig_snap['cl_x']:.4f}",
                        "Ajustado":   f"{lim['xbar']['cl']:.4f}",
                        "Delta":      _ds(lim["xbar"]["cl"]  - lim_orig_snap["cl_x"]),
                    },
                    {
                        "Parámetro":  "LCL  X-barra",
                        "Original":   f"{lim_orig_snap['lcl_x']:.4f}",
                        "Ajustado":   f"{lim['xbar']['lcl']:.4f}",
                        "Delta":      _ds(lim["xbar"]["lcl"] - lim_orig_snap["lcl_x"]),
                    },
                    {
                        "Parámetro":  f"UCL  {tipo_disp}",
                        "Original":   f"{lim_orig_snap['ucl_d']:.4f}",
                        "Ajustado":   f"{lim['disp']['ucl']:.4f}",
                        "Delta":      _ds(lim["disp"]["ucl"]  - lim_orig_snap["ucl_d"]),
                    },
                    {
                        "Parámetro":  f"CL  {tipo_disp}",
                        "Original":   f"{lim_orig_snap['cl_d']:.4f}",
                        "Ajustado":   f"{lim['disp']['cl']:.4f}",
                        "Delta":      _ds(lim["disp"]["cl"]   - lim_orig_snap["cl_d"]),
                    },
                    {
                        "Parámetro":  "σ estimado",
                        "Original":   f"{lim_orig_snap['sigma']:.4f}",
                        "Ajustado":   f"{sigma_est:.4f}",
                        "Delta":      _ds(sigma_est - lim_orig_snap["sigma"]),
                    },
                    {
                        "Parámetro":  "N° subgrupos",
                        "Original":   str(lim_orig_snap["n_sgs"]),
                        "Ajustado":   str(n_subgrupos),
                        "Delta":      _ds(n_subgrupos - lim_orig_snap["n_sgs"]),
                    },
                ])
                st.dataframe(df_cmp, use_container_width=True, hide_index=True)

                # Interpretacion automatica del sigma
                delta_sig = sigma_est - lim_orig_snap["sigma"]
                if abs(delta_sig) > 1e-6:
                    if delta_sig < 0:
                        sig_msg = (
                            f"La variabilidad del proceso **se redujo** "
                            f"{abs(delta_sig):.4f} unidades al eliminar las causas especiales, "
                            "confirmando que inflaban artificialmente la dispersión."
                        )
                        caja(sig_msg, tipo="success")
                    else:
                        sig_msg = (
                            f"La variabilidad **aumentó** {abs(delta_sig):.4f} unidades. "
                            "Verifique si los datos excluidos tenían un efecto compensatorio."
                        )
                        caja(sig_msg, tipo="warning")
            else:
                caja(
                    "La referencia original aún no está disponible. "
                    "Se guardará automáticamente al eliminar el primer subgrupo.",
                    tipo="info",
                )

        sep()

    # ══════════════════════════════════════════════════════════════════════════
    # BLOQUE G - MODULO DE GESTION DE CAUSAS ESPECIALES
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("### 🔬 Gestión de causas especiales")

    # Advertencia de calidad (siempre visible)
    st.markdown(
        """
        <div style="background:#1a1000;border:1.5px solid #f59e0b;border-radius:10px;
                    padding:16px 20px;margin:10px 0">
            <div style="font-size:.95rem;font-weight:700;color:#f59e0b;margin-bottom:6px">
                ⚠️ Principio fundamental de integridad estadística
            </div>
            <p style="font-size:.85rem;color:#e2e8f0;margin:0 0 6px">
                <strong>La eliminación de causas especiales debe basarse en evidencia
                y no en conveniencia estadística.</strong>
            </p>
            <ul style="font-size:.82rem;color:#94a3b8;margin:0;padding-left:18px">
                <li>No elimines puntos sin una justificación técnica documentada.</li>
                <li>Eliminar datos sin análisis puede invalidar el control estadístico.</li>
                <li>Cada eliminación queda registrada en el historial de auditoría.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Subgrupos actualmente en señal (usando IDs reales del dataset activo)
    sg_en_senal_x = [subgrupo_ids[i] for i in inf_x if i < len(subgrupo_ids)]
    sg_en_senal_d = [subgrupo_ids[i] for i in inf_d if i < len(subgrupo_ids)]
    sg_en_senal   = sorted(set(sg_en_senal_x) | set(sg_en_senal_d))

    if not sg_en_senal:
        caja(
            "No hay subgrupos en señal actualmente. "
            "El proceso está bajo control estadístico con los datos activos.",
            tipo="success",
        )
    else:
        st.markdown(
            f"<p style='font-size:.88rem;color:#94a3b8;margin:12px 0 6px'>"
            f"Se detectaron <strong style='color:#ef4444'>{len(sg_en_senal)} "
            f"subgrupo(s)</strong> con señal. "
            f"Seleccione uno para analizar su causa especial.</p>",
            unsafe_allow_html=True,
        )

        col_sel, col_inf = st.columns([1, 2])
        with col_sel:
            sg_elegido = st.selectbox(
                "Subgrupo en señal a analizar",
                options=sg_en_senal,
                format_func=lambda x: f"Subgrupo {x}",
                key="f1_sg_elegido",
            )

        with col_inf:
            idx_sg  = subgrupo_ids.index(sg_elegido) if sg_elegido in subgrupo_ids else None
            if idx_sg is not None:
                val_xbar_sg = f"{xbar_arr[idx_sg]:.4f}" if idx_sg < len(xbar_arr) else "—"
                val_disp_sg = f"{disp_plot[idx_sg]:.4f}" if idx_sg < len(disp_plot) else "—"
                carta_senal = []
                if sg_elegido in sg_en_senal_x:
                    carta_senal.append("X-barra")
                if sg_elegido in sg_en_senal_d:
                    carta_senal.append(tipo_disp)
                cartas_str = " y ".join(carta_senal) if carta_senal else "—"

                st.markdown(
                    f"""
                    <div style="background:#1a1d27;border:1px solid #2a2d3e;
                                border-radius:8px;padding:14px 18px;margin-top:6px">
                        <div style="display:flex;gap:24px;flex-wrap:wrap">
                            <div>
                                <div style="font-size:.65rem;color:#64748b;
                                            text-transform:uppercase;letter-spacing:.1em">X-barra</div>
                                <div style="font-family:monospace;font-size:1.1rem;
                                            color:#ef4444;font-weight:700">{val_xbar_sg}</div>
                            </div>
                            <div>
                                <div style="font-size:.65rem;color:#64748b;
                                            text-transform:uppercase;letter-spacing:.1em">{tipo_disp}</div>
                                <div style="font-family:monospace;font-size:1.1rem;
                                            color:#ef4444;font-weight:700">{val_disp_sg}</div>
                            </div>
                            <div>
                                <div style="font-size:.65rem;color:#64748b;
                                            text-transform:uppercase;letter-spacing:.1em">Carta(s) en señal</div>
                                <div style="font-size:.9rem;color:#f59e0b;font-weight:600">{cartas_str}</div>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.markdown("<div style='margin-top:14px'></div>", unsafe_allow_html=True)

        with st.expander(
            f"📝 Formulario de causa especial — Subgrupo {sg_elegido}",
            expanded=True,
        ):
            st.markdown(
                "<p style='font-size:.83rem;color:#94a3b8;margin-bottom:10px'>"
                "Todos los campos marcados con * son obligatorios para proceder "
                "con la eliminación del subgrupo.</p>",
                unsafe_allow_html=True,
            )

            tipo_causa = st.selectbox(
                "* Tipo de causa especial",
                [
                    "— Seleccione —",
                    "Fallo de equipo / maquinaria",
                    "Error de operario",
                    "Cambio de materia prima",
                    "Error de medición / instrumento descalibrado",
                    "Condición ambiental atípica (temperatura, humedad)",
                    "Interrupción del proceso (corte de energía, parada)",
                    "Dato erróneo registrado (error de transcripción)",
                    "Muestra no representativa del lote",
                    "Otro (especificar en justificación)",
                ],
                key=f"f1_tipo_causa_{sg_elegido}",
            )

            justificacion = st.text_area(
                "* Justificación / evidencia del evento",
                placeholder=(
                    "Describa qué ocurrió durante este subgrupo.\n"
                    "Ejemplo: 'La mezcladora sufrió un fallo mecánico a las 10:30 AM. "
                    "El operario reportó vibración anormal. Se detuvo la producción "
                    "y se realizó mantenimiento correctivo.'"
                ),
                height=100,
                key=f"f1_justificacion_{sg_elegido}",
            )

            accion_correctiva = st.text_area(
                "Acción correctiva tomada o planificada (recomendada)",
                placeholder=(
                    "Ejemplo: 'Se realizó mantenimiento preventivo a la mezcladora. "
                    "Se verificó calibración de instrumentos.'"
                ),
                height=80,
                key=f"f1_accion_{sg_elegido}",
            )

            confirmado = st.checkbox(
                "✅ Confirmo que este subgrupo corresponde a una causa especial "
                "identificada y documentada, y que su eliminación está técnicamente justificada.",
                key=f"f1_confirmar_{sg_elegido}",
            )

            st.markdown("<div style='margin-top:8px'></div>", unsafe_allow_html=True)

            tipo_valido    = tipo_causa != "— Seleccione —"
            justif_valida  = len(justificacion.strip()) >= 20
            puede_eliminar = tipo_valido and justif_valida and confirmado

            if not tipo_valido:
                st.markdown(
                    "<p style='font-size:.8rem;color:#ef4444'>⚠ Seleccione el tipo de causa especial.</p>",
                    unsafe_allow_html=True,
                )
            if not justif_valida:
                chars_r = max(0, 20 - len(justificacion.strip()))
                st.markdown(
                    f"<p style='font-size:.8rem;color:#ef4444'>"
                    f"⚠ La justificación debe tener al menos 20 caracteres ({chars_r} restantes).</p>",
                    unsafe_allow_html=True,
                )
            if tipo_valido and justif_valida and not confirmado:
                st.markdown(
                    "<p style='font-size:.8rem;color:#f59e0b'>"
                    "⚠ Marque la confirmación para habilitar la eliminación.</p>",
                    unsafe_allow_html=True,
                )

            col_btn1, col_btn2, _ = st.columns([1, 1, 2])
            with col_btn1:
                btn_eliminar = st.button(
                    "🗑️ Eliminar y recalcular",
                    disabled=not puede_eliminar,
                    type="primary",
                    key=f"f1_btn_eliminar_{sg_elegido}",
                    help=(
                        "Disponible solo con justificación completa y confirmación."
                        if not puede_eliminar
                        else "Eliminar este subgrupo y recalcular los límites de control."
                    ),
                )
            with col_btn2:
                if not puede_eliminar:
                    st.markdown(
                        "<span style='font-size:.8rem;color:#64748b;padding-top:8px;"
                        "display:block'>❌ Requisitos incompletos</span>",
                        unsafe_allow_html=True,
                    )

            # ── Procesar eliminacion: guarda el estado ORIGINAL antes de excluir ──
            if btn_eliminar and puede_eliminar:
                import datetime

                # Guardar limites Y ARRAYS ORIGINALES (antes de esta exclusion).
                # Solo se capturan una vez: la primera vez que se elimina un subgrupo.
                # Esto permite dibujar el grafico "Antes" en el panel comparativo.
                if "f1_limites_originales" not in st.session_state:
                    st.session_state.f1_limites_originales = {
                        "ucl_x":       lim["xbar"]["ucl"],
                        "cl_x":        lim["xbar"]["cl"],
                        "lcl_x":       lim["xbar"]["lcl"],
                        "ucl_d":       lim["disp"]["ucl"],
                        "cl_d":        lim["disp"]["cl"],
                        "lcl_d":       lim["disp"]["lcl"],
                        "sigma":       sigma_est,
                        "n_sgs":       n_subgrupos,
                        "tipo":        tipo_carta,
                        # Arrays completos para redibujar la carta original
                        "xbar_arr":    xbar_arr.tolist(),
                        "disp_arr":    disp_plot.tolist(),
                        "sg_ids":      list(subgrupo_ids),
                        "inf_x":       list(inf_x),
                        "inf_d":       list(inf_d),
                        "variable":    variable,
                        "ylabel_d":    ylabel_d,
                        "lsl_v":       lsl_v,
                        "usl_v":       usl_v,
                    }

                st.session_state.f1_excluidos.add(sg_elegido)
                st.session_state.f1_eliminados.append({
                    "subgrupo":      sg_elegido,
                    "tipo_causa":    tipo_causa,
                    "justificacion": justificacion.strip(),
                    "accion":        accion_correctiva.strip() if accion_correctiva.strip() else "—",
                    "timestamp":     datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                })
                caja(
                    f"Subgrupo {sg_elegido} excluido. "
                    "Recalculando límites y actualizando gráficos...",
                    tipo="success",
                )
                st.rerun()

    sep()

    # ══════════════════════════════════════════════════════════════════════════
    # BLOQUE H - Panel de comparacion Antes vs Después + recalculo manual
    # ══════════════════════════════════════════════════════════════════════════
    if n_excluidos > 0:
        lim_orig = st.session_state.get("f1_limites_originales")

        # Boton de recalculo manual (util si el usuario cambia variable o tipo de carta)
        col_recalc, col_reset_lim, _ = st.columns([1, 1, 2])
        with col_recalc:
            if st.button(
                "🔄 Recalcular límites ahora",
                key="f1_btn_recalcular",
                help="Fuerza el recálculo con el conjunto activo de subgrupos.",
            ):
                # Limpiar limites originales guardados para que se registren de nuevo
                if "f1_limites_originales" in st.session_state:
                    del st.session_state.f1_limites_originales
                caja("Recalculando con subgrupos activos...", tipo="info")
                st.rerun()

        with col_reset_lim:
            if st.button(
                "↺ Limpiar referencia original",
                key="f1_btn_clear_orig",
                help="Elimina la referencia de los límites originales para refrescarla.",
            ):
                if "f1_limites_originales" in st.session_state:
                    del st.session_state.f1_limites_originales
                st.rerun()

        # ── Mensaje de interpretacion automatica post-recalculo ───────────────
        st.markdown(
            """
            <div style="background:#0d1f17;border:1.5px solid #22c55e;border-radius:10px;
                        padding:15px 20px;margin:12px 0">
                <div style="font-size:.92rem;font-weight:700;color:#22c55e;margin-bottom:6px">
                    ✅ Límites recalculados después de eliminar causas especiales
                </div>
                <p style="font-size:.84rem;color:#e2e8f0;margin:0">
                    Los gráficos y límites mostrados arriba ya corresponden al conjunto
                    de datos <strong>sin las causas especiales documentadas</strong>.
                    El recálculo se ejecutó automáticamente al confirmar cada eliminación.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ── Panel Antes vs Despues ─────────────────────────────────────────────
        if lim_orig is not None:
            st.markdown("#### 📊 Comparación: Antes vs Después del ajuste")

            # Calcular deltas de forma segura
            delta_ucl_x = lim["xbar"]["ucl"] - lim_orig["ucl_x"]
            delta_lcl_x = lim["xbar"]["lcl"] - lim_orig["lcl_x"]
            delta_cl_x  = lim["xbar"]["cl"]  - lim_orig["cl_x"]
            delta_sigma = sigma_est           - lim_orig["sigma"]
            delta_sgs   = n_subgrupos         - lim_orig["n_sgs"]

            # Strings de delta con signo
            def _delta_str(v):
                if v is None:
                    return "—"
                sign = "+" if v > 0 else ""
                return f"{sign}{v:.4f}"

            delta_ucl_str   = _delta_str(delta_ucl_x)
            delta_lcl_str   = _delta_str(delta_lcl_x)
            delta_cl_str    = _delta_str(delta_cl_x)
            delta_sigma_str = _delta_str(delta_sigma)
            delta_sgs_str   = _delta_str(delta_sgs)

            # Tabla de comparacion
            df_comp = pd.DataFrame([
                {
                    "Parámetro":  "UCL  X-barra",
                    "Original":   f"{lim_orig['ucl_x']:.4f}",
                    "Ajustado":   f"{lim['xbar']['ucl']:.4f}",
                    "Delta":      delta_ucl_str,
                },
                {
                    "Parámetro":  "CL  X-barra (X=)",
                    "Original":   f"{lim_orig['cl_x']:.4f}",
                    "Ajustado":   f"{lim['xbar']['cl']:.4f}",
                    "Delta":      delta_cl_str,
                },
                {
                    "Parámetro":  "LCL  X-barra",
                    "Original":   f"{lim_orig['lcl_x']:.4f}",
                    "Ajustado":   f"{lim['xbar']['lcl']:.4f}",
                    "Delta":      delta_lcl_str,
                },
                {
                    "Parámetro":  f"UCL  {tipo_disp}",
                    "Original":   f"{lim_orig['ucl_d']:.4f}",
                    "Ajustado":   f"{lim['disp']['ucl']:.4f}",
                    "Delta":      _delta_str(lim["disp"]["ucl"] - lim_orig["ucl_d"]),
                },
                {
                    "Parámetro":  f"CL  {tipo_disp}",
                    "Original":   f"{lim_orig['cl_d']:.4f}",
                    "Ajustado":   f"{lim['disp']['cl']:.4f}",
                    "Delta":      _delta_str(lim["disp"]["cl"] - lim_orig["cl_d"]),
                },
                {
                    "Parámetro":  "σ estimado",
                    "Original":   f"{lim_orig['sigma']:.4f}",
                    "Ajustado":   f"{sigma_est:.4f}",
                    "Delta":      delta_sigma_str,
                },
                {
                    "Parámetro":  "N° subgrupos",
                    "Original":   str(lim_orig["n_sgs"]),
                    "Ajustado":   str(n_subgrupos),
                    "Delta":      delta_sgs_str,
                },
            ])
            st.dataframe(df_comp, use_container_width=True, hide_index=True)

            # Interpretacion automatica de los cambios
            if abs(delta_sigma) > 0:
                if delta_sigma < 0:
                    interp_sigma = (
                        f"La desviación estándar estimada se **redujo** "
                        f"{abs(delta_sigma):.4f} unidades tras la exclusión, "
                        "lo que indica que las causas especiales estaban inflando la variabilidad."
                    )
                else:
                    interp_sigma = (
                        f"La desviación estándar estimada **aumentó** "
                        f"{abs(delta_sigma):.4f} unidades, lo que podría indicar "
                        "que los datos excluidos estabilizaban artificialmente el proceso."
                    )
                caja(interp_sigma, tipo="info")

        sep()

    # ══════════════════════════════════════════════════════════════════════════
    # BLOQUE H2 - Historial de eliminaciones
    # ══════════════════════════════════════════════════════════════════════════
    if st.session_state.f1_eliminados:
        st.markdown("### 📂 Historial de exclusiones")
        caja(
            "Registro de auditoría de todos los subgrupos excluidos en esta sesión. "
            "Este historial garantiza trazabilidad y transparencia del análisis.",
            tipo="info",
        )

        df_hist = pd.DataFrame(st.session_state.f1_eliminados)
        df_hist = df_hist.rename(columns={
            "subgrupo":      "Subgrupo",
            "tipo_causa":    "Tipo de causa",
            "justificacion": "Justificación",
            "accion":        "Acción correctiva",
            "timestamp":     "Fecha/Hora",
        })
        st.dataframe(df_hist, use_container_width=True, hide_index=True)

        col_rst1, col_rst2, _ = st.columns([1, 1, 2])
        with col_rst1:
            sg_restaurar = st.selectbox(
                "Restaurar subgrupo",
                options=sorted(st.session_state.f1_excluidos),
                format_func=lambda x: f"Subgrupo {x}",
                key="f1_sg_restaurar",
            )
        with col_rst2:
            st.markdown("<div style='margin-top:24px'></div>", unsafe_allow_html=True)
            if st.button("↩️ Restaurar seleccionado", key="f1_btn_restaurar"):
                st.session_state.f1_excluidos.discard(sg_restaurar)
                st.session_state.f1_eliminados = [
                    r for r in st.session_state.f1_eliminados
                    if r["subgrupo"] != sg_restaurar
                ]
                # Si restauramos todos, limpiar referencia original
                if not st.session_state.f1_excluidos:
                    if "f1_limites_originales" in st.session_state:
                        del st.session_state.f1_limites_originales
                caja(f"Subgrupo {sg_restaurar} restaurado al análisis.", tipo="success")
                st.rerun()

        if st.button("🔄 Restaurar todos los subgrupos", key="f1_btn_restaurar_todo"):
            st.session_state.f1_excluidos   = set()
            st.session_state.f1_eliminados  = []
            if "f1_limites_originales" in st.session_state:
                del st.session_state.f1_limites_originales
            caja("Todos los subgrupos han sido restaurados.", tipo="success")
            st.rerun()

        sep()

    # ══════════════════════════════════════════════════════════════════════════
    # BLOQUE I - Veredicto automatico de estabilidad
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("### 🧭 Veredicto de estabilidad del proceso")

    if n_excluidos > 0:
        caja(
            f"Análisis con **{n_excluidos} subgrupo(s) excluido(s)** "
            f"por causa especial documentada. "
            f"Los límites y el veredicto corresponden a los {n_sgs} subgrupos activos.",
            tipo="info",
        )

    _panel_veredicto(n_senales_total, n_subgrupos, sigma_est, tipo_carta)

    # Mensaje adicional cuando el proceso queda bajo control tras la eliminacion
    if n_excluidos > 0 and n_senales_total == 0:
        st.markdown(
            """
            <div style="background:#0d1f17;border:2px solid #22c55e;border-radius:12px;
                        padding:18px 24px;margin:14px 0">
                <div style="font-size:1.05rem;font-weight:700;color:#22c55e;margin-bottom:8px">
                    ✅ El proceso ahora está bajo control estadístico
                </div>
                <p style="font-size:.86rem;color:#e2e8f0;margin:0">
                    Después de eliminar las causas especiales documentadas, ningún subgrupo
                    activo viola las reglas de detección seleccionadas.
                    Los límites recalculados son válidos para usar en
                    <strong>Fase 2 – Monitoreo</strong> y para estimar la
                    <strong>capacidad del proceso</strong>.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ══════════════════════════════════════════════════════════════════════════
    # BLOQUE J - Guardar resultados en session_state
    # ══════════════════════════════════════════════════════════════════════════
    proceso_estable = (n_senales_total == 0)

    st.session_state.fase1 = {
        "calculado":             True,
        "variable":              variable,
        "tipo_carta":            tipo_carta,
        "limites_xbar":          lim["xbar"],
        "limites_disp":          lim["disp"],
        "tipo_disp":             tipo_disp,
        "sigma_est":             sigma_est,
        "xbar_arr":              xbar_arr.tolist(),
        "disp_arr":              disp_plot.tolist(),
        "inf_xbar":              inf_x,
        "inf_disp":              inf_d,
        "n_senales":             n_senales_total,
        "proceso_estable":       proceso_estable,
        "reglas_usadas":         reglas_activas,
        "subgrupos_activos":     list(subgrupo_ids),
        "subgrupos_excluidos":   list(excluidos),
        "historial_exclusiones": list(st.session_state.f1_eliminados),
        "limites_originales":    st.session_state.get("f1_limites_originales"),
    }
# SECCIÓN 5 – Fase 2: Monitoreo
# ─────────────────────────────────────────────────────────────────────────────

# ── Funciones auxiliares de Fase 2 ────────────────────────────────────────────

def _f2_calcular_estadisticos_sg(observaciones: list, tipo_carta: str) -> dict:
    """Calcula X-barra y R/S/MR para un nuevo subgrupo ingresado.

    Args:
        observaciones: lista de floats con las mediciones del subgrupo.
        tipo_carta:    'X-R', 'X-S' o 'I-MR'.

    Returns:
        dict con xbar, disp, tipo_disp.
    """
    arr = np.array(observaciones, dtype=float)
    xbar = float(arr.mean())

    if tipo_carta == "X-R":
        disp      = float(arr.max() - arr.min())
        tipo_disp = "R"
    elif tipo_carta == "X-S":
        disp      = float(arr.std(ddof=1)) if len(arr) > 1 else 0.0
        tipo_disp = "S"
    else:                          # I-MR — el MR se calcula frente al anterior
        disp      = None           # se calcula en contexto con el punto previo
        tipo_disp = "MR"

    return {"xbar": xbar, "disp": disp, "tipo_disp": tipo_disp}


def _f2_evaluar_punto(xbar: float, disp: float | None,
                      limites_xbar: dict, limites_disp: dict,
                      sigma_est: float, reglas: list,
                      historial_xbar: list, historial_disp: list) -> dict:
    """Evalúa si un nuevo punto viola alguna regla de control.

    Aplica las reglas activas sobre la ventana de historial + nuevo punto.
    Sólo retorna señales del *último* punto añadido (índice -1).

    Args:
        xbar, disp:      estadísticos del nuevo subgrupo.
        limites_xbar:    dict {ucl, cl, lcl} de Fase 1.
        limites_disp:    dict {ucl, cl, lcl} de Fase 1.
        sigma_est:       σ estimado en Fase 1.
        reglas:          lista de reglas WE activas.
        historial_xbar:  todos los X-barra anteriores (Fase 1 + Fase 2).
        historial_disp:  todos los R/S anteriores.

    Returns:
        dict con alarmas_xbar (bool), alarmas_disp (bool), reglas_violadas (list).
    """
    ucl_x = limites_xbar["ucl"]
    cl_x  = limites_xbar["cl"]
    lcl_x = limites_xbar["lcl"]
    ucl_d = limites_disp["ucl"]
    cl_d  = limites_disp["cl"]
    lcl_d = limites_disp["lcl"]

    serie_x = np.array(historial_xbar + [xbar])
    serie_d = np.array(historial_disp + ([disp] if disp is not None else []))

    inf_x = _aplicar_reglas_we(serie_x, ucl_x, cl_x, lcl_x, sigma_est, reglas)
    inf_d = _aplicar_reglas_we(serie_d, ucl_d, cl_d, lcl_d, sigma_est, reglas) if len(serie_d) > 0 else []

    last_idx_x = len(serie_x) - 1
    last_idx_d = len(serie_d) - 1

    alarma_x = last_idx_x in inf_x
    alarma_d = (last_idx_d in inf_d) if len(serie_d) > 0 else False

    reglas_txt = []
    if alarma_x:
        reglas_txt.append("Carta X-barra: punto fuera de límites / patrón detectado")
    if alarma_d:
        reglas_txt.append(f"Carta dispersión: punto fuera de límites / patrón detectado")

    return {
        "alarma_xbar": alarma_x,
        "alarma_disp": alarma_d,
        "fuera_control": alarma_x or alarma_d,
        "reglas_violadas": reglas_txt,
    }


def _f2_fig_monitoreo(
    xbar_fase1: list, disp_fase1: list,
    xbar_fase2: list, disp_fase2: list,
    alertas_idx: list,
    limites_xbar: dict, limites_disp: dict,
    sigma_est: float,
    titulo_x: str, titulo_d: str,
    ylabel_d: str,
    lsl: float | None = None,
    usl: float | None = None,
    sg_ids_fase1: list = None,
) -> plt.Figure:
    """Genera una figura con dos subplots: carta X-barra y carta dispersión.

    Los puntos de Fase 1 se muestran en azul apagado como referencia.
    Los puntos de Fase 2 se muestran en azul brillante (normales) o rojo (alarma).
    Los límites son los de Fase 1 (fijos).

    Args:
        xbar_fase1, disp_fase1: arrays de Fase 1 (referencia, no editables).
        xbar_fase2, disp_fase2: puntos nuevos de monitoreo.
        alertas_idx:            índices (base-0 en el array fase2) de puntos en alarma.
        limites_xbar, limites_disp: dicts {ucl, cl, lcl} de Fase 1.
        sigma_est:              σ estimado de Fase 1.
        titulo_x, titulo_d:     títulos de cada subcarta.
        ylabel_d:               etiqueta eje Y de la carta de dispersión.
        lsl, usl:               límites de especificación opcionales.
        sg_ids_fase1:           IDs reales de los subgrupos de Fase 1.

    Returns:
        Figura matplotlib con 2 subplots apilados verticalmente.
    """
    fig, (ax_x, ax_d) = plt.subplots(2, 1, figsize=(12, 7.5), sharex=False)

    k1 = len(xbar_fase1)
    k2 = len(xbar_fase2)
    k_total = k1 + k2

    x1 = np.arange(1, k1 + 1)
    x2 = np.arange(k1 + 1, k_total + 1)

    # ── Helper: dibujar una subcarta ─────────────────────────────────────────
    def _draw_subcarta(ax, arr1, arr2, lim, ylabel, titulo, alerta_idx_disp=None):
        ucl = lim["ucl"]; cl = lim["cl"]; lcl = lim["lcl"]
        sig = (ucl - cl) / 3.0 if (ucl - cl) != 0 else sigma_est

        # Zonas A/B/C de fondo (sobre toda la longitud)
        x_all = np.arange(1, k_total + 1)
        zona_kw = dict(alpha=0.04, linewidth=0)
        ax.fill_between(x_all, cl + 2*sig, ucl,          color="#ef4444", **zona_kw)
        ax.fill_between(x_all, lcl,        cl - 2*sig,   color="#ef4444", **zona_kw)
        ax.fill_between(x_all, cl + sig,   cl + 2*sig,   color="#f59e0b", **zona_kw)
        ax.fill_between(x_all, cl - 2*sig, cl - sig,     color="#f59e0b", **zona_kw)
        ax.fill_between(x_all, cl - sig,   cl + sig,     color="#22c55e", **zona_kw)

        # Línea divisoria Fase 1 / Fase 2
        if k1 > 0 and k2 > 0:
            ax.axvline(k1 + 0.5, color="#64748b", linewidth=1.2,
                       linestyle=":", alpha=0.9)
            ax.text(k1 + 0.6, ucl, "▶ Fase 2", fontsize=7, color="#64748b",
                    va="top")

        # Límites de especificación opcionales (sólo en carta X)
        if ylabel != ylabel_d and lsl is not None:
            ax.axhline(lsl, color="#94a3b8", linewidth=1.0,
                       linestyle=":", alpha=0.55, label=f"LSL={lsl}")
        if ylabel != ylabel_d and usl is not None:
            ax.axhline(usl, color="#94a3b8", linewidth=1.0,
                       linestyle=":", alpha=0.55, label=f"USL={usl}")

        # Líneas de control (fijas de Fase 1)
        ax.axhline(ucl, color="#ef4444", linewidth=1.5, linestyle="--",
                   label=f"UCL = {ucl:.4f}")
        ax.axhline(cl,  color="#22c55e", linewidth=1.8, linestyle="-",
                   label=f"CL  = {cl:.4f}")
        ax.axhline(lcl, color="#ef4444", linewidth=1.5, linestyle="--",
                   label=f"LCL = {lcl:.4f}")

        # Puntos Fase 1 (referencia, azul apagado)
        if len(arr1) > 0:
            ax.plot(x1, arr1, color="#475569", linewidth=1.0, marker="o",
                    markersize=3.5, alpha=0.6, label="Fase 1 (referencia)")

        # Puntos Fase 2 (monitoreo)
        if len(arr2) > 0:
            # Separar normales y en alarma
            arr2_arr = np.array(arr2)
            alerta_set = set(alerta_idx_disp) if alerta_idx_disp else set()

            for i, v in enumerate(arr2_arr):
                xi = k1 + 1 + i
                color_pt = "#ef4444" if i in alerta_set else "#3b82f6"
                size_pt  = 9 if i in alerta_set else 5
                ax.plot([xi], [v], marker="o", markersize=size_pt,
                        color=color_pt, zorder=5)

            # Línea conectora de Fase 2
            ax.plot(x2, arr2_arr, color="#3b82f6", linewidth=1.3,
                    zorder=3, label="Fase 2 (monitoreo)")

            # Scatter de alarmas con borde blanco
            if alerta_set:
                xi_a = np.array([k1 + 1 + i for i in sorted(alerta_set)])
                yi_a = arr2_arr[sorted(alerta_set)]
                ax.scatter(xi_a, yi_a, color="#ef4444", s=90, zorder=6,
                           edgecolors="white", linewidths=0.8,
                           label=f"Alarma ({len(alerta_set)} pto.)")
                # Anotar con "!"
                for xi_ann, yi_ann in zip(xi_a, yi_a):
                    ax.annotate("⚠", xy=(xi_ann, yi_ann),
                                xytext=(0, 10), textcoords="offset points",
                                ha="center", fontsize=9, color="#ef4444")

        # Etiquetas de límites al borde derecho
        for val, lbl, c in [(ucl,"UCL","#ef4444"),(cl,"CL","#22c55e"),(lcl,"LCL","#ef4444")]:
            ax.text(k_total + 0.3, val, f" {lbl}", va="center",
                    fontsize=7.5, color=c)

        ax.set_title(titulo, fontsize=10, fontweight="bold", pad=7)
        ax.set_ylabel(ylabel, fontsize=9)
        ax.set_xlim(0.5, k_total + 1.5)
        ax.legend(fontsize=7, loc="upper right",
                  facecolor="#0f1117", edgecolor="#2a2d3e", ncol=3)
        ax.grid(True, axis="y")

    # Determinar índices de alarma en fase 2 para cada subcarta
    alerta_idx_x = [i for i, a in enumerate(
        st.session_state.get("f2_historial", [])
    ) if a.get("alarma_xbar")]

    alerta_idx_d = [i for i, a in enumerate(
        st.session_state.get("f2_historial", [])
    ) if a.get("alarma_disp")]

    _draw_subcarta(ax_x, xbar_fase1, xbar_fase2, limites_xbar,
                   "X-barra", titulo_x, alerta_idx_x)
    _draw_subcarta(ax_d, disp_fase1, disp_fase2, limites_disp,
                   ylabel_d, titulo_d, alerta_idx_d)

    ax_d.set_xlabel("Subgrupo (secuencia)", fontsize=9)

    # Sombrear fondo Fase 2
    for ax in (ax_x, ax_d):
        if k2 > 0:
            ax.axvspan(k1 + 0.5, k_total + 0.5,
                       color="#3b82f6", alpha=0.04, zorder=0)

    fig.suptitle("Cartas de control — Fase 2: Monitoreo continuo",
                 fontsize=11, fontweight="bold", y=1.01, color="#e2e8f0")
    fig.tight_layout()
    return fig


def _f2_badge_estado(fuera_control: bool, n_alertas: int) -> str:
    """Devuelve HTML de badge de estado para el encabezado."""
    if fuera_control:
        return (
            "<span style='background:rgba(239,68,68,.15);color:#f87171;"
            "border:1px solid #ef4444;border-radius:20px;padding:4px 14px;"
            "font-size:.82rem;font-weight:700'>⛔ FUERA DE CONTROL</span>"
        )
    return (
        "<span style='background:rgba(34,197,94,.15);color:#4ade80;"
        "border:1px solid #22c55e;border-radius:20px;padding:4px 14px;"
        "font-size:.82rem;font-weight:700'>✅ ESTABLE</span>"
    )


def seccion_fase2():
    """Módulo Fase 2 – Monitoreo continuo del proceso CEP.

    Prerrequisito: Fase 1 debe estar calculada y el proceso estable.

    Flujo:
    1. Leer límites y parámetros de Fase 1 (session_state.fase1).
    2. Inicializar estado interno de Fase 2.
    3. Panel de estado actual del proceso (KPIs dinámicos).
    4. Formulario de ingreso de nuevo subgrupo.
    5. Evaluación automática con reglas WE al registrar.
    6. Alertas visuales: estable (verde) / fuera de control (rojo).
    7. Cartas de monitoreo: Fase 1 como referencia + Fase 2 en tiempo real.
    8. Bitácora de alertas con tabla cronológica.
    9. Guardar estado en session_state.fase2.
    """
    encabezado(
        "📈", "Fase 2 – Monitoreo",
        "Vigilancia continua del proceso usando los límites establecidos en Fase 1",
    )

    # ── Prerequisito: Fase 1 calculada ───────────────────────────────────────
    f1 = st.session_state.get("fase1", {})
    if not f1.get("calculado"):
        caja(
            "Complete la **Fase 1 – Estabilización** para habilitar el monitoreo. "
            "Los límites de control deben estar calculados.",
            tipo="warning",
        )
        return

    if not f1.get("proceso_estable"):
        caja(
            "La Fase 1 indica que el proceso **no está bajo control estadístico**. "
            "Elimine las causas especiales detectadas antes de iniciar el monitoreo.",
            tipo="warning",
        )
        # Permitir continuar igualmente (el usuario puede querer monitorear de todas formas)

    # ── Leer parámetros de Fase 1 ─────────────────────────────────────────────
    limites_xbar = f1["limites_xbar"]          # {ucl, cl, lcl}
    limites_disp = f1["limites_disp"]          # {ucl, cl, lcl}
    tipo_disp    = f1["tipo_disp"]             # "R", "S" o "MR"
    sigma_est    = f1["sigma_est"]
    tipo_carta   = f1["tipo_carta"]            # "X-R", "X-S", "I-MR"
    variable     = f1["variable"]
    reglas_f1    = f1.get("reglas_usadas", [1, 2, 3, 5])
    xbar_f1      = np.array(f1.get("xbar_arr", []))
    disp_f1      = np.array(f1.get("disp_arr", []))
    sg_ids_f1    = f1.get("subgrupos_activos", list(range(1, len(xbar_f1)+1)))

    cfg   = st.session_state.config_proceso
    n_tam = int(cfg.get("tamano_subgrupo", 5))
    lsl_v = cfg["lsl_res"] if "Resisten" in variable else cfg["lsl_abs"]
    usl_v = cfg["usl_res"] if "Resisten" in variable else cfg["usl_abs"]

    ylabel_d = {"R": "Rango (R)", "S": "Desv. estándar (S)",
                "MR": "Rango móvil (MR)"}.get(tipo_disp, tipo_disp)

    # ── Inicializar estado interno de Fase 2 ──────────────────────────────────
    if "f2_historial" not in st.session_state:
        st.session_state.f2_historial = []  # lista de dicts por subgrupo registrado
    if "f2_xbar_arr" not in st.session_state:
        st.session_state.f2_xbar_arr = []   # X-barra de cada subgrupo de Fase 2
    if "f2_disp_arr" not in st.session_state:
        st.session_state.f2_disp_arr = []   # R/S/MR de cada subgrupo de Fase 2
    if "f2_contador" not in st.session_state:
        st.session_state.f2_contador = 0    # número secuencial de subgrupos en F2

    f2_hist   = st.session_state.f2_historial
    f2_xbar   = st.session_state.f2_xbar_arr
    f2_disp   = st.session_state.f2_disp_arr
    n_f2      = len(f2_hist)

    # Métricas derivadas del historial
    n_alertas       = sum(1 for h in f2_hist if h.get("fuera_control"))
    ultimo_xbar     = f2_xbar[-1]  if f2_xbar  else None
    ultimo_disp     = f2_disp[-1]  if f2_disp  else None
    ultimo_fuera    = f2_hist[-1].get("fuera_control", False) if f2_hist else False
    pct_alertas     = (n_alertas / n_f2 * 100) if n_f2 > 0 else 0.0

    ucl_x_str = f"{limites_xbar['ucl']:.4f}"
    cl_x_str  = f"{limites_xbar['cl']:.4f}"
    lcl_x_str = f"{limites_xbar['lcl']:.4f}"

    # ══════════════════════════════════════════════════════════════════════════
    # BLOQUE A – Panel de estado actual
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("### 🟢 Estado actual del proceso")

    # Badge de estado
    badge_html = _f2_badge_estado(ultimo_fuera, n_alertas)
    st.markdown(
        f"<div style='margin-bottom:14px'>{badge_html}</div>",
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    ultimo_xbar_str = f"{ultimo_xbar:.4f}" if ultimo_xbar is not None else "—"
    ultimo_disp_str = f"{ultimo_disp:.4f}" if ultimo_disp is not None else "—"
    pct_str         = f"{pct_alertas:.1f}%"

    with col1: tarjeta("Último X-barra",      ultimo_xbar_str, "Subgrupo más reciente")
    with col2: tarjeta(f"Último {tipo_disp}", ultimo_disp_str, "Dispersión más reciente")
    with col3: tarjeta("Subgrupos registrados", str(n_f2),     "En Fase 2")
    with col4: tarjeta("Alertas detectadas",    str(n_alertas), f"{pct_str} del total")
    with col5: tarjeta("UCL X-barra",           ucl_x_str,     f"CL={cl_x_str}  LCL={lcl_x_str}")

    # Información de límites de Fase 1
    caja(
        f"Límites fijos de Fase 1 — "
        f"X-barra: UCL={ucl_x_str}  CL={cl_x_str}  LCL={lcl_x_str} | "
        f"{tipo_disp}: UCL={limites_disp['ucl']:.4f}  CL={limites_disp['cl']:.4f} | "
        f"σ̂={sigma_est:.4f} | Carta: {tipo_carta}",
        tipo="info",
    )

    sep()

    # ══════════════════════════════════════════════════════════════════════════
    # BLOQUE B – Alerta visual del último punto
    # ══════════════════════════════════════════════════════════════════════════
    if f2_hist:
        ultimo = f2_hist[-1]
        if ultimo["fuera_control"]:
            reglas_txt = "\n".join(f"• {r}" for r in ultimo.get("reglas_violadas", []))
            st.markdown(
                f"""
                <div style="background:#1a0a0a;border:2px solid #ef4444;
                            border-radius:12px;padding:18px 22px;margin:12px 0">
                    <div style="font-size:1.1rem;font-weight:700;color:#ef4444;margin-bottom:8px">
                        ⛔ ALERTA — Subgrupo {ultimo['numero']} FUERA DE CONTROL
                    </div>
                    <p style="font-size:.86rem;color:#e2e8f0;margin:0 0 8px">
                        Se detectaron señales en las cartas de control.
                        Investigue la causa antes de continuar la producción.
                    </p>
                    <pre style="font-size:.82rem;color:#f87171;margin:0;
                                background:transparent;border:none">{reglas_txt}</pre>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            sg_num_str = str(ultimo['numero'])
            xbar_ok_str = f"{ultimo['xbar']:.4f}"
            st.markdown(
                f"""
                <div style="background:#0d1f17;border:1.5px solid #22c55e;
                            border-radius:10px;padding:14px 20px;margin:12px 0">
                    <div style="font-size:.95rem;font-weight:700;color:#22c55e;margin-bottom:4px">
                        ✅ Subgrupo {sg_num_str} dentro de control
                    </div>
                    <p style="font-size:.83rem;color:#e2e8f0;margin:0">
                        X-barra = {xbar_ok_str} — ninguna regla de detección fue violada.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    sep()

    # ══════════════════════════════════════════════════════════════════════════
    # BLOQUE C – Formulario de ingreso de nuevo subgrupo
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("### ➕ Registrar nuevo subgrupo")

    with st.expander(
        f"Ingresar mediciones del subgrupo #{st.session_state.f2_contador + 1}",
        expanded=True,
    ):
        caja(
            f"Ingrese las {n_tam} mediciones del próximo subgrupo. "
            "Al registrar, el sistema evaluará automáticamente los límites de Fase 1.",
            tipo="info",
        )

        # Reglas de detección activas (heredadas de Fase 1 o configurables)
        col_reg, col_n = st.columns([2, 1])
        with col_reg:
            opciones_reg = {
                "Heredar de Fase 1": reglas_f1,
                "Regla 1 solo (±3σ)": [1],
                "4 Reglas básicas (1,2,3,5)": [1, 2, 3, 5],
                "8 Reglas WE completo": [1, 2, 3, 4, 5, 6, 7, 8],
            }
            sel_reg = st.selectbox(
                "Reglas de detección para monitoreo",
                list(opciones_reg.keys()),
                index=0,
                key="f2_sel_reglas",
            )
        with col_n:
            st.markdown(f"**Tamaño subgrupo:** {n_tam}")
            st.markdown(f"**Carta activa:** {tipo_carta}")

        reglas_monitoreo = opciones_reg[sel_reg]

        # Campos de medición
        mediciones_cols = st.columns(min(n_tam, 6))
        mediciones = []
        for i in range(n_tam):
            col_idx = i % len(mediciones_cols)
            with mediciones_cols[col_idx]:
                val = st.number_input(
                    f"Medición {i+1}",
                    key=f"f2_med_{i}",
                    value=float(limites_xbar["cl"]),   # default = CL (valor central)
                    step=0.1,
                    format="%.2f",
                )
                mediciones.append(val)

        # Validación inline: verificar que no sean todos iguales al default sin cambio
        mediciones_validas = len(set(mediciones)) > 1 or n_tam == 1

        col_btn, col_rst, _ = st.columns([1, 1, 3])
        with col_btn:
            btn_registrar = st.button(
                "✅ Registrar subgrupo",
                type="primary",
                key="f2_btn_registrar",
                help="Registra el subgrupo y evalúa si está bajo control.",
            )
        with col_rst:
            if st.button("🗑️ Limpiar historial Fase 2", key="f2_btn_limpiar"):
                st.session_state.f2_historial  = []
                st.session_state.f2_xbar_arr   = []
                st.session_state.f2_disp_arr   = []
                st.session_state.f2_contador   = 0
                caja("Historial de Fase 2 limpiado.", tipo="info")
                st.rerun()

        # ── Procesar registro ─────────────────────────────────────────────────
        if btn_registrar:
            stats_sg = _f2_calcular_estadisticos_sg(mediciones, tipo_carta)

            # Para I-MR: calcular MR respecto al punto anterior
            xbar_nuevo = stats_sg["xbar"]
            if tipo_carta == "I-MR" and f2_xbar:
                disp_nuevo = abs(xbar_nuevo - f2_xbar[-1])
            elif tipo_carta == "I-MR":
                # Primer punto I-MR: usar la primera diferencia con el último de Fase 1
                if len(xbar_f1) > 0:
                    disp_nuevo = abs(xbar_nuevo - float(xbar_f1[-1]))
                else:
                    disp_nuevo = 0.0
            else:
                disp_nuevo = stats_sg["disp"]

            # Historial completo para evaluación de reglas
            hist_x_completo = list(xbar_f1) + f2_xbar
            hist_d_completo = list(disp_f1) + f2_disp

            evaluacion = _f2_evaluar_punto(
                xbar=xbar_nuevo,
                disp=disp_nuevo,
                limites_xbar=limites_xbar,
                limites_disp=limites_disp,
                sigma_est=sigma_est,
                reglas=reglas_monitoreo,
                historial_xbar=hist_x_completo,
                historial_disp=hist_d_completo,
            )

            # Guardar en historial
            import datetime
            st.session_state.f2_contador += 1
            nuevo_registro = {
                "numero":        st.session_state.f2_contador,
                "timestamp":     datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "mediciones":    mediciones,
                "xbar":          round(xbar_nuevo, 4),
                "disp":          round(disp_nuevo, 4) if disp_nuevo is not None else None,
                "alarma_xbar":   evaluacion["alarma_xbar"],
                "alarma_disp":   evaluacion["alarma_disp"],
                "fuera_control": evaluacion["fuera_control"],
                "reglas_violadas": evaluacion["reglas_violadas"],
            }
            st.session_state.f2_historial.append(nuevo_registro)
            st.session_state.f2_xbar_arr.append(round(xbar_nuevo, 4))
            st.session_state.f2_disp_arr.append(round(disp_nuevo, 4) if disp_nuevo is not None else 0.0)

            if evaluacion["fuera_control"]:
                caja(
                    f"⛔ Subgrupo #{st.session_state.f2_contador} registrado — "
                    "FUERA DE CONTROL. Revise la bitácora de alertas.",
                    tipo="warning",
                )
            else:
                caja(
                    f"✅ Subgrupo #{st.session_state.f2_contador} registrado — "
                    "proceso dentro de control.",
                    tipo="success",
                )
            st.rerun()

    sep()

    # ══════════════════════════════════════════════════════════════════════════
    # BLOQUE D – Cartas de monitoreo
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("### 📉 Cartas de control — Monitoreo en tiempo real")

    if not f2_xbar:
        caja(
            "Registre al menos un subgrupo en el formulario anterior "
            "para visualizar las cartas de monitoreo.",
            tipo="info",
        )
    else:
        sufijo_v = variable.split("(")[0].strip()
        titulo_x_mon = (
            f"Carta X-barra — {sufijo_v} | Fase 1 (ref.) + {n_f2} subgrupos Fase 2"
        )
        titulo_d_mon = (
            f"Carta {tipo_disp} — {sufijo_v} | Fase 1 (ref.) + {n_f2} subgrupos Fase 2"
        )

        fig_mon = _f2_fig_monitoreo(
            xbar_fase1   = list(xbar_f1),
            disp_fase1   = list(disp_f1),
            xbar_fase2   = f2_xbar,
            disp_fase2   = f2_disp,
            alertas_idx  = [],          # índices se leen desde session_state dentro de la función
            limites_xbar = limites_xbar,
            limites_disp = limites_disp,
            sigma_est    = sigma_est,
            titulo_x     = titulo_x_mon,
            titulo_d     = titulo_d_mon,
            ylabel_d     = ylabel_d,
            lsl          = lsl_v,
            usl          = usl_v,
            sg_ids_fase1 = sg_ids_f1,
        )
        st.pyplot(fig_mon, use_container_width=True)
        plt.close(fig_mon)

    sep()

    # ══════════════════════════════════════════════════════════════════════════
    # BLOQUE E – Bitácora de alertas
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("### 🚨 Bitácora de alertas")

    if not f2_hist:
        caja("No se han registrado subgrupos aún.", tipo="info")
    else:
        # Tabla de todos los subgrupos registrados
        filas = []
        for h in f2_hist:
            disp_val = h.get("disp")
            disp_str = f"{disp_val:.4f}" if disp_val is not None else "—"
            estado   = "⛔ ALERTA" if h["fuera_control"] else "✅ OK"
            reglas_v = "; ".join(h.get("reglas_violadas", [])) if h["fuera_control"] else "—"
            filas.append({
                "N°":            h["numero"],
                "Fecha/Hora":    h["timestamp"],
                "X-barra":       f"{h['xbar']:.4f}",
                tipo_disp:       disp_str,
                "Estado":        estado,
                "Reglas violadas": reglas_v,
            })

        df_bitacora = pd.DataFrame(filas)
        st.dataframe(df_bitacora, use_container_width=True, hide_index=True)

        # Resumen de alertas
        n_ok     = sum(1 for h in f2_hist if not h["fuera_control"])
        n_alerta = n_alertas
        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1: tarjeta("Total subgrupos",  str(n_f2))
        with col_s2: tarjeta("✅ Dentro control", str(n_ok),     f"{100-pct_alertas:.1f}%")
        with col_s3: tarjeta("⛔ Alertas",        str(n_alerta), f"{pct_alertas:.1f}%")

        if n_alerta == 0:
            caja(
                "El proceso se ha mantenido bajo control estadístico "
                "durante todo el periodo de monitoreo.",
                tipo="success",
            )
        elif pct_alertas <= 10:
            caja(
                f"{n_alerta} subgrupo(s) en alerta ({pct_alertas:.1f}%). "
                "Investigue las causas de las señales detectadas.",
                tipo="warning",
            )
        else:
            caja(
                f"⛔ {n_alerta} subgrupo(s) en alerta ({pct_alertas:.1f}%). "
                "El proceso presenta variación por causas especiales en Fase 2. "
                "Actualice la Fase 1 con los nuevos datos.",
                tipo="warning",
            )

    sep()

    # ══════════════════════════════════════════════════════════════════════════
    # BLOQUE F – Guardar estado en session_state
    # ══════════════════════════════════════════════════════════════════════════
    st.session_state.fase2 = {
        "alertas":            [h for h in f2_hist if h["fuera_control"]],
        "ultimas_mediciones": f2_hist[-1]["mediciones"] if f2_hist else [],
        "n_subgrupos":        n_f2,
        "n_alertas":          n_alertas,
        "xbar_arr":           list(f2_xbar),
        "disp_arr":           list(f2_disp),
    }


# SECCIÓN 6 – Control por atributos
# ─────────────────────────────────────────────────────────────────────────────

# ── Funciones de cálculo – cartas por atributos ───────────────────────────────

def _attr_limites_p(n_arr: np.ndarray, d_arr: np.ndarray) -> dict:
    """Calcula límites para carta p (fracción defectiva).

    Permite tamaños de muestra variables: los límites se recalculan por punto.
    Sigue el modelo de distribución binomial, ±3σ.

    Args:
        n_arr: array de tamaños de muestra por lote.
        d_arr: array de defectivos por lote.

    Returns:
        dict con p_bar, ucl (array), lcl (array), cl.
    """
    p_i   = d_arr / n_arr                     # fracción por lote
    p_bar = float(d_arr.sum() / n_arr.sum())  # fracción global
    sigma = np.sqrt(p_bar * (1 - p_bar) / n_arr)

    ucl = np.minimum(p_bar + 3 * sigma, 1.0)  # no superar 1
    lcl = np.maximum(p_bar - 3 * sigma, 0.0)  # no ser negativo

    return {
        "tipo":  "p",
        "p_bar": p_bar,
        "p_i":   p_i,
        "cl":    p_bar,
        "ucl":   ucl,
        "lcl":   lcl,
        "variable_limits": True,   # límites distintos por punto
    }


def _attr_limites_np(n: float, d_arr: np.ndarray) -> dict:
    """Calcula límites para carta np (número de defectivos).

    Requiere tamaño de muestra constante.

    Args:
        n:     tamaño de muestra constante.
        d_arr: array de defectivos por lote.

    Returns:
        dict con np_bar, ucl, lcl, cl.
    """
    p_bar  = float(d_arr.mean() / n)
    np_bar = float(d_arr.mean())
    sigma  = np.sqrt(n * p_bar * (1 - p_bar))

    ucl = min(np_bar + 3 * sigma, n)
    lcl = max(np_bar - 3 * sigma, 0.0)

    return {
        "tipo":   "np",
        "np_bar": np_bar,
        "p_bar":  p_bar,
        "cl":     np_bar,
        "ucl":    ucl,
        "lcl":    lcl,
        "variable_limits": False,
    }


def _attr_limites_c(defectos_arr: np.ndarray) -> dict:
    """Calcula límites para carta c (número de defectos por unidad fija).

    Distribución de Poisson: σ = √c̄.

    Args:
        defectos_arr: array de conteo de defectos por unidad de inspección.

    Returns:
        dict con c_bar, ucl, lcl, cl.
    """
    c_bar = float(defectos_arr.mean())
    sigma = np.sqrt(c_bar)

    ucl = c_bar + 3 * sigma
    lcl = max(c_bar - 3 * sigma, 0.0)

    return {
        "tipo":  "c",
        "c_bar": c_bar,
        "cl":    c_bar,
        "ucl":   ucl,
        "lcl":   lcl,
        "variable_limits": False,
    }


def _attr_limites_u(n_arr: np.ndarray, defectos_arr: np.ndarray) -> dict:
    """Calcula límites para carta u (defectos por unidad, área variable).

    u_i = defectos_i / n_i; ū = Σdefectos / Σn; límites varían por muestra.

    Args:
        n_arr:        array de tamaños de muestra (unidades inspeccionadas).
        defectos_arr: array de defectos totales por lote.

    Returns:
        dict con u_bar, ucl (array), lcl (array), cl.
    """
    u_i   = defectos_arr / n_arr
    u_bar = float(defectos_arr.sum() / n_arr.sum())
    sigma = np.sqrt(u_bar / n_arr)

    ucl = u_bar + 3 * sigma
    lcl = np.maximum(u_bar - 3 * sigma, 0.0)

    return {
        "tipo":  "u",
        "u_bar": u_bar,
        "u_i":   u_i,
        "cl":    u_bar,
        "ucl":   ucl,
        "lcl":   lcl,
        "variable_limits": True,
    }


def _attr_detectar_señales(serie: np.ndarray, ucl, lcl) -> list:
    """Detecta puntos fuera de los límites de control (regla 1 básica).

    Args:
        serie: array de estadísticos por lote.
        ucl:   límite superior (escalar o array).
        lcl:   límite inferior (escalar o array).

    Returns:
        Lista de índices base-0 con señales.
    """
    ucl_arr = np.full_like(serie, ucl) if np.isscalar(ucl) else np.array(ucl)
    lcl_arr = np.full_like(serie, lcl) if np.isscalar(lcl) else np.array(lcl)
    return [i for i, (v, u, l) in enumerate(zip(serie, ucl_arr, lcl_arr))
            if v > u or v < l]


def _attr_calcular_pnc(n_total: int, d_total: int) -> dict:
    """Calcula el porcentaje de productos no conformes y métricas asociadas.

    Args:
        n_total: total de unidades inspeccionadas.
        d_total: total de unidades no conformes.

    Returns:
        dict con pnc (%), conformes, no_conformes, dpmo, nivel_sigma.
    """
    if n_total == 0:
        return {"pnc": None, "conformes": 0, "no_conformes": 0,
                "dpmo": None, "nivel_sigma": None}

    pnc = d_total / n_total * 100
    conformes = n_total - d_total
    dpmo = d_total / n_total * 1_000_000

    # Nivel sigma aproximado (tabla Six Sigma, corregido por 1.5σ shift)
    if dpmo > 0:
        from scipy.stats import norm as _norm
        nivel_sigma = round(_norm.ppf(1 - d_total / n_total) + 1.5, 2)
    else:
        nivel_sigma = 6.0

    return {
        "pnc":          round(pnc, 4),
        "conformes":    int(conformes),
        "no_conformes": int(d_total),
        "dpmo":         round(dpmo, 1),
        "nivel_sigma":  nivel_sigma,
    }


def _attr_interpretar(tipo_carta: str, lim: dict, señales: list,
                      n_lotes: int, pnc: dict) -> dict:
    """Genera interpretación automática de los resultados.

    Returns:
        dict con estado ('control'|'marginal'|'fuera'), mensaje, recomendaciones.
    """
    n_señales = len(señales)
    pct_sen   = n_señales / n_lotes * 100 if n_lotes > 0 else 0

    if n_señales == 0:
        estado = "control"
        msg    = (
            "El proceso de atributos está bajo control estadístico. "
            "No se detectaron señales fuera de los límites en ningún lote."
        )
        recom  = [
            "Continúe el monitoreo con la frecuencia actual.",
            "Documente los límites como referencia para auditorías.",
            "Evalúe oportunidades de mejora si el %PNC supera las metas.",
        ]
    elif pct_sen <= 10:
        estado = "marginal"
        msg    = (
            f"Se detectaron {n_señales} lote(s) con señal ({pct_sen:.1f} % del total). "
            "El proceso muestra variabilidad de atributos que requiere investigación."
        )
        recom  = [
            "Identifique las causas de los lotes en señal.",
            "Implemente acciones correctivas en los lotes señalados.",
            "Reevalúe los límites si las causas son atribuibles a cambios de proceso.",
        ]
    else:
        estado = "fuera"
        msg    = (
            f"Se detectaron {n_señales} lote(s) con señal ({pct_sen:.1f} % del total). "
            "El proceso de atributos presenta variación por causas especiales."
        )
        recom  = [
            "Suspenda la producción o aplique revisión 100 % hasta identificar causas.",
            "Realice un análisis de causa raíz (diagrama de Ishikawa, Pareto).",
            "Actualice los límites de control después de eliminar causas especiales.",
        ]

    # Interpretación de %PNC
    pnc_val = pnc.get("pnc")
    if pnc_val is not None:
        if pnc_val < 1:
            pnc_msg = f"%PNC = {pnc_val:.2f}% — Proceso competitivo (< 1 %)."
        elif pnc_val < 5:
            pnc_msg = f"%PNC = {pnc_val:.2f}% — Nivel aceptable, con oportunidad de mejora."
        else:
            pnc_msg = f"%PNC = {pnc_val:.2f}% — Nivel alto de no conformes. Acción correctiva urgente."
    else:
        pnc_msg = "No hay datos suficientes para calcular %PNC."

    return {"estado": estado, "mensaje": msg,
            "recomendaciones": recom, "pnc_mensaje": pnc_msg}


# ── Gráfica de carta por atributos ────────────────────────────────────────────

def _attr_fig_carta(
    serie: np.ndarray,
    ucl, cl: float, lcl,
    señales: list,
    titulo: str,
    ylabel: str,
    tipo: str,
    n_lotes: int,
) -> plt.Figure:
    """Genera la carta de control para atributos.

    Soporta UCL/LCL variables (array) para cartas p y u.

    Args:
        serie:   estadístico por lote.
        ucl:     límite superior (escalar o array).
        cl:      línea central (escalar).
        lcl:     límite inferior (escalar o array).
        señales: índices base-0 de lotes fuera de control.
        titulo:  título del gráfico.
        ylabel:  etiqueta eje Y.
        tipo:    'p', 'np', 'c' o 'u'.
        n_lotes: número de lotes.

    Returns:
        Figura matplotlib.
    """
    fig, ax = plt.subplots(figsize=(11, 4.0))
    x = np.arange(1, n_lotes + 1)

    ucl_arr = np.full(n_lotes, ucl) if np.isscalar(ucl) else np.array(ucl)
    lcl_arr = np.full(n_lotes, lcl) if np.isscalar(lcl) else np.array(lcl)

    # Banda entre LCL y UCL (zona de control)
    ax.fill_between(x, lcl_arr, ucl_arr, alpha=0.06,
                    color=C_SUCCESS, linewidth=0)

    # Líneas de control
    if np.isscalar(ucl):
        ax.axhline(ucl, color=C_DANGER,  linewidth=1.5, linestyle="--",
                   label=f"UCL = {ucl:.4f}")
        ax.axhline(lcl, color=C_DANGER,  linewidth=1.5, linestyle="--",
                   label=f"LCL = {lcl:.4f}")
    else:
        ax.plot(x, ucl_arr, color=C_DANGER, linewidth=1.3,
                linestyle="--", label="UCL (variable)")
        ax.plot(x, lcl_arr, color=C_DANGER, linewidth=1.3,
                linestyle="--", label="LCL (variable)")

    ax.axhline(cl, color=C_SUCCESS, linewidth=1.8,
               label=f"CL = {cl:.4f}")

    # Serie principal
    ax.plot(x, serie, color=C_PRIMARY, linewidth=1.3,
            marker="o", markersize=4.5, zorder=3)

    # Señales
    if señales:
        xi = np.array([i + 1 for i in señales])
        yi = serie[señales]
        ax.scatter(xi, yi, color=C_DANGER, s=70, zorder=5,
                   edgecolors="white", linewidths=0.8,
                   label=f"Señal ({len(señales)} lote(s))")
        for xv, yv in zip(xi, yi):
            ax.annotate("⚠", xy=(xv, yv), xytext=(0, 9),
                        textcoords="offset points", ha="center",
                        fontsize=9, color=C_DANGER)

    # Etiquetas de límites al extremo derecho
    ax.text(n_lotes + 0.3, ucl_arr[-1], " UCL", va="center",
            fontsize=7.5, color=C_DANGER)
    ax.text(n_lotes + 0.3, cl, " CL", va="center",
            fontsize=7.5, color=C_SUCCESS)
    if lcl_arr[-1] > 0:
        ax.text(n_lotes + 0.3, lcl_arr[-1], " LCL", va="center",
                fontsize=7.5, color=C_DANGER)

    ax.set_title(titulo, fontsize=10.5, fontweight="bold", pad=8)
    ax.set_xlabel("Lote / muestra", fontsize=9)
    ax.set_ylabel(ylabel, fontsize=9)
    ax.set_xlim(0.5, n_lotes + 1.5)
    ax.legend(fontsize=7.5, loc="upper right",
              facecolor="#0f1117", edgecolor="#2a2d3e", ncol=2)
    ax.grid(True, axis="y")
    fig.tight_layout()
    return fig


def _attr_fig_pnc_tendencia(lotes: np.ndarray, pnc_i: np.ndarray,
                             pnc_bar: float) -> plt.Figure:
    """Gráfico de tendencia del %PNC lote a lote."""
    fig, ax = plt.subplots(figsize=(11, 3.2))
    x = np.arange(1, len(lotes) + 1)

    ax.fill_between(x, 0, pnc_i * 100,
                    color=C_PRIMARY, alpha=0.15, linewidth=0)
    ax.plot(x, pnc_i * 100, color=C_PRIMARY, linewidth=1.4,
            marker="o", markersize=4)
    ax.axhline(pnc_bar * 100, color=C_ACCENT, linewidth=1.5,
               linestyle="--", label=f"%PNC promedio = {pnc_bar*100:.2f}%")
    ax.axhline(0, color=C_SUCCESS, linewidth=0.8, linestyle=":")

    ax.set_title("Tendencia del % de Productos No Conformes (%PNC) por lote",
                 fontsize=10.5, fontweight="bold", pad=8)
    ax.set_xlabel("Lote", fontsize=9)
    ax.set_ylabel("%PNC", fontsize=9)
    ax.set_xlim(0.5, len(lotes) + 0.5)
    ax.legend(fontsize=8, facecolor="#0f1117", edgecolor="#2a2d3e")
    ax.grid(True, axis="y")
    fig.tight_layout()
    return fig


# ── Datos de ejemplo por tipo de carta ────────────────────────────────────────

def _attr_ejemplo_p() -> pd.DataFrame:
    """Genera datos de ejemplo para carta p (tamaño variable)."""
    np.random.seed(7)
    n_lotes = 25
    n_arr   = np.random.choice([48, 50, 52], n_lotes)
    p_base  = 0.04
    # Inyectar dos lotes con defectiva alta
    d_arr   = np.array([int(n * np.random.beta(2, 48)) for n in n_arr])
    d_arr[9]  = int(n_arr[9]  * 0.18)  # señal lote 10
    d_arr[20] = int(n_arr[20] * 0.15)  # señal lote 21
    return pd.DataFrame({"Lote": range(1, n_lotes+1),
                         "n_muestra": n_arr, "defectivos": d_arr})


def _attr_ejemplo_np() -> pd.DataFrame:
    """Genera datos de ejemplo para carta np (tamaño constante)."""
    np.random.seed(8)
    n_lotes = 25; n = 50
    d_arr   = np.random.binomial(n, 0.04, n_lotes)
    d_arr[11] = 18; d_arr[19] = 16  # señales
    return pd.DataFrame({"Lote": range(1, n_lotes+1),
                         "n_muestra": n, "defectivos": d_arr})


def _attr_ejemplo_c() -> pd.DataFrame:
    """Genera datos de ejemplo para carta c."""
    np.random.seed(9)
    n_lotes = 25
    c_arr   = np.random.poisson(3.5, n_lotes)
    c_arr[6]  = 12; c_arr[18] = 13  # señales
    return pd.DataFrame({"Lote": range(1, n_lotes+1),
                         "defectos": c_arr})


def _attr_ejemplo_u() -> pd.DataFrame:
    """Genera datos de ejemplo para carta u (unidades variables)."""
    np.random.seed(10)
    n_lotes = 25
    n_arr   = np.random.choice([8, 10, 12], n_lotes)
    c_arr   = np.array([int(n * np.random.exponential(0.35)) for n in n_arr])
    c_arr[13] = int(n_arr[13] * 1.8); c_arr[22] = int(n_arr[22] * 1.9)
    return pd.DataFrame({"Lote": range(1, n_lotes+1),
                         "n_unidades": n_arr, "defectos": c_arr})


# ── Función principal ──────────────────────────────────────────────────────────

def seccion_atributos():
    """Módulo de Control por Atributos del sistema CEP.

    Implementa las cuatro cartas de control para atributos:
    - Carta p  (fracción defectiva, n variable)
    - Carta np (número de defectivos, n constante)
    - Carta c  (número de defectos, área fija)
    - Carta u  (defectos por unidad, área variable)

    Incluye:
    - Ingreso de datos manual o carga de ejemplo
    - Cálculo de límites con distribuciones Binomial/Poisson
    - Detección de señales (regla ±3σ)
    - %PNC y DPMO con nivel sigma
    - Interpretación automática
    """
    encabezado(
        "🔢", "Control por atributos",
        "Cartas p, np, c y u para variables cualitativas del proceso productivo",
    )

    # ══════════════════════════════════════════════════════════════════════════
    # BLOQUE A – Selección de carta y descripción
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("### 📊 Tipo de carta de control")

    TIPOS_CARTA = {
        "p  – Fracción defectiva":    "Proporción de unidades defectuosas. Acepta tamaño de muestra variable. Distribución Binomial.",
        "np – N° de defectivos":      "Número absoluto de defectuosos. Requiere tamaño de muestra **constante**. Distribución Binomial.",
        "c  – N° de defectos":        "Conteo total de defectos en una unidad de inspección de tamaño fijo. Distribución Poisson.",
        "u  – Defectos por unidad":   "Defectos por unidad cuando el área de oportunidad varía entre muestras. Distribución Poisson.",
    }

    c_sel, c_desc = st.columns([1, 2])
    with c_sel:
        tipo_sel = st.radio(
            "Carta a construir:",
            list(TIPOS_CARTA.keys()),
            key="attr_tipo",
        )
    with c_desc:
        caja(TIPOS_CARTA[tipo_sel], tipo="info")
        tipo_clave = tipo_sel.split("–")[0].strip().split()[0]  # "p","np","c","u"

    # Mapas de ayuda
    YLABEL = {"p": "Fracción defectiva (p)", "np": "N° defectivos (np)",
              "c": "N° defectos (c)", "u": "Defectos por unidad (u)"}

    sep()

    # ══════════════════════════════════════════════════════════════════════════
    # BLOQUE B – Ingreso de datos
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("### 📥 Datos de atributos")

    fuente = st.radio(
        "Fuente de datos:",
        ["🎲 Usar datos de ejemplo", "✏️ Ingreso manual"],
        horizontal=True,
        key="attr_fuente",
    )

    df_raw = None  # DataFrame con los datos crudos

    if fuente == "🎲 Usar datos de ejemplo":
        gen_map = {"p": _attr_ejemplo_p, "np": _attr_ejemplo_np,
                   "c": _attr_ejemplo_c, "u": _attr_ejemplo_u}
        df_raw = gen_map[tipo_clave]()
        caja(
            f"Datos de ejemplo generados para carta **{tipo_clave.upper()}**: "
            f"{len(df_raw)} lotes con causas especiales inyectadas en lotes {[10,21] if tipo_clave=='p' else [12,20] if tipo_clave=='np' else [7,19] if tipo_clave=='c' else [14,23]}.",
            tipo="success",
        )
        st.dataframe(df_raw, use_container_width=True, hide_index=True)

    else:
        # Ingreso manual con número configurable de lotes
        n_lotes_m = st.number_input(
            "Número de lotes a ingresar", value=10, min_value=5, max_value=50,
            key="attr_n_lotes_manual",
        )

        if tipo_clave in ("p", "np"):
            st.markdown("**Defectivos por lote** (ingrese `n` y `defectivos` por fila)")
            n_const = None
            if tipo_clave == "np":
                n_const = st.number_input(
                    "Tamaño de muestra constante (n)", value=50, min_value=5,
                    key="attr_n_const",
                )
            filas = []
            for i in range(int(n_lotes_m)):
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.text(f"Lote {i+1}")
                with c2:
                    ni = n_const if n_const else st.number_input(
                        "n", key=f"attr_ni_{i}", value=50, min_value=1,
                        label_visibility="collapsed",
                    )
                with c3:
                    di = st.number_input(
                        "defectivos", key=f"attr_di_{i}", value=0, min_value=0,
                        label_visibility="collapsed",
                    )
                filas.append({"Lote": i+1, "n_muestra": int(ni), "defectivos": int(di)})
            df_raw = pd.DataFrame(filas)

        else:  # c o u
            st.markdown("**Defectos por lote**")
            filas = []
            for i in range(int(n_lotes_m)):
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.text(f"Lote {i+1}")
                if tipo_clave == "u":
                    with c2:
                        ni = st.number_input(
                            "n unidades", key=f"attr_nu_{i}", value=10, min_value=1,
                            label_visibility="collapsed",
                        )
                else:
                    ni = 1
                with c3:
                    ci = st.number_input(
                        "defectos", key=f"attr_ci_{i}", value=0, min_value=0,
                        label_visibility="collapsed",
                    )
                col_n = "n_unidades" if tipo_clave == "u" else "n_muestra"
                filas.append({"Lote": i+1, col_n: int(ni), "defectos": int(ci)})
            df_raw = pd.DataFrame(filas)

    if df_raw is None or len(df_raw) < 3:
        caja("Se necesitan al menos 3 lotes para construir la carta.", tipo="warning")
        return

    sep()

    # ══════════════════════════════════════════════════════════════════════════
    # BLOQUE C – Cálculo de límites
    # ══════════════════════════════════════════════════════════════════════════

    # Extraer arrays según tipo
    try:
        if tipo_clave == "p":
            n_arr = df_raw["n_muestra"].to_numpy(dtype=float)
            d_arr = df_raw["defectivos"].to_numpy(dtype=float)
            lim   = _attr_limites_p(n_arr, d_arr)
            serie = lim["p_i"]
            pnc_d = _attr_calcular_pnc(int(n_arr.sum()), int(d_arr.sum()))

        elif tipo_clave == "np":
            n_arr = df_raw["n_muestra"].to_numpy(dtype=float)
            d_arr = df_raw["defectivos"].to_numpy(dtype=float)
            n_c   = float(n_arr[0])          # asume constante
            lim   = _attr_limites_np(n_c, d_arr)
            serie = d_arr.astype(float)
            pnc_d = _attr_calcular_pnc(int(n_arr.sum()), int(d_arr.sum()))

        elif tipo_clave == "c":
            c_arr = df_raw["defectos"].to_numpy(dtype=float)
            n_arr = np.ones(len(c_arr))      # 1 unidad por lote
            lim   = _attr_limites_c(c_arr)
            serie = c_arr
            pnc_d = {"pnc": None, "conformes": 0, "no_conformes": int(c_arr.sum()),
                     "dpmo": None, "nivel_sigma": None}

        else:  # u
            n_arr  = df_raw["n_unidades"].to_numpy(dtype=float)
            c_arr  = df_raw["defectos"].to_numpy(dtype=float)
            lim    = _attr_limites_u(n_arr, c_arr)
            serie  = lim["u_i"]
            pnc_d  = {"pnc": None, "conformes": 0, "no_conformes": int(c_arr.sum()),
                      "dpmo": None, "nivel_sigma": None}

    except Exception as exc:
        caja(f"Error al procesar los datos: {exc}", tipo="warning")
        return

    señales     = _attr_detectar_señales(serie, lim["ucl"], lim["lcl"])
    n_lotes     = len(serie)
    interp      = _attr_interpretar(tipo_clave, lim, señales, n_lotes, pnc_d)

    sep()

    # ══════════════════════════════════════════════════════════════════════════
    # BLOQUE D – KPIs de límites
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("### 📐 Parámetros calculados")

    # Construir strings seguros (nunca inline conditional)
    cl_str  = f"{lim['cl']:.4f}"
    ucl_scalar = lim["ucl"] if np.isscalar(lim["ucl"]) else float(np.mean(lim["ucl"]))
    lcl_scalar = lim["lcl"] if np.isscalar(lim["lcl"]) else float(np.mean(lim["lcl"]))
    ucl_str = f"{ucl_scalar:.4f}" + (" (variable)" if lim["variable_limits"] else "")
    lcl_str = f"{max(lcl_scalar, 0):.4f}" + (" (variable)" if lim["variable_limits"] else "")

    pnc_str   = f"{pnc_d['pnc']:.2f}%" if pnc_d["pnc"] is not None else "N/A"
    dpmo_str  = f"{pnc_d['dpmo']:,.0f}" if pnc_d["dpmo"] is not None else "N/A"
    nsig_str  = f"{pnc_d['nivel_sigma']:.2f}" if pnc_d["nivel_sigma"] is not None else "N/A"
    señ_str   = str(len(señales))

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1: tarjeta(f"CL – Carta {tipo_clave.upper()}", cl_str,  "Línea central")
    with c2: tarjeta("UCL",                              ucl_str, "Límite superior")
    with c3: tarjeta("LCL",                              lcl_str, "Límite inferior")
    with c4: tarjeta("%PNC",                             pnc_str, "Productos no conformes")
    with c5: tarjeta("DPMO",                             dpmo_str,"Defectos por millón")
    with c6: tarjeta("Lotes en señal",                   señ_str, f"de {n_lotes} lotes")

    sep()

    # ══════════════════════════════════════════════════════════════════════════
    # BLOQUE E – Carta de control
    # ══════════════════════════════════════════════════════════════════════════
    nombre_carta = tipo_sel.split("–")[0].strip()
    titulo_carta = (
        f"Carta {nombre_carta} — {n_lotes} lotes "
        f"({'límites variables' if lim['variable_limits'] else 'límites constantes'})"
    )

    st.markdown(f"### 📉 {titulo_carta}")
    caja(
        "Los **puntos rojos** representan lotes fuera de los límites de control. "
        "La banda verde es la zona de proceso bajo control. "
        + ("Los límites varían por lote según el tamaño de muestra." if lim["variable_limits"] else ""),
        tipo="info",
    )

    fig_carta = _attr_fig_carta(
        serie, lim["ucl"], lim["cl"], lim["lcl"],
        señales, titulo_carta, YLABEL[tipo_clave], tipo_clave, n_lotes,
    )
    st.pyplot(fig_carta, use_container_width=True)
    plt.close(fig_carta)

    sep()

    # ══════════════════════════════════════════════════════════════════════════
    # BLOQUE F – Gráfico de tendencia %PNC (solo p y np)
    # ══════════════════════════════════════════════════════════════════════════
    if tipo_clave in ("p", "np"):
        st.markdown("### 📈 Tendencia del %PNC por lote")
        p_i_arr = (d_arr / n_arr)
        fig_pnc = _attr_fig_pnc_tendencia(
            np.arange(1, n_lotes + 1), p_i_arr, lim.get("p_bar", p_i_arr.mean())
        )
        st.pyplot(fig_pnc, use_container_width=True)
        plt.close(fig_pnc)
        sep()

    # ══════════════════════════════════════════════════════════════════════════
    # BLOQUE G – Tabla de resultados
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("### 📋 Tabla de resultados por lote")

    filas_res = []
    for i in range(n_lotes):
        ucl_i = float(lim["ucl"][i]) if not np.isscalar(lim["ucl"]) else float(lim["ucl"])
        lcl_i = float(lim["lcl"][i]) if not np.isscalar(lim["lcl"]) else float(lim["lcl"])
        estado = "⛔ Señal" if i in señales else "✅ OK"
        fila = {
            "Lote":       int(df_raw["Lote"].iloc[i]),
            "Estadístico": f"{serie[i]:.4f}",
            "UCL":         f"{ucl_i:.4f}",
            "CL":          f"{lim['cl']:.4f}",
            "LCL":         f"{max(lcl_i, 0):.4f}",
            "Estado":      estado,
        }
        filas_res.append(fila)

    df_res = pd.DataFrame(filas_res)
    st.dataframe(df_res, use_container_width=True, hide_index=True)

    sep()

    # ══════════════════════════════════════════════════════════════════════════
    # BLOQUE H – %PNC y métricas de calidad
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("### 💯 Métricas de productos no conformes (%PNC)")

    if pnc_d["pnc"] is not None:
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1: tarjeta("Unidades inspeccionadas",
                             f"{pnc_d['conformes'] + pnc_d['no_conformes']:,}")
        with col_m2: tarjeta("Conformes",
                             f"{pnc_d['conformes']:,}",
                             f"{100 - pnc_d['pnc']:.2f}%")
        with col_m3: tarjeta("No conformes",
                             f"{pnc_d['no_conformes']:,}",
                             pnc_str)
        with col_m4: tarjeta("Nivel sigma",
                             nsig_str,
                             f"DPMO: {dpmo_str}")
    else:
        caja(
            "Las métricas %PNC y DPMO aplican para cartas p y np "
            "(unidades defectuosas). Para c y u se reportan defectos totales.",
            tipo="info",
        )
        col_c1, col_c2 = st.columns(2)
        total_def = int(serie.sum()) if tipo_clave == "c" else int(c_arr.sum())
        with col_c1: tarjeta("Total defectos detectados", str(total_def))
        with col_c2: tarjeta("Promedio defectos/lote", f"{serie.mean():.2f}")

    sep()

    # ══════════════════════════════════════════════════════════════════════════
    # BLOQUE I – Interpretación automática
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("### 🧭 Interpretación automática")

    color_est = {
        "control":  "#22c55e",
        "marginal": "#f59e0b",
        "fuera":    "#ef4444",
    }[interp["estado"]]

    icono_est = {
        "control": "✅", "marginal": "⚠️", "fuera": "❌"
    }[interp["estado"]]

    estado_txt = {
        "control":  "PROCESO BAJO CONTROL",
        "marginal": "PROCESO MARGINALMENTE ESTABLE",
        "fuera":    "PROCESO FUERA DE CONTROL",
    }[interp["estado"]]

    señ_str2 = str(len(señales))
    n_lotes_str = str(n_lotes)

    st.markdown(
        f"""
        <div style="background:#0f1117;border:2px solid {color_est};
                    border-radius:12px;padding:20px 24px;margin:10px 0">
            <div style="font-size:1.1rem;font-weight:700;
                        color:{color_est};margin-bottom:8px">
                {icono_est} {estado_txt}
            </div>
            <p style="font-size:.87rem;color:#e2e8f0;margin:0 0 10px">
                {interp["mensaje"]}
            </p>
            <div style="display:flex;gap:30px;flex-wrap:wrap;margin-top:8px">
                <div>
                    <div style="font-size:.65rem;color:#64748b;
                                text-transform:uppercase;letter-spacing:.1em">Lotes analizados</div>
                    <div style="font-family:monospace;font-size:1.3rem;
                                color:#e2e8f0;font-weight:700">{n_lotes_str}</div>
                </div>
                <div>
                    <div style="font-size:.65rem;color:#64748b;
                                text-transform:uppercase;letter-spacing:.1em">Lotes en señal</div>
                    <div style="font-family:monospace;font-size:1.3rem;
                                color:{color_est};font-weight:700">{señ_str2}</div>
                </div>
                <div>
                    <div style="font-size:.65rem;color:#64748b;
                                text-transform:uppercase;letter-spacing:.1em">%PNC proceso</div>
                    <div style="font-family:monospace;font-size:1.3rem;
                                color:#3b82f6;font-weight:700">{pnc_str}</div>
                </div>
                <div>
                    <div style="font-size:.65rem;color:#64748b;
                                text-transform:uppercase;letter-spacing:.1em">Nivel sigma</div>
                    <div style="font-family:monospace;font-size:1.3rem;
                                color:#818cf8;font-weight:700">{nsig_str}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Mensaje específico de %PNC
    caja(interp["pnc_mensaje"], tipo={
        "control": "success", "marginal": "info", "fuera": "warning"
    }[interp["estado"]])

    # Recomendaciones
    st.markdown("#### 🔧 Recomendaciones")
    for rec in interp["recomendaciones"]:
        color_rec = color_est
        st.markdown(
            f"""<div style="display:flex;gap:10px;align-items:flex-start;
                            padding:9px 14px;background:#1a1d27;border-radius:8px;
                            border-left:3px solid {color_rec};margin-bottom:7px">
                    <span style="font-size:.87rem;color:#e2e8f0">{rec}</span>
                </div>""",
            unsafe_allow_html=True,
        )


# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 7 – Capacidad del proceso
# ─────────────────────────────────────────────────────────────────────────────

# ── Funciones de cálculo de capacidad ────────────────────────────────────────

def _calcular_indices_capacidad(datos: np.ndarray, lsl: float, usl: float,
                                 sigma_within: float | None = None) -> dict:
    """Calcula Cp, Cpk, Pp, Ppk y métricas asociadas.

    Args:
        datos:        array 1-D de observaciones individuales.
        lsl:          límite inferior de especificación.
        usl:          límite superior de especificación.
        sigma_within: σ estimado por cartas de control (Fase 1). Si None usa σ_total.

    Returns:
        dict con: media, sigma_total, sigma_within, cp, cpk, pp, ppk,
                  pnc_pct, pnc_lsl, pnc_usl, ppm, nivel_sigma,
                  n_fuera_lsl, n_fuera_usl, n_conforme, n_total.
    """
    n        = len(datos)
    media    = float(np.mean(datos))
    std_tot  = float(np.std(datos, ddof=1))       # σ total  → Pp / Ppk
    std_wit  = sigma_within if (sigma_within is not None and sigma_within > 0) else std_tot

    # Protección contra sigma = 0
    if std_tot <= 0:
        return {"error": "σ total = 0. Todos los datos son idénticos."}
    if std_wit <= 0:
        std_wit = std_tot

    tolerancia = usl - lsl

    # ── Índices de capacidad ──────────────────────────────────────────────────
    cp   = tolerancia / (6.0 * std_wit)
    cpu  = (usl - media) / (3.0 * std_wit)
    cpl  = (media - lsl) / (3.0 * std_wit)
    cpk  = min(cpu, cpl)

    pp   = tolerancia / (6.0 * std_tot)
    ppu  = (usl - media) / (3.0 * std_tot)
    ppl  = (media - lsl) / (3.0 * std_tot)
    ppk  = min(ppu, ppl)

    # ── Productos no conformes (observados) ───────────────────────────────────
    mask_lsl   = datos < lsl
    mask_usl   = datos > usl
    n_fuera_l  = int(mask_lsl.sum())
    n_fuera_u  = int(mask_usl.sum())
    n_fuera    = n_fuera_l + n_fuera_u
    n_conf     = n - n_fuera
    pnc_pct    = (n_fuera / n * 100) if n > 0 else 0.0

    # ── PPM teórico (basado en la distribución normal ajustada) ───────────────
    ppm_lsl = sp_stats.norm.cdf((lsl - media) / std_tot) * 1_000_000
    ppm_usl = (1 - sp_stats.norm.cdf((usl - media) / std_tot)) * 1_000_000
    ppm_tot = ppm_lsl + ppm_usl

    # ── Nivel sigma equivalente (a partir de Cpk) ─────────────────────────────
    nivel_sigma = cpk * 3.0

    return {
        "n":             n,
        "media":         round(media,   4),
        "sigma_total":   round(std_tot, 4),
        "sigma_within":  round(std_wit, 4),
        "tolerancia":    round(tolerancia, 4),
        "cp":            round(cp,   3),
        "cpu":           round(cpu,  3),
        "cpl":           round(cpl,  3),
        "cpk":           round(cpk,  3),
        "pp":            round(pp,   3),
        "ppu":           round(ppu,  3),
        "ppl":           round(ppl,  3),
        "ppk":           round(ppk,  3),
        "n_fuera_lsl":   n_fuera_l,
        "n_fuera_usl":   n_fuera_u,
        "n_fuera":       n_fuera,
        "n_conforme":    n_conf,
        "pnc_pct":       round(pnc_pct, 3),
        "ppm_lsl":       round(ppm_lsl, 1),
        "ppm_usl":       round(ppm_usl, 1),
        "ppm_total":     round(ppm_tot, 1),
        "nivel_sigma":   round(nivel_sigma, 3),
    }


def _nivel_capacidad(valor: float) -> tuple[str, str, str]:
    """Devuelve (etiqueta, color, ícono) según el valor del índice."""
    if valor >= 1.67:
        return "Excelente",  C_SUCCESS, "🌟"
    if valor >= 1.33:
        return "Capaz",      C_SUCCESS, "✅"
    if valor >= 1.00:
        return "Marginal",   C_ACCENT,  "⚠️"
    return "No capaz",       C_DANGER,  "❌"


def _fig_capacidad_histograma(datos: np.ndarray, lsl: float, usl: float,
                               target: float, res: dict,
                               variable: str, unidad: str) -> plt.Figure:
    """Histograma de capacidad con curva normal, spec lines y coloreado de NC.

    Args:
        datos:    array 1-D de observaciones.
        lsl/usl:  límites de especificación.
        target:   valor objetivo.
        res:      resultado de _calcular_indices_capacidad.
        variable: nombre de la variable (título).
        unidad:   unidad de medida.

    Returns:
        Figura matplotlib.
    """
    media   = res["media"]
    std_tot = res["sigma_total"]
    cp      = res["cp"]
    cpk     = res["cpk"]

    fig, ax = plt.subplots(figsize=(10, 4.8))
    n_bins  = max(12, int(1 + 3.322 * np.log10(len(datos))))

    # ── Histograma con coloreado por conformidad ──────────────────────────────
    counts, edges, patches = ax.hist(
        datos, bins=n_bins,
        color=C_PRIMARY, alpha=0.80,
        edgecolor="#0f1117", linewidth=0.5, zorder=2,
    )
    for patch, left_e, right_e in zip(patches, edges[:-1], edges[1:]):
        if right_e <= lsl or left_e >= usl:
            patch.set_facecolor(C_DANGER)
            patch.set_alpha(0.90)
            patch.set_edgecolor("#ff0000")
            patch.set_linewidth(0.8)

    # ── Curva normal teórica ──────────────────────────────────────────────────
    x_min = min(datos.min(), lsl) - 2.5 * std_tot
    x_max = max(datos.max(), usl) + 2.5 * std_tot
    x_c   = np.linspace(x_min, x_max, 400)
    pdf   = sp_stats.norm.pdf(x_c, media, std_tot)
    # Escalar la curva a la altura del histograma
    bin_w = edges[1] - edges[0]
    pdf_s = pdf * len(datos) * bin_w
    ax.plot(x_c, pdf_s, color=C_NORMAL, linewidth=2.2, zorder=4, label="Normal teórica")

    # ── Líneas de especificación ───────────────────────────────────────────────
    ymax = ax.get_ylim()[1] * 1.02
    ax.axvline(lsl,    color=C_DANGER,  linewidth=2.0, linestyle="--",
               label=f"LSL = {lsl}", zorder=5)
    ax.axvline(usl,    color=C_DANGER,  linewidth=2.0, linestyle="--",
               label=f"USL = {usl}", zorder=5)
    ax.axvline(target, color=C_ACCENT,  linewidth=1.5, linestyle=":",
               label=f"Target = {target}", zorder=5)
    ax.axvline(media,  color=C_SUCCESS, linewidth=1.8, linestyle="-",
               label=f"Media = {media:.3f}", zorder=5)

    # Etiquetas flotantes sobre las líneas verticales
    for xv, txt, col in [
        (lsl,    "LSL",    C_DANGER),
        (usl,    "USL",    C_DANGER),
        (target, "Target", C_ACCENT),
        (media,  "X̄",      C_SUCCESS),
    ]:
        ax.text(xv, ymax * 0.97, txt, color=col, fontsize=7.5,
                ha="center", va="top", rotation=90,
                bbox=dict(boxstyle="round,pad=0.2", facecolor="#0f1117",
                          edgecolor=col, alpha=0.85))

    # ── Anotación de índices en el gráfico ────────────────────────────────────
    _, color_cp,  _ = _nivel_capacidad(cp)
    _, color_cpk, _ = _nivel_capacidad(cpk)
    txt_ind = (
        f"Cp  = {cp:.3f}\n"
        f"Cpk = {cpk:.3f}\n"
        f"Pp  = {res['pp']:.3f}\n"
        f"Ppk = {res['ppk']:.3f}"
    )
    ax.text(
        0.985, 0.97, txt_ind,
        transform=ax.transAxes,
        fontsize=8.5, va="top", ha="right",
        fontfamily="monospace",
        color="#e2e8f0",
        bbox=dict(boxstyle="round,pad=0.45", facecolor="#0f1117",
                  edgecolor="#2a2d3e", alpha=0.92),
    )

    ax.set_title(
        f"Histograma de Capacidad – {variable}",
        fontsize=11, fontweight="bold", pad=10,
    )
    ax.set_xlabel(f"{variable} ({unidad})", fontsize=9)
    ax.set_ylabel("Frecuencia", fontsize=9)
    ax.set_xlim(x_min, x_max)
    ax.legend(fontsize=7.5, loc="upper left",
              facecolor="#0f1117", edgecolor="#2a2d3e", ncol=2)
    ax.grid(True, axis="y", alpha=0.5)
    fig.tight_layout()
    return fig


def _fig_conformidad_barras(res: dict) -> plt.Figure:
    """Gráfico de barras de conformes vs no conformes."""
    n_conf = res["n_conforme"]
    n_lsl  = res["n_fuera_lsl"]
    n_usl  = res["n_fuera_usl"]
    total  = res["n"]

    fig, axes = plt.subplots(1, 2, figsize=(9, 3.8))

    # ── Panel izquierdo: barras apiladas horizontales ─────────────────────────
    ax1 = axes[0]
    cats   = ["Proceso"]
    conf_p = [n_conf / total * 100]
    lsl_p  = [n_lsl  / total * 100]
    usl_p  = [n_usl  / total * 100]

    ax1.barh(cats, conf_p, color=C_SUCCESS, alpha=0.85, label=f"Conforme ({n_conf})")
    ax1.barh(cats, lsl_p, left=conf_p, color=C_DANGER,  alpha=0.85,
             label=f"NC < LSL ({n_lsl})")
    ax1.barh(cats, usl_p,
             left=[c + l for c, l in zip(conf_p, lsl_p)],
             color="#f97316", alpha=0.85, label=f"NC > USL ({n_usl})")

    ax1.set_xlim(0, 100)
    ax1.set_xlabel("Porcentaje (%)", fontsize=9)
    ax1.set_title("Distribución de conformidad", fontsize=10, fontweight="bold")
    ax1.legend(fontsize=8, facecolor="#0f1117", edgecolor="#2a2d3e")
    ax1.grid(True, axis="x", alpha=0.4)

    # Etiquetas dentro de las barras
    for pct, xstart, color_t in [
        (conf_p[0], 0,                   "#0f1117"),
        (lsl_p[0],  conf_p[0],           "#ffffff"),
        (usl_p[0],  conf_p[0]+lsl_p[0],  "#ffffff"),
    ]:
        if pct > 3:
            ax1.text(xstart + pct / 2, 0, f"{pct:.1f}%",
                     va="center", ha="center", fontsize=8.5,
                     fontweight="bold", color=color_t)

    # ── Panel derecho: gráfico de dona ────────────────────────────────────────
    ax2 = axes[1]
    sizes  = [n_conf, n_lsl, n_usl]
    labels = [f"Conforme\n{n_conf}", f"NC < LSL\n{n_lsl}", f"NC > USL\n{n_usl}"]
    colors = [C_SUCCESS, C_DANGER, "#f97316"]
    explode = [0, 0.06, 0.06]

    # Filtrar segmentos vacíos para evitar warnings
    datos_dona = [(s, l, c, e) for s, l, c, e in zip(sizes, labels, colors, explode) if s > 0]
    if datos_dona:
        sz, lb, co, ex = zip(*datos_dona)
        wedges, texts, autotexts = ax2.pie(
            sz, labels=lb, colors=co, explode=ex,
            autopct=lambda p: f"{p:.1f}%" if p > 1 else "",
            startangle=90,
            wedgeprops=dict(width=0.55, edgecolor="#0f1117", linewidth=1.2),
            textprops=dict(fontsize=8, color="#e2e8f0"),
        )
        for at in autotexts:
            at.set_fontsize(8)
            at.set_color("#0f1117")
            at.set_fontweight("bold")

    ax2.set_title("Productos no conformes", fontsize=10, fontweight="bold")

    fig.suptitle(
        f"Total: {total} observaciones  |  PNC: {res['pnc_pct']:.2f}%",
        fontsize=9, color="#94a3b8", y=1.01,
    )
    fig.tight_layout()
    return fig


def _tarjeta_indice(col_ui, nombre: str, valor: float, desc: str):
    """Renderiza una tarjeta de índice con color según nivel de capacidad."""
    lbl, color, icono = _nivel_capacidad(valor)
    col_ui.markdown(
        f"""
        <div class="m-card" style="border-color:{color}33">
            <div class="m-lbl">{nombre}</div>
            <div class="m-val" style="color:{color}">{valor:.3f}</div>
            <div class="m-note">{icono} {lbl}</div>
            <div class="m-note" style="margin-top:4px;font-size:.68rem">{desc}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _panel_interpretacion_cap(res: dict, proceso_estable: bool | None,
                               variable: str) -> None:
    """Renderiza el panel de interpretación automática y recomendaciones."""
    cp   = res["cp"]
    cpk  = res["cpk"]
    pnc  = res["pnc_pct"]
    media = res["media"]

    # ── Determinar estado del proceso ─────────────────────────────────────────
    cap_ok      = cpk >= 1.33
    variab_ok   = cp  >= 1.33
    centrado_ok = abs(cp - cpk) < 0.10   # centrado si Cp ≈ Cpk

    if proceso_estable is None:
        estable_txt = "no se ha evaluado"
        estable_col = C_MUTED
    elif proceso_estable:
        estable_txt = "estable (bajo control estadístico)"
        estable_col = C_SUCCESS
    else:
        estable_txt = "inestable (causas especiales detectadas)"
        estable_col = C_DANGER

    # Veredicto principal
    if cap_ok and variab_ok:
        estado     = "PROCESO CAPAZ"
        color_est  = C_SUCCESS
        icono_est  = "✅"
        msg_est    = (
            f"El proceso de {variable} es capaz y cumple las especificaciones. "
            f"La variabilidad es adecuada (Cp = {cp:.3f}) y el proceso está bien centrado (Cpk = {cpk:.3f})."
        )
    elif variab_ok and not cap_ok:
        estado     = "PROCESO DESCENTRADO"
        color_est  = C_ACCENT
        icono_est  = "⚠️"
        msg_est    = (
            f"La variabilidad del proceso es adecuada (Cp = {cp:.3f}), "
            f"pero el proceso está descentrado (Cpk = {cpk:.3f}). "
            "Ajuste la media del proceso hacia el valor objetivo."
        )
    elif proceso_estable and not cap_ok:
        estado     = "PROCESO ESTABLE PERO NO CAPAZ"
        color_est  = C_ACCENT
        icono_est  = "⚠️"
        msg_est    = (
            "El proceso es estable (bajo control estadístico), pero NO es capaz de cumplir las especificaciones. "
            f"Cp = {cp:.3f} y Cpk = {cpk:.3f} indican que la variabilidad inherente del proceso supera los límites. "
            "Se requiere reducción de variabilidad (mejora del proceso), no solo ajuste de la media."
        )
    else:
        estado     = "PROCESO NO CAPAZ"
        color_est  = C_DANGER
        icono_est  = "❌"
        msg_est    = (
            f"El proceso de {variable} NO es capaz. "
            f"Cpk = {cpk:.3f} y Cp = {cp:.3f} indican alta variabilidad y/o descentramiento. "
            f"El proceso genera productos fuera de especificación ({pnc:.2f} % observado)."
        )

    st.markdown(
        f"""
        <div style="background:#0f1117;border:2px solid {color_est};border-radius:12px;
                    padding:22px 26px;margin:14px 0">
            <div style="font-size:1.15rem;font-weight:700;color:{color_est};margin-bottom:10px">
                {icono_est} &nbsp; {estado}
            </div>
            <p style="font-size:.88rem;color:#e2e8f0;margin:0 0 14px">{msg_est}</p>
            <div style="font-size:.82rem;color:{estable_col}">
                🔄 Estabilidad del proceso: <strong>{estable_txt}</strong>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Recomendaciones automáticas ───────────────────────────────────────────
    recom = []
    if cpk < 1.00:
        recom.append(("❌", C_DANGER,
                       "El proceso genera una proporción inaceptable de productos NC. "
                       "Intervención urgente requerida."))
    if not variab_ok:
        recom.append(("📉", C_DANGER,
                       "Reducir la variabilidad del proceso. Revise causas comunes: "
                       "materia prima, maquinaria, método de compactación."))
    if variab_ok and not centrado_ok:
        recom.append(("🎯", C_ACCENT,
                       "Ajustar la media del proceso hacia el valor objetivo (Target). "
                       "La variabilidad es aceptable, pero el centrado debe corregirse."))
    if not proceso_estable and proceso_estable is not None:
        recom.append(("⚡", C_DANGER,
                       "Eliminar las causas especiales detectadas en Fase 1 antes de "
                       "tomar decisiones sobre capacidad."))
    if pnc > 5:
        recom.append(("🗑️", C_DANGER,
                       f"El {pnc:.1f}% de productos no conformes genera costos de scrap y reproceso. "
                       "Evalúe inspección 100% temporalmente."))
    if res["ppm_total"] > 6_210:
        recom.append(("📊", C_ACCENT,
                       f"PPM teórico = {res['ppm_total']:,.0f}. "
                       "El proceso opera por debajo del estándar Four-Sigma (6 210 PPM)."))
    if cap_ok and cpk >= 1.33:
        recom.append(("📋", C_SUCCESS,
                       "Documente los límites de control actuales y establezca frecuencia "
                       "de muestreo para mantener el proceso capaz en Fase 2."))
    if not recom:
        recom.append(("✅", C_SUCCESS,
                       "El proceso cumple los estándares de capacidad Six Sigma. "
                       "Mantenga el monitoreo continuo para preservar el desempeño."))

    st.markdown("#### 🔧 Recomendaciones automáticas")
    for ico, color_r, texto in recom:
        st.markdown(
            f"""
            <div style="display:flex;gap:12px;align-items:flex-start;
                        padding:10px 15px;background:#1a1d27;border-radius:8px;
                        border-left:3px solid {color_r};margin-bottom:7px">
                <span style="font-size:1.1rem">{ico}</span>
                <span style="font-size:.86rem;color:#e2e8f0">{texto}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ── Panel principal de la sección ─────────────────────────────────────────────

def seccion_capacidad():
    """Módulo completo de Capacidad del Proceso del sistema CEP.

    Flujo interno:
    1.  Verificar datos cargados (o modo manual).
    2.  Selector de variable y fuente de sigma.
    3.  Cálculo de Cp, Cpk, Pp, Ppk con validaciones.
    4.  Panel de tarjetas de índices con código de color.
    5.  Guía de interpretación.
    6.  Histograma de capacidad con curva normal y spec lines.
    7.  Métricas de productos no conformes (PNC, PPM).
    8.  Gráfico de barras/dona de conformidad.
    9.  Panel de interpretación automática y recomendaciones.
    10. Guardar resultados en st.session_state.capacidad.
    """
    encabezado(
        "⚙️", "Capacidad del proceso",
        "Evaluación de Cp, Cpk, Pp, Ppk · Histograma de capacidad · Productos no conformes",
    )

    cfg          = st.session_state.config_proceso
    datos_ok     = st.session_state.get("datos_cargados", False)
    df_sg        = st.session_state.get("df_subgrupos")
    fase1_estado = st.session_state.get("fase1", {})

    # ══════════════════════════════════════════════════════════════════════════
    # BLOQUE A – Selector de variable y configuración de especificaciones
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("### 🎛️ Configuración del análisis")

    col_var, col_info = st.columns([1, 3])
    with col_var:
        variable_cap = st.radio(
            "Variable a analizar:",
            ["Resistencia", "Absorción"],
            key="cap_variable",
        )
    with col_info:
        if datos_ok and df_sg is not None:
            n_obs = len(df_sg)
            n_sgs = df_sg["subgrupo"].nunique()
            caja(
                f"Dataset activo: **{n_obs} observaciones** · **{n_sgs} subgrupos** · "
                "Especificaciones tomadas de la configuración del proceso.",
                tipo="info",
            )
        else:
            caja(
                "No hay datos cargados. Puede ingresar datos manualmente abajo, "
                "o vaya a **📥 Ingreso de datos** para cargar un archivo.",
                tipo="warning",
            )

    # ── Especificaciones (editables inline) ───────────────────────────────────
    with st.expander("📐 Especificaciones de proceso (editables)", expanded=not datos_ok):
        if variable_cap == "Resistencia":
            c1, c2, c3 = st.columns(3)
            with c1:
                lsl_cap = st.number_input(
                    "LSL – Límite inferior (kg/cm²)",
                    value=float(cfg.get("lsl_res", 130.0)),
                    step=0.5, format="%.1f", key="cap_lsl",
                )
            with c2:
                usl_cap = st.number_input(
                    "USL – Límite superior (kg/cm²)",
                    value=float(cfg.get("usl_res", 160.0)),
                    step=0.5, format="%.1f", key="cap_usl",
                )
            with c3:
                target_cap = st.number_input(
                    "Target – Valor objetivo (kg/cm²)",
                    value=float(cfg.get("target_res", 145.0)),
                    step=0.5, format="%.1f", key="cap_target",
                )
            unidad_cap = "kg/cm²"
        else:
            c1, c2, c3 = st.columns(3)
            with c1:
                lsl_cap = st.number_input(
                    "LSL – Mínimo de absorción (%)",
                    value=float(cfg.get("lsl_abs", 0.0)),
                    step=0.1, format="%.1f", key="cap_lsl",
                )
            with c2:
                usl_cap = st.number_input(
                    "USL – Máximo de absorción (%)",
                    value=float(cfg.get("usl_abs", 10.0)),
                    step=0.1, format="%.1f", key="cap_usl",
                )
            with c3:
                target_cap = st.number_input(
                    "Target – Valor objetivo (%)",
                    value=float(cfg.get("usl_abs", 10.0)) / 2.0,
                    step=0.1, format="%.1f", key="cap_target",
                )
            unidad_cap = "%"

        if not (lsl_cap < target_cap < usl_cap):
            caja("⚠️ Verifique: debe cumplirse LSL < Target < USL.", tipo="warning")

    # ── Fuente de datos ───────────────────────────────────────────────────────
    if datos_ok and df_sg is not None:
        col_datos = "resistencia" if variable_cap == "Resistencia" else "absorcion"
        datos_cap = df_sg[col_datos].dropna().to_numpy()
        modo_manual = False
    else:
        st.markdown("#### ✏️ Ingreso manual de datos")
        caja(
            "Ingrese las observaciones separadas por comas o espacios. "
            "Mínimo 10 valores.",
            tipo="info",
        )
        raw_text = st.text_area(
            "Observaciones:",
            placeholder="Ej: 142.1, 145.3, 138.7, 149.2, 143.0, ...",
            height=100,
            key="cap_datos_manuales",
        )
        try:
            import re as _re
            tokens   = _re.split(r"[,\s;]+", raw_text.strip())
            datos_cap = np.array([float(t) for t in tokens if t], dtype=float)
        except Exception:
            datos_cap = np.array([])
        modo_manual = True

        if len(datos_cap) < 10:
            if raw_text.strip():
                caja(f"Se necesitan al menos 10 observaciones. Actualmente: {len(datos_cap)}.", tipo="warning")
            return

    # ── Sigma estimado (desde Fase 1 si está disponible) ──────────────────────
    sigma_within = None
    f1_ok        = fase1_estado.get("calculado", False)
    f1_var       = fase1_estado.get("variable", "")
    variable_f1  = "Resistencia" if "resist" in f1_var.lower() else "Absorción"

    if f1_ok and variable_f1 == variable_cap:
        sigma_within = fase1_estado.get("sigma_est")

    proceso_estable = fase1_estado.get("proceso_estable", None) if f1_ok else None

    sep()

    # ══════════════════════════════════════════════════════════════════════════
    # BLOQUE B – Validaciones previas al cálculo
    # ══════════════════════════════════════════════════════════════════════════
    if len(datos_cap) < 10:
        caja("Se requieren al menos 10 observaciones para calcular la capacidad.", tipo="warning")
        return

    if usl_cap <= lsl_cap:
        caja("USL debe ser mayor que LSL. Corrija las especificaciones.", tipo="warning")
        return

    # ══════════════════════════════════════════════════════════════════════════
    # BLOQUE C – Cálculo de índices
    # ══════════════════════════════════════════════════════════════════════════
    res = _calcular_indices_capacidad(datos_cap, lsl_cap, usl_cap, sigma_within)

    if "error" in res:
        caja(f"Error en el cálculo: {res['error']}", tipo="warning")
        return

    # Guardar en session_state para uso por otros módulos
    st.session_state.capacidad = {
        "cp":    res["cp"],
        "cpk":   res["cpk"],
        "pp":    res["pp"],
        "ppk":   res["ppk"],
        "variable": variable_cap,
    }

    # ══════════════════════════════════════════════════════════════════════════
    # BLOQUE D – Tarjetas de índices
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("### 📐 Índices de capacidad y desempeño")

    # Indicador de sigma fuente
    if sigma_within is not None and not modo_manual:
        caja(
            f"σ within = **{res['sigma_within']:.4f}** (tomado de Fase 1 · carta de control). "
            f"σ total = **{res['sigma_total']:.4f}** (calculado de los datos).",
            tipo="success",
        )
    else:
        caja(
            f"σ within = σ total = **{res['sigma_total']:.4f}** "
            "(Fase 1 no ejecutada o variable diferente; Cp = Pp y Cpk = Ppk).",
            tipo="info",
        )

    c1, c2, c3, c4 = st.columns(4)
    _tarjeta_indice(c1, "Cp",  res["cp"],  "Capacidad potencial · centrado ignorado")
    _tarjeta_indice(c2, "Cpk", res["cpk"], "Capacidad real · considera descentramiento")
    _tarjeta_indice(c3, "Pp",  res["pp"],  "Desempeño global · σ total")
    _tarjeta_indice(c4, "Ppk", res["ppk"], "Desempeño real · σ total")

    sep()

    # Detalle CPU / CPL
    with st.expander("🔍 Detalle de índices unilaterales", expanded=False):
        dc1, dc2, dc3, dc4, dc5, dc6 = st.columns(6)
        for col_u, nom, val in [
            (dc1, "CPU",      res["cpu"]),
            (dc2, "CPL",      res["cpl"]),
            (dc3, "PPU",      res["ppu"]),
            (dc4, "PPL",      res["ppl"]),
            (dc5, "σ within", res["sigma_within"]),
            (dc6, "σ total",  res["sigma_total"]),
        ]:
            lbl_u, col_u_color, _ = _nivel_capacidad(val) if nom not in ("σ within", "σ total") else ("—", C_PRIMARY, "")
            col_u.markdown(
                f"""<div class="m-card">
                    <div class="m-lbl">{nom}</div>
                    <div class="m-val" style="color:{col_u_color if nom not in ('σ within','σ total') else C_PRIMARY}">{val:.4f}</div>
                </div>""",
                unsafe_allow_html=True,
            )

    # ── Guía de interpretación ────────────────────────────────────────────────
    st.markdown("#### 🔎 Guía de interpretación rápida")
    st.markdown(
        """
        | Índice | < 1.00 | 1.00 – 1.33 | 1.33 – 1.67 | ≥ 1.67 |
        |--------|:------:|:-----------:|:-----------:|:------:|
        | **Nivel** | ❌ No capaz | ⚠️ Marginal | ✅ Capaz | 🌟 Excelente (Six Sigma) |
        """
    )

    sep()

    # ══════════════════════════════════════════════════════════════════════════
    # BLOQUE E – Histograma de capacidad
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("### 📈 Histograma de capacidad")
    caja(
        "Las barras en **rojo** corresponden a observaciones fuera de especificación. "
        "La curva violeta es la distribución normal teórica ajustada a los datos.",
        tipo="info",
    )

    fig_hist = _fig_capacidad_histograma(
        datos_cap, lsl_cap, usl_cap, target_cap,
        res, variable_cap, unidad_cap,
    )
    st.pyplot(fig_hist, use_container_width=True)
    plt.close(fig_hist)

    sep()

    # ══════════════════════════════════════════════════════════════════════════
    # BLOQUE F – Métricas de productos no conformes
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("### 🚫 Productos no conformes (PNC)")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total observaciones",   f"{res['n']:,}")
    m2.metric("Conformes",             f"{res['n_conforme']:,}",
              delta=f"{100 - res['pnc_pct']:.2f}%",
              delta_color="normal")
    m3.metric("No conformes",          f"{res['n_fuera']:,}",
              delta=f"{res['pnc_pct']:.2f}%",
              delta_color="inverse")
    m4.metric("PPM teórico",           f"{res['ppm_total']:,.0f}",
              help="Partes por millón fuera de especificación según la normal teórica.")

    st.markdown("<div style='margin-top:10px'></div>", unsafe_allow_html=True)

    # Métricas de desglose NC
    mn1, mn2, mn3, mn4 = st.columns(4)
    mn1.metric("NC < LSL (observado)", f"{res['n_fuera_lsl']:,}")
    mn2.metric("NC > USL (observado)", f"{res['n_fuera_usl']:,}")
    mn3.metric("PPM < LSL (teórico)",  f"{res['ppm_lsl']:,.0f}")
    mn4.metric("PPM > USL (teórico)",  f"{res['ppm_usl']:,.0f}")

    # Interpretación automática de PNC
    pnc = res["pnc_pct"]
    if pnc == 0:
        st.success("✅ No se detectaron productos no conformes en el dataset analizado.")
    elif pnc < 1.0:
        st.success(
            f"✅ El porcentaje de productos no conformes es bajo ({pnc:.3f} %). "
            "El proceso opera cerca de las especificaciones."
        )
    elif pnc < 5.0:
        st.warning(
            f"⚠️ El {pnc:.2f}% de los productos no cumple especificaciones. "
            "El proceso requiere mejora para reducir la variabilidad."
        )
    else:
        st.error(
            f"❌ El {pnc:.2f}% de los productos no cumple especificaciones (elevado). "
            "El proceso genera un volumen inaceptable de defectos. "
            "Se recomienda revisión inmediata de materia prima, maquinaria y método."
        )

    # Nivel sigma
    st.markdown(
        f"""
        <div style="background:#1a1d27;border:1px solid #2a2d3e;border-radius:10px;
                    padding:14px 18px;margin:12px 0;display:flex;align-items:center;gap:20px">
            <div>
                <div style="font-size:.65rem;color:#64748b;letter-spacing:.1em;
                            text-transform:uppercase">Nivel sigma equivalente</div>
                <div style="font-family:monospace;font-size:2rem;font-weight:700;
                            color:{C_PRIMARY}">{res['nivel_sigma']:.2f}σ</div>
            </div>
            <div style="font-size:.84rem;color:#94a3b8">
                Calculado como Cpk × 3. Un proceso Six Sigma alcanza ≥ 5σ (Cpk ≥ 1.67).
                El nivel actual corresponde a <strong style="color:#e2e8f0">
                {res['ppm_total']:,.0f} PPM</strong> teórico.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    sep()

    # ══════════════════════════════════════════════════════════════════════════
    # BLOQUE G – Gráfico de conformidad
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("### 📊 Distribución de conformidad")
    fig_conf = _fig_conformidad_barras(res)
    st.pyplot(fig_conf, use_container_width=True)
    plt.close(fig_conf)

    sep()

    # ══════════════════════════════════════════════════════════════════════════
    # BLOQUE H – Tabla resumen de resultados
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("### 📋 Tabla resumen de resultados")

    def _nivel_txt(v):
        lbl, _, ico = _nivel_capacidad(v)
        return f"{ico} {lbl}"

    df_res = pd.DataFrame([
        {"Parámetro": "Variable analizada",    "Valor": variable_cap,                      "Nivel": "—"},
        {"Parámetro": "n (observaciones)",     "Valor": str(res["n"]),                     "Nivel": "—"},
        {"Parámetro": "Media (x̄)",             "Valor": f"{res['media']:.4f} {unidad_cap}", "Nivel": "—"},
        {"Parámetro": "σ within (cartas)",     "Valor": f"{res['sigma_within']:.4f}",       "Nivel": "—"},
        {"Parámetro": "σ total (global)",      "Valor": f"{res['sigma_total']:.4f}",        "Nivel": "—"},
        {"Parámetro": "LSL",                   "Valor": f"{lsl_cap:.2f} {unidad_cap}",      "Nivel": "—"},
        {"Parámetro": "USL",                   "Valor": f"{usl_cap:.2f} {unidad_cap}",      "Nivel": "—"},
        {"Parámetro": "Target",                "Valor": f"{target_cap:.2f} {unidad_cap}",   "Nivel": "—"},
        {"Parámetro": "Cp",                    "Valor": f"{res['cp']:.3f}",                 "Nivel": _nivel_txt(res["cp"])},
        {"Parámetro": "Cpk",                   "Valor": f"{res['cpk']:.3f}",                "Nivel": _nivel_txt(res["cpk"])},
        {"Parámetro": "Pp",                    "Valor": f"{res['pp']:.3f}",                 "Nivel": _nivel_txt(res["pp"])},
        {"Parámetro": "Ppk",                   "Valor": f"{res['ppk']:.3f}",                "Nivel": _nivel_txt(res["ppk"])},
        {"Parámetro": "PNC observado (%)",     "Valor": f"{res['pnc_pct']:.3f}",            "Nivel": "—"},
        {"Parámetro": "NC < LSL (obs.)",       "Valor": str(res["n_fuera_lsl"]),            "Nivel": "—"},
        {"Parámetro": "NC > USL (obs.)",       "Valor": str(res["n_fuera_usl"]),            "Nivel": "—"},
        {"Parámetro": "PPM total (teórico)",   "Valor": f"{res['ppm_total']:,.0f}",         "Nivel": "—"},
        {"Parámetro": "Nivel sigma",           "Valor": f"{res['nivel_sigma']:.3f}σ",       "Nivel": "—"},
    ])
    st.dataframe(df_res, use_container_width=True, hide_index=True)

    sep()

    # ══════════════════════════════════════════════════════════════════════════
    # BLOQUE I – Interpretación automática y recomendaciones
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("### 🧠 Interpretación automática")
    _panel_interpretacion_cap(res, proceso_estable, variable_cap)


# ─────────────────────────────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 8 – Desempeño del sistema
# Incluye: Potencia, ARL, ATS, curvas OC, KPIs y GR&R placeholder
# ══════════════════════════════════════════════════════════════════════════════

# ─────────────────────────────────────────────────────────────────────────────
# 8-A  Funciones estadísticas: Potencia, ARL y ATS
# ─────────────────────────────────────────────────────────────────────────────

def _ds_potencia_xbar(delta_sigma: float, n: int, k: float = 3.0) -> float:
    """Potencia de la carta X̄ para detectar un desplazamiento de δ·σ.

    La potencia es la probabilidad de que AL MENOS un punto caiga fuera de los
    límites de control en un subgrupo dado un desplazamiento de la media de
    δ desviaciones estándar del proceso (σ_proceso, no σ_xbar).

    Formula:
        σ_xbar = σ / √n
        LCL_z  = -k  (límites en unidades de σ_xbar)
        UCL_z  = +k
        Media desplazada: μ_nueva = δ (en unidades de σ_xbar = δ·√n en σ_proceso)
        Potencia = 1 - P(LCL_z < Z < UCL_z | μ_nueva)

    Args:
        delta_sigma: desplazamiento expresado en múltiplos de σ_proceso.
        n:           tamaño del subgrupo.
        k:           multiplicador de límites (default 3).

    Returns:
        Potencia ∈ [0, 1].
    """
    if n <= 0 or k <= 0:
        return 0.0
    # Desplazamiento de la media en unidades de σ_xbar
    delta_xbar = delta_sigma * np.sqrt(n)
    # P(dentro de límites | desplazamiento)
    prob_dentro = sp_stats.norm.cdf(k - delta_xbar) - sp_stats.norm.cdf(-k - delta_xbar)
    potencia    = 1.0 - prob_dentro
    return float(np.clip(potencia, 0.0, 1.0))


def _ds_arl(potencia: float) -> float:
    """ARL = 1 / potencia (subgrupos esperados hasta la primera señal).

    Nota: cuando potencia → 0 el ARL tiende a infinito; se limita a 10 000
    para evitar desbordamientos numéricos en la UI.

    Args:
        potencia: probabilidad de señal en un subgrupo (0 < p ≤ 1).

    Returns:
        ARL ≥ 1.
    """
    if potencia <= 0.0:
        return 10_000.0
    return min(1.0 / potencia, 10_000.0)


def _ds_ats(arl: float, intervalo_h: float) -> float:
    """ATS = ARL × h  (tiempo esperado hasta la primera señal).

    Args:
        arl:         Average Run Length.
        intervalo_h: tiempo entre subgrupos consecutivos (horas).

    Returns:
        ATS en horas.
    """
    return arl * intervalo_h


def _ds_arl0_teorico(k: float = 3.0) -> float:
    """ARL₀ teórico bajo control (probabilidad de falsa alarma = 2·Φ(-k)).

    Args:
        k: multiplicador de límites.

    Returns:
        ARL₀ ≈ 370 para k=3.
    """
    alpha_fa = 2.0 * sp_stats.norm.cdf(-k)   # P(falsa alarma por subgrupo)
    return 1.0 / alpha_fa if alpha_fa > 0 else 10_000.0


def _ds_curva_potencia(n: int, k: float = 3.0,
                        deltas: np.ndarray | None = None) -> tuple[np.ndarray, np.ndarray]:
    """Genera la curva de potencia para un rango de desplazamientos.

    Args:
        n:      tamaño del subgrupo.
        k:      multiplicador de límites.
        deltas: vector de desplazamientos δ·σ (default 0..4 en 200 puntos).

    Returns:
        (deltas, potencias) — arrays numpy.
    """
    if deltas is None:
        deltas = np.linspace(0, 4, 200)
    potencias = np.array([_ds_potencia_xbar(d, n, k) for d in deltas])
    return deltas, potencias


def _ds_tabla_resumen(n: int, k: float, intervalo_h: float,
                       deltas_ref: list[float] | None = None) -> pd.DataFrame:
    """Tabla de potencia, ARL y ATS para desplazamientos de referencia.

    Args:
        n:            tamaño del subgrupo.
        k:            multiplicador de límites.
        intervalo_h:  intervalo entre subgrupos (horas).
        deltas_ref:   desplazamientos δ·σ a evaluar.

    Returns:
        DataFrame con columnas: δ·σ, Potencia, ARL, ATS (h), Señal esperada.
    """
    if deltas_ref is None:
        deltas_ref = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0]

    rows = []
    for d in deltas_ref:
        p   = _ds_potencia_xbar(d, n, k)
        arl = _ds_arl(p)
        ats = _ds_ats(arl, intervalo_h)

        if d == 0.0:
            senal = f"Falsa alarma (ARL₀ ≈ {arl:.0f})"
        elif arl <= 5:
            senal = "🔴 Detección casi inmediata"
        elif arl <= 20:
            senal = "🟡 Detección rápida"
        elif arl <= 100:
            senal = "🟠 Detección moderada"
        else:
            senal = "⚪ Detección lenta"

        rows.append({
            "δ·σ (desplazamiento)": f"{d:.1f}",
            "Potencia":             f"{p:.4f}",
            "ARL":                  f"{arl:.1f}",
            f"ATS ({intervalo_h:.1f} h)": f"{ats:.1f} h",
            "Evaluación":           senal,
        })
    return pd.DataFrame(rows)


def _ds_comparar_n(k: float = 3.0,
                   ns: list[int] | None = None,
                   deltas: np.ndarray | None = None
                   ) -> dict[int, np.ndarray]:
    """Curvas de potencia para distintos tamaños de subgrupo.

    Útil para comparar el efecto de aumentar n en la sensibilidad de la carta.

    Args:
        k:      multiplicador de límites.
        ns:     lista de tamaños de subgrupo.
        deltas: vector de desplazamientos.

    Returns:
        dict {n: array_de_potencias}.
    """
    if ns is None:
        ns = [2, 3, 4, 5, 7, 10]
    if deltas is None:
        deltas = np.linspace(0, 4, 200)
    return {n_i: np.array([_ds_potencia_xbar(d, n_i, k) for d in deltas]) for n_i in ns}


# ─────────────────────────────────────────────────────────────────────────────
# 8-B  Funciones de graficación
# ─────────────────────────────────────────────────────────────────────────────

def _ds_fig_curva_potencia(n: int, k: float, delta_actual: float) -> plt.Figure:
    """Curva de potencia con punto de operación resaltado.

    Incluye:
      - Curva de potencia principal.
      - Bandas de referencia (potencia 0.5 y 0.9).
      - Punto de operación (δ seleccionado por el usuario).
      - Zona sombreada de "alta detección" (potencia ≥ 0.9).
    """
    deltas, potencias = _ds_curva_potencia(n, k)

    fig, ax = plt.subplots(figsize=(9, 4.5))

    # Área de alta detección
    ax.fill_between(deltas, 0.9, 1.0, alpha=0.08, color=C_SUCCESS,
                    label="Zona alta detección (≥ 0.90)")
    ax.fill_between(deltas, 0.5, 0.9, alpha=0.06, color=C_ACCENT,
                    label="Zona detección moderada (0.50–0.90)")

    # Curva principal
    ax.plot(deltas, potencias, color=C_PRIMARY, linewidth=2.4, zorder=4,
            label=f"Potencia  (n={n}, k={k:.2f})")

    # Líneas de referencia horizontales
    for pref, col, lbl in [(0.50, C_ACCENT,  "50 %"),
                            (0.90, C_SUCCESS, "90 %")]:
        ax.axhline(pref, color=col, linewidth=1.2, linestyle="--", alpha=0.7,
                   label=f"Potencia = {lbl}")

    # Punto de operación
    p_op = _ds_potencia_xbar(delta_actual, n, k)
    ax.scatter([delta_actual], [p_op], color=C_DANGER, s=100, zorder=6,
               label=f"Punto operación: δ={delta_actual:.1f}σ → P={p_op:.3f}")
    ax.annotate(
        f"δ={delta_actual:.1f}σ\nP={p_op:.3f}",
        xy=(delta_actual, p_op),
        xytext=(delta_actual + 0.15, p_op - 0.12),
        fontsize=8, color=C_DANGER,
        arrowprops=dict(arrowstyle="->", color=C_DANGER, lw=1.2),
        bbox=dict(boxstyle="round,pad=0.3", facecolor="#0f1117",
                  edgecolor=C_DANGER, alpha=0.9),
    )

    ax.set_title(f"Curva de Potencia — Carta X̄  (n={n}, k={k:.2f})",
                 fontsize=11, fontweight="bold", pad=10)
    ax.set_xlabel("Desplazamiento de la media (δ·σ proceso)", fontsize=9)
    ax.set_ylabel("Potencia  P(señal | desplazamiento)", fontsize=9)
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 1.05)
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1, decimals=0))
    ax.legend(fontsize=8, loc="lower right",
              facecolor="#0f1117", edgecolor="#2a2d3e", ncol=2)
    ax.grid(True, alpha=0.4)
    fig.tight_layout()
    return fig


def _ds_fig_comparacion_n(k: float, delta_actual: float) -> plt.Figure:
    """Curvas de potencia comparativas para distintos n."""
    deltas    = np.linspace(0, 4, 200)
    ns        = [2, 3, 4, 5, 7, 10]
    colores_n = ["#94a3b8", "#60a5fa", "#34d399", "#f59e0b", "#f87171", "#c084fc"]

    fig, ax = plt.subplots(figsize=(9, 4.5))

    curvas = _ds_comparar_n(k=k, ns=ns, deltas=deltas)
    for n_i, col_i in zip(ns, colores_n):
        pots = curvas[n_i]
        ax.plot(deltas, pots, color=col_i, linewidth=1.8,
                label=f"n = {n_i}")
        # Punto de operación en cada curva
        p_op = _ds_potencia_xbar(delta_actual, n_i, k)
        ax.scatter([delta_actual], [p_op], color=col_i, s=45, zorder=5)

    ax.axhline(0.90, color=C_SUCCESS, linewidth=1.0, linestyle="--",
               alpha=0.6, label="Referencia 90%")
    ax.axvline(delta_actual, color=C_DANGER, linewidth=1.2, linestyle=":",
               alpha=0.7, label=f"δ = {delta_actual:.1f}σ")

    ax.set_title(f"Comparación de sensibilidad por tamaño de subgrupo (k={k:.2f})",
                 fontsize=11, fontweight="bold", pad=10)
    ax.set_xlabel("Desplazamiento de la media (δ·σ proceso)", fontsize=9)
    ax.set_ylabel("Potencia", fontsize=9)
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 1.05)
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1, decimals=0))
    ax.legend(fontsize=8, loc="lower right",
              facecolor="#0f1117", edgecolor="#2a2d3e", ncol=2)
    ax.grid(True, alpha=0.4)
    fig.tight_layout()
    return fig


def _ds_fig_arl_vs_delta(n: int, k: float, delta_actual: float) -> plt.Figure:
    """Curva ARL vs. desplazamiento en escala logarítmica."""
    deltas = np.linspace(0.01, 4, 300)
    arls   = np.array([_ds_arl(_ds_potencia_xbar(d, n, k)) for d in deltas])

    fig, ax = plt.subplots(figsize=(9, 4.2))

    ax.semilogy(deltas, arls, color=C_NORMAL, linewidth=2.3, zorder=4,
                label=f"ARL  (n={n}, k={k:.2f})")

    # Líneas de referencia
    for arl_ref, col_r, lbl_r in [
        (370,  C_SUCCESS, "ARL₀ ≈ 370 (bajo control)"),
        (50,   C_ACCENT,  "ARL = 50"),
        (10,   C_DANGER,  "ARL = 10  (detección rápida)"),
        (1,    "#f97316", "ARL = 1   (detección inmediata)"),
    ]:
        ax.axhline(arl_ref, color=col_r, linewidth=1.1, linestyle="--",
                   alpha=0.65, label=lbl_r)

    # Punto de operación
    p_op  = _ds_potencia_xbar(delta_actual, n, k)
    arl_op = _ds_arl(p_op)
    ax.scatter([delta_actual], [arl_op], color=C_DANGER, s=90, zorder=6,
               label=f"δ={delta_actual:.1f}σ → ARL={arl_op:.1f}")
    ax.annotate(
        f"ARL = {arl_op:.1f}",
        xy=(delta_actual, arl_op),
        xytext=(delta_actual + 0.2, arl_op * 2.5),
        fontsize=8, color=C_DANGER,
        arrowprops=dict(arrowstyle="->", color=C_DANGER, lw=1.1),
        bbox=dict(boxstyle="round,pad=0.3", facecolor="#0f1117",
                  edgecolor=C_DANGER, alpha=0.9),
    )

    ax.set_title(f"ARL vs. Desplazamiento — Carta X̄  (n={n}, k={k:.2f})",
                 fontsize=11, fontweight="bold", pad=10)
    ax.set_xlabel("Desplazamiento de la media (δ·σ proceso)", fontsize=9)
    ax.set_ylabel("ARL (escala log)", fontsize=9)
    ax.set_xlim(0.01, 4)
    ax.legend(fontsize=8, loc="upper right",
              facecolor="#0f1117", edgecolor="#2a2d3e", ncol=2)
    ax.grid(True, which="both", alpha=0.35)
    fig.tight_layout()
    return fig


def _ds_fig_ats_heatmap(k: float, intervalo_h: float) -> plt.Figure:
    """Heatmap ATS (h) en función de n y δ — mapa de calor industrial."""
    ns     = [2, 3, 4, 5, 6, 7, 8, 10]
    deltas = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]

    matriz = np.zeros((len(ns), len(deltas)))
    for i, n_i in enumerate(ns):
        for j, d_j in enumerate(deltas):
            p    = _ds_potencia_xbar(d_j, n_i, k)
            arl  = _ds_arl(p)
            ats  = _ds_ats(arl, intervalo_h)
            matriz[i, j] = min(ats, 500.0)   # truncar para legibilidad

    fig, ax = plt.subplots(figsize=(9, 4.2))
    im = ax.imshow(matriz, cmap="RdYlGn_r", aspect="auto",
                   vmin=0, vmax=min(500, matriz.max()))

    ax.set_xticks(range(len(deltas)))
    ax.set_xticklabels([f"{d:.1f}σ" for d in deltas], fontsize=8.5)
    ax.set_yticks(range(len(ns)))
    ax.set_yticklabels([f"n={n_i}" for n_i in ns], fontsize=8.5)

    # Anotaciones de valor en cada celda
    for i in range(len(ns)):
        for j in range(len(deltas)):
            val = matriz[i, j]
            txt_col = "white" if val > matriz.max() * 0.55 else "#0f1117"
            ax.text(j, i, f"{val:.1f}h",
                    ha="center", va="center", fontsize=7.5,
                    fontweight="bold", color=txt_col)

    plt.colorbar(im, ax=ax, label="ATS (horas)", shrink=0.85)
    ax.set_title(
        f"Mapa de ATS (h) — intervalo entre subgrupos = {intervalo_h:.1f} h  |  k = {k:.2f}",
        fontsize=10, fontweight="bold", pad=10,
    )
    ax.set_xlabel("Desplazamiento δ·σ", fontsize=9)
    ax.set_ylabel("Tamaño de subgrupo n", fontsize=9)
    fig.tight_layout()
    return fig


def _ds_fig_kpis_proceso(f1: dict, cap: dict) -> plt.Figure:
    """Gráfico de gauge-estilo para los KPIs de desempeño del proceso."""
    indicadores = []

    # Cp / Cpk desde módulo de capacidad
    for lbl, val, umbral_ok, umbral_warn in [
        ("Cpk",  cap.get("cpk"),  1.33, 1.00),
        ("Cp",   cap.get("cp"),   1.33, 1.00),
        ("Pp",   cap.get("pp"),   1.33, 1.00),
        ("Ppk",  cap.get("ppk"),  1.33, 1.00),
    ]:
        if val is not None:
            indicadores.append((lbl, float(val), umbral_ok, umbral_warn, 2.0))

    if not indicadores:
        fig, ax = plt.subplots(figsize=(8, 2))
        ax.text(0.5, 0.5, "Ejecute primero el módulo de Capacidad del proceso",
                ha="center", va="center", color=C_MUTED, fontsize=11,
                transform=ax.transAxes)
        ax.axis("off")
        fig.tight_layout()
        return fig

    n_ind = len(indicadores)
    fig, axes = plt.subplots(1, n_ind, figsize=(n_ind * 2.5, 3.0))
    if n_ind == 1:
        axes = [axes]

    for ax_i, (lbl, val, umb_ok, umb_warn, max_v) in zip(axes, indicadores):
        # Barra horizontal tipo gauge
        color_bar = C_SUCCESS if val >= umb_ok else (C_ACCENT if val >= umb_warn else C_DANGER)
        ax_i.barh([0], [min(val, max_v)], color=color_bar, alpha=0.85, height=0.5)
        ax_i.barh([0], [max_v], color="#2a2d3e", alpha=0.4, height=0.5)

        # Marcadores de umbral
        for umb, col_u in [(umb_ok, C_SUCCESS), (umb_warn, C_ACCENT)]:
            ax_i.axvline(umb, color=col_u, linewidth=1.5, linestyle="--", alpha=0.8)

        ax_i.set_xlim(0, max_v)
        ax_i.set_ylim(-0.5, 0.5)
        ax_i.set_yticks([])
        ax_i.set_title(lbl, fontsize=10, fontweight="bold", color=C_TEXT if True else C_MUTED)
        ax_i.set_xlabel(f"{val:.3f}", fontsize=11, fontweight="bold", color=color_bar)
        ax_i.tick_params(labelsize=7.5)
        ax_i.grid(True, axis="x", alpha=0.3)

    fig.suptitle("Índices de Capacidad del Proceso", fontsize=10.5,
                 fontweight="bold", y=1.02)
    fig.tight_layout()
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# 8-C  Panel de interpretación y recomendaciones
# ─────────────────────────────────────────────────────────────────────────────

def _ds_nivel_potencia(p: float) -> tuple[str, str, str]:
    """(etiqueta, color, ícono) según nivel de potencia."""
    if p >= 0.90:
        return "Alta sensibilidad",    C_SUCCESS, "✅"
    if p >= 0.70:
        return "Sensibilidad media",   C_ACCENT,  "⚠️"
    if p >= 0.50:
        return "Sensibilidad baja",    C_ACCENT,  "⚠️"
    return "Sensibilidad muy baja",    C_DANGER,  "❌"


def _ds_nivel_arl(arl: float, arl0: float) -> tuple[str, str, str]:
    """(etiqueta, color, ícono) según el ARL₁ relativo al ARL₀."""
    if arl <= 5:
        return "Detección casi inmediata", C_SUCCESS, "🔴"
    if arl <= 20:
        return "Detección rápida",         C_SUCCESS, "🟡"
    if arl <= arl0 * 0.10:
        return "Detección moderada",       C_ACCENT,  "🟠"
    if arl <= arl0 * 0.50:
        return "Detección lenta",          C_DANGER,  "⚪"
    return "Sin sensibilidad práctica",    C_DANGER,  "⬜"


def _ds_panel_interpretacion(p: float, arl: float, ats_h: float,
                              arl0: float, n: int, k: float,
                              delta: float, intervalo_h: float) -> None:
    """Renderiza veredicto + mensaje industrial + recomendaciones."""
    lbl_p, col_p, ico_p   = _ds_nivel_potencia(p)
    lbl_a, col_a, ico_a   = _ds_nivel_arl(arl, arl0)
    fa_pct                 = (1.0 / arl0) * 100

    # ── Veredicto principal ───────────────────────────────────────────────────
    if p >= 0.90 and arl <= 20:
        estado   = "SISTEMA DE MONITOREO ALTAMENTE SENSIBLE"
        color_e  = C_SUCCESS
        icono_e  = "✅"
        msg_e    = (
            f"El sistema detecta rápidamente cambios de {delta:.1f}σ en la media. "
            f"Con potencia = {p:.1%} y ARL₁ = {arl:.1f}, se espera una señal en promedio "
            f"cada {arl:.1f} subgrupos ({ats_h:.1f} horas con el intervalo actual). "
            "La probabilidad de falsa alarma es controlada."
        )
    elif p >= 0.70:
        estado   = "SENSIBILIDAD ACEPTABLE — MEJORA POSIBLE"
        color_e  = C_ACCENT
        icono_e  = "⚠️"
        msg_e    = (
            f"El sistema detecta cambios de {delta:.1f}σ con potencia {p:.1%}. "
            f"El ARL₁ = {arl:.1f} subgrupos ({ats_h:.1f} h) indica que pueden producirse "
            f"{arl:.0f} lotes con defectos antes de la primera señal. "
            "Considere aumentar el tamaño de subgrupo para mejorar la sensibilidad."
        )
    elif p >= 0.50:
        estado   = "BAJA SENSIBILIDAD — ACCIÓN RECOMENDADA"
        color_e  = C_DANGER
        icono_e  = "❌"
        msg_e    = (
            f"El monitoreo puede reaccionar lentamente ante desplazamientos de {delta:.1f}σ. "
            f"Potencia = {p:.1%} y ARL₁ = {arl:.1f} subgrupos ({ats_h:.1f} h). "
            "La producción de artículos defectuosos puede prolongarse significativamente "
            "antes de generar una señal. Se requiere revisión del plan de control."
        )
    else:
        estado   = "SISTEMA SIN SENSIBILIDAD PRÁCTICA"
        color_e  = C_DANGER
        icono_e  = "🔴"
        msg_e    = (
            f"El sistema presenta riesgo alto: potencia = {p:.1%} para un desplazamiento de {delta:.1f}σ. "
            f"Se esperan en promedio {arl:.0f} subgrupos ({ats_h:.1f} h) antes de detectar el cambio. "
            "El proceso puede generar una gran cantidad de productos defectuosos sin activar alarmas. "
            "Se recomienda rediseñar el plan de control urgentemente."
        )

    st.markdown(
        f"""
        <div style="background:#0f1117;border:2px solid {color_e};border-radius:12px;
                    padding:22px 26px;margin:14px 0">
            <div style="font-size:1.15rem;font-weight:700;color:{color_e};margin-bottom:10px">
                {icono_e} &nbsp; {estado}
            </div>
            <p style="font-size:.88rem;color:#e2e8f0;margin:0 0 16px">{msg_e}</p>
            <div style="display:flex;gap:28px;flex-wrap:wrap">
                <div>
                    <div style="font-size:.63rem;color:#64748b;letter-spacing:.1em;
                                text-transform:uppercase">Potencia</div>
                    <div style="font-family:monospace;font-size:1.4rem;
                                font-weight:700;color:{col_p}">{ico_p} {p:.1%}</div>
                </div>
                <div>
                    <div style="font-size:.63rem;color:#64748b;letter-spacing:.1em;
                                text-transform:uppercase">ARL₁</div>
                    <div style="font-family:monospace;font-size:1.4rem;
                                font-weight:700;color:{col_a}">{arl:.1f} sg.</div>
                </div>
                <div>
                    <div style="font-size:.63rem;color:#64748b;letter-spacing:.1em;
                                text-transform:uppercase">ATS</div>
                    <div style="font-family:monospace;font-size:1.4rem;
                                font-weight:700;color:{col_a}">{ats_h:.1f} h</div>
                </div>
                <div>
                    <div style="font-size:.63rem;color:#64748b;letter-spacing:.1em;
                                text-transform:uppercase">ARL₀ (falsa alarma)</div>
                    <div style="font-family:monospace;font-size:1.4rem;
                                font-weight:700;color:{C_MUTED}">{arl0:.0f} sg.</div>
                </div>
                <div>
                    <div style="font-size:.63rem;color:#64748b;letter-spacing:.1em;
                                text-transform:uppercase">P(FA) por sg.</div>
                    <div style="font-family:monospace;font-size:1.4rem;
                                font-weight:700;color:{C_MUTED}">{fa_pct:.3f}%</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Mensaje industrial de vinculación ─────────────────────────────────────
    prod_defect_arl = arl  # unidades defectuosas si n=1 por sg; contextual
    st.markdown(
        f"""
        <div style="background:rgba(59,130,246,.08);border:1px solid rgba(59,130,246,.3);
                    border-radius:10px;padding:15px 20px;margin:10px 0">
            <div style="font-size:.8rem;color:{C_PRIMARY};font-weight:700;
                        letter-spacing:.08em;text-transform:uppercase;margin-bottom:6px">
                🏭 Impacto operativo
            </div>
            <p style="font-size:.88rem;color:#e2e8f0;margin:0">
                Una detección rápida reduce directamente la producción de artículos defectuosos
                y disminuye los costos de no calidad (scrap, reproceso, devoluciones).
                Con el plan actual se espera detectar un desplazamiento de
                <strong style="color:{C_ACCENT}">{delta:.1f}σ</strong> en
                <strong style="color:{col_a}">{arl:.1f} subgrupos</strong>
                ({ats_h:.1f} h), durante los cuales podrían producirse lotes fuera
                de especificación. Reducir el ARL₁ mediante mayor <em>n</em> o
                reglas complementarias de Western Electric mejora la rentabilidad del proceso.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Recomendaciones automáticas priorizadas ────────────────────────────────
    recom = []
    if p < 0.90:
        mejora_n = None
        for n_p in [n + 1, n + 2, n + 3, n + 5]:
            if _ds_potencia_xbar(delta, n_p, k) >= 0.90:
                mejora_n = n_p
                break
        if mejora_n:
            recom.append((C_PRIMARY, "📈",
                f"Aumentar el tamaño de subgrupo a n={mejora_n} elevaría la potencia por "
                f"encima del 90% para δ={delta:.1f}σ."))
        else:
            recom.append((C_PRIMARY, "📈",
                "Aumentar progresivamente el tamaño de subgrupo para mejorar la sensibilidad."))

    if intervalo_h > 2.0 and ats_h > 8.0:
        recom.append((C_ACCENT, "⏱️",
            f"El ATS = {ats_h:.1f} h indica que pueden pasar varias horas antes de detectar "
            "el cambio. Considere aumentar la frecuencia de muestreo."))

    if k > 3.0:
        recom.append((C_ACCENT, "🎯",
            f"Los límites de control están en ±{k:.2f}σ, lo que reduce la potencia. "
            "Evalúe usar k=3.00 como estándar AIAG/ISO."))

    if arl0 < 200:
        recom.append((C_DANGER, "⚠️",
            f"ARL₀ = {arl0:.0f}: el sistema generará falsas alarmas con frecuencia elevada "
            f"({fa_pct:.2f}% por subgrupo). Verifique que k sea ≥ 3."))

    recom.append((C_SUCCESS, "📋",
        "Combine la carta X̄ con reglas de Western Electric para detectar tendencias "
        "y patrones sin reducir drásticamente el ARL₀."))

    recom.append((C_SUCCESS, "🔬",
        "Reduzca la variabilidad del proceso (σ) mediante mejoras en materia prima "
        "y condiciones de mezcla para que desplazamientos pequeños sean más significativos."))

    st.markdown("#### 🔧 Recomendaciones del sistema")
    for col_r, ico_r, txt_r in recom:
        st.markdown(
            f"""
            <div style="display:flex;gap:12px;align-items:flex-start;padding:10px 15px;
                        background:#1a1d27;border-radius:8px;
                        border-left:3px solid {col_r};margin-bottom:7px">
                <span style="font-size:1.1rem;flex-shrink:0">{ico_r}</span>
                <span style="font-size:.86rem;color:#e2e8f0">{txt_r}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ─────────────────────────────────────────────────────────────────────────────
# 8-D  Función principal seccion_desempeno
# ─────────────────────────────────────────────────────────────────────────────

# Constante de color texto (no definida globalmente en el archivo original)
C_TEXT = "#e2e8f0"

def seccion_desempeno():
    """Módulo completo de Desempeño del Sistema CEP.

    Flujo interno:
    1.  Parámetros del plan de control (n, k, intervalo, δ).
    2.  Cálculo de Potencia, ARL₀, ARL₁ y ATS.
    3.  Dashboard de métricas clave.
    4.  Curva de potencia con punto de operación.
    5.  Curvas comparativas para distintos n.
    6.  Curva ARL vs. desplazamiento (log).
    7.  Heatmap ATS(n, δ).
    8.  Tabla resumen exportable.
    9.  KPIs de capacidad vinculados (si existen).
    10. Panel de interpretación y recomendaciones.
    11. Tab GR&R (estructura conservada).
    """
    encabezado(
        "🏭", "Desempeño del sistema de monitoreo",
        "Potencia · ARL · ATS · Curvas OC · KPIs del proceso · Sistema de medición",
    )

    f1  = st.session_state.get("fase1", {})
    cap = st.session_state.get("capacidad", {})
    cfg = st.session_state.config_proceso

    # ══════════════════════════════════════════════════════════════════════════
    # TABS PRINCIPALES
    # ══════════════════════════════════════════════════════════════════════════
    tab_pot, tab_grr, tab_kpi = st.tabs([
        "📈 Potencia · ARL · ATS",
        "📏 Sistema de medición (GR&R)",
        "📊 KPIs del proceso",
    ])

    # ──────────────────────────────────────────────────────────────────────────
    # TAB 1 – Potencia / ARL / ATS
    # ──────────────────────────────────────────────────────────────────────────
    with tab_pot:

        st.markdown("### ⚙️ Parámetros del plan de control")
        caja(
            "Configure los parámetros del sistema de monitoreo. Si Fase 1 está ejecutada, "
            "los valores de n y σ se tomarán automáticamente del estado de la aplicación.",
            tipo="info",
        )

        # ── Fuente de parámetros ──────────────────────────────────────────────
        f1_ok       = f1.get("calculado", False)
        n_f1        = int(cfg.get("tamano_subgrupo", 5))
        sigma_f1    = f1.get("sigma_est")
        tipo_carta  = f1.get("tipo_carta", "X-R")

        if f1_ok and sigma_f1:
            caja(
                f"Fase 1 detectada → n = {n_f1} · σ estimado = {sigma_f1:.4f} · "
                f"Carta: {tipo_carta}. Puede ajustar los parámetros manualmente.",
                tipo="success",
            )

        pa1, pa2, pa3, pa4 = st.columns(4)
        with pa1:
            n_plan = st.number_input(
                "Tamaño de subgrupo (n)",
                min_value=2, max_value=25, value=n_f1, step=1,
                key="ds_n",
                help="Número de unidades medidas por subgrupo racional.",
            )
        with pa2:
            k_plan = st.number_input(
                "Multiplicador de límites (k)",
                min_value=2.0, max_value=4.0, value=3.0, step=0.1,
                format="%.2f", key="ds_k",
                help="Ancho de los límites en múltiplos de σ_xbar. Estándar: k=3.",
            )
        with pa3:
            delta_plan = st.number_input(
                "Desplazamiento a detectar (δ·σ)",
                min_value=0.1, max_value=4.0, value=1.0, step=0.1,
                format="%.1f", key="ds_delta",
                help="Cambio de la media a detectar, expresado en múltiplos de σ proceso.",
            )
        with pa4:
            intervalo_h = st.number_input(
                "Intervalo entre subgrupos (h)",
                min_value=0.08, max_value=24.0, value=1.0, step=0.25,
                format="%.2f", key="ds_h",
                help="Tiempo entre subgrupos consecutivos. Determina el ATS.",
            )

        sep()

        # ── Cálculos principales ──────────────────────────────────────────────
        potencia  = _ds_potencia_xbar(delta_plan, n_plan, k_plan)
        arl0      = _ds_arl0_teorico(k_plan)
        arl1      = _ds_arl(potencia)
        ats_h_val = _ds_ats(arl1, intervalo_h)
        fa_pct    = (1.0 / arl0) * 100

        # ── Dashboard de métricas ─────────────────────────────────────────────
        st.markdown("### 📊 Indicadores de desempeño")

        lbl_p, col_p, ico_p = _ds_nivel_potencia(potencia)
        lbl_a, col_a, ico_a = _ds_nivel_arl(arl1, arl0)

        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Potencia",        f"{potencia:.1%}",
                  delta=lbl_p,
                  delta_color="normal" if potencia >= 0.90 else "inverse",
                  help="P(señal | desplazamiento δ·σ)")
        m2.metric("ARL₁",            f"{arl1:.1f} sg.",
                  delta=lbl_a,
                  delta_color="normal" if arl1 <= 20 else "inverse",
                  help="Subgrupos esperados hasta la primera señal.")
        m3.metric("ATS",             f"{ats_h_val:.1f} h",
                  help="Tiempo esperado hasta la primera señal.")
        m4.metric("ARL₀ (H₀)",      f"{arl0:.0f} sg.",
                  help="Subgrupos esperados sin desplazamiento (bajo control).")
        m5.metric("P(FA) / sg.",    f"{fa_pct:.3f}%",
                  help="Probabilidad de falsa alarma por subgrupo.")

        # Tarjetas de estado adicionales con estilo HTML
        tc1, tc2, tc3 = st.columns(3)
        for col_ui, lbl_t, val_t, nota_t, col_t in [
            (tc1, "n analizado",     str(n_plan),
             f"Subgrupo tamaño {n_plan}", C_PRIMARY),
            (tc2, "k (límites)",     f"{k_plan:.2f}",
             "Ancho de límites control", C_PRIMARY),
            (tc3, "δ objetivo",      f"{delta_plan:.1f}σ",
             "Desplazamiento a detectar", C_ACCENT),
        ]:
            col_ui.markdown(
                f"""<div class="m-card" style="border-color:{col_t}33">
                    <div class="m-lbl">{lbl_t}</div>
                    <div class="m-val" style="color:{col_t}">{val_t}</div>
                    <div class="m-note">{nota_t}</div>
                </div>""",
                unsafe_allow_html=True,
            )

        sep()

        # ── Gráficos ──────────────────────────────────────────────────────────
        st.markdown("### 📈 Curvas de desempeño")

        # Fila 1: curva potencia + ARL log
        g1, g2 = st.columns(2)
        with g1:
            st.markdown("#### Curva de Potencia")
            fig_pot = _ds_fig_curva_potencia(n_plan, k_plan, delta_plan)
            st.pyplot(fig_pot, use_container_width=True)
            plt.close(fig_pot)

        with g2:
            st.markdown("#### Curva ARL (escala logarítmica)")
            fig_arl = _ds_fig_arl_vs_delta(n_plan, k_plan, delta_plan)
            st.pyplot(fig_arl, use_container_width=True)
            plt.close(fig_arl)

        sep()

        # Fila 2: comparación n + heatmap ATS
        g3, g4 = st.columns(2)
        with g3:
            st.markdown("#### Sensibilidad por tamaño de subgrupo")
            fig_comp = _ds_fig_comparacion_n(k_plan, delta_plan)
            st.pyplot(fig_comp, use_container_width=True)
            plt.close(fig_comp)

        with g4:
            st.markdown("#### Mapa de ATS (h) — n vs. δ")
            fig_heat = _ds_fig_ats_heatmap(k_plan, intervalo_h)
            st.pyplot(fig_heat, use_container_width=True)
            plt.close(fig_heat)

        sep()

        # ── Tabla resumen ─────────────────────────────────────────────────────
        st.markdown("### 📋 Tabla resumen — Potencia · ARL · ATS")
        caja(
            "La tabla muestra el desempeño del sistema para desplazamientos de referencia "
            "con los parámetros configurados (n, k, intervalo).",
            tipo="info",
        )
        df_tabla = _ds_tabla_resumen(n_plan, k_plan, intervalo_h)
        st.dataframe(df_tabla, use_container_width=True, hide_index=True)

        csv_ds = df_tabla.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Descargar tabla CSV",
            data=csv_ds,
            file_name="desempeno_sistema_cep.csv",
            mime="text/csv",
        )

        sep()

        # ── Panel de interpretación y recomendaciones ─────────────────────────
        st.markdown("### 🧠 Interpretación automática del sistema")
        _ds_panel_interpretacion(
            potencia, arl1, ats_h_val, arl0,
            n_plan, k_plan, delta_plan, intervalo_h,
        )

    # ──────────────────────────────────────────────────────────────────────────
    # TAB 2 – GR&R (estructura conservada, pendiente de lógica ANOVA)
    # ──────────────────────────────────────────────────────────────────────────
    with tab_grr:
        st.markdown("### 📏 Estudio de Repetibilidad y Reproducibilidad")
        caja(
            "El GR&R cuantifica la variación debida al sistema de medición. "
            "Se recomienda %GR&R < 10% para un sistema aceptable; "
            "entre 10–30% es marginal; > 30% es inaceptable.",
            tipo="info",
        )

        gc1, gc2, gc3 = st.columns(3)
        with gc1: st.number_input("N° operadores",      value=2,  min_value=1,  key="grr_ops")
        with gc2: st.number_input("N° partes",          value=10, min_value=5,  key="grr_par")
        with gc3: st.number_input("Réplicas por parte", value=2,  min_value=2,  key="grr_rep")

        if st.button("Calcular GR&R", type="primary"):
            caja("El cálculo detallado de GR&R (ANOVA) se implementará en la siguiente versión.",
                 tipo="warning")

        sep()
        proximamente(
            "Resultados GR&R",
            "Tabla ANOVA, %GR&R, %Repetibilidad, %Reproducibilidad y gráficos de varianza.",
        )

    # ──────────────────────────────────────────────────────────────────────────
    # TAB 3 – KPIs globales del proceso
    # ──────────────────────────────────────────────────────────────────────────
    with tab_kpi:
        st.markdown("### 📊 KPIs globales del proceso")

        datos_ok = st.session_state.get("datos_cargados", False)
        df_sg    = st.session_state.get("df_subgrupos")

        # ── Calcular FPY y DPU si hay datos ───────────────────────────────────
        if datos_ok and df_sg is not None:
            cfg_proc = st.session_state.config_proceso
            lsl_r    = cfg_proc.get("lsl_res", 130.0)
            usl_r    = cfg_proc.get("usl_res", 160.0)
            n_total  = len(df_sg)
            n_nc     = int(((df_sg["resistencia"] < lsl_r) |
                            (df_sg["resistencia"] > usl_r)).sum())
            n_conf   = n_total - n_nc
            fpy_val  = n_conf / n_total if n_total > 0 else 0.0
            dpu_val  = n_nc   / n_total if n_total > 0 else 0.0

            k1, k2, k3, k4 = st.columns(4)
            k1.metric("FPY — Primera pasada",
                      f"{fpy_val:.1%}",
                      delta="✅ Bueno" if fpy_val >= 0.97 else ("⚠️ Atención" if fpy_val >= 0.90 else "❌ Crítico"),
                      delta_color="normal" if fpy_val >= 0.97 else "inverse")
            k2.metric("DPU — Defectos/unidad",
                      f"{dpu_val:.4f}",
                      delta="✅ < 1%" if dpu_val < 0.01 else "⚠️ Elevado",
                      delta_color="normal" if dpu_val < 0.01 else "inverse")
            k3.metric("Total observaciones", f"{n_total:,}")
            k4.metric("No conformes",        f"{n_nc:,}")

            # Vinculación con capacidad
            if cap.get("cpk"):
                sep()
                st.markdown("#### 🔗 Vinculación CEP → Capacidad → KPIs")
                caja(
                    f"Cpk = **{cap['cpk']:.3f}** · FPY = **{fpy_val:.1%}** · "
                    f"DPU = **{dpu_val:.4f}**. "
                    "Un Cpk elevado se corresponde con FPY alto y DPU bajo, "
                    "confirmando la coherencia del sistema de monitoreo.",
                    tipo="success" if cap["cpk"] >= 1.33 else "warning",
                )
        else:
            caja(
                "Cargue datos en **📥 Ingreso de datos** para calcular FPY y DPU automáticamente.",
                tipo="warning",
            )
            k1, k2, k3 = st.columns(3)
            with k1: tarjeta("FPY – Rendimiento primera pasada", "—", "Unidades conformes / total")
            with k2: tarjeta("DPU – Defectos por unidad",        "—", "Defectos / total unidades")
            with k3: tarjeta("OEE – Efectividad global equipo",  "—", "Disp. × Rend. × Calidad")

        sep()

        # ── Índices de capacidad como KPIs ────────────────────────────────────
        st.markdown("#### 🎯 Índices de capacidad del proceso")
        if cap.get("cpk"):
            fig_kpi = _ds_fig_kpis_proceso(f1, cap)
            st.pyplot(fig_kpi, use_container_width=True)
            plt.close(fig_kpi)
        else:
            caja(
                "Ejecute el módulo **⚙️ Capacidad del proceso** para visualizar "
                "los índices Cp, Cpk, Pp, Ppk aquí.",
                tipo="info",
            )

        sep()
        proximamente(
            "Tendencia histórica de KPIs",
            "Gráfico de FPY, DPU y OEE por período de producción.",
        )


# ─────────────────────────────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 9 – Muestreo por aceptación
# Incluye: Evaluación de lotes, Curva OC, Diseño automático de planes,
#          Análisis de riesgos α/β, Historial de lotes, Recomendaciones
# ══════════════════════════════════════════════════════════════════════════════

# ─────────────────────────────────────────────────────────────────────────────
# 9-A  Funciones estadísticas de muestreo de aceptación
# ─────────────────────────────────────────────────────────────────────────────

def _ms_prob_aceptacion_binomial(n: int, c: int, p: float) -> float:
    """Probabilidad de aceptación usando distribución binomial.

    P(X ≤ c | n, p) = Σ C(n,x) · p^x · (1-p)^(n-x),  x = 0..c

    La distribución binomial asume muestreo con reposición o N muy grande
    (N/n > 10). Es la más usada en muestreo de aceptación estándar (ISO 2859).

    Args:
        n: tamaño de muestra.
        c: número de aceptación (máx. defectuosos permitidos).
        p: fracción defectiva real del lote (0 ≤ p ≤ 1).

    Returns:
        Probabilidad de aceptación P_a ∈ [0, 1].
    """
    if n <= 0 or c < 0 or not (0.0 <= p <= 1.0):
        return 0.0
    return float(sp_stats.binom.cdf(c, n, p))


def _ms_prob_aceptacion_hipergeometrica(N: int, n: int, c: int, p: float) -> float:
    """Probabilidad de aceptación usando distribución hipergeométrica.

    Más precisa cuando N/n ≤ 10 (lotes pequeños). La hipergeométrica modela
    el muestreo sin reposición exactamente.

    P(X ≤ c) = Σ C(D, x)·C(N-D, n-x) / C(N, n),  x = 0..min(c, D)
    donde D = round(p·N) es el número de defectuosos en el lote.

    Args:
        N: tamaño del lote.
        n: tamaño de muestra.
        c: número de aceptación.
        p: fracción defectiva real.

    Returns:
        Probabilidad de aceptación P_a ∈ [0, 1].
    """
    if N <= 0 or n <= 0 or c < 0 or not (0.0 <= p <= 1.0):
        return 0.0
    D = round(p * N)            # defectuosos en el lote
    D = max(0, min(D, N))
    # sp_stats.hypergeom(M, n, N) → M=población, n=éxitos en pob., N=muestra
    return float(sp_stats.hypergeom.cdf(c, N, D, n))


def _ms_elegir_distribucion(N: int, n: int) -> str:
    """Selecciona la distribución más adecuada según la razón N/n.

    Regla estándar (ISO 2859-1 commentary):
    - N/n > 10 → binomial suficientemente precisa.
    - N/n ≤ 10 → hipergeométrica recomendada.

    Returns:
        'binomial' | 'hipergeometrica'
    """
    return "hipergeometrica" if (N > 0 and n > 0 and N / n <= 10) else "binomial"


def _ms_calcular_pa(N: int, n: int, c: int, p: float) -> float:
    """Wrapper que elige automáticamente la distribución correcta."""
    dist = _ms_elegir_distribucion(N, n)
    if dist == "hipergeometrica":
        return _ms_prob_aceptacion_hipergeometrica(N, n, c, p)
    return _ms_prob_aceptacion_binomial(n, c, p)


def _ms_curva_oc(N: int, n: int, c: int,
                 n_puntos: int = 300) -> tuple[np.ndarray, np.ndarray]:
    """Genera la Curva Característica de Operación (OC / CCA).

    Args:
        N:        tamaño de lote.
        n:        tamaño de muestra.
        c:        número de aceptación.
        n_puntos: resolución de la curva.

    Returns:
        (ps, pas) — fracción defectiva y probabilidad de aceptación.
    """
    ps  = np.linspace(0.0, 0.5, n_puntos)
    pas = np.array([_ms_calcular_pa(N, n, c, float(p)) for p in ps])
    return ps, pas


def _ms_riesgo_productor(N: int, n: int, c: int, nca: float) -> float:
    """α = 1 - P(aceptar | NCA)  — riesgo del productor.

    El riesgo del productor es la probabilidad de rechazar un lote con
    calidad aceptable (NCA). Idealmente α ≤ 0.05.
    """
    pa_nca = _ms_calcular_pa(N, n, c, nca)
    return round(1.0 - pa_nca, 6)


def _ms_riesgo_consumidor(N: int, n: int, c: int, nrl: float) -> float:
    """β = P(aceptar | NRL)  — riesgo del consumidor.

    El riesgo del consumidor es la probabilidad de aceptar un lote con
    calidad rechazable (NRL). Idealmente β ≤ 0.10.
    """
    return round(_ms_calcular_pa(N, n, c, nrl), 6)


def _ms_disenar_plan(N: int, nca: float, nrl: float,
                      alpha: float, beta: float,
                      n_max: int = 500) -> list[dict]:
    """Diseño automático del plan de muestreo simple (n, c).

    Búsqueda sistemática de todos los pares (n, c) que satisfacen:
      1. P(aceptar | NCA) ≥ 1 - α        (protección al productor)
      2. P(aceptar | NRL) ≤ β            (protección al consumidor)

    El algoritmo itera n desde 5 hasta min(N, n_max) y c desde 0 hasta
    n//2, evaluando ambas condiciones con la distribución elegida.
    Retorna los planes válidos ordenados por n ascendente (menos inspección).

    Args:
        N:     tamaño del lote.
        nca:   NCA en fracción (ej. 0.01 para 1%).
        nrl:   NRL en fracción (ej. 0.05 para 5%).
        alpha: riesgo del productor (ej. 0.05).
        beta:  riesgo del consumidor (ej. 0.10).
        n_max: límite superior de búsqueda de n.

    Returns:
        Lista de dicts con los planes válidos, ordenada por n.
    """
    planes = []
    n_limite = min(N, n_max)

    for n_i in range(5, n_limite + 1):
        for c_i in range(0, n_i // 2 + 1):
            pa_nca = _ms_calcular_pa(N, n_i, c_i, nca)
            pa_nrl = _ms_calcular_pa(N, n_i, c_i, nrl)

            cumple_alpha = pa_nca >= (1.0 - alpha)   # Condición 1
            cumple_beta  = pa_nrl <= beta             # Condición 2

            if cumple_alpha and cumple_beta:
                alpha_real = round(1.0 - pa_nca, 5)
                beta_real  = round(pa_nrl, 5)
                planes.append({
                    "n":          n_i,
                    "c":          c_i,
                    "Pa(NCA)":    round(pa_nca, 5),
                    "Pa(NRL)":    round(pa_nrl, 5),
                    "α real":     alpha_real,
                    "β real":     beta_real,
                    "Cumple α":   "✅" if cumple_alpha else "❌",
                    "Cumple β":   "✅" if cumple_beta  else "❌",
                })
                break   # Para cada n, tomar solo el menor c que cumple

    return sorted(planes, key=lambda x: (x["n"], x["c"]))


def _ms_indices_calidad_lote(N: int, n: int, c: int,
                              defectuosos: int) -> dict:
    """Calcula métricas de calidad del lote inspeccionado.

    Args:
        N:           tamaño del lote.
        n:           tamaño de muestra.
        c:           número de aceptación.
        defectuosos: defectuosos encontrados en la muestra.

    Returns:
        dict con decision, p_obs, p_estimada_lote, cobertura.
    """
    aceptado    = defectuosos <= c
    p_obs       = defectuosos / n if n > 0 else 0.0
    # Estimación del % defectuoso en el lote completo (máxima verosimilitud)
    p_lote_est  = p_obs
    # Intervalo de Wilson para proporción (más robusto que Wald)
    z_95  = sp_stats.norm.ppf(0.975)
    denom = 1.0 + z_95**2 / n
    phat  = (p_obs + z_95**2 / (2 * n)) / denom
    margen = z_95 * np.sqrt(p_obs * (1 - p_obs) / n + z_95**2 / (4 * n**2)) / denom
    ic_lo = max(0.0, phat - margen)
    ic_hi = min(1.0, phat + margen)

    # Defectuosos estimados en el lote completo
    n_def_lote_est = round(p_lote_est * N)

    return {
        "aceptado":         aceptado,
        "p_obs":            round(p_obs, 6),
        "p_lote_est":       round(p_lote_est, 6),
        "ic_lo":            round(ic_lo, 6),
        "ic_hi":            round(ic_hi, 6),
        "n_def_lote_est":   n_def_lote_est,
        "cobertura_pct":    round((1 - defectuosos / max(n, 1)) * 100, 2),
    }


# ─────────────────────────────────────────────────────────────────────────────
# 9-B  Funciones de graficación
# ─────────────────────────────────────────────────────────────────────────────

def _ms_fig_curva_oc(N: int, n: int, c: int,
                      nca: float, nrl: float,
                      alpha: float, beta: float,
                      defectuosos: int | None = None) -> plt.Figure:
    """Curva OC profesional con marcadores NCA, NRL, α, β y punto de lote.

    Args:
        N:           tamaño del lote.
        n, c:        parámetros del plan.
        nca, nrl:    fracciones defectivas de referencia.
        alpha, beta: riesgos objetivo.
        defectuosos: observados en el lote (para marcar p_obs en la curva).

    Returns:
        Figura matplotlib.
    """
    ps, pas = _ms_curva_oc(N, n, c)

    fig, ax = plt.subplots(figsize=(10, 4.8))

    # ── Zonas de riesgo ───────────────────────────────────────────────────────
    ax.fill_between(ps, 0, pas, where=(ps <= nca),
                    color=C_SUCCESS, alpha=0.08, label="Zona aceptable (≤ NCA)")
    ax.fill_between(ps, 0, pas, where=(ps >= nrl),
                    color=C_DANGER, alpha=0.08, label="Zona de rechazo (≥ NRL)")

    # ── Curva OC ──────────────────────────────────────────────────────────────
    ax.plot(ps * 100, pas, color=C_PRIMARY, linewidth=2.5, zorder=4,
            label=f"Curva OC  (n={n}, c={c})")

    # ── Líneas de referencia NCA y NRL ────────────────────────────────────────
    pa_nca = _ms_calcular_pa(N, n, c, nca)
    pa_nrl = _ms_calcular_pa(N, n, c, nrl)
    alpha_r = 1.0 - pa_nca
    beta_r  = pa_nrl

    for xv, pav, col, lbl_v in [
        (nca * 100, pa_nca, C_SUCCESS, f"NCA = {nca*100:.2f}%"),
        (nrl * 100, pa_nrl, C_DANGER,  f"NRL = {nrl*100:.2f}%"),
    ]:
        ax.axvline(xv, color=col, linewidth=1.5, linestyle="--", alpha=0.8,
                   label=lbl_v)
        ax.scatter([xv], [pav], color=col, s=70, zorder=6)
        ax.annotate(
            f"P_a={pav:.3f}",
            xy=(xv, pav), xytext=(xv + 0.5, pav + 0.07),
            fontsize=7.5, color=col,
            bbox=dict(boxstyle="round,pad=0.25", facecolor="#0f1117",
                      edgecolor=col, alpha=0.9),
        )

    # ── Líneas horizontales α y β ─────────────────────────────────────────────
    ax.axhline(1 - alpha, color=C_SUCCESS, linewidth=1.1, linestyle=":",
               alpha=0.7, label=f"1-α = {(1-alpha)*100:.0f}%  (α={alpha:.3f} objetivo)")
    ax.axhline(beta,      color=C_DANGER,  linewidth=1.1, linestyle=":",
               alpha=0.7, label=f"β = {beta*100:.0f}%  (β={beta:.3f} objetivo)")

    # ── Anotación α real y β real en el gráfico ───────────────────────────────
    ax.text(
        0.98, 0.97,
        f"α real = {alpha_r:.4f}\nβ real = {beta_r:.4f}",
        transform=ax.transAxes, fontsize=8, va="top", ha="right",
        fontfamily="monospace", color="#e2e8f0",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#0f1117",
                  edgecolor="#2a2d3e", alpha=0.92),
    )

    # ── Punto de lote actual (si aplica) ─────────────────────────────────────
    if defectuosos is not None and n > 0:
        p_obs = defectuosos / n
        pa_obs = _ms_calcular_pa(N, n, c, p_obs)
        color_obs = C_SUCCESS if defectuosos <= c else C_DANGER
        ax.scatter([p_obs * 100], [pa_obs], color=color_obs, s=120,
                   zorder=7, marker="D",
                   label=f"Lote actual: d={defectuosos}  p={p_obs*100:.2f}%")
        ax.annotate(
            f"Lote: d={defectuosos}\np={p_obs*100:.2f}%",
            xy=(p_obs * 100, pa_obs),
            xytext=(p_obs * 100 + 1.0, pa_obs - 0.12),
            fontsize=7.5, color=color_obs,
            arrowprops=dict(arrowstyle="->", color=color_obs, lw=1.1),
            bbox=dict(boxstyle="round,pad=0.25", facecolor="#0f1117",
                      edgecolor=color_obs, alpha=0.9),
        )

    ax.set_title(f"Curva Característica de Operación (OC) — n={n}, c={c}, N={N}",
                 fontsize=11, fontweight="bold", pad=10)
    ax.set_xlabel("Fracción defectiva del lote (%)", fontsize=9)
    ax.set_ylabel("Probabilidad de aceptación  P(A)", fontsize=9)
    ax.set_xlim(0, 50)
    ax.set_ylim(0, 1.05)
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1, decimals=0))
    ax.legend(fontsize=7.5, loc="upper right",
              facecolor="#0f1117", edgecolor="#2a2d3e", ncol=2)
    ax.grid(True, alpha=0.4)
    fig.tight_layout()
    return fig


def _ms_fig_decision_lote(defectuosos: int, c: int, n: int) -> plt.Figure:
    """Gráfico de barras horizontal: defectuosos encontrados vs. número de aceptación."""
    fig, ax = plt.subplots(figsize=(7, 2.4))

    aceptado  = defectuosos <= c
    col_d     = C_SUCCESS if aceptado else C_DANGER
    col_c     = C_MUTED

    ax.barh(["Límite c", "Defectuosos"], [c, defectuosos],
            color=[col_c, col_d], alpha=0.85,
            edgecolor="#0f1117", linewidth=0.8, height=0.45)

    # Etiquetas
    for val, y, txt in [(c, 0, f"c = {c}  (límite)"),
                        (defectuosos, 1, f"d = {defectuosos}  (encontrados)")]:
        ax.text(val + max(c, defectuosos) * 0.02, y, txt,
                va="center", fontsize=9, color="#e2e8f0", fontweight="bold")

    ax.axvline(c, color=C_ACCENT, linewidth=1.5, linestyle="--",
               label=f"Número de aceptación c={c}")

    decision_txt = f"✅ ACEPTADO" if aceptado else f"❌ RECHAZADO"
    ax.text(
        0.98, 0.97, decision_txt,
        transform=ax.transAxes, fontsize=12, va="top", ha="right",
        fontweight="bold",
        color=C_SUCCESS if aceptado else C_DANGER,
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#0f1117",
                  edgecolor=C_SUCCESS if aceptado else C_DANGER, alpha=0.9),
    )

    ax.set_title("Decisión del lote: defectuosos vs. número de aceptación",
                 fontsize=10, fontweight="bold")
    ax.set_xlabel("Unidades", fontsize=9)
    ax.set_xlim(0, max(c, defectuosos) * 1.35 + 1)
    ax.legend(fontsize=8, facecolor="#0f1117", edgecolor="#2a2d3e")
    ax.grid(True, axis="x", alpha=0.4)
    fig.tight_layout()
    return fig


def _ms_fig_planes_comparativa(planes: list[dict],
                                nca: float, nrl: float) -> plt.Figure:
    """Gráfico de burbujas: planes válidos según n, c y riesgos."""
    if not planes:
        fig, ax = plt.subplots(figsize=(8, 3))
        ax.text(0.5, 0.5, "No se encontraron planes válidos",
                ha="center", va="center", color=C_MUTED, fontsize=11,
                transform=ax.transAxes)
        ax.axis("off")
        fig.tight_layout()
        return fig

    df_p  = pd.DataFrame(planes)
    ns    = df_p["n"].to_numpy(dtype=float)
    cs    = df_p["c"].to_numpy(dtype=float)
    betas = df_p["β real"].to_numpy(dtype=float)
    alphas= df_p["α real"].to_numpy(dtype=float)

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))

    # Panel izq: n vs c, tamaño = β
    sc1 = axes[0].scatter(ns, cs, s=betas * 3000 + 30, c=alphas,
                           cmap="RdYlGn_r", alpha=0.75, edgecolors="#0f1117",
                           linewidths=0.6, zorder=4)
    axes[0].set_xlabel("Tamaño de muestra n", fontsize=9)
    axes[0].set_ylabel("Número de aceptación c", fontsize=9)
    axes[0].set_title("Planes válidos: n vs. c  (tamaño ∝ β real)", fontsize=10, fontweight="bold")
    cb1 = plt.colorbar(sc1, ax=axes[0])
    cb1.set_label("α real", fontsize=8)
    axes[0].grid(True, alpha=0.4)

    # Panel der: α real vs β real
    sc2 = axes[1].scatter(alphas * 100, betas * 100, s=ns / ns.max() * 200 + 30,
                           c=cs, cmap="Blues", alpha=0.75,
                           edgecolors="#0f1117", linewidths=0.6, zorder=4)
    axes[1].set_xlabel("α real (%)", fontsize=9)
    axes[1].set_ylabel("β real (%)", fontsize=9)
    axes[1].set_title("Mapa de riesgos α–β  (tamaño ∝ n)", fontsize=10, fontweight="bold")
    cb2 = plt.colorbar(sc2, ax=axes[1])
    cb2.set_label("c", fontsize=8)
    axes[1].grid(True, alpha=0.4)

    fig.suptitle(
        f"Comparativa de planes válidos — NCA={nca*100:.2f}%  NRL={nrl*100:.2f}%",
        fontsize=10, color="#94a3b8", y=1.01,
    )
    fig.tight_layout()
    return fig


def _ms_fig_historial(historial: list[dict]) -> plt.Figure:
    """Gráfico de barras del historial de lotes inspeccionados."""
    if not historial:
        fig, ax = plt.subplots(figsize=(8, 2.5))
        ax.text(0.5, 0.5, "Sin lotes registrados aún",
                ha="center", va="center", color=C_MUTED, fontsize=11,
                transform=ax.transAxes)
        ax.axis("off")
        fig.tight_layout()
        return fig

    ids     = [f"Lote {h['id']}" for h in historial]
    defs    = [h["defectuosos"] for h in historial]
    cs_h    = [h["c"] for h in historial]
    colores = [C_SUCCESS if h["aceptado"] else C_DANGER for h in historial]

    fig, ax = plt.subplots(figsize=(max(8, len(historial) * 1.4), 3.5))
    x = np.arange(len(historial))
    w = 0.38

    ax.bar(x - w/2, defs,  width=w, color=colores, alpha=0.85,
           label="Defectuosos encontrados", edgecolor="#0f1117", linewidth=0.6)
    ax.bar(x + w/2, cs_h,  width=w, color=C_MUTED, alpha=0.55,
           label="Número de aceptación c", edgecolor="#0f1117", linewidth=0.6)

    # Etiquetas
    for xi, di, ci, col in zip(x, defs, cs_h, colores):
        ax.text(xi - w/2, di + 0.05, str(di), ha="center", fontsize=8,
                fontweight="bold", color=col)
        ax.text(xi + w/2, ci + 0.05, str(ci), ha="center", fontsize=8,
                color=C_MUTED)

    # Línea escalonada de c (puede variar entre lotes)
    ax.step(x, cs_h, where="mid", color=C_ACCENT, linewidth=1.4,
            linestyle="--", label="Límite c (escalonado)", zorder=5)

    ax.set_xticks(x)
    ax.set_xticklabels(ids, rotation=30 if len(historial) > 6 else 0, fontsize=8.5)
    ax.set_ylabel("Unidades defectuosas", fontsize=9)
    ax.set_title("Historial de lotes inspeccionados", fontsize=11, fontweight="bold")
    ax.legend(fontsize=8, facecolor="#0f1117", edgecolor="#2a2d3e", ncol=3)
    ax.grid(True, axis="y", alpha=0.4)
    fig.tight_layout()
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# 9-C  Panel de interpretación y recomendaciones
# ─────────────────────────────────────────────────────────────────────────────

def _ms_panel_interpretacion(aceptado: bool, defectuosos: int, c: int, n: int,
                               N: int, nca: float, nrl: float,
                               alpha_r: float, beta_r: float,
                               p_obs: float, ic_lo: float, ic_hi: float) -> None:
    """Interpretación automática del resultado del lote + recomendaciones."""

    # ── Veredicto principal ───────────────────────────────────────────────────
    if aceptado:
        estado  = "LOTE ACEPTADO"
        color_e = C_SUCCESS
        icono_e = "✅"
        msg_e   = (
            f"El lote cumple los criterios de calidad establecidos. "
            f"Se encontraron **{defectuosos}** defectuosos en la muestra de {n} unidades, "
            f"dentro del límite de aceptación c = {c}. "
            f"La fracción defectiva estimada en el lote es **{p_obs*100:.3f}%** "
            f"(IC 95%: [{ic_lo*100:.3f}% – {ic_hi*100:.3f}%]). "
            "El lote puede ser liberado al siguiente proceso o cliente."
        )
    else:
        estado  = "LOTE RECHAZADO"
        color_e = C_DANGER
        icono_e = "❌"
        msg_e   = (
            f"El lote **no cumple** los requisitos de calidad. "
            f"Se encontraron **{defectuosos}** defectuosos en la muestra de {n} unidades, "
            f"superando el número de aceptación c = {c}. "
            f"La fracción defectiva estimada es **{p_obs*100:.3f}%** "
            f"(IC 95%: [{ic_lo*100:.3f}% – {ic_hi*100:.3f}%]). "
            "Se recomienda inspección adicional al 100% o acciones correctivas inmediatas."
        )

    st.markdown(
        f"""
        <div style="background:#0f1117;border:2px solid {color_e};border-radius:12px;
                    padding:22px 26px;margin:14px 0">
            <div style="font-size:1.15rem;font-weight:700;color:{color_e};margin-bottom:10px">
                {icono_e} &nbsp; {estado}
            </div>
            <p style="font-size:.88rem;color:#e2e8f0;margin:0 0 16px">{msg_e}</p>
            <div style="display:flex;gap:28px;flex-wrap:wrap">
                <div>
                    <div style="font-size:.63rem;color:#64748b;letter-spacing:.1em;
                                text-transform:uppercase">Defectuosos</div>
                    <div style="font-family:monospace;font-size:1.4rem;
                                font-weight:700;color:{color_e}">{defectuosos} / {c}</div>
                </div>
                <div>
                    <div style="font-size:.63rem;color:#64748b;letter-spacing:.1em;
                                text-transform:uppercase">% Defectivo obs.</div>
                    <div style="font-family:monospace;font-size:1.4rem;
                                font-weight:700;color:{color_e}">{p_obs*100:.3f}%</div>
                </div>
                <div>
                    <div style="font-size:.63rem;color:#64748b;letter-spacing:.1em;
                                text-transform:uppercase">α real</div>
                    <div style="font-family:monospace;font-size:1.4rem;
                                font-weight:700;color:{C_ACCENT}">{alpha_r*100:.2f}%</div>
                </div>
                <div>
                    <div style="font-size:.63rem;color:#64748b;letter-spacing:.1em;
                                text-transform:uppercase">β real</div>
                    <div style="font-family:monospace;font-size:1.4rem;
                                font-weight:700;color:{C_ACCENT}">{beta_r*100:.2f}%</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Mensaje de protección del plan ────────────────────────────────────────
    prot_cons = "adecuada" if beta_r <= 0.10 else "insuficiente"
    prot_prod = "adecuada" if alpha_r <= 0.05 else "elevada"
    col_cons  = C_SUCCESS if beta_r  <= 0.10 else C_DANGER
    col_prod  = C_SUCCESS if alpha_r <= 0.05 else C_ACCENT

    st.markdown(
        f"""
        <div style="background:rgba(59,130,246,.08);border:1px solid rgba(59,130,246,.3);
                    border-radius:10px;padding:15px 20px;margin:10px 0">
            <div style="font-size:.8rem;color:{C_PRIMARY};font-weight:700;
                        letter-spacing:.08em;text-transform:uppercase;margin-bottom:6px">
                🏭 Análisis de protección del plan
            </div>
            <p style="font-size:.88rem;color:#e2e8f0;margin:0">
                Protección al <strong>consumidor</strong>: &nbsp;
                <span style="color:{col_cons};font-weight:700">
                    {prot_cons} (β={beta_r*100:.2f}%)
                </span> — riesgo de aceptar lotes con {nrl*100:.1f}% de defectuosos.<br>
                Protección al <strong>productor</strong>: &nbsp;
                <span style="color:{col_prod};font-weight:700">
                    {prot_prod} (α={alpha_r*100:.2f}%)
                </span> — riesgo de rechazar lotes con {nca*100:.2f}% de defectuosos.<br><br>
                Aceptar lotes con alta fracción defectiva incrementa los costos de no calidad
                (scrap, reproceso, reclamos). El tamaño de muestra n={n} inspecciona el
                <strong>{n/N*100:.1f}%</strong> del lote, minimizando costos de inspección
                con protección estadística verificada.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Recomendaciones automáticas priorizadas ───────────────────────────────
    recom = []
    if not aceptado:
        recom.append((C_DANGER, "❌",
            "Realizar inspección adicional al 100% del lote rechazado antes de liberar. "
            "Segregar unidades defectuosas para reproceso o scrap."))
        recom.append((C_DANGER, "🔍",
            "Investigar la causa raíz del exceso de defectuosos: revisar mezcla, "
            "relación agua/cemento, proceso de compactación y curado."))
    if p_obs > nrl:
        recom.append((C_DANGER, "⚠️",
            f"La fracción defectiva observada ({p_obs*100:.2f}%) supera el NRL "
            f"({nrl*100:.2f}%). Implementar acciones correctivas urgentes en el proceso."))
    if p_obs > nca and aceptado:
        recom.append((C_ACCENT, "⚠️",
            f"El lote fue aceptado, pero la fracción defectiva ({p_obs*100:.2f}%) "
            f"supera el NCA ({nca*100:.2f}%). Monitorear la tendencia del proceso."))
    if alpha_r > 0.05:
        recom.append((C_ACCENT, "📊",
            f"α real = {alpha_r*100:.2f}% > 5%. Considere aumentar n o c para "
            "reducir el riesgo del productor."))
    if beta_r > 0.10:
        recom.append((C_DANGER, "📉",
            f"β real = {beta_r*100:.2f}% > 10%. El plan no protege suficientemente "
            "al consumidor. Reduzca c o aumente n."))
    if n / N < 0.05:
        recom.append((C_ACCENT, "📋",
            f"La muestra representa solo el {n/N*100:.1f}% del lote. "
            "Para lotes con historial deficiente, considere aumentar n temporalmente."))
    recom.append((C_SUCCESS, "📈",
        "Fortalecer el control estadístico del proceso (CEP) para reducir la variabilidad "
        "y disminuir la dependencia del muestreo de aceptación."))

    st.markdown("#### 🔧 Recomendaciones automáticas")
    for col_r, ico_r, txt_r in recom:
        st.markdown(
            f"""
            <div style="display:flex;gap:12px;align-items:flex-start;padding:10px 15px;
                        background:#1a1d27;border-radius:8px;
                        border-left:3px solid {col_r};margin-bottom:7px">
                <span style="font-size:1.1rem;flex-shrink:0">{ico_r}</span>
                <span style="font-size:.86rem;color:#e2e8f0">{txt_r}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ─────────────────────────────────────────────────────────────────────────────
# 9-D  Función principal
# ─────────────────────────────────────────────────────────────────────────────

def seccion_muestreo():
    """Módulo completo de Muestreo de Aceptación del sistema CEP.

    Flujo interno:
    1.  Parámetros del lote y plan de muestreo.
    2.  Evaluación de lote actual: decisión Aceptar/Rechazar.
    3.  Dashboard de métricas clave.
    4.  Curva OC con marcadores NCA/NRL/α/β.
    5.  Gráfico de decisión defectuosos vs. c.
    6.  Interpretación automática + recomendaciones.
    7.  Diseño automático del plan (búsqueda óptima n, c).
    8.  Tabla y gráfico comparativa de planes válidos.
    9.  Historial de lotes inspeccionados (sesión).
    """
    encabezado(
        "📦", "Muestreo por aceptación",
        "Evaluación de lotes · Curva OC · Diseño automático de planes · Riesgos α y β",
    )

    # Inicializar historial en session_state
    if "ms_historial" not in st.session_state:
        st.session_state.ms_historial = []

    # ══════════════════════════════════════════════════════════════════════════
    # TABS PRINCIPALES
    # ══════════════════════════════════════════════════════════════════════════
    tab_eval, tab_dis, tab_hist = st.tabs([
        "🔍 Evaluación de lote",
        "⚙️ Diseño automático del plan",
        "📜 Historial de lotes",
    ])

    # ──────────────────────────────────────────────────────────────────────────
    # TAB 1 – Evaluación de lote
    # ──────────────────────────────────────────────────────────────────────────
    with tab_eval:

        st.markdown("### 🗂️ Parámetros del plan de muestreo")
        caja(
            "La distribución de probabilidad se selecciona automáticamente: "
            "**Hipergeométrica** cuando N/n ≤ 10; **Binomial** en caso contrario (estándar ISO 2859).",
            tipo="info",
        )

        with st.expander("📐 Parámetros del lote y del plan", expanded=True):
            pe1, pe2, pe3 = st.columns(3)
            with pe1:
                N_val = int(st.number_input(
                    "Tamaño del lote (N)",
                    min_value=10, max_value=100_000,
                    value=1000, step=50, key="ms_N",
                    help="Total de unidades en el lote a evaluar.",
                ))
                nca_pct = st.number_input(
                    "NCA / AQL (%)",
                    min_value=0.01, max_value=15.0,
                    value=1.0, step=0.1, format="%.2f", key="ms_NCA",
                    help="Nivel de calidad aceptable: fracción defectiva máxima para el productor.",
                )
            with pe2:
                n_val = int(st.number_input(
                    "Tamaño de muestra (n)",
                    min_value=5, max_value=10_000,
                    value=80, step=5, key="ms_n",
                    help="Número de unidades que se inspeccionan del lote.",
                ))
                nrl_pct = st.number_input(
                    "NRL / LTPD (%)",
                    min_value=0.1, max_value=50.0,
                    value=5.0, step=0.5, format="%.2f", key="ms_NRL",
                    help="Nivel rechazable de calidad: fracción defectiva que el consumidor no tolera.",
                )
            with pe3:
                c_val = int(st.number_input(
                    "Número de aceptación (c)",
                    min_value=0, max_value=500,
                    value=3, step=1, key="ms_c",
                    help="Máximo de defectuosos que se permiten para aceptar el lote.",
                ))
                norm_ref = st.selectbox(
                    "Norma de referencia",
                    ["ISO 2859-1", "ANSI/ASQ Z1.4", "MIL-STD-1916"],
                    key="ms_nor",
                )

        with st.expander("⚖️ Riesgos estadísticos objetivo", expanded=False):
            ra1, ra2 = st.columns(2)
            with ra1:
                alpha_obj = st.slider(
                    "α — Riesgo del productor",
                    min_value=0.01, max_value=0.20,
                    value=0.05, step=0.01, format="%.2f", key="ms_alpha",
                    help="P(rechazar lote bueno). Máximo aceptable: 5%.",
                )
            with ra2:
                beta_obj = st.slider(
                    "β — Riesgo del consumidor",
                    min_value=0.01, max_value=0.30,
                    value=0.10, step=0.01, format="%.2f", key="ms_beta",
                    help="P(aceptar lote malo). Máximo aceptable: 10%.",
                )

        # ── Validaciones cruzadas ──────────────────────────────────────────────
        nca = nca_pct / 100.0
        nrl = nrl_pct / 100.0

        if n_val > N_val:
            caja("n no puede ser mayor que N. Ajuste los parámetros.", tipo="warning")
        elif nca >= nrl:
            caja("El NCA debe ser menor que el NRL. Verifique los parámetros.", tipo="warning")
        else:
            # ── Evaluar lote ──────────────────────────────────────────────────
            st.markdown("### 🔬 Inspección del lote")
            li1, li2 = st.columns([2, 1])
            with li1:
                defectuosos_val = int(st.number_input(
                    "Defectuosos encontrados en la muestra (d)",
                    min_value=0, max_value=n_val,
                    value=min(2, n_val), step=1, key="ms_def",
                    help="Número de unidades defectuosas encontradas en la muestra.",
                ))
            with li2:
                st.markdown("<br>", unsafe_allow_html=True)
                registrar = st.button("📥 Registrar lote en historial",
                                      type="primary", key="ms_reg")

            # Calcular todo
            dist_usada   = _ms_elegir_distribucion(N_val, n_val)
            aceptado_val = defectuosos_val <= c_val
            iq           = _ms_indices_calidad_lote(N_val, n_val, c_val, defectuosos_val)
            alpha_r      = _ms_riesgo_productor(N_val, n_val, c_val, nca)
            beta_r       = _ms_riesgo_consumidor(N_val, n_val, c_val, nrl)

            # ── Dashboard de métricas ─────────────────────────────────────────
            st.markdown("### 📊 Indicadores del lote")
            dm1, dm2, dm3, dm4, dm5, dm6 = st.columns(6)
            dm1.metric("Tamaño lote N",    f"{N_val:,}")
            dm2.metric("Muestra n",        f"{n_val}",
                       delta=f"{n_val/N_val*100:.1f}% del lote")
            dm3.metric("Número accept. c", f"{c_val}")
            dm4.metric("Defectuosos d",    f"{defectuosos_val}",
                       delta="ACEPTADO" if aceptado_val else "RECHAZADO",
                       delta_color="normal" if aceptado_val else "inverse")
            dm5.metric("α real",           f"{alpha_r*100:.2f}%",
                       delta="✅ OK" if alpha_r <= alpha_obj else "⚠️ Elevado",
                       delta_color="normal" if alpha_r <= alpha_obj else "inverse")
            dm6.metric("β real",           f"{beta_r*100:.2f}%",
                       delta="✅ OK" if beta_r <= beta_obj else "⚠️ Elevado",
                       delta_color="normal" if beta_r <= beta_obj else "inverse")

            # Distribución utilizada
            caja(
                f"Distribución utilizada: **{dist_usada.capitalize()}** "
                f"(N/n = {N_val/n_val:.1f}). "
                f"Norma de referencia: **{norm_ref}**.",
                tipo="info",
            )

            # Decisión inmediata
            if aceptado_val:
                st.success(
                    f"✅ **LOTE ACEPTADO** — {defectuosos_val} defectuosos ≤ c={c_val}. "
                    f"Fracción defectiva estimada: {iq['p_obs']*100:.3f}% "
                    f"(IC 95%: {iq['ic_lo']*100:.3f}% – {iq['ic_hi']*100:.3f}%)."
                )
            else:
                st.error(
                    f"❌ **LOTE RECHAZADO** — {defectuosos_val} defectuosos > c={c_val}. "
                    f"Fracción defectiva estimada: {iq['p_obs']*100:.3f}%. "
                    "Se recomienda inspección adicional."
                )

            # Registrar en historial
            if registrar:
                hist_id = len(st.session_state.ms_historial) + 1
                st.session_state.ms_historial.append({
                    "id":          hist_id,
                    "N":           N_val,
                    "n":           n_val,
                    "c":           c_val,
                    "defectuosos": defectuosos_val,
                    "aceptado":    aceptado_val,
                    "p_obs":       iq["p_obs"],
                    "alpha_r":     alpha_r,
                    "beta_r":      beta_r,
                    "norma":       norm_ref,
                })
                st.success(f"Lote #{hist_id} registrado en el historial.")

            sep()

            # ── Gráficos ──────────────────────────────────────────────────────
            st.markdown("### 📈 Curva OC y decisión visual")
            goc1, goc2 = st.columns([3, 2])
            with goc1:
                st.markdown("#### Curva Característica de Operación")
                fig_oc = _ms_fig_curva_oc(
                    N_val, n_val, c_val, nca, nrl,
                    alpha_obj, beta_obj, defectuosos_val,
                )
                st.pyplot(fig_oc, use_container_width=True)
                plt.close(fig_oc)

            with goc2:
                st.markdown("#### Decisión: d vs. c")
                fig_dec = _ms_fig_decision_lote(defectuosos_val, c_val, n_val)
                st.pyplot(fig_dec, use_container_width=True)
                plt.close(fig_dec)

            sep()

            # ── Interpretación automática ─────────────────────────────────────
            st.markdown("### 🧠 Interpretación automática")
            _ms_panel_interpretacion(
                aceptado_val, defectuosos_val, c_val, n_val,
                N_val, nca, nrl, alpha_r, beta_r,
                iq["p_obs"], iq["ic_lo"], iq["ic_hi"],
            )

    # ──────────────────────────────────────────────────────────────────────────
    # TAB 2 – Diseño automático del plan
    # ──────────────────────────────────────────────────────────────────────────
    with tab_dis:
        st.markdown("### ⚙️ Diseño automático del plan de muestreo simple")
        caja(
            "El sistema busca todas las combinaciones (n, c) que satisfacen simultáneamente "
            "**P(aceptar|NCA) ≥ 1−α** y **P(aceptar|NRL) ≤ β**. "
            "Se usa la distribución más adecuada según N/n.",
            tipo="info",
        )

        dd1, dd2, dd3, dd4 = st.columns(4)
        with dd1:
            N_dis  = int(st.number_input("Tamaño de lote N",    value=1000, min_value=10,
                                          step=50,  key="dis_N"))
        with dd2:
            nca_d  = st.number_input("NCA (%)",                 value=1.0,  min_value=0.01,
                                      max_value=15.0, step=0.1, format="%.2f", key="dis_nca") / 100
        with dd3:
            nrl_d  = st.number_input("NRL (%)",                 value=5.0,  min_value=0.1,
                                      max_value=50.0, step=0.5, format="%.2f", key="dis_nrl") / 100
        with dd4:
            n_max_d = int(st.number_input("n máximo a explorar", value=300, min_value=20,
                                           max_value=1000, step=10, key="dis_nmax"))

        da1, da2 = st.columns(2)
        with da1:
            alpha_d = st.slider("α objetivo", 0.01, 0.20, 0.05, 0.01,
                                format="%.2f", key="dis_alpha")
        with da2:
            beta_d  = st.slider("β objetivo", 0.01, 0.30, 0.10, 0.01,
                                format="%.2f", key="dis_beta")

        if nca_d >= nrl_d:
            caja("NCA debe ser menor que NRL.", tipo="warning")
        else:
            if st.button("🔍 Buscar planes óptimos", type="primary", key="dis_btn"):
                with st.spinner("Buscando planes válidos..."):
                    planes = _ms_disenar_plan(N_dis, nca_d, nrl_d, alpha_d, beta_d, n_max_d)

                if not planes:
                    st.error(
                        "❌ No se encontraron planes que satisfagan ambas restricciones. "
                        "Intente: aumentar n_máximo, relajar α o β, o revisar NCA/NRL."
                    )
                else:
                    st.success(f"✅ Se encontraron **{len(planes)} planes válidos**. "
                               "Se muestran ordenados por tamaño de muestra (menor inspección primero).")

                    # Plan recomendado: el primero (menor n)
                    plan_rec = planes[0]
                    pr1, pr2, pr3, pr4, pr5 = st.columns(5)
                    pr1.metric("n recomendado", str(plan_rec["n"]))
                    pr2.metric("c recomendado", str(plan_rec["c"]))
                    pr3.metric("Pa(NCA)",        f"{plan_rec['Pa(NCA)']:.4f}")
                    pr4.metric("α real",         f"{plan_rec['α real']*100:.2f}%")
                    pr5.metric("β real",         f"{plan_rec['β real']*100:.2f}%")

                    caja(
                        f"**Plan recomendado: n={plan_rec['n']}, c={plan_rec['c']}**. "
                        f"Este plan minimiza el costo de inspección ({plan_rec['n']} unidades) "
                        f"mientras protege al consumidor (β={plan_rec['β real']*100:.2f}%) "
                        f"y al productor (α={plan_rec['α real']*100:.2f}%).",
                        tipo="success",
                    )

                    sep()

                    # Tabla de planes
                    st.markdown("#### 📋 Tabla de planes válidos")
                    df_planes = pd.DataFrame(planes)
                    st.dataframe(df_planes, use_container_width=True, hide_index=True)
                    csv_p = df_planes.to_csv(index=False).encode("utf-8")
                    st.download_button("⬇️ Descargar planes CSV", csv_p,
                                       "planes_muestreo.csv", "text/csv")

                    sep()

                    # Gráfico comparativa de planes + Curva OC del plan recomendado
                    st.markdown("#### 📈 Comparativa de planes y curva OC recomendada")
                    gp1, gp2 = st.columns([2, 3])
                    with gp1:
                        fig_pla = _ms_fig_planes_comparativa(planes, nca_d, nrl_d)
                        st.pyplot(fig_pla, use_container_width=True)
                        plt.close(fig_pla)
                    with gp2:
                        fig_rec = _ms_fig_curva_oc(
                            N_dis, plan_rec["n"], plan_rec["c"],
                            nca_d, nrl_d, alpha_d, beta_d,
                        )
                        st.pyplot(fig_rec, use_container_width=True)
                        plt.close(fig_rec)

    # ──────────────────────────────────────────────────────────────────────────
    # TAB 3 – Historial de lotes
    # ──────────────────────────────────────────────────────────────────────────
    with tab_hist:
        st.markdown("### 📜 Historial de lotes inspeccionados")
        historial = st.session_state.ms_historial

        if not historial:
            caja("Aún no hay lotes registrados. Evalúe lotes en la pestaña "
                 "**🔍 Evaluación de lote** y presione **Registrar lote en historial**.",
                 tipo="info")
        else:
            # Métricas del historial
            n_lotes    = len(historial)
            n_acept    = sum(1 for h in historial if h["aceptado"])
            n_rechaz   = n_lotes - n_acept
            tasa_acept = n_acept / n_lotes * 100

            hm1, hm2, hm3, hm4 = st.columns(4)
            hm1.metric("Lotes inspeccionados", str(n_lotes))
            hm2.metric("Aceptados",  f"{n_acept}",
                       delta=f"{tasa_acept:.1f}%", delta_color="normal")
            hm3.metric("Rechazados", f"{n_rechaz}",
                       delta=f"{100-tasa_acept:.1f}%", delta_color="inverse")
            hm4.metric("Tasa de aceptación", f"{tasa_acept:.1f}%")

            # Gráfico historial
            fig_hist = _ms_fig_historial(historial)
            st.pyplot(fig_hist, use_container_width=True)
            plt.close(fig_hist)

            sep()

            # Tabla detallada
            st.markdown("#### 📋 Detalle de lotes")
            df_hist = pd.DataFrame([{
                "Lote":         f"#{h['id']}",
                "N":            h["N"],
                "n":            h["n"],
                "c":            h["c"],
                "Defectuosos":  h["defectuosos"],
                "% Defect.":    f"{h['p_obs']*100:.3f}%",
                "α real (%)":   f"{h['alpha_r']*100:.2f}%",
                "β real (%)":   f"{h['beta_r']*100:.2f}%",
                "Decisión":     "✅ Aceptado" if h["aceptado"] else "❌ Rechazado",
                "Norma":        h["norma"],
            } for h in historial])
            st.dataframe(df_hist, use_container_width=True, hide_index=True)

            csv_hist = df_hist.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Descargar historial CSV", csv_hist,
                               "historial_lotes.csv", "text/csv")

            # Botón limpiar historial
            if st.button("🗑️ Limpiar historial", type="secondary"):
                st.session_state.ms_historial = []
                st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 10 – Análisis de causas
# Incluye: Ishikawa 6M, Pareto interactivo, Priorización, Correlación,
#          Dashboard de causas raíz, Recomendaciones automáticas
# ══════════════════════════════════════════════════════════════════════════════

# ─────────────────────────────────────────────────────────────────────────────
# 10-A  Datos por defecto para la empresa de bloques de concreto
# ─────────────────────────────────────────────────────────────────────────────

# Causas predefinidas por categoría 6M para la industria de bloques de concreto.
# El usuario puede editarlas, eliminarlas o añadir las suyas.
_CA_CAUSAS_DEFAULT: dict[str, list[dict]] = {
    "Método": [
        {"causa": "Relación agua/cemento fuera de rango",     "impacto": 5, "frecuencia": 4},
        {"causa": "Procedimientos de compactación variables",  "impacto": 4, "frecuencia": 3},
        {"causa": "Tiempo de curado insuficiente",             "impacto": 5, "frecuencia": 5},
        {"causa": "Falta de estandarización del proceso",      "impacto": 3, "frecuencia": 3},
        {"causa": "Parámetros de vibración mal definidos",     "impacto": 4, "frecuencia": 2},
    ],
    "Mano de obra": [
        {"causa": "Falta de capacitación en mezcla",           "impacto": 4, "frecuencia": 4},
        {"causa": "Errores en dosificación manual",            "impacto": 5, "frecuencia": 3},
        {"causa": "Fatiga del operador en turno nocturno",     "impacto": 3, "frecuencia": 2},
        {"causa": "Alta rotación del personal",                "impacto": 3, "frecuencia": 2},
        {"causa": "Incumplimiento de procedimientos",          "impacto": 4, "frecuencia": 3},
    ],
    "Maquinaria": [
        {"causa": "Desgaste de moldes de bloque",              "impacto": 5, "frecuencia": 4},
        {"causa": "Mala calibración de la mezcladora",         "impacto": 5, "frecuencia": 3},
        {"causa": "Fallas en sistema de vibración",            "impacto": 4, "frecuencia": 3},
        {"causa": "Mantenimiento preventivo deficiente",       "impacto": 4, "frecuencia": 4},
        {"causa": "Variación en presión de compactación",      "impacto": 5, "frecuencia": 3},
    ],
    "Materiales": [
        {"causa": "Variabilidad en calidad del cemento",       "impacto": 5, "frecuencia": 3},
        {"causa": "Agregados con granulometría incorrecta",    "impacto": 4, "frecuencia": 3},
        {"causa": "Humedad variable en arena/agregado",        "impacto": 4, "frecuencia": 4},
        {"causa": "Cambio de proveedor de cemento",            "impacto": 3, "frecuencia": 2},
        {"causa": "Contaminación de materia prima",            "impacto": 5, "frecuencia": 2},
    ],
    "Medio ambiente": [
        {"causa": "Alta temperatura en área de curado",        "impacto": 4, "frecuencia": 3},
        {"causa": "Humedad relativa no controlada",            "impacto": 4, "frecuencia": 4},
        {"causa": "Exposición a lluvia antes del curado",      "impacto": 5, "frecuencia": 2},
        {"causa": "Polvo en ambiente de mezclado",             "impacto": 2, "frecuencia": 2},
        {"causa": "Variaciones térmicas entre turnos",         "impacto": 3, "frecuencia": 3},
    ],
    "Medición": [
        {"causa": "Instrumentos de ensayo sin calibrar",       "impacto": 5, "frecuencia": 3},
        {"causa": "Error en lectura de balanzas",              "impacto": 4, "frecuencia": 2},
        {"causa": "Método de muestreo inconsistente",          "impacto": 4, "frecuencia": 3},
        {"causa": "Sistema de inspección visual subjetivo",    "impacto": 3, "frecuencia": 3},
        {"causa": "Falta de trazabilidad de ensayos",          "impacto": 4, "frecuencia": 2},
    ],
}

# Defectos predefinidos para el diagrama de Pareto
_CA_DEFECTOS_DEFAULT: dict[str, int] = {
    "Baja resistencia a compresión":         45,
    "Grietas superficiales":                 28,
    "Dimensiones fuera de tolerancia":       18,
    "Porosidad excesiva / absorción alta":   15,
    "Segregación de agregados":              10,
    "Desportillado en aristas":               8,
    "Coloración no uniforme":                 5,
    "Peso unitario fuera de rango":           4,
}

# Íconos y colores por categoría 6M
_CA_CATEGORIA_META: dict[str, tuple[str, str]] = {
    "Método":        ("⚙️",  "#3b82f6"),
    "Mano de obra":  ("👷",  "#f59e0b"),
    "Maquinaria":    ("🔧",  "#ef4444"),
    "Materiales":    ("🧱",  "#22c55e"),
    "Medio ambiente":("🌡️", "#818cf8"),
    "Medición":      ("📏",  "#f97316"),
}


# ─────────────────────────────────────────────────────────────────────────────
# 10-B  Funciones de cálculo y análisis
# ─────────────────────────────────────────────────────────────────────────────

def _ca_score_causa(impacto: int, frecuencia: int) -> float:
    """Score de prioridad = impacto × frecuencia (escala 1–25).

    Args:
        impacto:    valor 1–5 (severidad del impacto en calidad).
        frecuencia: valor 1–5 (con qué frecuencia ocurre).

    Returns:
        Score numérico ∈ [1, 25].
    """
    return float(impacto * frecuencia)


def _ca_nivel_prioridad(score: float) -> tuple[str, str, str]:
    """Clasifica la prioridad de una causa según su score.

    Returns:
        (etiqueta, color_hex, ícono)
    """
    if score >= 16:
        return "🔴 Alta",    C_DANGER,  "🔴"
    if score >= 9:
        return "🟡 Media",   C_ACCENT,  "🟡"
    return "🟢 Baja",        C_SUCCESS, "🟢"


def _ca_construir_df_causas(causas_dict: dict[str, list[dict]]) -> pd.DataFrame:
    """Convierte el dict de causas en un DataFrame enriquecido.

    Columnas resultantes: Categoría, Causa, Impacto, Frecuencia, Score, Prioridad.
    """
    rows = []
    for cat, causas in causas_dict.items():
        for c in causas:
            score = _ca_score_causa(c.get("impacto", 3), c.get("frecuencia", 3))
            lbl_p, col_p, ico_p = _ca_nivel_prioridad(score)
            rows.append({
                "Categoría":  cat,
                "Causa":      c["causa"],
                "Impacto":    c.get("impacto",    3),
                "Frecuencia": c.get("frecuencia", 3),
                "Score":      score,
                "Prioridad":  lbl_p,
                "_color":     col_p,
            })
    df = pd.DataFrame(rows).sort_values("Score", ascending=False).reset_index(drop=True)
    return df


def _ca_pareto_data(defectos: dict[str, int]) -> pd.DataFrame:
    """Genera el DataFrame ordenado para el diagrama de Pareto.

    Añade columna de porcentaje acumulado para la línea de Pareto.
    """
    df = pd.DataFrame(list(defectos.items()), columns=["Defecto", "Frecuencia"])
    df = df.sort_values("Frecuencia", ascending=False).reset_index(drop=True)
    total = df["Frecuencia"].sum()
    df["%"] = df["Frecuencia"] / total * 100
    df["% Acumulado"] = df["%"].cumsum()
    df["% Frec."] = df["%"].round(1).astype(str) + "%"
    return df


def _ca_resumen_por_categoria(df_causas: pd.DataFrame) -> pd.DataFrame:
    """Agrega el DataFrame de causas por categoría para el dashboard."""
    return (
        df_causas.groupby("Categoría")
        .agg(
            N_causas=("Causa",      "count"),
            Score_total=("Score",   "sum"),
            Score_max=("Score",     "max"),
            Altas=(   "Prioridad",  lambda s: (s.str.contains("Alta")).sum()),
        )
        .sort_values("Score_total", ascending=False)
        .reset_index()
    )


# ─────────────────────────────────────────────────────────────────────────────
# 10-C  Funciones de graficación
# ─────────────────────────────────────────────────────────────────────────────

def _ca_fig_ishikawa(causas_dict: dict[str, list[dict]],
                      efecto: str) -> plt.Figure:
    """Diagrama de Ishikawa (espina de pescado) profesional con 6M.

    Diseño:
    - Espina central horizontal → efecto a la derecha.
    - 6 espinas diagonales (3 arriba, 3 abajo) con sus causas.
    - Cada causa coloreada según prioridad (score).
    - Fondo oscuro coherente con el tema de la aplicación.

    Args:
        causas_dict: dict {categoría: [{causa, impacto, frecuencia}]}.
        efecto:      texto del problema/efecto principal.

    Returns:
        Figura matplotlib.
    """
    categorias = list(_CA_CATEGORIA_META.keys())
    # Posiciones: 3 arriba (izq→der), 3 abajo (izq→der)
    posiciones = [
        # (x_base, lado: +1 arriba / -1 abajo)
        (1.5,  1), (4.5,  1), (7.5,  1),
        (1.5, -1), (4.5, -1), (7.5, -1),
    ]

    fig, ax = plt.subplots(figsize=(16, 9))
    ax.set_xlim(-0.5, 13)
    ax.set_ylim(-5.5, 5.5)
    ax.axis("off")
    fig.patch.set_facecolor("#0f1117")
    ax.set_facecolor("#0f1117")

    # ── Espina central ────────────────────────────────────────────────────────
    ax.annotate("", xy=(10.8, 0), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color="#94a3b8",
                                lw=2.5, mutation_scale=20))

    # ── Cabeza: caja del efecto ───────────────────────────────────────────────
    efecto_corto = efecto[:40] + "…" if len(efecto) > 40 else efecto
    bbox_ef = dict(boxstyle="round,pad=0.6", facecolor=C_DANGER,
                   edgecolor="#ff6b6b", alpha=0.92)
    ax.text(11.5, 0, efecto_corto, ha="center", va="center",
            fontsize=9, fontweight="bold", color="white",
            bbox=bbox_ef, wrap=True)

    # ── Espinas por categoría ─────────────────────────────────────────────────
    for idx, (cat, (ico, col_cat)) in enumerate(_CA_CATEGORIA_META.items()):
        x_base, lado = posiciones[idx]
        y_punta = 0.0          # punto en la espina central
        y_raiz  = lado * 3.8   # punta de la espina diagonal

        # Espina diagonal
        ax.annotate("", xy=(x_base, y_punta), xytext=(x_base - 0.3, y_raiz),
                    arrowprops=dict(arrowstyle="-|>", color=col_cat,
                                    lw=1.8, mutation_scale=14, alpha=0.85))

        # Etiqueta de categoría
        ax.text(x_base - 0.3, y_raiz + lado * 0.45,
                f"{ico} {cat}", ha="center", va="center",
                fontsize=9.5, fontweight="bold", color=col_cat,
                bbox=dict(boxstyle="round,pad=0.35", facecolor="#1a1d27",
                          edgecolor=col_cat, alpha=0.9))

        # Causas de esta categoría
        causas_cat = causas_dict.get(cat, [])
        for j, c in enumerate(causas_cat[:5]):      # máx. 5 causas por categoría
            score  = _ca_score_causa(c.get("impacto", 3), c.get("frecuencia", 3))
            _, col_p, _ = _ca_nivel_prioridad(score)

            # Posición de la causa: a lo largo de la espina diagonal
            frac    = (j + 1) / (len(causas_cat[:5]) + 1)
            x_causa = x_base - 0.3 + frac * 0.3   # avanzar hacia la espina
            y_causa = y_raiz + frac * (-y_raiz)    # interpolar hacia y=0

            # Línea de la causa hacia la espina
            ax.plot([x_causa, x_causa + 0.0], [y_causa, y_causa + lado * 0.6],
                    color=col_p, linewidth=0.9, alpha=0.7)

            # Texto de causa con salto de línea automático (máx. 28 chars)
            causa_txt = c["causa"]
            if len(causa_txt) > 28:
                # Cortar en el espacio más cercano al carácter 28
                idx_sp = causa_txt[:28].rfind(" ")
                causa_txt = (causa_txt[:idx_sp] + "\n" + causa_txt[idx_sp+1:]) \
                            if idx_sp > 0 else causa_txt[:28] + "…"

            ax.text(x_causa, y_causa + lado * 0.65,
                    causa_txt, ha="center", va="bottom" if lado > 0 else "top",
                    fontsize=6.2, color="#e2e8f0",
                    bbox=dict(boxstyle="round,pad=0.2", facecolor="#1a1d27",
                              edgecolor=col_p, alpha=0.75, linewidth=0.6))

    # ── Título ────────────────────────────────────────────────────────────────
    ax.set_title(f"Diagrama de Ishikawa — 6M\nEfecto: {efecto[:60]}",
                 fontsize=12, fontweight="bold", color="#e2e8f0",
                 pad=12, loc="left")

    # Leyenda de prioridad
    for lbl_leg, col_leg in [("Alta prioridad (score≥16)", C_DANGER),
                               ("Media prioridad (9–15)",   C_ACCENT),
                               ("Baja prioridad (≤8)",      C_SUCCESS)]:
        ax.plot([], [], "s", color=col_leg, label=lbl_leg, markersize=7)
    ax.legend(loc="lower left", fontsize=7.5,
              facecolor="#0f1117", edgecolor="#2a2d3e",
              labelcolor="#e2e8f0")

    fig.tight_layout()
    return fig


def _ca_fig_pareto(df_pareto: pd.DataFrame) -> plt.Figure:
    """Diagrama de Pareto profesional con barras de frecuencia y línea acumulada.

    Incluye:
    - Barras coloreadas: las que aportan el 80% se destacan.
    - Línea acumulada en eje secundario.
    - Línea de referencia al 80%.
    - Etiquetas de % sobre cada barra.
    """
    n = len(df_pareto)
    colores = []
    acum = 0.0
    for pct in df_pareto["%"].tolist():
        acum += pct
        colores.append(C_PRIMARY if acum <= 80.0 else C_MUTED)

    fig, ax1 = plt.subplots(figsize=(10, 4.5))
    ax2 = ax1.twinx()

    x = np.arange(n)
    bars = ax1.bar(x, df_pareto["Frecuencia"], color=colores, alpha=0.85,
                   edgecolor="#0f1117", linewidth=0.7, width=0.65)

    # Etiquetas de % sobre cada barra
    for bar, pct in zip(bars, df_pareto["%"].tolist()):
        ax1.text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() + df_pareto["Frecuencia"].max() * 0.01,
                 f"{pct:.1f}%", ha="center", va="bottom",
                 fontsize=8, color="#e2e8f0", fontweight="bold")

    # Línea acumulada
    ax2.plot(x, df_pareto["% Acumulado"], color=C_ACCENT,
             linewidth=2.2, marker="o", markersize=5, zorder=5)

    # Línea 80%
    ax2.axhline(80, color=C_DANGER, linewidth=1.4, linestyle="--",
                alpha=0.75, label="80%")
    ax2.text(n - 0.5, 81, "80%", color=C_DANGER, fontsize=8.5, va="bottom")

    # Relleno zona 80%
    ax2.fill_between(x, df_pareto["% Acumulado"], 100,
                     alpha=0.05, color=C_MUTED)

    ax1.set_xticks(x)
    ax1.set_xticklabels(df_pareto["Defecto"], rotation=28,
                        ha="right", fontsize=8)
    ax1.set_ylabel("Frecuencia de defectos", fontsize=9)
    ax2.set_ylabel("% Acumulado", fontsize=9)
    ax2.set_ylim(0, 110)
    ax1.set_title("Diagrama de Pareto — Defectos del proceso",
                  fontsize=11, fontweight="bold", pad=10)
    ax1.grid(True, axis="y", alpha=0.4)

    # Leyenda manual
    from matplotlib.patches import Patch
    ax1.legend(handles=[
        Patch(facecolor=C_PRIMARY, label="Causas vitales (≤80%)"),
        Patch(facecolor=C_MUTED,   label="Causas triviales (>80%)"),
    ], fontsize=8, facecolor="#0f1117", edgecolor="#2a2d3e", loc="center right")

    fig.tight_layout()
    return fig


def _ca_fig_prioridad_scatter(df_causas: pd.DataFrame) -> plt.Figure:
    """Scatter de priorización: Impacto vs. Frecuencia con burbuja = score.

    Cada burbuja representa una causa; el color indica la categoría 6M.
    """
    fig, ax = plt.subplots(figsize=(9, 5))

    categorias_unicas = df_causas["Categoría"].unique()
    cmap_cat = {cat: _CA_CATEGORIA_META[cat][1]
                for cat in categorias_unicas if cat in _CA_CATEGORIA_META}

    for cat in categorias_unicas:
        sub   = df_causas[df_causas["Categoría"] == cat]
        col_c = cmap_cat.get(cat, C_PRIMARY)
        ico_c = _CA_CATEGORIA_META.get(cat, ("", ""))[0]
        ax.scatter(sub["Frecuencia"], sub["Impacto"],
                   s=sub["Score"] * 12 + 40,
                   c=col_c, alpha=0.72, edgecolors="#0f1117",
                   linewidths=0.6, zorder=4,
                   label=f"{ico_c} {cat}")

    # Líneas de cuadrante
    ax.axvline(3, color="#64748b", linewidth=0.8, linestyle="--", alpha=0.5)
    ax.axhline(3, color="#64748b", linewidth=0.8, linestyle="--", alpha=0.5)

    # Etiquetas de cuadrante
    for (xt, yt, txt, col_t) in [
        (4.5, 4.5, "CRÍTICAS\n(Alta/Alta)",     C_DANGER),
        (1.5, 4.5, "IMPACTO ALTO\n(Baja frec.)",C_ACCENT),
        (4.5, 1.5, "FRECUENTES\n(Bajo impacto)",C_ACCENT),
        (1.5, 1.5, "MENORES\n(Ignorar)",         C_MUTED),
    ]:
        ax.text(xt, yt, txt, ha="center", va="center",
                fontsize=7.5, color=col_t, alpha=0.55, fontweight="bold")

    ax.set_xlim(0.5, 5.8)
    ax.set_ylim(0.5, 5.8)
    ax.set_xlabel("Frecuencia (1–5)", fontsize=9)
    ax.set_ylabel("Impacto (1–5)", fontsize=9)
    ax.set_title("Mapa de priorización de causas — Impacto vs. Frecuencia",
                 fontsize=11, fontweight="bold", pad=10)
    ax.legend(fontsize=7.5, facecolor="#0f1117", edgecolor="#2a2d3e",
              loc="lower right", ncol=2)
    ax.grid(True, alpha=0.35)
    ax.set_xticks(range(1, 6))
    ax.set_yticks(range(1, 6))
    fig.tight_layout()
    return fig


def _ca_fig_barras_categoria(resumen: pd.DataFrame) -> plt.Figure:
    """Barras horizontales de score total por categoría 6M."""
    cats  = resumen["Categoría"].tolist()
    scores= resumen["Score_total"].tolist()
    altas = resumen["Altas"].tolist()
    colores = [_CA_CATEGORIA_META.get(c, ("", C_PRIMARY))[1] for c in cats]

    fig, ax = plt.subplots(figsize=(8, 3.8))
    y = np.arange(len(cats))
    bars = ax.barh(y, scores, color=colores, alpha=0.82,
                   edgecolor="#0f1117", linewidth=0.6, height=0.55)

    for bar, sc, alt, cat in zip(bars, scores, altas, cats):
        w = bar.get_width()
        ax.text(w + max(scores) * 0.01, bar.get_y() + bar.get_height() / 2,
                f"Score {sc:.0f}  |  {alt} Alta(s)",
                va="center", fontsize=8, color="#e2e8f0")

    ax.set_yticks(y)
    ax.set_yticklabels([f"{_CA_CATEGORIA_META.get(c,('',''))[0]} {c}" for c in cats],
                       fontsize=8.5)
    ax.set_xlabel("Score de riesgo total (Impacto × Frecuencia × N°causas)",
                  fontsize=8.5)
    ax.set_title("Riesgo acumulado por categoría 6M",
                 fontsize=11, fontweight="bold", pad=10)
    ax.set_xlim(0, max(scores) * 1.35)
    ax.grid(True, axis="x", alpha=0.4)
    fig.tight_layout()
    return fig


def _ca_fig_correlacion(df_sg: pd.DataFrame | None,
                          var_x: str, var_y: str) -> plt.Figure:
    """Scatter de correlación entre dos variables del proceso con regresión lineal.

    Args:
        df_sg: DataFrame de subgrupos de la aplicación.
        var_x: nombre de la columna X.
        var_y: nombre de la columna Y.
    """
    fig, ax = plt.subplots(figsize=(8, 4.2))

    if df_sg is None or var_x not in df_sg.columns or var_y not in df_sg.columns:
        ax.text(0.5, 0.5,
                "Cargue datos en '📥 Ingreso de datos'\npara activar el análisis de correlación.",
                ha="center", va="center", color=C_MUTED, fontsize=11,
                transform=ax.transAxes)
        ax.axis("off")
        fig.tight_layout()
        return fig

    x = df_sg[var_x].dropna().to_numpy(dtype=float)
    y = df_sg[var_y].dropna().to_numpy(dtype=float)
    n_min = min(len(x), len(y))
    x, y  = x[:n_min], y[:n_min]

    if len(x) < 3:
        ax.text(0.5, 0.5, "Datos insuficientes para correlación (mín. 3 puntos).",
                ha="center", va="center", color=C_MUTED, fontsize=11,
                transform=ax.transAxes)
        ax.axis("off")
        fig.tight_layout()
        return fig

    # Regresión lineal
    slope, intercept, r, p_val, se = sp_stats.linregress(x, y)
    r2 = r ** 2
    x_line = np.linspace(x.min(), x.max(), 100)
    y_line  = slope * x_line + intercept

    # Clasificación de r
    if abs(r) >= 0.70:
        lbl_r, col_r = "Correlación fuerte",  C_SUCCESS if r > 0 else C_DANGER
    elif abs(r) >= 0.40:
        lbl_r, col_r = "Correlación moderada", C_ACCENT
    else:
        lbl_r, col_r = "Correlación débil",    C_MUTED

    sig_txt = f"p={p_val:.4f} ({'sig.' if p_val < 0.05 else 'no sig.'})"

    ax.scatter(x, y, color=C_PRIMARY, alpha=0.65, s=30,
               edgecolors="#0f1117", linewidths=0.4, zorder=4)
    ax.plot(x_line, y_line, color=col_r, linewidth=2.0,
            label=f"r = {r:.3f}  |  R² = {r2:.3f}  |  {lbl_r}\n{sig_txt}")

    ax.set_xlabel(var_x, fontsize=9)
    ax.set_ylabel(var_y, fontsize=9)
    ax.set_title(f"Correlación: {var_x}  vs.  {var_y}",
                 fontsize=11, fontweight="bold", pad=10)
    ax.legend(fontsize=8, facecolor="#0f1117", edgecolor="#2a2d3e")
    ax.grid(True, alpha=0.4)
    fig.tight_layout()
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# 10-D  Panel de interpretación y recomendaciones
# ─────────────────────────────────────────────────────────────────────────────

def _ca_panel_interpretacion(df_causas: pd.DataFrame,
                               resumen_cat: pd.DataFrame,
                               efecto: str) -> None:
    """Genera interpretación automática y recomendaciones priorizadas."""

    # Categoría más crítica
    cat_critica  = resumen_cat.iloc[0]["Categoría"]
    score_max    = resumen_cat.iloc[0]["Score_total"]
    n_altas_tot  = df_causas["Prioridad"].str.contains("Alta").sum()
    n_total      = len(df_causas)
    top3_causas  = df_causas.head(3)

    # ── Veredicto ─────────────────────────────────────────────────────────────
    if n_altas_tot >= n_total * 0.5:
        color_e = C_DANGER
        icono_e = "🔴"
        msg_e   = (
            f"**{n_altas_tot}** de las {n_total} causas analizadas tienen prioridad ALTA. "
            f"La categoría con mayor riesgo acumulado es **{cat_critica}** "
            f"(Score total = {score_max:.0f}). "
            "Se requieren acciones correctivas inmediatas para reducir la variabilidad del proceso."
        )
    elif n_altas_tot > 0:
        color_e = C_ACCENT
        icono_e = "🟡"
        msg_e   = (
            f"Se identificaron **{n_altas_tot}** causa(s) de prioridad alta. "
            f"La mayor concentración de riesgo está en **{cat_critica}**. "
            "Focalice recursos en las causas críticas antes de abordar las de menor impacto."
        )
    else:
        color_e = C_SUCCESS
        icono_e = "✅"
        msg_e   = (
            "Las causas analizadas presentan prioridad baja a media. "
            f"La categoría con mayor score es **{cat_critica}**. "
            "Mantenga monitoreo continuo y prevenga que estas causas escalen."
        )

    st.markdown(
        f"""
        <div style="background:#0f1117;border:2px solid {color_e};border-radius:12px;
                    padding:22px 26px;margin:14px 0">
            <div style="font-size:1.1rem;font-weight:700;color:{color_e};margin-bottom:10px">
                {icono_e} &nbsp; ANÁLISIS DE CAUSAS — {efecto[:50].upper()}
            </div>
            <p style="font-size:.88rem;color:#e2e8f0;margin:0 0 14px">{msg_e}</p>
            <div style="font-size:.82rem;color:#94a3b8">
                📋 Categoría más crítica: <strong style="color:{color_e}">{cat_critica}</strong> &nbsp;|&nbsp;
                Causas altas: <strong style="color:{C_DANGER}">{n_altas_tot}</strong> &nbsp;|&nbsp;
                Total causas: <strong>{n_total}</strong>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Top 3 causas ──────────────────────────────────────────────────────────
    st.markdown("#### 🔴 Top 3 causas más críticas")
    for i, row in top3_causas.iterrows():
        _, col_p, ico_p = _ca_nivel_prioridad(row["Score"])
        ico_cat = _CA_CATEGORIA_META.get(row["Categoría"], ("🔹", ""))[0]
        st.markdown(
            f"""
            <div style="display:flex;gap:14px;align-items:center;padding:10px 15px;
                        background:#1a1d27;border-radius:8px;
                        border-left:4px solid {col_p};margin-bottom:6px">
                <span style="font-size:1.3rem;flex-shrink:0">{ico_cat}</span>
                <div>
                    <div style="font-size:.88rem;color:#e2e8f0;font-weight:600">
                        {row['Causa']}
                    </div>
                    <div style="font-size:.75rem;color:#64748b;margin-top:2px">
                        {row['Categoría']} &nbsp;·&nbsp;
                        Impacto: {row['Impacto']}/5 &nbsp;·&nbsp;
                        Frecuencia: {row['Frecuencia']}/5 &nbsp;·&nbsp;
                        Score: <strong style="color:{col_p}">{row['Score']:.0f}</strong>
                        &nbsp;{ico_p}
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── Interpretación automática por categoría ───────────────────────────────
    st.markdown("#### 💡 Análisis automático por categoría")
    msgs_cat = {
        "Método":         "La variabilidad del proceso puede estar asociada a métodos no estandarizados. Revise procedimientos operativos estándar (POE).",
        "Mano de obra":   "Los errores humanos contribuyen a la variabilidad. Fortalezca la capacitación y certifique competencias.",
        "Maquinaria":     "El desgaste o calibración deficiente de equipos puede ser causa directa de defectos. Implemente un plan de mantenimiento preventivo.",
        "Materiales":     "La variabilidad en materiales impacta directamente la resistencia y absorción. Evalúe proveedores y establezca control de recepción.",
        "Medio ambiente": "Las condiciones ambientales no controladas afectan el curado y la calidad. Implemente controles de temperatura y humedad.",
        "Medición":       "Un sistema de medición deficiente distorsiona la información del proceso. Implemente un plan de calibración y estudio GR&R.",
    }
    for _, row_cat in resumen_cat.iterrows():
        cat  = row_cat["Categoría"]
        ico_c= _CA_CATEGORIA_META.get(cat, ("🔹", C_PRIMARY))[0]
        col_c= _CA_CATEGORIA_META.get(cat, ("", C_PRIMARY))[1]
        msg  = msgs_cat.get(cat, "Revise las causas identificadas en esta categoría.")
        st.markdown(
            f"""
            <div style="padding:8px 14px;background:#1a1d27;border-radius:7px;
                        border-left:3px solid {col_c};margin-bottom:5px">
                <span style="font-size:.9rem;font-weight:600;color:{col_c}">{ico_c} {cat}</span>
                <span style="font-size:.8rem;color:#94a3b8"> — Score: {row_cat['Score_total']:.0f}
                &nbsp;|&nbsp; {row_cat['Altas']:.0f} causa(s) alta(s)</span><br>
                <span style="font-size:.82rem;color:#e2e8f0">{msg}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── Recomendaciones priorizadas ────────────────────────────────────────────
    st.markdown("#### 🔧 Recomendaciones automáticas")
    _recom_map = {
        "Método":         (C_PRIMARY, "📋", "Estandarizar procedimientos operativos. Implementar control de mezcla y curado según norma NTC 4026."),
        "Mano de obra":   (C_ACCENT,  "👷", "Capacitar operarios en dosificación y compactación. Establecer certificación interna por tarea."),
        "Maquinaria":     (C_DANGER,  "🔧", "Recalibrar mezcladora y vibrador. Implementar plan de mantenimiento preventivo mensual."),
        "Materiales":     (C_SUCCESS, "🧱", "Establecer control de recepción de cemento y áridos. Verificar granulometría y humedad por lote."),
        "Medio ambiente": (C_NORMAL,  "🌡️","Monitorear temperatura y humedad en cámara de curado. Instalar termohigrómetros registradores."),
        "Medición":       (C_ACCENT,  "📏", "Calibrar equipos de ensayo (prensa, balanza). Realizar estudio GR&R en variables críticas."),
    }
    recom_ordenadas = [(resumen_cat.iloc[i]["Categoría"],
                        resumen_cat.iloc[i]["Score_total"])
                       for i in range(len(resumen_cat))]
    for cat, sc in recom_ordenadas:
        col_r, ico_r, txt_r = _recom_map.get(cat, (C_PRIMARY, "🔹", "Revisar causas de esta categoría."))
        st.markdown(
            f"""
            <div style="display:flex;gap:12px;align-items:flex-start;padding:9px 14px;
                        background:#1a1d27;border-radius:8px;
                        border-left:3px solid {col_r};margin-bottom:6px">
                <span style="font-size:1.1rem;flex-shrink:0">{ico_r}</span>
                <span style="font-size:.85rem;color:#e2e8f0">{txt_r}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ─────────────────────────────────────────────────────────────────────────────
# 10-E  Función principal
# ─────────────────────────────────────────────────────────────────────────────

def seccion_causas():
    """Módulo completo de Análisis de Causas del sistema CEP.

    Flujo interno:
    1.  Ingreso del efecto / problema principal.
    2.  Editor de causas por categoría 6M con impacto y frecuencia.
    3.  Diagrama de Ishikawa (espina de pescado) profesional.
    4.  Diagrama de Pareto de defectos.
    5.  Mapa de priorización Impacto vs. Frecuencia.
    6.  Barras de riesgo acumulado por categoría.
    7.  Análisis de correlación entre variables del proceso.
    8.  Tabla resumen de causas exportable.
    9.  Dashboard de interpretación automática y recomendaciones.
    """
    encabezado(
        "🔎", "Análisis de causas",
        "Ishikawa 6M · Pareto · Priorización · Correlación · Recomendaciones automáticas",
    )

    # Inicializar estado de causas en la sesión
    if "ca_causas" not in st.session_state:
        import copy
        st.session_state.ca_causas = copy.deepcopy(_CA_CAUSAS_DEFAULT)
    if "ca_defectos" not in st.session_state:
        st.session_state.ca_defectos = dict(_CA_DEFECTOS_DEFAULT)

    df_sg    = st.session_state.get("df_subgrupos")
    datos_ok = st.session_state.get("datos_cargados", False)
    cap_res  = st.session_state.get("capacidad", {})
    f1       = st.session_state.get("fase1", {})

    # ── Contexto automático desde otros módulos ────────────────────────────────
    alertas_cep = []
    if f1.get("calculado") and not f1.get("proceso_estable", True):
        alertas_cep.append("⚡ Fase 1 detectó causas especiales — el proceso no es estable.")
    if cap_res.get("cpk") and cap_res["cpk"] < 1.00:
        alertas_cep.append(f"📉 Cpk = {cap_res['cpk']:.3f} — proceso no capaz. Alta variabilidad.")
    if cap_res.get("pnc_pct") and cap_res.get("pnc_pct", 0) > 5:
        alertas_cep.append(f"🚫 PNC = {cap_res.get('pnc_pct',0):.2f}% — porcentaje de defectos elevado.")

    if alertas_cep:
        caja(
            "**Alertas del sistema CEP vinculadas al análisis de causas:**\n\n" +
            "\n\n".join(alertas_cep),
            tipo="warning",
        )

    # ══════════════════════════════════════════════════════════════════════════
    # TABS PRINCIPALES
    # ══════════════════════════════════════════════════════════════════════════
    tab_ishi, tab_pareto, tab_prior, tab_corr, tab_dash = st.tabs([
        "🐟 Ishikawa 6M",
        "📊 Pareto de defectos",
        "🎯 Priorización",
        "📉 Correlación",
        "🧠 Dashboard y recomendaciones",
    ])

    # ──────────────────────────────────────────────────────────────────────────
    # TAB 1 – Diagrama de Ishikawa
    # ──────────────────────────────────────────────────────────────────────────
    with tab_ishi:
        st.markdown("### 🐟 Diagrama de Ishikawa — 6M")
        caja(
            "Ingrese el efecto/problema principal y registre las causas potenciales "
            "por categoría. Cada causa se evalúa con **Impacto** (1–5) y "
            "**Frecuencia** (1–5) para calcular automáticamente su prioridad.",
            tipo="info",
        )

        efecto = st.text_input(
            "🎯 Efecto / Problema principal",
            value="Baja resistencia a compresión del bloque de concreto",
            key="ca_efecto",
            help="Describa el defecto o problema que se desea analizar.",
        )

        sep()
        st.markdown("#### ✏️ Editor de causas por categoría")

        # Editor por categoría
        for cat, (ico, col_cat) in _CA_CATEGORIA_META.items():
            with st.expander(f"{ico} **{cat}**", expanded=False):
                causas_cat = st.session_state.ca_causas.get(cat, [])
                nuevas_causas = []
                for j, c in enumerate(causas_cat):
                    ec1, ec2, ec3, ec4 = st.columns([5, 1, 1, 0.5])
                    with ec1:
                        causa_txt = st.text_input(
                            f"Causa {j+1}",
                            value=c["causa"],
                            key=f"ca_{cat}_{j}_txt",
                            label_visibility="collapsed",
                        )
                    with ec2:
                        imp = st.selectbox("Imp.", [1,2,3,4,5],
                                           index=c.get("impacto",3)-1,
                                           key=f"ca_{cat}_{j}_imp",
                                           label_visibility="collapsed",
                                           help="Impacto en calidad (1=mínimo, 5=crítico)")
                    with ec3:
                        frec = st.selectbox("Frec.", [1,2,3,4,5],
                                            index=c.get("frecuencia",3)-1,
                                            key=f"ca_{cat}_{j}_frec",
                                            label_visibility="collapsed",
                                            help="Frecuencia (1=rara, 5=muy frecuente)")
                    with ec4:
                        score_c = imp * frec
                        _, col_p, ico_p = _ca_nivel_prioridad(score_c)
                        st.markdown(
                            f"<div style='padding:4px 0;text-align:center;font-size:1.1rem'>"
                            f"{ico_p}</div>",
                            unsafe_allow_html=True,
                        )
                    nuevas_causas.append({"causa": causa_txt, "impacto": imp, "frecuencia": frec})

                # Añadir causa nueva
                col_add, _ = st.columns([3, 1])
                with col_add:
                    nueva = st.text_input(
                        f"➕ Nueva causa en {cat}",
                        value="",
                        key=f"ca_{cat}_nueva",
                        placeholder="Escriba y presione Enter…",
                    )
                    if nueva.strip():
                        nuevas_causas.append({"causa": nueva.strip(), "impacto": 3, "frecuencia": 3})

                st.session_state.ca_causas[cat] = nuevas_causas

        sep()

        # Generar diagrama
        if st.button("🐟 Generar diagrama de Ishikawa", type="primary", key="ca_ishi_btn"):
            with st.spinner("Generando diagrama Ishikawa..."):
                fig_ishi = _ca_fig_ishikawa(st.session_state.ca_causas, efecto)
                st.pyplot(fig_ishi, use_container_width=True)
                plt.close(fig_ishi)
        else:
            # Mostrar siempre (con datos actuales)
            fig_ishi = _ca_fig_ishikawa(st.session_state.ca_causas, efecto)
            st.pyplot(fig_ishi, use_container_width=True)
            plt.close(fig_ishi)

    # ──────────────────────────────────────────────────────────────────────────
    # TAB 2 – Pareto de defectos
    # ──────────────────────────────────────────────────────────────────────────
    with tab_pareto:
        st.markdown("### 📊 Diagrama de Pareto — Tipos de defecto")
        caja(
            "El Principio de Pareto establece que el **80% de los defectos** proviene "
            "del **20% de las causas**. Concentre recursos en las barras azules.",
            tipo="info",
        )

        st.markdown("#### ✏️ Frecuencia de defectos observados")
        defectos_ui = {}
        cols_par = st.columns(2)
        defectos_list = list(st.session_state.ca_defectos.items())
        for i, (def_txt, def_frec) in enumerate(defectos_list):
            col_idx = i % 2
            with cols_par[col_idx]:
                val = st.number_input(
                    def_txt, min_value=0, value=def_frec,
                    step=1, key=f"par_{i}_{def_txt[:8]}",
                )
                defectos_ui[def_txt] = val

        # Nueva categoría de defecto
        nd1, nd2 = st.columns([3, 1])
        with nd1:
            nuevo_def = st.text_input("➕ Nuevo tipo de defecto", value="",
                                       placeholder="Ej: Eflorescencia", key="par_nuevo_def")
        with nd2:
            nuevo_def_frec = st.number_input("Frecuencia", min_value=0, value=0,
                                              step=1, key="par_nuevo_frec")
        if nuevo_def.strip() and nuevo_def_frec > 0:
            defectos_ui[nuevo_def.strip()] = nuevo_def_frec

        st.session_state.ca_defectos = defectos_ui

        sep()

        defectos_filtrados = {k: v for k, v in defectos_ui.items() if v > 0}
        if not defectos_filtrados:
            caja("Ingrese al menos un tipo de defecto con frecuencia > 0.", tipo="warning")
        else:
            df_pareto = _ca_pareto_data(defectos_filtrados)
            fig_par   = _ca_fig_pareto(df_pareto)
            st.pyplot(fig_par, use_container_width=True)
            plt.close(fig_par)

            # Análisis 80/20
            vitales = df_pareto[df_pareto["% Acumulado"] <= 80.0]
            if len(vitales) == 0:
                vitales = df_pareto.head(1)
            n_vitales = len(vitales)
            total_d   = df_pareto["Frecuencia"].sum()

            st.success(
                f"**Ley de Pareto:** Los {n_vitales} defectos principales "
                f"({', '.join(vitales['Defecto'].tolist()[:3])}) "
                f"representan el {vitales['% Acumulado'].iloc[-1]:.1f}% de los defectos totales. "
                f"Total registrado: **{total_d} defectos**."
            )

            sep()
            st.markdown("#### 📋 Tabla de defectos")
            df_show = df_pareto[["Defecto","Frecuencia","% Frec.","% Acumulado"]].copy()
            df_show["% Acumulado"] = df_show["% Acumulado"].round(1).astype(str) + "%"
            st.dataframe(df_show, use_container_width=True, hide_index=True)
            csv_par = df_pareto.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Descargar Pareto CSV", csv_par,
                               "pareto_defectos.csv", "text/csv")

    # ──────────────────────────────────────────────────────────────────────────
    # TAB 3 – Priorización
    # ──────────────────────────────────────────────────────────────────────────
    with tab_prior:
        st.markdown("### 🎯 Priorización de causas")
        caja(
            "**Score = Impacto × Frecuencia** (máx. 25). "
            "🔴 Alta: ≥16 · 🟡 Media: 9–15 · 🟢 Baja: ≤8.",
            tipo="info",
        )

        df_causas_all = _ca_construir_df_causas(st.session_state.ca_causas)
        resumen_cat   = _ca_resumen_por_categoria(df_causas_all)

        # Métricas globales
        n_alta  = (df_causas_all["Prioridad"].str.contains("Alta")).sum()
        n_media = (df_causas_all["Prioridad"].str.contains("Media")).sum()
        n_baja  = (df_causas_all["Prioridad"].str.contains("Baja")).sum()
        pm1, pm2, pm3, pm4 = st.columns(4)
        pm1.metric("Total causas",      str(len(df_causas_all)))
        pm2.metric("🔴 Alta prioridad",  str(n_alta),
                   delta_color="inverse", delta=f"{n_alta/max(len(df_causas_all),1)*100:.0f}%")
        pm3.metric("🟡 Media prioridad", str(n_media))
        pm4.metric("🟢 Baja prioridad",  str(n_baja))

        sep()

        # Gráficos de priorización
        gpr1, gpr2 = st.columns([3, 2])
        with gpr1:
            st.markdown("#### Mapa Impacto vs. Frecuencia")
            fig_sc = _ca_fig_prioridad_scatter(df_causas_all)
            st.pyplot(fig_sc, use_container_width=True)
            plt.close(fig_sc)
        with gpr2:
            st.markdown("#### Riesgo acumulado por categoría")
            fig_bar_cat = _ca_fig_barras_categoria(resumen_cat)
            st.pyplot(fig_bar_cat, use_container_width=True)
            plt.close(fig_bar_cat)

        sep()

        # Tabla de causas por prioridad
        st.markdown("#### 📋 Tabla completa de causas priorizadas")
        df_show_c = df_causas_all[["Categoría","Causa","Impacto","Frecuencia","Score","Prioridad"]].copy()
        st.dataframe(df_show_c, use_container_width=True, hide_index=True)
        csv_causas = df_causas_all.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Descargar tabla de causas CSV", csv_causas,
                           "causas_priorizadas.csv", "text/csv")

    # ──────────────────────────────────────────────────────────────────────────
    # TAB 4 – Análisis de correlación
    # ──────────────────────────────────────────────────────────────────────────
    with tab_corr:
        st.markdown("### 📉 Análisis de correlación entre variables del proceso")
        caja(
            "Identifique variables del proceso correlacionadas con la resistencia "
            "a compresión. Se requieren datos cargados en **📥 Ingreso de datos**.",
            tipo="info",
        )

        cols_disponibles = []
        if datos_ok and df_sg is not None:
            cols_disponibles = [c for c in df_sg.columns
                                if df_sg[c].dtype in [float, np.float64, int, np.int64]]
            caja(f"Dataset activo: **{len(df_sg)} observaciones** · columnas numéricas disponibles.",
                 tipo="success")
        else:
            caja("Cargue datos en **📥 Ingreso de datos** para activar el análisis de correlación.",
                 tipo="warning")

        if cols_disponibles:
            cc1, cc2 = st.columns(2)
            with cc1:
                var_x = st.selectbox("Variable X (posible causa / factor)",
                                     cols_disponibles,
                                     index=min(1, len(cols_disponibles)-1),
                                     key="ca_corr_x")
            with cc2:
                var_y = st.selectbox("Variable Y (efecto / respuesta)",
                                     cols_disponibles,
                                     index=0,
                                     key="ca_corr_y")

            if var_x == var_y:
                caja("Seleccione variables distintas para el análisis de correlación.", tipo="warning")
            else:
                fig_corr = _ca_fig_correlacion(df_sg, var_x, var_y)
                st.pyplot(fig_corr, use_container_width=True)
                plt.close(fig_corr)

                # Calcular e interpretar r
                x_arr = df_sg[var_x].dropna().to_numpy(dtype=float)
                y_arr = df_sg[var_y].dropna().to_numpy(dtype=float)
                n_min = min(len(x_arr), len(y_arr))
                if n_min >= 3:
                    r_val, p_val = sp_stats.pearsonr(x_arr[:n_min], y_arr[:n_min])
                    if abs(r_val) >= 0.70 and p_val < 0.05:
                        st.success(f"✅ Correlación significativa fuerte (r={r_val:.3f}, p={p_val:.4f}). "
                                   f"**{var_x}** es un buen predictor de **{var_y}**.")
                    elif abs(r_val) >= 0.40 and p_val < 0.05:
                        st.warning(f"⚠️ Correlación moderada (r={r_val:.3f}, p={p_val:.4f}). "
                                   f"**{var_x}** tiene influencia parcial sobre **{var_y}**.")
                    else:
                        st.info(f"ℹ️ Correlación débil o no significativa (r={r_val:.3f}, p={p_val:.4f}). "
                                f"Explore otras variables como posibles causas.")
        else:
            # Mostrar gráfico informativo aunque no haya datos
            fig_corr = _ca_fig_correlacion(None, "", "")
            st.pyplot(fig_corr, use_container_width=True)
            plt.close(fig_corr)

        # Tabla de referencia de correlación
        with st.expander("📖 Guía de interpretación del coeficiente de Pearson (r)"):
            st.markdown("""
            | |r| | Interpretación |
            |:---:|:---|
            | 0.90 – 1.00 | Correlación muy fuerte — relación casi lineal |
            | 0.70 – 0.89 | Correlación fuerte — variable predictora relevante |
            | 0.40 – 0.69 | Correlación moderada — influencia parcial |
            | 0.20 – 0.39 | Correlación débil — poca asociación |
            | 0.00 – 0.19 | Sin correlación práctica |
            """)

    # ──────────────────────────────────────────────────────────────────────────
    # TAB 5 – Dashboard y recomendaciones
    # ──────────────────────────────────────────────────────────────────────────
    with tab_dash:
        st.markdown("### 🧠 Dashboard de análisis causa raíz")

        df_causas_dash = _ca_construir_df_causas(st.session_state.ca_causas)
        resumen_dash   = _ca_resumen_por_categoria(df_causas_dash)
        efecto_dash    = st.session_state.get("ca_efecto",
                         "Baja resistencia a compresión del bloque de concreto")

        # Métricas ejecutivas
        d1, d2, d3, d4, d5 = st.columns(5)
        d1.metric("Categorías analizadas",  str(len(resumen_dash)))
        d2.metric("Total causas",           str(len(df_causas_dash)))
        d3.metric("🔴 Alta prioridad",
                  str((df_causas_dash["Prioridad"].str.contains("Alta")).sum()))
        d4.metric("Score máximo",
                  f"{df_causas_dash['Score'].max():.0f}/25")
        d5.metric("Categoría crítica",
                  resumen_dash.iloc[0]["Categoría"] if len(resumen_dash) > 0 else "—")

        sep()

        _ca_panel_interpretacion(df_causas_dash, resumen_dash, efecto_dash)


# ─────────────────────────────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 11 – Dashboard general
# Vista ejecutiva del sistema CEP con semáforo, KPIs, gráficos resumen,
# score global de salud del proceso e interpretación automática integrada.
# ══════════════════════════════════════════════════════════════════════════════

# ─────────────────────────────────────────────────────────────────────────────
# 11-A  Funciones de soporte del dashboard
# ─────────────────────────────────────────────────────────────────────────────

def _db_recolectar_estado() -> dict:
    """Lee todos los estados relevantes del session_state y los consolida.

    Returns:
        dict con llaves tipadas y seguras para el dashboard.
        Todas las llaves tienen valor por defecto para evitar KeyError.
    """
    ss   = st.session_state
    f1   = ss.get("fase1",      {})
    cap  = ss.get("capacidad",  {})
    cq   = ss.get("calidad_costos_res", {})   # guardado por seccion_calidad_costos si existe
    hist = ss.get("ms_historial", [])
    cfg  = ss.get("config_proceso", {})
    df_sg= ss.get("df_subgrupos")

    # ── Datos disponibles ─────────────────────────────────────────────────────
    datos_ok   = bool(ss.get("datos_cargados", False))
    n_obs      = len(df_sg) if (datos_ok and df_sg is not None) else 0
    n_sgs      = df_sg["subgrupo"].nunique() if (datos_ok and df_sg is not None) else 0

    # ── Fase 1 ────────────────────────────────────────────────────────────────
    f1_ok        = f1.get("calculado", False)
    estable      = f1.get("proceso_estable", None)   # True / False / None
    n_fuera_f1   = f1.get("n_puntos_fuera", 0)
    tipo_carta   = f1.get("tipo_carta", "X-R")
    sigma_est    = f1.get("sigma_est")

    # ── Capacidad ─────────────────────────────────────────────────────────────
    cap_ok  = bool(cap)
    cp_val  = cap.get("cp")
    cpk_val = cap.get("cpk")
    pnc_val = cap.get("pnc_pct")      # % no conformes
    pp_val  = cap.get("pp")
    ppk_val = cap.get("ppk")
    var_cap = cap.get("variable", "Resistencia")

    # ── Costos (si se calcularon en el módulo Calidad y Costos) ───────────────
    cq_ok          = bool(cq)
    costo_total    = cq.get("costo_total",    None)
    costo_falla    = cq.get("costo_falla",    None)
    pct_falla_cq   = cq.get("pct_falla",      None)
    ahorro_pot     = cq.get("ahorro_potencial",None)

    # ── Muestreo ──────────────────────────────────────────────────────────────
    n_lotes      = len(hist)
    n_acept      = sum(1 for h in hist if h.get("aceptado", False))
    tasa_acept   = (n_acept / n_lotes * 100) if n_lotes > 0 else None

    # ── Desempeño (ds) ────────────────────────────────────────────────────────
    ds           = ss.get("ds_ultimo", {})     # guardado si se calculó en sec_desempeno
    potencia_ds  = ds.get("potencia")
    arl1_ds      = ds.get("arl1")
    ats_ds       = ds.get("ats_h")

    return {
        "datos_ok":    datos_ok,
        "n_obs":       n_obs,
        "n_sgs":       n_sgs,
        "f1_ok":       f1_ok,
        "estable":     estable,
        "n_fuera_f1":  n_fuera_f1,
        "tipo_carta":  tipo_carta,
        "sigma_est":   sigma_est,
        "cap_ok":      cap_ok,
        "cp":          cp_val,
        "cpk":         cpk_val,
        "pnc":         pnc_val,
        "pp":          pp_val,
        "ppk":         ppk_val,
        "var_cap":     var_cap,
        "cq_ok":       cq_ok,
        "costo_total": costo_total,
        "costo_falla": costo_falla,
        "pct_falla":   pct_falla_cq,
        "ahorro_pot":  ahorro_pot,
        "n_lotes":     n_lotes,
        "n_acept":     n_acept,
        "tasa_acept":  tasa_acept,
        "potencia":    potencia_ds,
        "arl1":        arl1_ds,
        "ats_h":       ats_ds,
        "cfg":         cfg,
        "df_sg":       df_sg,
    }


def _db_score_salud(e: dict) -> tuple[float, str, str, str]:
    """Calcula el Score Global de Salud del Proceso (0–100).

    Ponderación:
        Estabilidad (Fase 1)   : 25 pts
        Capacidad (Cpk)        : 30 pts
        % No conformes         : 20 pts
        Costos de falla        : 15 pts
        Muestreo               : 10 pts

    Returns:
        (score, etiqueta, color, ícono)
    """
    score = 0.0

    # Estabilidad
    if e["f1_ok"]:
        if e["estable"] is True:
            score += 25.0
        elif e["estable"] is False:
            score += max(0.0, 25.0 - e["n_fuera_f1"] * 3.0)
        else:
            score += 10.0   # calculado pero estabilidad indeterminada

    # Capacidad
    if e["cap_ok"] and e["cpk"] is not None:
        cpk = e["cpk"]
        if cpk >= 1.67:   score += 30.0
        elif cpk >= 1.33: score += 25.0
        elif cpk >= 1.00: score += 15.0
        elif cpk >= 0.67: score += 5.0

    # % PNC
    if e["pnc"] is not None:
        pnc = e["pnc"]
        if pnc < 1.0:    score += 20.0
        elif pnc < 3.0:  score += 15.0
        elif pnc < 5.0:  score += 8.0
        elif pnc < 10.0: score += 3.0

    # Costos de falla
    if e["pct_falla"] is not None:
        pf = e["pct_falla"]
        if pf < 20:   score += 15.0
        elif pf < 40: score += 10.0
        elif pf < 60: score += 4.0

    # Muestreo
    if e["tasa_acept"] is not None:
        ta = e["tasa_acept"]
        if ta >= 95:   score += 10.0
        elif ta >= 80: score += 6.0
        elif ta >= 60: score += 2.0

    score = min(100.0, score)

    if score >= 80:
        return score, "PROCESO SALUDABLE",       C_SUCCESS, "🟢"
    if score >= 55:
        return score, "ATENCIÓN REQUERIDA",       C_ACCENT,  "🟡"
    if score >= 30:
        return score, "PROCESO EN RIESGO",        C_DANGER,  "🔴"
    return score,     "ESTADO CRÍTICO",           C_DANGER,  "🔴"


def _db_estado_modulo(completado: bool | None,
                       ok: bool | None = None) -> tuple[str, str, str]:
    """Devuelve (ícono, texto_badge, color_badge) para el semáforo de módulos."""
    if completado is None or not completado:
        return "⚪", "Pendiente",  "#64748b"
    if ok is True:
        return "🟢", "OK",         C_SUCCESS
    if ok is False:
        return "🔴", "Alerta",     C_DANGER
    return "🟡", "Revisar",         C_ACCENT


# ─────────────────────────────────────────────────────────────────────────────
# 11-B  Funciones de graficación del dashboard
# ─────────────────────────────────────────────────────────────────────────────

def _db_fig_gauge_score(score: float, color: str) -> plt.Figure:
    """Gauge semicircular para el Score Global de Salud (0–100)."""
    fig, ax = plt.subplots(figsize=(4.5, 2.8),
                            subplot_kw=dict(aspect="equal"))
    fig.patch.set_facecolor("#0f1117")
    ax.set_facecolor("#0f1117")

    # Fondo del arco (gris)
    theta_bg = np.linspace(np.pi, 0, 200)
    ax.plot(np.cos(theta_bg), np.sin(theta_bg),
            linewidth=18, color="#2a2d3e", solid_capstyle="round")

    # Arco coloreado según score
    frac     = score / 100.0
    theta_fg = np.linspace(np.pi, np.pi - frac * np.pi, 200)
    ax.plot(np.cos(theta_fg), np.sin(theta_fg),
            linewidth=18, color=color, solid_capstyle="round", alpha=0.88)

    # Texto central
    ax.text(0, -0.15, f"{score:.0f}", ha="center", va="center",
            fontsize=32, fontweight="bold", color=color,
            fontfamily="monospace")
    ax.text(0, -0.55, "/ 100", ha="center", va="center",
            fontsize=11, color="#64748b")
    ax.text(0, -0.85, "Score Global CEP", ha="center", va="center",
            fontsize=8.5, color="#94a3b8")

    # Marcadores 0 / 50 / 100
    for ang, txt in [(np.pi, "0"), (np.pi/2, "50"), (0, "100")]:
        ax.text(np.cos(ang)*1.18, np.sin(ang)*1.18, txt,
                ha="center", va="center", fontsize=7.5, color="#64748b")

    ax.set_xlim(-1.4, 1.4)
    ax.set_ylim(-1.1, 1.2)
    ax.axis("off")
    fig.tight_layout(pad=0.3)
    return fig


def _db_fig_radar_modulos(e: dict) -> plt.Figure:
    """Radar de 5 dimensiones de calidad del proceso."""
    cats = ["Estabilidad", "Capacidad", "Calidad\nPNC", "Costos\nFalla", "Muestreo"]

    # Normalizar cada dimensión a 0–10
    def _s(val, mx): return min(10.0, (val / mx) * 10.0) if val is not None else 0.0

    # Estabilidad
    if e["f1_ok"] and e["estable"] is True:  est_s = 10.0
    elif e["f1_ok"] and e["estable"] is False: est_s = max(0.0, 10.0 - e["n_fuera_f1"] * 1.5)
    else: est_s = 0.0

    # Capacidad (cpk 0..2 → 0..10)
    cap_s  = _s(e["cpk"], 2.0) if e["cpk"] is not None else 0.0

    # PNC inverso (0%=10, 10%=0)
    pnc_s  = max(0.0, 10.0 - (e["pnc"] or 10.0)) if e["pnc"] is not None else 0.0

    # Costos falla inverso (0%=10, 100%=0)
    cq_s   = max(0.0, 10.0 * (1.0 - (e["pct_falla"] or 100.0) / 100.0)) \
             if e["pct_falla"] is not None else 0.0

    # Muestreo (tasa aceptación)
    ms_s   = _s(e["tasa_acept"], 100.0) if e["tasa_acept"] is not None else 0.0

    valores = [est_s, cap_s, pnc_s, cq_s, ms_s]
    N       = len(cats)
    angles  = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]
    valores += valores[:1]

    fig, ax = plt.subplots(figsize=(4.5, 4.5),
                            subplot_kw=dict(polar=True))
    fig.patch.set_facecolor("#0f1117")
    ax.set_facecolor("#0f1117")

    # Rejilla
    ax.set_ylim(0, 10)
    for yg in [2, 4, 6, 8, 10]:
        ax.plot([a for a in angles], [yg]*len(angles),
                color="#2a2d3e", linewidth=0.6)

    # Área del proceso
    ax.fill(angles, valores, alpha=0.25, color=C_PRIMARY)
    ax.plot(angles, valores, color=C_PRIMARY, linewidth=2.0)
    ax.scatter(angles[:-1], valores[:-1], color=C_PRIMARY, s=45, zorder=5)

    # Área de referencia (objetivo)
    ref = [8]*N + [8]
    ax.fill(angles, ref, alpha=0.06, color=C_SUCCESS)
    ax.plot(angles, ref, color=C_SUCCESS, linewidth=0.8,
            linestyle="--", alpha=0.5)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(cats, fontsize=8, color="#e2e8f0")
    ax.set_yticks([])
    ax.spines["polar"].set_color("#2a2d3e")
    ax.set_title("Radar CEP\n(objetivo: ≥ 8/10 en cada dimensión)",
                 fontsize=8.5, color="#94a3b8", pad=14)
    fig.tight_layout(pad=0.5)
    return fig


def _db_fig_mini_xbar(df_sg: pd.DataFrame | None, e: dict) -> plt.Figure:
    """Mini carta X̄ (últimos 20 subgrupos) para el dashboard."""
    fig, ax = plt.subplots(figsize=(7, 2.6))
    fig.patch.set_facecolor("#0f1117")
    ax.set_facecolor("#0f1117")

    if df_sg is None or "subgrupo" not in df_sg.columns:
        ax.text(0.5, 0.5, "Datos no disponibles",
                ha="center", va="center", color=C_MUTED, fontsize=10,
                transform=ax.transAxes)
        ax.axis("off")
        fig.tight_layout()
        return fig

    col_var = "resistencia" if e["var_cap"] == "Resistencia" else "absorcion"
    if col_var not in df_sg.columns:
        col_var = df_sg.select_dtypes("number").columns[0]

    # Calcular medias por subgrupo
    medias = df_sg.groupby("subgrupo")[col_var].mean().reset_index()
    medias.columns = ["sg", "xbar"]
    medias = medias.tail(20).reset_index(drop=True)

    xbar_g = medias["xbar"].mean()
    std_g  = medias["xbar"].std(ddof=1)
    lcl    = xbar_g - 3 * std_g
    ucl    = xbar_g + 3 * std_g

    x = np.arange(len(medias))
    fuera = (medias["xbar"] < lcl) | (medias["xbar"] > ucl)

    ax.plot(x, medias["xbar"], color=C_PRIMARY, linewidth=1.5,
            marker="o", markersize=4, zorder=4)
    ax.scatter(x[fuera], medias["xbar"][fuera],
               color=C_DANGER, s=55, zorder=5,
               label=f"Fuera: {fuera.sum()}")
    ax.axhline(xbar_g, color=C_SUCCESS,   linewidth=1.2, linestyle="-",  alpha=0.8)
    ax.axhline(ucl,    color=C_DANGER,    linewidth=1.0, linestyle="--", alpha=0.7)
    ax.axhline(lcl,    color=C_DANGER,    linewidth=1.0, linestyle="--", alpha=0.7)

    ax.fill_between(x, lcl, ucl, alpha=0.05, color=C_SUCCESS)
    ax.set_title("Mini carta X̄ (últimos 20 sg.)", fontsize=9,
                 fontweight="bold", color="#e2e8f0", pad=5)
    ax.set_xlabel("Subgrupo", fontsize=7.5)
    ax.set_ylabel(col_var[:12], fontsize=7.5)
    ax.tick_params(labelsize=7)
    ax.legend(fontsize=7, facecolor="#0f1117", edgecolor="#2a2d3e")
    ax.grid(True, alpha=0.3)
    fig.tight_layout(pad=0.4)
    return fig


def _db_fig_tendencia_cpk(cap: dict) -> plt.Figure:
    """Placeholder visual para tendencia de Cpk (simula histórico de períodos)."""
    fig, ax = plt.subplots(figsize=(7, 2.4))
    fig.patch.set_facecolor("#0f1117")
    ax.set_facecolor("#0f1117")

    cpk_val = cap.get("cpk")
    if cpk_val is None:
        ax.text(0.5, 0.5, "Ejecute el módulo de Capacidad del proceso",
                ha="center", va="center", color=C_MUTED, fontsize=10,
                transform=ax.transAxes)
        ax.axis("off")
        fig.tight_layout()
        return fig

    # Simular 6 períodos anteriores con variación aleatoria controlada
    rng       = np.random.default_rng(42)
    periodos  = ["P-5", "P-4", "P-3", "P-2", "P-1", "Actual"]
    cpks      = np.clip(rng.normal(cpk_val - 0.05, 0.08, 5), 0.5, 2.5).tolist()
    cpks.append(cpk_val)
    x         = np.arange(len(periodos))
    colores_t = [C_SUCCESS if v >= 1.33 else (C_ACCENT if v >= 1.00 else C_DANGER)
                 for v in cpks]

    ax.bar(x, cpks, color=colores_t, alpha=0.78,
           edgecolor="#0f1117", linewidth=0.5, width=0.55)
    ax.axhline(1.33, color=C_SUCCESS, linewidth=1.2, linestyle="--",
               alpha=0.7, label="Objetivo Cpk=1.33")
    ax.axhline(1.00, color=C_ACCENT,  linewidth=1.0, linestyle=":",
               alpha=0.7, label="Mínimo Cpk=1.00")

    for xi, v in zip(x, cpks):
        ax.text(xi, v + 0.02, f"{v:.2f}", ha="center", fontsize=7.5,
                fontweight="bold", color="#e2e8f0")

    ax.set_xticks(x)
    ax.set_xticklabels(periodos, fontsize=8)
    ax.set_ylim(0, max(cpks) * 1.25)
    ax.set_ylabel("Cpk", fontsize=8)
    ax.set_title("Tendencia de Cpk por período", fontsize=9,
                 fontweight="bold", color="#e2e8f0")
    ax.legend(fontsize=7.5, facecolor="#0f1117", edgecolor="#2a2d3e")
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout(pad=0.4)
    return fig


def _db_fig_costos_mini(cq: dict) -> plt.Figure:
    """Mini dona de costos de calidad para el dashboard."""
    fig, ax = plt.subplots(figsize=(4.2, 3.5))
    fig.patch.set_facecolor("#0f1117")
    ax.set_facecolor("#0f1117")

    prev  = cq.get("prev",  0)
    eval_ = cq.get("eval_", 0)
    fi    = cq.get("fi",    0)
    fe    = cq.get("fe",    0)

    vals   = [prev, eval_, fi, fe]
    labels = ["Prevención", "Evaluación", "F.Internas", "F.Externas"]
    colors = [C_SUCCESS, C_PRIMARY, C_ACCENT, C_DANGER]

    if sum(vals) == 0:
        ax.text(0.5, 0.5, "Sin datos de costos",
                ha="center", va="center", color=C_MUTED, fontsize=9,
                transform=ax.transAxes)
        ax.axis("off")
        fig.tight_layout()
        return fig

    datos_d = [(v, l, c) for v, l, c in zip(vals, labels, colors) if v > 0]
    vs, ls, cs = zip(*datos_d)
    ax.pie(vs, labels=ls, colors=cs,
           autopct=lambda p: f"{p:.0f}%" if p > 4 else "",
           startangle=90,
           wedgeprops=dict(width=0.52, edgecolor="#0f1117", linewidth=1.2),
           textprops=dict(fontsize=7.5, color="#e2e8f0"))

    total = sum(vs)
    ax.text(0, 0, f"${total:,.0f}", ha="center", va="center",
            fontsize=8, fontweight="bold", color="#e2e8f0")
    ax.set_title("Costos de calidad", fontsize=9,
                 fontweight="bold", color="#e2e8f0", pad=8)
    fig.tight_layout(pad=0.3)
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# 11-C  Panel de interpretación integrada y recomendaciones del dashboard
# ─────────────────────────────────────────────────────────────────────────────

def _db_generar_alertas(e: dict) -> list[tuple[str, str, str]]:
    """Genera lista priorizada de alertas activas del sistema CEP.

    Returns:
        Lista de (color, ícono, mensaje) ordenada por severidad.
    """
    alertas = []

    # Estabilidad
    if e["f1_ok"] and e["estable"] is False:
        alertas.append((C_DANGER, "⚡",
            f"Fase 1: proceso **inestable** — {e['n_fuera_f1']} punto(s) fuera de control detectados. "
            "Identifique y elimine causas especiales antes de evaluar capacidad."))
    elif not e["f1_ok"]:
        alertas.append((C_MUTED, "⚪",
            "Fase 1 pendiente. Ejecute el análisis de estabilización para activar este indicador."))

    # Capacidad
    if e["cap_ok"] and e["cpk"] is not None:
        if e["cpk"] < 1.00:
            alertas.append((C_DANGER, "❌",
                f"Capacidad crítica: Cpk = {e['cpk']:.3f}. El proceso NO es capaz. "
                "Alta generación de productos fuera de especificación."))
        elif e["cpk"] < 1.33:
            alertas.append((C_ACCENT, "⚠️",
                f"Capacidad marginal: Cpk = {e['cpk']:.3f}. Proceso en zona de riesgo. "
                "Se requiere mejora para alcanzar el estándar (Cpk ≥ 1.33)."))

    # PNC
    if e["pnc"] is not None and e["pnc"] >= 5.0:
        alertas.append((C_DANGER, "🚫",
            f"% No conformes = {e['pnc']:.2f}%. Nivel crítico de defectos. "
            "Revisar parámetros de mezcla, curado y compactación urgentemente."))
    elif e["pnc"] is not None and e["pnc"] >= 3.0:
        alertas.append((C_ACCENT, "⚠️",
            f"% No conformes = {e['pnc']:.2f}%. Nivel de atención. "
            "Monitorear tendencia y aplicar acciones preventivas."))

    # Costos
    if e["pct_falla"] is not None and e["pct_falla"] >= 60.0:
        alertas.append((C_DANGER, "💸",
            f"Costos de falla = {e['pct_falla']:.1f}% del total. "
            "Impacto crítico en rentabilidad. Fortalecer prevención."))
    elif e["pct_falla"] is not None and e["pct_falla"] >= 40.0:
        alertas.append((C_ACCENT, "⚠️",
            f"Costos de falla = {e['pct_falla']:.1f}% del total. "
            "Nivel elevado. Incrementar inversión en prevención."))

    # Muestreo
    if e["tasa_acept"] is not None and e["tasa_acept"] < 80.0:
        alertas.append((C_DANGER, "📦",
            f"Tasa de aceptación de lotes = {e['tasa_acept']:.1f}%. "
            "Alto rechazo de lotes. Revisar proceso productivo y plan de muestreo."))

    # Sin datos
    if not e["datos_ok"]:
        alertas.append((C_MUTED, "📥",
            "No hay datos cargados. Vaya a **📥 Ingreso de datos** para activar el dashboard."))

    # Si todo bien
    if not alertas or all(a[0] == C_MUTED for a in alertas):
        alertas.append((C_SUCCESS, "✅",
            "El sistema CEP no detecta alertas críticas. "
            "Continúe el monitoreo regular del proceso."))

    return alertas


def _db_generar_recomendaciones(e: dict, score: float) -> list[tuple[str, str, str]]:
    """Recomendaciones automáticas priorizadas según el estado del sistema."""
    recom = []

    if e["f1_ok"] and e["estable"] is False:
        recom.append((C_DANGER, "⚡",
            "Investigar y eliminar causas especiales detectadas en Fase 1 antes de cualquier "
            "otra acción. Use el módulo 🔎 Análisis de causas para identificar la causa raíz."))

    if e["cap_ok"] and e["cpk"] is not None and e["cpk"] < 1.33:
        if e["cpk"] < 1.00:
            recom.append((C_DANGER, "📉",
                "Reducir urgentemente la variabilidad del proceso. Revisar relación agua/cemento, "
                "tiempo de curado y calibración de la mezcladora."))
        else:
            recom.append((C_ACCENT, "🎯",
                f"Ajustar la media del proceso hacia el valor objetivo (Cpk={e['cpk']:.3f} < 1.33). "
                "La variabilidad es controlable; el centrado requiere ajuste."))

    if e["pnc"] is not None and e["pnc"] >= 3.0:
        recom.append((C_DANGER, "🧱",
            f"PNC = {e['pnc']:.2f}%. Revisar granulometría de agregados, dosificación "
            "y proceso de compactación. Implementar inspección al 100% temporalmente."))

    if e["pct_falla"] is not None and e["pct_falla"] >= 40.0:
        recom.append((C_ACCENT, "💰",
            "Incrementar la inversión en prevención (capacitación, mantenimiento preventivo). "
            "Cada $1 en prevención puede ahorrar $4–$10 en costos de falla (principio de Juran)."))

    if e["tasa_acept"] is not None and e["tasa_acept"] < 90.0:
        recom.append((C_ACCENT, "📦",
            f"Tasa de aceptación = {e['tasa_acept']:.1f}%. Revisar el plan de muestreo "
            "y las causas de rechazo. Considere diseñar un plan más estricto (menor AQL)."))

    if score >= 70:
        recom.append((C_SUCCESS, "📋",
            "El proceso opera en un nivel aceptable. Documente las prácticas actuales, "
            "establezca Fase 2 de monitoreo y evalúe reducir costos de evaluación."))

    recom.append((C_PRIMARY, "📈",
        "Implemente las reglas complementarias de Western Electric en Fase 2 para detectar "
        "tendencias y patrones antes de que ocurran defectos."))

    recom.append((C_PRIMARY, "🔬",
        "Realice un estudio GR&R periódico para asegurar que el sistema de medición "
        "no está inflando artificialmente la variabilidad observada."))

    return recom


# ─────────────────────────────────────────────────────────────────────────────
# 11-D  Función principal del dashboard
# ─────────────────────────────────────────────────────────────────────────────

def seccion_dashboard():
    """Dashboard ejecutivo premium del sistema CEP — tipo Power BI industrial.

    Arquitectura en 5 zonas:
    ┌─────────────────────────────────────────────────────────┐
    │  ZONA 0: Banner ejecutivo + Semáforo general            │
    ├─────────────────────────────────────────────────────────┤
    │  ZONA 1: KPI strip (8 métricas conectadas)              │
    ├──────────────────┬──────────────────────────────────────┤
    │  ZONA 2A: Gauge  │  ZONA 2B: Radar 5D                   │
    ├──────────────────┴──────────────────────────────────────┤
    │  ZONA 3: Mini carta X̄ | Tendencia Cpk | Costos         │
    ├─────────────────────────────────────────────────────────┤
    │  ZONA 4: Panel inteligencia — Narrativa + Alertas       │
    ├─────────────────────────────────────────────────────────┤
    │  ZONA 5: Semáforo módulos | Recomendaciones             │
    └─────────────────────────────────────────────────────────┘
    """
    # ── CSS adicional exclusivo del dashboard ─────────────────────────────────
    st.markdown("""
    <style>
    /* ── Banner ejecutivo ─────────────────────────────────────────── */
    .db-banner {
        position: relative; overflow: hidden;
        border-radius: 16px; padding: 26px 30px;
        margin-bottom: 20px;
        border: 1px solid transparent;
    }
    .db-banner::before {
        content: '';
        position: absolute; inset: 0;
        background: linear-gradient(135deg,
            rgba(59,130,246,.12) 0%,
            rgba(16,185,129,.04) 50%,
            rgba(0,0,0,0) 100%);
        pointer-events: none;
    }
    .db-banner-grid {
        display: grid;
        grid-template-columns: 1fr auto;
        align-items: center; gap: 20px;
    }
    .db-banner-title {
        font-size: 1.7rem; font-weight: 800;
        letter-spacing: -.02em; line-height: 1.1;
        margin-bottom: 6px;
    }
    .db-banner-sub {
        font-size: .82rem; color: #94a3b8; line-height: 1.5;
    }
    .db-banner-stats {
        display: flex; gap: 26px; align-items: center;
    }
    .db-stat {
        text-align: center;
    }
    .db-stat-lbl {
        font-size: .58rem; color: #64748b;
        letter-spacing: .12em; text-transform: uppercase;
        font-weight: 600; margin-bottom: 2px;
    }
    .db-stat-val {
        font-family: 'JetBrains Mono', monospace;
        font-size: 2rem; font-weight: 800; line-height: 1;
    }
    .db-stat-divider {
        width: 1px; height: 48px;
        background: rgba(255,255,255,.08);
    }

    /* ── KPI Strip ─────────────────────────────────────────────────── */
    .db-kpi-strip {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 10px; margin-bottom: 18px;
    }
    .db-kpi {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 14px 16px;
        position: relative; overflow: hidden;
        transition: transform .18s, box-shadow .18s;
    }
    .db-kpi:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0,0,0,.4);
    }
    .db-kpi-accent {
        position: absolute; top: 0; left: 0; right: 0; height: 2px;
    }
    .db-kpi-lbl {
        font-size: .6rem; color: #64748b;
        letter-spacing: .1em; text-transform: uppercase;
        font-weight: 600; margin-bottom: 6px;
    }
    .db-kpi-val {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.45rem; font-weight: 700; line-height: 1;
        margin-bottom: 4px;
    }
    .db-kpi-delta {
        font-size: .68rem; font-weight: 600;
        display: flex; align-items: center; gap: 4px;
    }
    .db-kpi-icon {
        position: absolute; right: 12px; top: 14px;
        font-size: 1.4rem; opacity: .18;
    }

    /* ── Semáforo de módulos ────────────────────────────────────────── */
    .db-module-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 8px;
    }
    .db-module-card {
        background: var(--surface);
        border-radius: 10px; padding: 12px 14px;
        display: flex; align-items: center;
        justify-content: space-between;
        border: 1px solid var(--border);
        transition: border-color .18s;
    }
    .db-module-card:hover { border-color: var(--border2); }
    .db-module-name { font-size: .82rem; color: #e2e8f0; font-weight: 500; }
    .db-module-badge {
        font-size: .65rem; font-weight: 700;
        padding: 3px 9px; border-radius: 20px;
        letter-spacing: .06em; text-transform: uppercase;
        white-space: nowrap;
    }

    /* ── Alerta card ──────────────────────────────────────────────── */
    .db-alert {
        display: flex; gap: 13px; align-items: flex-start;
        padding: 12px 15px;
        background: var(--surface);
        border-radius: 10px;
        margin-bottom: 7px;
        box-shadow: 0 1px 3px rgba(0,0,0,.3);
        transition: transform .18s;
    }
    .db-alert:hover { transform: translateX(3px); }
    .db-alert-ico { font-size: 1.15rem; flex-shrink: 0; margin-top: 1px; }
    .db-alert-body { flex: 1; }
    .db-alert-msg { font-size: .84rem; color: #e2e8f0; line-height: 1.5; }
    .db-alert-tag {
        display: inline-block; margin-top: 4px;
        font-size: .6rem; font-weight: 700;
        letter-spacing: .08em; text-transform: uppercase;
        padding: 1px 7px; border-radius: 20px;
    }

    /* ── Narrativa inteligente ─────────────────────────────────────── */
    .db-narrative {
        background: linear-gradient(135deg,
            rgba(59,130,246,.06) 0%,
            rgba(139,92,246,.04) 100%);
        border: 1px solid rgba(59,130,246,.18);
        border-left: 3px solid #3b82f6;
        border-radius: 12px;
        padding: 18px 22px;
        margin-bottom: 14px;
    }
    .db-narrative-title {
        font-size: .68rem; font-weight: 700;
        color: #60a5fa; letter-spacing: .1em;
        text-transform: uppercase; margin-bottom: 10px;
    }
    .db-narrative-body {
        font-size: .88rem; color: #e2e8f0; line-height: 1.7;
    }

    /* ── Recomendación ─────────────────────────────────────────────── */
    .db-recom {
        display: flex; gap: 12px; align-items: flex-start;
        padding: 10px 14px;
        background: var(--surface2);
        border-radius: 9px; margin-bottom: 7px;
        transition: background .18s;
    }
    .db-recom:hover { background: var(--surface3); }
    .db-recom-ico { font-size: 1rem; flex-shrink: 0; margin-top: 2px; }
    .db-recom-txt { font-size: .83rem; color: #e2e8f0; line-height: 1.5; }

    /* ── Sección de zona ──────────────────────────────────────────── */
    .db-zone-title {
        font-size: .62rem; font-weight: 700;
        color: #64748b; letter-spacing: .14em;
        text-transform: uppercase;
        margin: 20px 0 10px;
        display: flex; align-items: center; gap: 8px;
    }
    .db-zone-title::after {
        content: '';
        flex: 1; height: 1px;
        background: linear-gradient(90deg, rgba(59,130,246,.3), transparent);
    }
    </style>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # RECOLECTAR ESTADO DE TODOS LOS MÓDULOS
    # ══════════════════════════════════════════════════════════════════════════
    e       = _db_recolectar_estado()
    score, lbl_score, col_score, ico_score = _db_score_salud(e)
    alertas = _db_generar_alertas(e)
    recom   = _db_generar_recomendaciones(e, score)

    n_criticas = sum(1 for a in alertas if a[0] == C_DANGER)
    n_warning  = sum(1 for a in alertas if a[0] == C_ACCENT)
    n_ok_mods  = sum(1 for a in alertas if a[0] == C_SUCCESS)

    # Timestamp
    ts = pd.Timestamp.now().strftime("%d/%m/%Y %H:%M")

    # ══════════════════════════════════════════════════════════════════════════
    # ZONA 0 — BANNER EJECUTIVO + SEMÁFORO
    # ══════════════════════════════════════════════════════════════════════════
    # Color del banner según estado
    banner_border = f"border-color:{col_score}44"
    banner_glow   = f"box-shadow: 0 0 40px {col_score}18, 0 1px 3px rgba(0,0,0,.4)"

    st.markdown(
        f"""
        <div class="db-banner" style="{banner_border};{banner_glow}">
            <div class="db-banner-grid">
                <div>
                    <div class="db-banner-title" style="color:{col_score}">
                        {ico_score} &nbsp; {lbl_score}
                    </div>
                    <div class="db-banner-sub">
                        Sistema CEP — Manufactura de Bloques de Concreto
                        &nbsp;·&nbsp; Actualizado: {ts}
                        &nbsp;·&nbsp; {e['n_obs']:,} obs. en {e['n_sgs']} subgrupos
                    </div>
                </div>
                <div class="db-banner-stats">
                    <div class="db-stat">
                        <div class="db-stat-lbl">Salud</div>
                        <div class="db-stat-val" style="color:{col_score}">{score:.0f}%</div>
                    </div>
                    <div class="db-stat-divider"></div>
                    <div class="db-stat">
                        <div class="db-stat-lbl">🔴 Crítico</div>
                        <div class="db-stat-val" style="color:{C_DANGER}">{n_criticas}</div>
                    </div>
                    <div class="db-stat-divider"></div>
                    <div class="db-stat">
                        <div class="db-stat-lbl">🟡 Atención</div>
                        <div class="db-stat-val" style="color:{C_ACCENT}">{n_warning}</div>
                    </div>
                    <div class="db-stat-divider"></div>
                    <div class="db-stat">
                        <div class="db-stat-lbl">Módulos</div>
                        <div class="db-stat-val" style="color:#94a3b8">13</div>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ══════════════════════════════════════════════════════════════════════════
    # ZONA 1 — KPI STRIP (8 métricas conectadas con colores dinámicos)
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="db-zone-title">📊 Indicadores clave del proceso</div>',
                unsafe_allow_html=True)

    def _kpi_card(lbl: str, val: str, delta: str, color: str,
                  icon: str = "📊", tag: str = "") -> str:
        """Genera HTML de un KPI premium conectado."""
        tag_html = (
            f'<div class="db-kpi-delta" style="color:{color}">'
            f'<span>{delta}</span></div>'
        ) if delta else ""
        return f"""
        <div class="db-kpi">
            <div class="db-kpi-accent" style="background:linear-gradient(90deg,{color},{color}44)"></div>
            <div class="db-kpi-icon">{icon}</div>
            <div class="db-kpi-lbl">{lbl}</div>
            <div class="db-kpi-val" style="color:{color}">{val}</div>
            {tag_html}
        </div>"""

    # Calcular colores dinámicos según valores reales
    _cp_c  = C_SUCCESS if (e["cp"]  or 0) >= 1.33 else (C_ACCENT if (e["cp"]  or 0) >= 1.0 else C_DANGER)
    _cpk_c = C_SUCCESS if (e["cpk"] or 0) >= 1.33 else (C_ACCENT if (e["cpk"] or 0) >= 1.0 else C_DANGER)
    _pnc_c = C_SUCCESS if (e["pnc"] or 99) < 1.0  else (C_ACCENT if (e["pnc"] or 99) < 5.0 else C_DANGER)
    _est_c = C_SUCCESS if e["estable"] is True else (C_DANGER if e["estable"] is False else C_MUTED)
    _ms_c  = C_SUCCESS if (e["tasa_acept"] or 0) >= 90 else (C_ACCENT if (e["tasa_acept"] or 0) >= 70 else C_DANGER)
    _cq_c  = C_SUCCESS if (e["pct_falla"] or 99) < 30 else (C_ACCENT if (e["pct_falla"] or 99) < 55 else C_DANGER)
    _f1_c  = C_SUCCESS if e["f1_ok"] else C_MUTED
    _sc_c  = col_score

    _cp_d  = "✅ Capaz"   if (e["cp"]  or 0) >= 1.33 else ("⚠️ Marginal" if (e["cp"]  or 0) >= 1.0 else "❌ No capaz")
    _cpk_d = "✅ Capaz"   if (e["cpk"] or 0) >= 1.33 else ("⚠️ Marginal" if (e["cpk"] or 0) >= 1.0 else "❌ No capaz")
    _pnc_d = "✅ Excelente" if (e["pnc"] or 99) < 1.0 else ("⚠️ Moderado" if (e["pnc"] or 99) < 5.0 else "❌ Crítico")
    _est_d = "✅ Estable"   if e["estable"] is True  else ("❌ Inestable" if e["estable"] is False else "⏳ Pendiente")

    # Fila 1: 4 KPIs de capacidad + calidad
    kpi_html_1 = (
        _kpi_card("Índice Cp",
                  f"{e['cp']:.3f}"  if e["cp"]  is not None else "—",
                  _cp_d, _cp_c, "🎯") +
        _kpi_card("Índice Cpk",
                  f"{e['cpk']:.3f}" if e["cpk"] is not None else "—",
                  _cpk_d, _cpk_c, "⚙️") +
        _kpi_card("% No conformes",
                  f"{e['pnc']:.2f}%" if e["pnc"] is not None else "—",
                  _pnc_d, _pnc_c, "🚫") +
        _kpi_card("Estabilidad F1",
                  "Estable" if e["estable"] is True
                  else ("Inestable" if e["estable"] is False else "Pendiente"),
                  f"{e['n_fuera_f1']} pts fuera" if e["f1_ok"] else "Ejecute Fase 1",
                  _est_c, "📊")
    )
    st.markdown(f'<div class="db-kpi-strip">{kpi_html_1}</div>', unsafe_allow_html=True)

    # Fila 2: 4 KPIs de costos + muestreo + score
    _ct_str  = f"${e['costo_falla']:,.0f}" if e["costo_falla"] else "—"
    _ct_d    = f"{e['pct_falla']:.0f}% del total" if e["pct_falla"] else "Sin datos"
    _ms_str  = f"{e['tasa_acept']:.1f}%"   if e["tasa_acept"] is not None else "—"
    _ms_d    = f"{e['n_acept']}/{e['n_lotes']} lotes" if e["n_lotes"] > 0 else "Sin lotes"
    _ah_str  = f"${e['ahorro_pot']:,.0f}"   if e["ahorro_pot"] else "—"
    _sg_str  = f"{score:.0f} / 100"

    kpi_html_2 = (
        _kpi_card("Costos de falla",
                  _ct_str, _ct_d, _cq_c, "💸") +
        _kpi_card("Tasa aceptación lotes",
                  _ms_str, _ms_d, _ms_c, "📦") +
        _kpi_card("Ahorro potencial",
                  _ah_str, "Reducir 90% fallas", C_SUCCESS if e["ahorro_pot"] else C_MUTED, "💡") +
        _kpi_card("Score Global CEP",
                  _sg_str, lbl_score, _sc_c, "🏆")
    )
    st.markdown(f'<div class="db-kpi-strip">{kpi_html_2}</div>', unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # ZONA 2 — GAUGE + RADAR + MINI CARTA X̄
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="db-zone-title">📈 Visualización del estado del proceso</div>',
                unsafe_allow_html=True)

    z2_col1, z2_col2, z2_col3 = st.columns([1.3, 1.6, 2.1])

    with z2_col1:
        st.markdown("##### Salud global")
        fig_gauge = _db_fig_gauge_score(score, col_score)
        st.pyplot(fig_gauge, use_container_width=True)
        plt.close(fig_gauge)

    with z2_col2:
        st.markdown("##### Radar CEP 5D")
        fig_radar = _db_fig_radar_modulos(e)
        st.pyplot(fig_radar, use_container_width=True)
        plt.close(fig_radar)

    with z2_col3:
        st.markdown("##### Carta X̄ en tiempo real")
        fig_xbar = _db_fig_mini_xbar(e["df_sg"], e)
        st.pyplot(fig_xbar, use_container_width=True)
        plt.close(fig_xbar)

    # ══════════════════════════════════════════════════════════════════════════
    # ZONA 3 — TENDENCIA CPK + COSTOS
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="db-zone-title">📉 Tendencias y costos de calidad</div>',
                unsafe_allow_html=True)

    z3_col1, z3_col2 = st.columns([2, 1.2])

    with z3_col1:
        st.markdown("##### Evolución de Cpk por período")
        fig_cpk = _db_fig_tendencia_cpk(st.session_state.get("capacidad", {}))
        st.pyplot(fig_cpk, use_container_width=True)
        plt.close(fig_cpk)

    with z3_col2:
        st.markdown("##### Distribución de costos")
        fig_cq = _db_fig_costos_mini(st.session_state.get("calidad_costos_res", {}))
        st.pyplot(fig_cq, use_container_width=True)
        plt.close(fig_cq)

    # ══════════════════════════════════════════════════════════════════════════
    # ZONA 4 — INTELIGENCIA NARRATIVA (interpretaciones automáticas conectadas)
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="db-zone-title">🧠 Inteligencia del proceso — Narrativa automática</div>',
                unsafe_allow_html=True)

    # Generar narrativa inteligente conectada con TODOS los módulos
    narrativa_partes: list[str] = []

    # 1. Estado general
    if score >= 80:
        narrativa_partes.append(
            f"El sistema CEP reporta un <strong style='color:{C_SUCCESS}'>estado saludable "
            f"({score:.0f}/100)</strong>. El proceso opera dentro de los parámetros de calidad esperados."
        )
    elif score >= 55:
        narrativa_partes.append(
            f"El sistema CEP indica un <strong style='color:{C_ACCENT}'>nivel de atención "
            f"({score:.0f}/100)</strong>. Se detectaron áreas que requieren monitoreo activo."
        )
    else:
        narrativa_partes.append(
            f"El sistema CEP reporta un <strong style='color:{C_DANGER}'>estado crítico "
            f"({score:.0f}/100)</strong>. Se requieren acciones correctivas inmediatas."
        )

    # 2. Estabilidad vs Capacidad — diagnóstico cruzado
    if e["f1_ok"] and e["cap_ok"]:
        if e["estable"] is True and (e["cpk"] or 0) >= 1.33:
            narrativa_partes.append(
                f"El proceso es <strong style='color:{C_SUCCESS}'>estable y capaz</strong> "
                f"(Cpk = {e['cpk']:.3f}). La variabilidad está bajo control estadístico."
            )
        elif e["estable"] is True and (e["cpk"] or 0) < 1.33:
            narrativa_partes.append(
                f"El proceso es <strong style='color:{C_ACCENT}'>estable pero NO capaz</strong> "
                f"(Cpk = {e['cpk']:.3f} &lt; 1.33). La variabilidad inherente supera los límites "
                "de especificación. Se requiere reducción estructural de variabilidad, no solo ajustes."
            )
        elif e["estable"] is False:
            narrativa_partes.append(
                f"El proceso es <strong style='color:{C_DANGER}'>inestable</strong>: "
                f"{e['n_fuera_f1']} punto(s) fuera de control detectados en Fase 1. "
                "La evaluación de capacidad no es confiable hasta eliminar las causas especiales."
            )

    # 3. % PNC conectado con costos
    if e["pnc"] is not None and e["costo_falla"] is not None:
        if e["pnc"] >= 5.0:
            narrativa_partes.append(
                f"El <strong style='color:{C_DANGER}'>porcentaje de defectos es elevado "
                f"({e['pnc']:.2f}%)</strong> y está incrementando los costos de no calidad. "
                f"Los costos de falla ascienden a <strong style='color:{C_DANGER}'>"
                f"${e['costo_falla']:,.0f}</strong> ({e['pct_falla']:.0f}% del presupuesto de calidad)."
            )
        elif e["pnc"] >= 2.0:
            narrativa_partes.append(
                f"El porcentaje de defectos es moderado ({e['pnc']:.2f}%) y contribuye a "
                f"costos de falla de ${e['costo_falla']:,.0f}. Monitorear la tendencia."
            )
        else:
            narrativa_partes.append(
                f"El porcentaje de defectos es bajo ({e['pnc']:.2f}%), "
                "lo que se refleja positivamente en los costos de calidad."
            )
    elif e["pnc"] is not None and e["pnc"] >= 3.0:
        narrativa_partes.append(
            f"El porcentaje de defectos ({e['pnc']:.2f}%) está aumentando. "
            "Ejecute el módulo de Calidad y Costos para evaluar el impacto económico."
        )

    # 4. Muestreo
    if e["tasa_acept"] is not None:
        if e["tasa_acept"] < 80.0:
            narrativa_partes.append(
                f"La <strong style='color:{C_DANGER}'>tasa de aceptación de lotes es baja "
                f"({e['tasa_acept']:.1f}%)</strong>: {e['n_lotes'] - e['n_acept']} de {e['n_lotes']} "
                "lotes fueron rechazados. Esto es consistente con los defectos detectados en proceso."
            )
        elif e["tasa_acept"] >= 95:
            narrativa_partes.append(
                f"La tasa de aceptación de lotes es excelente ({e['tasa_acept']:.1f}%), "
                "confirmando la buena calidad del producto terminado."
            )

    # 5. Ahorro potencial
    if e["ahorro_pot"] and e["ahorro_pot"] > 0:
        narrativa_partes.append(
            f"Eliminar el 90% de los costos de falla actuales liberaría "
            f"<strong style='color:{C_SUCCESS}'>${e['ahorro_pot']:,.0f}</strong> "
            "para reinversión en mejora continua y prevención."
        )

    narrativa_html = " ".join(
        f'<span style="display:inline">{"·" if i > 0 else ""} {p}</span>'
        for i, p in enumerate(narrativa_partes)
    ) if narrativa_partes else (
        "<em style='color:#64748b'>Complete los módulos del sistema para activar "
        "la narrativa inteligente automática.</em>"
    )

    st.markdown(
        f"""
        <div class="db-narrative">
            <div class="db-narrative-title">🤖 Diagnóstico automático integrado</div>
            <div class="db-narrative-body">{narrativa_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ══════════════════════════════════════════════════════════════════════════
    # ZONA 5 — ALERTAS + SEMÁFORO DE MÓDULOS (lado a lado)
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="db-zone-title">🚨 Alertas activas y estado de módulos</div>',
                unsafe_allow_html=True)

    z5_col1, z5_col2 = st.columns([1.4, 1])

    # ── Panel de alertas ──────────────────────────────────────────────────────
    with z5_col1:
        st.markdown("##### Alertas priorizadas del sistema")
        # Ordenar: críticas primero
        alertas_ord = sorted(alertas,
                             key=lambda a: (0 if a[0] == C_DANGER
                                            else 1 if a[0] == C_ACCENT else 2))
        for col_a, ico_a, msg_a in alertas_ord[:6]:   # máx. 6 alertas visibles
            # Determinar etiqueta
            if col_a == C_DANGER:
                tag_bg, tag_txt, tag_lbl = "#ef444422", "#f87171", "CRÍTICO"
            elif col_a == C_ACCENT:
                tag_bg, tag_txt, tag_lbl = "#f59e0b22", "#fbbf24", "ATENCIÓN"
            else:
                tag_bg, tag_txt, tag_lbl = "#22c55e22", "#4ade80", "OK"
            st.markdown(
                f"""
                <div class="db-alert" style="border-left:3px solid {col_a}">
                    <div class="db-alert-ico">{ico_a}</div>
                    <div class="db-alert-body">
                        <div class="db-alert-msg">{msg_a}</div>
                        <div class="db-alert-tag" style="background:{tag_bg};color:{tag_txt}">
                            {tag_lbl}
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ── Semáforo de módulos ───────────────────────────────────────────────────
    with z5_col2:
        st.markdown("##### 🚦 Semáforo de módulos")
        modulos_def = [
            ("📥 Ingreso de datos",  e["datos_ok"],   e["datos_ok"]),
            ("🔍 Validación",        e["f1_ok"],      e["f1_ok"]),
            ("📊 Fase 1",            e["f1_ok"],      e["estable"]),
            ("📈 Fase 2",            e["f1_ok"],      e["estable"]),
            ("⚙️ Capacidad",         e["cap_ok"],     (e["cpk"] or 0) >= 1.33 if e["cap_ok"] else None),
            ("💰 Calidad/Costos",    e["cq_ok"],      (e["pct_falla"] or 99) < 40 if e["cq_ok"] else None),
            ("📦 Muestreo",          e["n_lotes"] > 0, (e["tasa_acept"] or 0) >= 90 if e["n_lotes"] > 0 else None),
            ("🔎 Causas",            True,             True),   # siempre disponible
        ]
        for nom_m, comp_m, ok_m in modulos_def:
            ico_m, bdg_m, col_m = _db_estado_modulo(comp_m, ok_m)
            bg_m = f"{col_m}14"
            st.markdown(
                f"""
                <div class="db-module-card" style="border-color:{col_m}44">
                    <span class="db-module-name">{nom_m}</span>
                    <span class="db-module-badge"
                          style="background:{bg_m};color:{col_m};border:1px solid {col_m}44">
                        {ico_m} {bdg_m}
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ══════════════════════════════════════════════════════════════════════════
    # ZONA 6 — RECOMENDACIONES INTELIGENTES
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="db-zone-title">💡 Recomendaciones automáticas del sistema</div>',
                unsafe_allow_html=True)

    recom_ord = sorted(recom, key=lambda r: (0 if r[0] == C_DANGER
                                              else 1 if r[0] == C_ACCENT else 2))
    n_cols_r = 2
    cols_r   = st.columns(n_cols_r)
    for idx, (col_r, ico_r, txt_r) in enumerate(recom_ord):
        with cols_r[idx % n_cols_r]:
            st.markdown(
                f"""
                <div class="db-recom" style="border-left:3px solid {col_r}">
                    <div class="db-recom-ico">{ico_r}</div>
                    <div class="db-recom-txt">{txt_r[:160]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ══════════════════════════════════════════════════════════════════════════
    # ZONA 7 — RESUMEN EJECUTIVO EXPORTABLE
    # ══════════════════════════════════════════════════════════════════════════
    sep()
    with st.expander("📄 Resumen ejecutivo — Exportar datos del dashboard", expanded=False):
        resumen_rows = [
            {"Indicador": "Timestamp",              "Valor": ts,                                          "Estado": "—"},
            {"Indicador": "Score Global CEP",        "Valor": f"{score:.0f}/100",                          "Estado": lbl_score},
            {"Indicador": "Observaciones",           "Valor": str(e["n_obs"]),                             "Estado": "—"},
            {"Indicador": "Subgrupos",               "Valor": str(e["n_sgs"]),                             "Estado": "—"},
            {"Indicador": "Estabilidad (Fase 1)",    "Valor": str(e["estable"]),                           "Estado": "✅" if e["estable"] else "❌"},
            {"Indicador": "Pts fuera de control",    "Valor": str(e["n_fuera_f1"]),                        "Estado": "OK" if e["n_fuera_f1"] == 0 else "Alerta"},
            {"Indicador": "Cp",                      "Valor": f"{e['cp']:.3f}"  if e["cp"]  else "—",     "Estado": "—"},
            {"Indicador": "Cpk",                     "Valor": f"{e['cpk']:.3f}" if e["cpk"] else "—",     "Estado": "—"},
            {"Indicador": "% PNC",                   "Valor": f"{e['pnc']:.2f}%" if e["pnc"] is not None else "—", "Estado": "—"},
            {"Indicador": "Costo total calidad",     "Valor": f"${e['costo_total']:,.0f}" if e["costo_total"] else "—", "Estado": "—"},
            {"Indicador": "Costos de falla",         "Valor": f"${e['costo_falla']:,.0f}" if e["costo_falla"] else "—", "Estado": "—"},
            {"Indicador": "% Costos de falla",       "Valor": f"{e['pct_falla']:.1f}%"    if e["pct_falla"] else "—",  "Estado": "—"},
            {"Indicador": "Ahorro potencial",        "Valor": f"${e['ahorro_pot']:,.0f}"  if e["ahorro_pot"] else "—", "Estado": "—"},
            {"Indicador": "Lotes inspeccionados",    "Valor": str(e["n_lotes"]),                           "Estado": "—"},
            {"Indicador": "Tasa de aceptación",      "Valor": f"{e['tasa_acept']:.1f}%" if e["tasa_acept"] is not None else "—", "Estado": "—"},
            {"Indicador": "Alertas críticas",        "Valor": str(n_criticas),                             "Estado": "Crítico" if n_criticas > 0 else "OK"},
            {"Indicador": "Alertas atención",        "Valor": str(n_warning),                              "Estado": "—"},
        ]
        df_exec = pd.DataFrame(resumen_rows)
        st.dataframe(df_exec, use_container_width=True, hide_index=True)

        col_dl1, col_dl2 = st.columns(2)
        with col_dl1:
            csv_exec = df_exec.to_csv(index=False).encode("utf-8")
            st.download_button(
                "⬇️ Descargar CSV",
                data=csv_exec,
                file_name=f"dashboard_cep_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
            )
        with col_dl2:
            lines_txt = ["=" * 52, "DASHBOARD CEP — RESUMEN EJECUTIVO",
                         f"Fecha: {ts}", "=" * 52]
            for row in resumen_rows:
                lines_txt.append(f"  {row['Indicador']:.<35} {row['Valor']}")
            lines_txt += ["=" * 52, "ALERTAS ACTIVAS:"]
            for _, ico_a, msg_a in alertas:
                lines_txt.append(f"  {ico_a} {msg_a[:80]}")
            txt_out = "\n".join(lines_txt)
            st.download_button(
                "⬇️ Descargar TXT",
                data=txt_out.encode("utf-8"),
                file_name="dashboard_cep.txt",
                mime="text/plain",
            )
    encabezado(
        "📋", "Dashboard general del sistema CEP",
        "Vista ejecutiva · Score global · KPIs · Semáforo · Alertas · Recomendaciones",
    )

    # ── Recolectar estado ──────────────────────────────────────────────────────
    e     = _db_recolectar_estado()
    score, lbl_score, col_score, ico_score = _db_score_salud(e)
    alertas = _db_generar_alertas(e)
    recom   = _db_generar_recomendaciones(e, score)

    # ══════════════════════════════════════════════════════════════════════════
    # BANNER EJECUTIVO – Semáforo general
    # ══════════════════════════════════════════════════════════════════════════
    n_criticas = sum(1 for a in alertas if a[0] == C_DANGER)
    n_warning  = sum(1 for a in alertas if a[0] == C_ACCENT)

    st.markdown(
        f"""
        <div style="background:linear-gradient(135deg,#0f1117 0%,#1a1d27 100%);
                    border:2px solid {col_score};border-radius:14px;
                    padding:24px 30px;margin-bottom:18px;
                    display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:16px">
            <div>
                <div style="font-size:1.5rem;font-weight:800;color:{col_score};letter-spacing:-.01em">
                    {ico_score} &nbsp; {lbl_score}
                </div>
                <div style="font-size:.88rem;color:#94a3b8;margin-top:6px">
                    Sistema CEP — Bloques de concreto &nbsp;·&nbsp;
                    {e['n_obs']:,} observaciones &nbsp;·&nbsp; {e['n_sgs']} subgrupos
                </div>
            </div>
            <div style="display:flex;gap:22px;flex-wrap:wrap">
                <div style="text-align:center">
                    <div style="font-size:.62rem;color:#64748b;letter-spacing:.1em;
                                text-transform:uppercase">Score</div>
                    <div style="font-size:2.2rem;font-weight:800;color:{col_score};
                                font-family:monospace">{score:.0f}</div>
                </div>
                <div style="text-align:center">
                    <div style="font-size:.62rem;color:#64748b;letter-spacing:.1em;
                                text-transform:uppercase">Alertas 🔴</div>
                    <div style="font-size:2.2rem;font-weight:800;color:{C_DANGER};
                                font-family:monospace">{n_criticas}</div>
                </div>
                <div style="text-align:center">
                    <div style="font-size:.62rem;color:#64748b;letter-spacing:.1em;
                                text-transform:uppercase">Atención 🟡</div>
                    <div style="font-size:2.2rem;font-weight:800;color:{C_ACCENT};
                                font-family:monospace">{n_warning}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ══════════════════════════════════════════════════════════════════════════
    # TABS DEL DASHBOARD
    # ══════════════════════════════════════════════════════════════════════════
    tab_kpi, tab_viz, tab_alert, tab_exec = st.tabs([
        "📊 KPIs del proceso",
        "📈 Visualizaciones",
        "🚨 Alertas y semáforo",
        "📄 Resumen ejecutivo",
    ])

    # ──────────────────────────────────────────────────────────────────────────
    # TAB 1 – KPIs
    # ──────────────────────────────────────────────────────────────────────────
    with tab_kpi:
        st.markdown("### 🎯 Indicadores clave del proceso")

        # Fila 1: Estabilidad y capacidad
        k1, k2, k3, k4, k5 = st.columns(5)

        # Cp
        cp_str   = f"{e['cp']:.3f}"   if e["cp"]   is not None else "—"
        cpk_str  = f"{e['cpk']:.3f}"  if e["cpk"]  is not None else "—"
        pp_str   = f"{e['pp']:.3f}"   if e["pp"]   is not None else "—"
        ppk_str  = f"{e['ppk']:.3f}"  if e["ppk"]  is not None else "—"
        pnc_str  = f"{e['pnc']:.2f}%" if e["pnc"]  is not None else "—"

        k1.metric("Cp",  cp_str,
                  delta="Capaz" if (e["cp"] or 0) >= 1.33 else "No capaz",
                  delta_color="normal" if (e["cp"] or 0) >= 1.33 else "inverse")
        k2.metric("Cpk", cpk_str,
                  delta="Capaz" if (e["cpk"] or 0) >= 1.33 else "No capaz",
                  delta_color="normal" if (e["cpk"] or 0) >= 1.33 else "inverse")
        k3.metric("Pp",  pp_str)
        k4.metric("Ppk", ppk_str)
        k5.metric("% PNC", pnc_str,
                  delta="✅ < 1%" if (e["pnc"] or 99) < 1 else
                        ("⚠️ Atención" if (e["pnc"] or 99) < 5 else "❌ Crítico"),
                  delta_color="normal" if (e["pnc"] or 99) < 3 else "inverse")

        sep()

        # Fila 2: Estabilidad y monitoreo
        k6, k7, k8, k9, k10 = st.columns(5)
        est_str = ("✅ Estable" if e["estable"] is True
                   else ("❌ Inestable" if e["estable"] is False else "—"))
        k6.metric("Estabilidad (F1)",    est_str)
        k7.metric("Puntos fuera ctrl",   str(e["n_fuera_f1"]) if e["f1_ok"] else "—",
                  delta="✅ OK" if e["n_fuera_f1"] == 0 and e["f1_ok"] else
                        ("❌ Ver F1" if e["f1_ok"] else "—"),
                  delta_color="normal" if e["n_fuera_f1"] == 0 else "inverse")
        k8.metric("Carta usada",         e["tipo_carta"] if e["f1_ok"] else "—")
        k9.metric("σ estimado (F1)",
                  f"{e['sigma_est']:.4f}" if e["sigma_est"] else "—")
        k10.metric("Score Global",       f"{score:.0f} / 100",
                   delta=lbl_score,
                   delta_color="normal" if score >= 70 else "inverse")

        sep()

        # Fila 3: Costos y muestreo
        k11, k12, k13, k14, k15 = st.columns(5)
        k11.metric("Costo total calidad",
                   f"${e['costo_total']:,.0f}" if e["costo_total"] else "—")
        k12.metric("Costos de falla",
                   f"${e['costo_falla']:,.0f}" if e["costo_falla"] else "—",
                   delta=f"{e['pct_falla']:.1f}% del total" if e["pct_falla"] else "—",
                   delta_color="inverse" if (e["pct_falla"] or 0) > 40 else "normal")
        k13.metric("Ahorro potencial",
                   f"${e['ahorro_pot']:,.0f}" if e["ahorro_pot"] else "—")
        k14.metric("Lotes inspeccionados", str(e["n_lotes"]) if e["n_lotes"] > 0 else "—")
        k15.metric("Tasa de aceptación",
                   f"{e['tasa_acept']:.1f}%" if e["tasa_acept"] is not None else "—",
                   delta="✅ Buena" if (e["tasa_acept"] or 0) >= 90 else "⚠️ Revisar",
                   delta_color="normal" if (e["tasa_acept"] or 0) >= 90 else "inverse")

        sep()

        # Semáforo de módulos
        st.markdown("### 🚦 Estado de módulos del sistema CEP")
        modulos = [
            ("📥 Ingreso de datos",     e["datos_ok"],      e["datos_ok"]),
            ("🔍 Validación estad.",     e["f1_ok"],         e["f1_ok"]),
            ("📊 Fase 1 – Estabil.",     e["f1_ok"],         e["estable"]),
            ("⚙️ Capacidad proceso",     e["cap_ok"],        (e["cpk"] or 0) >= 1.33 if e["cap_ok"] else None),
            ("💰 Calidad y Costos",      e["cq_ok"],         (e["pct_falla"] or 99) < 40 if e["cq_ok"] else None),
            ("📦 Muestreo de acept.",    e["n_lotes"] > 0,   (e["tasa_acept"] or 0) >= 90 if e["n_lotes"] > 0 else None),
        ]
        cols_sm = st.columns(3)
        for idx, (nombre, completado, ok) in enumerate(modulos):
            ico_m, bdg_m, col_m = _db_estado_modulo(completado, ok)
            with cols_sm[idx % 3]:
                st.markdown(
                    f"""
                    <div style="background:#1a1d27;border:1px solid {col_m};
                                border-radius:9px;padding:12px 14px;margin-bottom:8px;
                                display:flex;align-items:center;justify-content:space-between">
                        <span style="font-size:.86rem;color:#e2e8f0;font-weight:500">{nombre}</span>
                        <span style="background:{col_m}22;color:{col_m};border:1px solid {col_m};
                                     border-radius:6px;padding:2px 8px;font-size:.72rem;
                                     font-weight:700">{ico_m} {bdg_m}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # ──────────────────────────────────────────────────────────────────────────
    # TAB 2 – Visualizaciones
    # ──────────────────────────────────────────────────────────────────────────
    with tab_viz:
        st.markdown("### 📈 Panel visual del proceso")

        # Fila 1: Gauge + Radar
        v1, v2 = st.columns([1.5, 2])
        with v1:
            st.markdown("#### Score Global de Salud")
            fig_gauge = _db_fig_gauge_score(score, col_score)
            st.pyplot(fig_gauge, use_container_width=True)
            plt.close(fig_gauge)
        with v2:
            st.markdown("#### Radar de dimensiones CEP")
            fig_radar = _db_fig_radar_modulos(e)
            st.pyplot(fig_radar, use_container_width=True)
            plt.close(fig_radar)

        sep()

        # Fila 2: Mini carta X̄ + tendencia Cpk
        v3, v4 = st.columns(2)
        with v3:
            st.markdown("#### Mini carta X̄")
            fig_xbar = _db_fig_mini_xbar(e["df_sg"], e)
            st.pyplot(fig_xbar, use_container_width=True)
            plt.close(fig_xbar)
        with v4:
            st.markdown("#### Tendencia de Cpk por período")
            fig_cpk = _db_fig_tendencia_cpk(st.session_state.get("capacidad", {}))
            st.pyplot(fig_cpk, use_container_width=True)
            plt.close(fig_cpk)

        sep()

        # Fila 3: Mini costos
        v5, v6 = st.columns([1, 2])
        with v5:
            st.markdown("#### Distribución de costos")
            cq_datos = st.session_state.get("calidad_costos_res", {})
            fig_cq = _db_fig_costos_mini(cq_datos)
            st.pyplot(fig_cq, use_container_width=True)
            plt.close(fig_cq)
        with v6:
            st.markdown("#### Índices de capacidad")
            if e["cap_ok"]:
                ic1, ic2, ic3, ic4 = st.columns(4)
                for col_ic, nom_ic, val_ic in [
                    (ic1, "Cp",  e["cp"]),
                    (ic2, "Cpk", e["cpk"]),
                    (ic3, "Pp",  e["pp"]),
                    (ic4, "Ppk", e["ppk"]),
                ]:
                    if val_ic is not None:
                        lbl_ic, col_ic_c, ico_ic = _nivel_capacidad(val_ic)
                        col_ic.markdown(
                            f"""<div class="m-card" style="border-color:{col_ic_c}33">
                                <div class="m-lbl">{nom_ic}</div>
                                <div class="m-val" style="color:{col_ic_c}">{val_ic:.3f}</div>
                                <div class="m-note">{ico_ic} {lbl_ic}</div>
                            </div>""",
                            unsafe_allow_html=True,
                        )
            else:
                caja("Ejecute el módulo ⚙️ Capacidad del proceso para ver los índices aquí.",
                     tipo="info")

    # ──────────────────────────────────────────────────────────────────────────
    # TAB 3 – Alertas y semáforo
    # ──────────────────────────────────────────────────────────────────────────
    with tab_alert:
        st.markdown("### 🚨 Alertas activas del sistema")

        if not alertas:
            st.success("✅ No hay alertas activas. El sistema opera correctamente.")
        else:
            for col_a, ico_a, msg_a in alertas:
                st.markdown(
                    f"""
                    <div style="display:flex;gap:14px;align-items:flex-start;
                                padding:12px 16px;background:#1a1d27;border-radius:9px;
                                border-left:4px solid {col_a};margin-bottom:8px">
                        <span style="font-size:1.25rem;flex-shrink:0">{ico_a}</span>
                        <span style="font-size:.87rem;color:#e2e8f0">{msg_a}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        sep()
        st.markdown("### 🔧 Recomendaciones priorizadas del sistema")
        for col_r, ico_r, msg_r in recom:
            st.markdown(
                f"""
                <div style="display:flex;gap:12px;align-items:flex-start;
                            padding:10px 15px;background:#1a1d27;border-radius:8px;
                            border-left:3px solid {col_r};margin-bottom:7px">
                    <span style="font-size:1.1rem;flex-shrink:0">{ico_r}</span>
                    <span style="font-size:.86rem;color:#e2e8f0">{msg_r}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ──────────────────────────────────────────────────────────────────────────
    # TAB 4 – Resumen ejecutivo
    # ──────────────────────────────────────────────────────────────────────────
    with tab_exec:
        st.markdown("### 📄 Resumen ejecutivo del sistema CEP")

        fecha_str = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")
        st.markdown(
            f"""
            <div style="background:#1a1d27;border:1px solid #2a2d3e;border-radius:12px;
                        padding:22px 26px;margin-bottom:16px">
                <div style="font-size:1.05rem;font-weight:700;color:#e2e8f0;margin-bottom:12px">
                    📋 Informe ejecutivo de calidad — {fecha_str}
                </div>
                <table style="width:100%;border-collapse:collapse;font-size:.84rem;color:#e2e8f0">
                    <tr style="border-bottom:1px solid #2a2d3e">
                        <td style="padding:6px 8px;color:#64748b;width:40%">Score global CEP</td>
                        <td style="padding:6px 8px;font-weight:700;color:{col_score}">{score:.0f}/100 — {lbl_score}</td>
                    </tr>
                    <tr style="border-bottom:1px solid #2a2d3e">
                        <td style="padding:6px 8px;color:#64748b">Observaciones analizadas</td>
                        <td style="padding:6px 8px">{e['n_obs']:,} ({e['n_sgs']} subgrupos)</td>
                    </tr>
                    <tr style="border-bottom:1px solid #2a2d3e">
                        <td style="padding:6px 8px;color:#64748b">Estabilidad del proceso</td>
                        <td style="padding:6px 8px">{"✅ Estable" if e["estable"] is True else ("❌ Inestable" if e["estable"] is False else "Pendiente")}</td>
                    </tr>
                    <tr style="border-bottom:1px solid #2a2d3e">
                        <td style="padding:6px 8px;color:#64748b">Índice Cpk</td>
                        <td style="padding:6px 8px">{f"{e['cpk']:.3f}" if e["cpk"] else "Pendiente"}</td>
                    </tr>
                    <tr style="border-bottom:1px solid #2a2d3e">
                        <td style="padding:6px 8px;color:#64748b">% Productos no conformes</td>
                        <td style="padding:6px 8px">{f"{e['pnc']:.2f}%" if e["pnc"] is not None else "Pendiente"}</td>
                    </tr>
                    <tr style="border-bottom:1px solid #2a2d3e">
                        <td style="padding:6px 8px;color:#64748b">Costo total de calidad</td>
                        <td style="padding:6px 8px">{f"${e['costo_total']:,.0f}" if e["costo_total"] else "Pendiente"}</td>
                    </tr>
                    <tr style="border-bottom:1px solid #2a2d3e">
                        <td style="padding:6px 8px;color:#64748b">Costos de falla</td>
                        <td style="padding:6px 8px">{f"${e['costo_falla']:,.0f} ({e['pct_falla']:.1f}%)" if e["costo_falla"] else "Pendiente"}</td>
                    </tr>
                    <tr style="border-bottom:1px solid #2a2d3e">
                        <td style="padding:6px 8px;color:#64748b">Lotes inspeccionados</td>
                        <td style="padding:6px 8px">{e['n_lotes']} ({f"{e['tasa_acept']:.1f}% aceptados" if e["tasa_acept"] is not None else "sin evaluaciones"})</td>
                    </tr>
                    <tr>
                        <td style="padding:6px 8px;color:#64748b">Alertas activas</td>
                        <td style="padding:6px 8px;color:{C_DANGER}">{n_criticas} crítica(s) · {n_warning} advertencia(s)</td>
                    </tr>
                </table>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Exportar resumen como CSV
        resumen_rows = [
            {"Indicador": "Score Global CEP",        "Valor": f"{score:.0f}/100",          "Estado": lbl_score},
            {"Indicador": "Observaciones",            "Valor": str(e["n_obs"]),              "Estado": "—"},
            {"Indicador": "Subgrupos",                "Valor": str(e["n_sgs"]),              "Estado": "—"},
            {"Indicador": "Estabilidad (Fase 1)",     "Valor": str(e["estable"]),            "Estado": "✅" if e["estable"] else "❌"},
            {"Indicador": "Puntos fuera de control",  "Valor": str(e["n_fuera_f1"]),         "Estado": "OK" if e["n_fuera_f1"]==0 else "Alerta"},
            {"Indicador": "Cp",                       "Valor": f"{e['cp']:.3f}"   if e["cp"]   else "—", "Estado": "—"},
            {"Indicador": "Cpk",                      "Valor": f"{e['cpk']:.3f}"  if e["cpk"]  else "—", "Estado": "—"},
            {"Indicador": "% PNC",                    "Valor": f"{e['pnc']:.2f}%" if e["pnc"] is not None else "—", "Estado": "—"},
            {"Indicador": "Costo total calidad",      "Valor": f"${e['costo_total']:,.0f}" if e["costo_total"] else "—", "Estado": "—"},
            {"Indicador": "Costos de falla",          "Valor": f"${e['costo_falla']:,.0f}" if e["costo_falla"] else "—", "Estado": "—"},
            {"Indicador": "% Costos de falla",        "Valor": f"{e['pct_falla']:.1f}%" if e["pct_falla"] else "—", "Estado": "—"},
            {"Indicador": "Ahorro potencial",         "Valor": f"${e['ahorro_pot']:,.0f}" if e["ahorro_pot"] else "—", "Estado": "—"},
            {"Indicador": "Lotes inspeccionados",     "Valor": str(e["n_lotes"]),            "Estado": "—"},
            {"Indicador": "Tasa de aceptación",       "Valor": f"{e['tasa_acept']:.1f}%" if e["tasa_acept"] is not None else "—", "Estado": "—"},
            {"Indicador": "Alertas críticas",         "Valor": str(n_criticas),              "Estado": "Crítico" if n_criticas > 0 else "OK"},
        ]
        df_exec = pd.DataFrame(resumen_rows)
        st.dataframe(df_exec, use_container_width=True, hide_index=True)
        csv_exec = df_exec.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Descargar resumen ejecutivo CSV",
            data=csv_exec,
            file_name=f"resumen_cep_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
        )


# ══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 12 – Recomendaciones
# Sistema completo de recomendaciones, plan de acción PDCA y síntesis final
# ══════════════════════════════════════════════════════════════════════════════

def seccion_recomendaciones():
    """Sección de recomendaciones integradas, plan de acción y ciclo PDCA.

    Lee el estado de todos los módulos y genera:
    - Síntesis de hallazgos por área.
    - Plan de acción priorizado (tabla).
    - Ciclo PHVA interactivo.
    - Exportación de informe.
    """
    encabezado(
        "💡", "Recomendaciones y plan de acción",
        "Síntesis CEP · Acciones correctivas · Ciclo PHVA · Mejora continua",
    )

    e       = _db_recolectar_estado()
    score, lbl_score, col_score, ico_score = _db_score_salud(e)
    alertas = _db_generar_alertas(e)
    recom   = _db_generar_recomendaciones(e, score)

    # ── Banner de score ────────────────────────────────────────────────────────
    caja(
        f"**Score Global CEP: {score:.0f}/100 — {lbl_score}**. "
        f"Alertas activas: {sum(1 for a in alertas if a[0]==C_DANGER)} crítica(s) · "
        f"{sum(1 for a in alertas if a[0]==C_ACCENT)} advertencia(s).",
        tipo="success" if score >= 70 else ("warning" if score >= 40 else "error"),
    )

    sep()

    # ── Síntesis de hallazgos ──────────────────────────────────────────────────
    st.markdown("### 🔍 Síntesis de hallazgos por área")
    hallazgos = [
        ("📊 Estabilidad",   e["f1_ok"],        e["estable"],
         f"Carta {e['tipo_carta']} · {e['n_fuera_f1']} pts fuera",
         "Ejecute Fase 1" if not e["f1_ok"] else ("✅ Estable" if e["estable"] else "❌ Inestable")),
        ("⚙️ Capacidad",     e["cap_ok"],        (e["cpk"] or 0) >= 1.33,
         f"Cpk={e['cpk']:.3f}  Cp={e['cp']:.3f}" if e["cap_ok"] else "—",
         "Ejecute Capacidad" if not e["cap_ok"] else
         ("✅ Capaz" if (e["cpk"] or 0) >= 1.33 else "❌ No capaz")),
        ("🚫 Defectos PNC",  e["pnc"] is not None, (e["pnc"] or 99) < 3.0,
         f"PNC = {e['pnc']:.2f}%" if e["pnc"] is not None else "—",
         "Sin datos" if e["pnc"] is None else
         ("✅ Bajo" if (e["pnc"] or 99) < 1 else ("⚠️ Moderado" if (e["pnc"] or 99) < 5 else "❌ Alto"))),
        ("💰 Costos",        e["cq_ok"],        (e["pct_falla"] or 99) < 40,
         f"${e['costo_total']:,.0f}  Falla={e['pct_falla']:.1f}%" if e["cq_ok"] else "—",
         "Ejecute Costos" if not e["cq_ok"] else
         ("✅ Controlados" if (e["pct_falla"] or 99) < 40 else "❌ Elevados")),
        ("📦 Muestreo",      e["n_lotes"] > 0,  (e["tasa_acept"] or 0) >= 90,
         f"{e['n_lotes']} lotes · {e['tasa_acept']:.1f}% aceptados" if e["n_lotes"] > 0 else "—",
         "Sin lotes" if e["n_lotes"] == 0 else
         ("✅ Buena" if (e["tasa_acept"] or 0) >= 90 else "⚠️ Revisar")),
    ]

    cols_h = st.columns(len(hallazgos))
    for col_h, (nom, comp, ok, detalle, estado) in zip(cols_h, hallazgos):
        col_ok = C_SUCCESS if (comp and ok) else (C_ACCENT if comp else C_MUTED)
        col_h.markdown(
            f"""
            <div class="m-card" style="border-color:{col_ok}33;min-height:110px">
                <div class="m-lbl">{nom}</div>
                <div class="m-val" style="color:{col_ok};font-size:.9rem">{estado}</div>
                <div class="m-note" style="font-size:.66rem">{detalle}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    sep()

    # ── Plan de acción priorizado ─────────────────────────────────────────────
    st.markdown("### ✅ Plan de acción priorizado")
    caja(
        "Las acciones están ordenadas por prioridad (Crítica → Alta → Media). "
        "Descargue la tabla para gestionar el plan de mejora.",
        tipo="info",
    )

    plan_rows = []
    prioridad_num = {"Crítica": 1, "Alta": 2, "Media": 3}
    for col_r, ico_r, msg_r in recom:
        prio = "Crítica" if col_r == C_DANGER else ("Alta" if col_r == C_ACCENT else "Media")
        plan_rows.append({
            "Prioridad":   f"{ico_r} {prio}",
            "Acción":      msg_r[:120],
            "Módulo CEP":  ("Fase 1/2" if "estab" in msg_r.lower() or "control" in msg_r.lower()
                            else "Capacidad" if "variab" in msg_r.lower() or "cpk" in msg_r.lower()
                            else "Costos" if "costo" in msg_r.lower() or "falla" in msg_r.lower()
                            else "Muestreo" if "lote" in msg_r.lower() or "aql" in msg_r.lower()
                            else "General"),
            "Estado":      "⏳ Pendiente",
        })

    df_plan = pd.DataFrame(plan_rows)
    st.dataframe(df_plan, use_container_width=True, hide_index=True)
    csv_plan = df_plan.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Descargar plan de acción CSV",
                       csv_plan, "plan_accion_cep.csv", "text/csv")

    sep()

    # ── Ciclo PHVA ────────────────────────────────────────────────────────────
    st.markdown("### 🔄 Ciclo PHVA de mejora continua")
    pdca_data = [
        ("🔵", "PLANEAR",
         f"Score actual: {score:.0f}/100. Identificar las {sum(1 for a in alertas if a[0]==C_DANGER)} "
         f"alertas críticas y establecer metas de mejora (Cpk ≥ 1.33, PNC < 1%, Costos falla < 40%).",
         C_PRIMARY),
        ("🟢", "HACER",
         "Implementar las acciones priorizadas del plan: reducir variabilidad, "
         "calibrar maquinaria, estandarizar procedimientos de mezcla y curado.",
         C_SUCCESS),
        ("🟡", "VERIFICAR",
         "Re-ejecutar Fase 1 y Capacidad con nuevos datos. Comparar Cpk antes/después. "
         "Evaluar reducción del %PNC y de los costos de falla.",
         C_ACCENT),
        ("🔴", "ACTUAR",
         "Si hay mejora: documentar como estándar y extender a otras líneas. "
         "Si no: replantear hipótesis de causa raíz y ajustar plan de acción.",
         C_DANGER),
    ]
    for ico_p, fase_p, desc_p, col_p in pdca_data:
        st.markdown(
            f"""
            <div style="display:flex;gap:16px;align-items:flex-start;padding:14px 18px;
                        background:#1a1d27;border-radius:10px;
                        border-left:4px solid {col_p};margin-bottom:8px">
                <div style="font-size:1.6rem;flex-shrink:0">{ico_p}</div>
                <div>
                    <div style="font-size:.95rem;font-weight:700;color:{col_p};
                                letter-spacing:.06em">{fase_p}</div>
                    <div style="font-size:.84rem;color:#e2e8f0;margin-top:4px">{desc_p}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    sep()

    # ── Exportar informe ──────────────────────────────────────────────────────
    st.markdown("### 📄 Exportar informe")
    caja(
        "Descargue el resumen ejecutivo completo desde el módulo "
        "**📋 Dashboard general → Pestaña Resumen ejecutivo**.",
        tipo="info",
    )
    ec1, ec2, ec3 = st.columns(3)
    with ec1:
        st.button("📊 Ir al Dashboard", use_container_width=True,
                  help="Acceda al resumen ejecutivo completo con descarga CSV.")
    with ec2:
        if st.button("📑 Generar resumen TXT", use_container_width=True):
            lines = [
                "=" * 50,
                "SISTEMA CEP — INFORME EJECUTIVO",
                f"Fecha: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}",
                "=" * 50,
                f"Score Global: {score:.0f}/100 — {lbl_score}",
                f"Observaciones: {e['n_obs']:,} | Subgrupos: {e['n_sgs']}",
                f"Estabilidad: {e['estable']}",
                f"Cpk: {e['cpk']:.3f if e['cpk'] else 'N/D'}",
                f"% PNC: {e['pnc']:.2f}% {e['pnc'] if e['pnc'] else 'N/D'}",
                f"Alertas críticas: {sum(1 for a in alertas if a[0]==C_DANGER)}",
                "=" * 50,
                "RECOMENDACIONES:",
            ] + [f"  [{('CRI' if c==C_DANGER else 'ALT' if c==C_ACCENT else 'MED')}] {m[:80]}"
                 for c, _, m in recom]
            txt_out = "\n".join(lines)
            st.download_button("⬇️ Descargar .txt", txt_out.encode("utf-8"),
                               "informe_cep.txt", "text/plain")
    with ec3:
        st.button("📧 Copiar al portapapeles",
                  use_container_width=True,
                  help="Funcionalidad disponible en entorno de escritorio.")


# ══════════════════════════════════════════════════════════════════════════════
# 6. SIDEBAR + ENRUTADOR PRINCIPAL
# ══════════════════════════════════════════════════════════════════════════════

# Mapa: etiqueta del sidebar → función de la sección
# ══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 13 – Calidad y Costos
# ══════════════════════════════════════════════════════════════════════════════

# ── Paleta local (reutiliza las constantes de la sección de validación) ────────
_CQ_GREEN  = "#22c55e"
_CQ_YELLOW = "#f59e0b"
_CQ_RED    = "#ef4444"
_CQ_BLUE   = "#3b82f6"
_CQ_PURPLE = "#818cf8"
_CQ_BG     = "#0f1117"
_CQ_SURF   = "#1a1d27"
_CQ_BORDER = "#2a2d3e"
_CQ_MUTED  = "#64748b"
_CQ_TEXT   = "#e2e8f0"


# ── Helpers de cálculo ─────────────────────────────────────────────────────────

def _cq_calcular_pnc(produccion: float, defectuosos: float) -> dict:
    """Calcula métricas de productos no conformes.

    Args:
        produccion:   total de unidades producidas.
        defectuosos:  unidades defectuosas.

    Returns:
        dict con pnc_pct, conformes, defectuosos, produccion.
    """
    if produccion <= 0:
        return {"error": "La producción total debe ser mayor a 0."}
    if defectuosos < 0:
        return {"error": "Los productos defectuosos no pueden ser negativos."}
    if defectuosos > produccion:
        return {"error": "Los productos defectuosos no pueden superar la producción total."}

    pnc_pct   = (defectuosos / produccion) * 100.0
    conformes = produccion - defectuosos
    return {
        "produccion":  produccion,
        "defectuosos": defectuosos,
        "conformes":   conformes,
        "pnc_pct":     round(pnc_pct, 3),
    }


def _cq_calcular_costos(prev: float, eval_: float,
                         fi: float, fe: float) -> dict:
    """Calcula todos los indicadores de costos de calidad.

    Args:
        prev:  costos de prevención.
        eval_: costos de evaluación.
        fi:    costos de fallas internas.
        fe:    costos de fallas externas.

    Returns:
        dict con totales, porcentajes y ratios.
    """
    for nombre, valor in [("Prevención", prev), ("Evaluación", eval_),
                           ("Fallas internas", fi), ("Fallas externas", fe)]:
        if valor < 0:
            return {"error": f"El costo de {nombre} no puede ser negativo."}

    costo_control    = prev + eval_              # Costos de control (inversión)
    costo_falla      = fi + fe                  # Costos de falla (pérdida)
    costo_total      = costo_control + costo_falla

    if costo_total <= 0:
        return {"error": "Al menos un costo debe ser mayor a 0."}

    pct_prev  = prev  / costo_total * 100
    pct_eval  = eval_ / costo_total * 100
    pct_fi    = fi    / costo_total * 100
    pct_fe    = fe    / costo_total * 100
    pct_ctrl  = costo_control / costo_total * 100
    pct_falla = costo_falla   / costo_total * 100

    # Ratio óptimo: prevención ≥ 50% del costo de control sugiere madurez
    ratio_prev_ctrl = (prev / costo_control * 100) if costo_control > 0 else 0.0

    # Ahorro potencial: si se reducen fallas al 10% del nivel actual
    ahorro_potencial = costo_falla * 0.90

    return {
        "prev":              prev,
        "eval_":             eval_,
        "fi":                fi,
        "fe":                fe,
        "costo_control":     round(costo_control, 2),
        "costo_falla":       round(costo_falla, 2),
        "costo_total":       round(costo_total, 2),
        "pct_prev":          round(pct_prev, 2),
        "pct_eval":          round(pct_eval, 2),
        "pct_fi":            round(pct_fi, 2),
        "pct_fe":            round(pct_fe, 2),
        "pct_control":       round(pct_ctrl, 2),
        "pct_falla":         round(pct_falla, 2),
        "ratio_prev_ctrl":   round(ratio_prev_ctrl, 2),
        "ahorro_potencial":  round(ahorro_potencial, 2),
    }


def _cq_nivel_pnc(pnc: float) -> tuple[str, str, str]:
    """Devuelve (etiqueta, color, ícono) según el %PNC."""
    if pnc < 1.0:
        return "Excelente",  _CQ_GREEN,  "✅"
    if pnc < 3.0:
        return "Aceptable",  _CQ_GREEN,  "✅"
    if pnc < 5.0:
        return "Atención",   _CQ_YELLOW, "⚠️"
    if pnc < 10.0:
        return "Crítico",    _CQ_RED,    "❌"
    return "Muy crítico",    _CQ_RED,    "🔴"


def _cq_nivel_falla(pct_falla: float) -> tuple[str, str, str]:
    """Devuelve (etiqueta, color, ícono) según % de costos de falla sobre total."""
    if pct_falla < 20.0:
        return "Óptimo",    _CQ_GREEN,  "✅"
    if pct_falla < 40.0:
        return "Aceptable", _CQ_GREEN,  "✅"
    if pct_falla < 60.0:
        return "Elevado",   _CQ_YELLOW, "⚠️"
    return "Muy elevado",   _CQ_RED,    "❌"


# ── Funciones de graficación ───────────────────────────────────────────────────

def _cq_fig_barras_costos(res_c: dict) -> plt.Figure:
    """Gráfico de barras de las cuatro categorías de costos con gradiente de color."""
    categorias = ["Prevención", "Evaluación", "Fallas internas", "Fallas externas"]
    valores    = [res_c["prev"], res_c["eval_"], res_c["fi"], res_c["fe"]]
    colores    = [_CQ_GREEN, _CQ_BLUE, _CQ_YELLOW, _CQ_RED]
    pcts       = [res_c["pct_prev"], res_c["pct_eval"], res_c["pct_fi"], res_c["pct_fe"]]

    fig, ax = plt.subplots(figsize=(9, 4.2))

    bars = ax.bar(categorias, valores, color=colores, alpha=0.85,
                  edgecolor=_CQ_BG, linewidth=0.8, width=0.55)

    # Etiquetas de valor y porcentaje sobre cada barra
    for bar, val, pct in zip(bars, valores, pcts):
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + max(valores) * 0.01,
                f"${val:,.0f}\n({pct:.1f}%)",
                ha="center", va="bottom", fontsize=8.5,
                color=_CQ_TEXT, fontweight="bold")

    # Línea de referencia: promedio de costos de falla
    falla_avg = (res_c["fi"] + res_c["fe"]) / 2
    ax.axhline(falla_avg, color=_CQ_RED, linestyle="--",
               linewidth=1.2, alpha=0.6, label=f"Prom. fallas = ${falla_avg:,.0f}")

    ax.set_title("Distribución de costos de calidad por categoría",
                 fontsize=11, fontweight="bold", pad=10)
    ax.set_ylabel("Costo (COP $)", fontsize=9)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    ax.legend(fontsize=8, facecolor=_CQ_BG, edgecolor=_CQ_BORDER)
    ax.grid(True, axis="y", alpha=0.4)
    ax.set_ylim(0, max(valores) * 1.22)
    fig.tight_layout()
    return fig


def _cq_fig_dona_costos(res_c: dict) -> plt.Figure:
    """Gráfico de dona con distribución porcentual de costos."""
    categorias = ["Prevención", "Evaluación", "Fallas internas", "Fallas externas"]
    valores    = [res_c["prev"], res_c["eval_"], res_c["fi"], res_c["fe"]]
    colores    = [_CQ_GREEN, _CQ_BLUE, _CQ_YELLOW, _CQ_RED]
    explode    = [0.0, 0.0, 0.05, 0.08]

    # Filtrar categorías vacías
    datos_d = [(v, l, c, e) for v, l, c, e in
               zip(valores, categorias, colores, explode) if v > 0]
    if not datos_d:
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.text(0.5, 0.5, "Sin datos", ha="center", va="center",
                color=_CQ_MUTED, fontsize=12, transform=ax.transAxes)
        fig.tight_layout()
        return fig

    vs, ls, cs, es = zip(*datos_d)

    fig, ax = plt.subplots(figsize=(6, 4.5))
    wedges, texts, autotexts = ax.pie(
        vs, labels=ls, colors=cs, explode=es,
        autopct=lambda p: f"{p:.1f}%" if p > 2 else "",
        startangle=90,
        wedgeprops=dict(width=0.55, edgecolor=_CQ_BG, linewidth=1.5),
        textprops=dict(fontsize=8.5, color=_CQ_TEXT),
    )
    for at in autotexts:
        at.set_fontsize(8)
        at.set_fontweight("bold")
        at.set_color(_CQ_BG)

    # Centro de la dona
    total = sum(vs)
    ax.text(0, 0, f"${total:,.0f}\nTotal", ha="center", va="center",
            fontsize=9, fontweight="bold", color=_CQ_TEXT)

    ax.set_title("Distribución % de costos de calidad",
                 fontsize=11, fontweight="bold", pad=10)
    fig.tight_layout()
    return fig


def _cq_fig_control_vs_falla(res_c: dict) -> plt.Figure:
    """Gráfico de barras horizontales: costos de control vs. costos de falla."""
    fig, ax = plt.subplots(figsize=(8, 2.8))

    total = res_c["costo_total"]
    ctrl  = res_c["costo_control"]
    falla = res_c["costo_falla"]

    pct_ctrl  = ctrl  / total * 100
    pct_falla = falla / total * 100

    ax.barh(["Costos"], [pct_ctrl],  color=_CQ_GREEN,  alpha=0.85,
            label=f"Control (Prev+Eval) — ${ctrl:,.0f}  ({pct_ctrl:.1f}%)")
    ax.barh(["Costos"], [pct_falla], left=[pct_ctrl], color=_CQ_RED, alpha=0.85,
            label=f"Fallas (Int+Ext) — ${falla:,.0f}  ({pct_falla:.1f}%)")

    # Etiquetas en el interior
    for xstart, pct, txt_c in [
        (0,        pct_ctrl,  _CQ_BG),
        (pct_ctrl, pct_falla, "#ffffff"),
    ]:
        if pct > 5:
            ax.text(xstart + pct / 2, 0, f"{pct:.1f}%",
                    ha="center", va="center", fontsize=10,
                    fontweight="bold", color=txt_c)

    ax.set_xlim(0, 100)
    ax.set_xlabel("Proporción (%)", fontsize=9)
    ax.set_title("Inversión en control vs. pérdidas por falla",
                 fontsize=11, fontweight="bold")
    ax.legend(fontsize=8.5, facecolor=_CQ_BG, edgecolor=_CQ_BORDER,
              loc="lower right")
    ax.grid(True, axis="x", alpha=0.4)
    fig.tight_layout()
    return fig


def _cq_fig_pnc_dona(res_p: dict) -> plt.Figure:
    """Gráfica de dona: conformes vs. no conformes."""
    conformes   = res_p["conformes"]
    defectuosos = res_p["defectuosos"]

    fig, ax = plt.subplots(figsize=(5, 4))
    datos_d = [(conformes, "Conformes", _CQ_GREEN, 0.0),
               (defectuosos, f"No conformes\n({res_p['pnc_pct']:.2f}%)", _CQ_RED, 0.06)]
    datos_d = [(v, l, c, e) for v, l, c, e in datos_d if v > 0]
    if not datos_d:
        ax.text(0.5, 0.5, "Sin datos", ha="center", va="center",
                color=_CQ_MUTED, fontsize=12, transform=ax.transAxes)
        fig.tight_layout()
        return fig

    vs, ls, cs, es = zip(*datos_d)
    wedges, texts, autotexts = ax.pie(
        vs, labels=ls, colors=cs, explode=es,
        autopct=lambda p: f"{p:.1f}%" if p > 0.5 else "",
        startangle=90,
        wedgeprops=dict(width=0.52, edgecolor=_CQ_BG, linewidth=1.5),
        textprops=dict(fontsize=8.5, color=_CQ_TEXT),
    )
    for at in autotexts:
        at.set_fontsize(8.5)
        at.set_fontweight("bold")
        at.set_color(_CQ_BG)

    total = res_p["produccion"]
    ax.text(0, 0, f"{total:,.0f}\nunidades", ha="center", va="center",
            fontsize=9, fontweight="bold", color=_CQ_TEXT)
    ax.set_title("Conformes vs. No conformes", fontsize=11, fontweight="bold")
    fig.tight_layout()
    return fig


# ── Panel de interpretación y recomendaciones ──────────────────────────────────

def _cq_panel_interpretacion(res_p: dict, res_c: dict) -> None:
    """Genera interpretación gerencial automática y recomendaciones priorizadas."""
    pnc         = res_p["pnc_pct"]
    pct_falla   = res_c["pct_falla"]
    pct_ctrl    = res_c["pct_control"]
    pct_prev    = res_c["pct_prev"]
    costo_falla = res_c["costo_falla"]
    costo_total = res_c["costo_total"]
    ahorro      = res_c["ahorro_potencial"]

    lbl_pnc, col_pnc, ico_pnc = _cq_nivel_pnc(pnc)
    lbl_f,   col_f,   ico_f   = _cq_nivel_falla(pct_falla)

    # ── Veredicto gerencial principal ─────────────────────────────────────────
    if pnc < 3.0 and pct_falla < 40.0:
        estado   = "PROCESO CON BUENA CALIDAD Y COSTOS CONTROLADOS"
        color_e  = _CQ_GREEN
        icono_e  = "✅"
        msg_e    = (
            "El proceso presenta un nivel de calidad satisfactorio. "
            f"El {pnc:.2f}% de PNC es bajo y los costos de falla representan el {pct_falla:.1f}% del costo total de calidad. "
            "La inversión en prevención y evaluación está dando resultados."
        )
    elif pct_falla > 60.0 and pnc >= 5.0:
        estado   = "IMPACTO CRÍTICO EN RENTABILIDAD"
        color_e  = _CQ_RED
        icono_e  = "❌"
        msg_e    = (
            f"El {pnc:.2f}% de PNC y los costos de falla del {pct_falla:.1f}% del total "
            "están erosionando significativamente la rentabilidad. "
            f"Las pérdidas por fallas ascienden a ${costo_falla:,.0f}, "
            "con un ahorro potencial de ${:.0f} si se reduce el 90% de estas fallas.".format(ahorro)
        )
    elif pct_falla > 40.0:
        estado   = "COSTOS DE FALLA ELEVADOS — ACCIÓN REQUERIDA"
        color_e  = _CQ_YELLOW
        icono_e  = "⚠️"
        msg_e    = (
            f"Los costos de fallas internas y externas representan el {pct_falla:.1f}% del costo total de calidad. "
            "Esto indica que la inversión en prevención es insuficiente para el nivel de defectos actual. "
            f"Fortalecer la prevención puede generar un ahorro estimado de ${ahorro:,.0f}."
        )
    else:
        estado   = "CALIDAD ACEPTABLE — MARGEN DE MEJORA DISPONIBLE"
        color_e  = _CQ_YELLOW
        icono_e  = "⚠️"
        msg_e    = (
            f"El proceso opera con {pnc:.2f}% PNC y costos de falla del {pct_falla:.1f}%. "
            "Existe margen de mejora en la gestión de calidad. "
            "Incrementar la prevención puede reducir los costos de falla a largo plazo."
        )

    st.markdown(
        f"""
        <div style="background:{_CQ_BG};border:2px solid {color_e};border-radius:12px;
                    padding:22px 26px;margin:14px 0">
            <div style="font-size:1.15rem;font-weight:700;color:{color_e};margin-bottom:10px">
                {icono_e} &nbsp; {estado}
            </div>
            <p style="font-size:.89rem;color:{_CQ_TEXT};margin:0 0 16px">{msg_e}</p>
            <div style="display:flex;gap:28px;flex-wrap:wrap;margin-top:4px">
                <div>
                    <div style="font-size:.63rem;color:{_CQ_MUTED};letter-spacing:.1em;
                                text-transform:uppercase">PNC observado</div>
                    <div style="font-family:monospace;font-size:1.4rem;
                                font-weight:700;color:{col_pnc}">{ico_pnc} {pnc:.2f}%</div>
                </div>
                <div>
                    <div style="font-size:.63rem;color:{_CQ_MUTED};letter-spacing:.1em;
                                text-transform:uppercase">Costo de fallas</div>
                    <div style="font-family:monospace;font-size:1.4rem;
                                font-weight:700;color:{col_f}">${costo_falla:,.0f}</div>
                </div>
                <div>
                    <div style="font-size:.63rem;color:{_CQ_MUTED};letter-spacing:.1em;
                                text-transform:uppercase">% Fallas / Total</div>
                    <div style="font-family:monospace;font-size:1.4rem;
                                font-weight:700;color:{col_f}">{pct_falla:.1f}%</div>
                </div>
                <div>
                    <div style="font-size:.63rem;color:{_CQ_MUTED};letter-spacing:.1em;
                                text-transform:uppercase">Ahorro potencial</div>
                    <div style="font-family:monospace;font-size:1.4rem;
                                font-weight:700;color:{_CQ_GREEN}">${ahorro:,.0f}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Mensaje gerencial de vinculación Calidad–Productividad–Rentabilidad ───
    st.markdown(
        f"""
        <div style="background:rgba(59,130,246,.08);border:1px solid rgba(59,130,246,.3);
                    border-radius:10px;padding:15px 20px;margin:10px 0">
            <div style="font-size:.8rem;color:{_CQ_BLUE};font-weight:700;
                        letter-spacing:.08em;text-transform:uppercase;margin-bottom:6px">
                💼 Mensaje gerencial
            </div>
            <p style="font-size:.88rem;color:{_CQ_TEXT};margin:0">
                Una mejora sostenida en la calidad del proceso reduce directamente los costos operativos,
                elimina el reproceso y el scrap, y aumenta la rentabilidad sin incrementar la capacidad instalada.
                Con el nivel actual, <strong style="color:{_CQ_GREEN}">invertir $1 en prevención</strong>
                puede evitar hasta <strong style="color:{_CQ_RED}">$4–$10 en costos de falla</strong>
                (principio de Juran). El costo total de calidad representa el
                <strong style="color:{_CQ_YELLOW}">{costo_total / max(costo_total, 1) * 100:.0f}%</strong>
                de sus costos de calidad registrados; reducir el {pct_falla:.0f}% de fallas al 10%
                liberaría <strong style="color:{_CQ_GREEN}">${ahorro:,.0f}</strong> para reinversión.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Recomendaciones priorizadas ────────────────────────────────────────────
    recomendaciones = []

    if pnc >= 5.0:
        recomendaciones.append((_CQ_RED, "❌",
            f"PNC del {pnc:.1f}% — Implementar acciones correctivas inmediatas. "
            "Revisar materia prima, proporciones de mezcla y proceso de compactación."))
    if pct_falla > 50.0:
        recomendaciones.append((_CQ_RED, "💸",
            f"Los costos de falla representan el {pct_falla:.1f}% del presupuesto de calidad. "
            "Priorizar reducción de fallas internas antes de escalar producción."))
    if pct_prev < 15.0:
        recomendaciones.append((_CQ_YELLOW, "📋",
            f"La prevención solo representa el {pct_prev:.1f}% del costo total. "
            "Incrementar inversión en capacitación, mantenimiento preventivo y control del proceso."))
    if res_c["fe"] > res_c["fi"]:
        recomendaciones.append((_CQ_RED, "🏭",
            "Las fallas externas superan las internas. Fortalecer la inspección en proceso "
            "para detectar defectos antes de que lleguen al cliente."))
    if res_c["eval_"] < res_c["prev"] * 0.3:
        recomendaciones.append((_CQ_YELLOW, "🔎",
            "La inversión en evaluación e inspección es baja respecto a la prevención. "
            "Reforzar ensayos de resistencia y absorción por lote."))
    if pnc < 1.0 and pct_falla < 20.0:
        recomendaciones.append((_CQ_GREEN, "✅",
            "El proceso opera con excelente calidad y costos controlados. "
            "Documentar las prácticas actuales como estándar y extender a otras líneas."))
    if not recomendaciones:
        recomendaciones.append((_CQ_GREEN, "📈",
            "Continúe monitoreando los indicadores. Evalúe reducir costos de evaluación "
            "a medida que la prevención consolide la estabilidad del proceso."))

    st.markdown("#### 🔧 Recomendaciones priorizadas")
    for color_r, ico_r, texto_r in recomendaciones:
        st.markdown(
            f"""
            <div style="display:flex;gap:12px;align-items:flex-start;padding:10px 15px;
                        background:{_CQ_SURF};border-radius:8px;
                        border-left:3px solid {color_r};margin-bottom:7px">
                <span style="font-size:1.1rem;flex-shrink:0">{ico_r}</span>
                <span style="font-size:.86rem;color:{_CQ_TEXT}">{texto_r}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ── Función principal de la sección ───────────────────────────────────────────

def seccion_calidad_costos():
    """Módulo completo de Calidad y Costos del sistema CEP.

    Flujo interno:
    1.  Configuración de fuente de datos (proceso o manual).
    2.  Ingreso de producción y defectuosos → %PNC.
    3.  Ingreso desagregado de las cuatro categorías de costos.
    4.  Dashboard de métricas clave (st.metric).
    5.  Gráfico de barras por categoría de costo.
    6.  Gráfico de dona de distribución porcentual.
    7.  Barra apilada control vs. falla.
    8.  Dona de conformes vs. no conformes.
    9.  Tabla resumen exportable.
    10. Panel de interpretación automática y recomendaciones.
    """
    encabezado(
        "💰", "Calidad y Costos",
        "Impacto económico de los defectos · Costos de calidad · Toma de decisiones gerenciales",
    )

    cfg      = st.session_state.config_proceso
    datos_ok = st.session_state.get("datos_cargados", False)
    df_sg    = st.session_state.get("df_subgrupos")
    cap_res  = st.session_state.get("capacidad", {})

    # ══════════════════════════════════════════════════════════════════════════
    # BLOQUE A – Configuración de fuente de datos
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("### 🎛️ Fuente de datos de producción")

    fuente = st.radio(
        "Seleccionar fuente:",
        ["Ingresar manualmente", "Usar datos cargados en la aplicación"],
        horizontal=True,
        key="cq_fuente",
        disabled=not datos_ok,
    )
    usar_datos_app = (fuente == "Usar datos cargados en la aplicación") and datos_ok

    sep()

    # ══════════════════════════════════════════════════════════════════════════
    # BLOQUE B – Producción y Defectuosos
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("### 🏭 Producción y productos no conformes")

    if usar_datos_app and df_sg is not None:
        n_total_app     = float(len(df_sg))
        lsl_app         = float(cfg.get("lsl_res", 130.0))
        usl_app         = float(cfg.get("usl_res", 160.0))
        datos_res_app   = df_sg["resistencia"].dropna().to_numpy()
        n_def_app       = float(((datos_res_app < lsl_app) | (datos_res_app > usl_app)).sum())

        caja(
            f"Datos del proceso activo: **{int(n_total_app):,} observaciones** · "
            f"LSL={lsl_app} / USL={usl_app} kg/cm² · "
            f"**{int(n_def_app):,} fuera de especificación** detectadas automáticamente.",
            tipo="success",
        )

        prod_total  = n_total_app
        prod_def    = n_def_app

        # Mostrar como métricas de lectura
        mp1, mp2 = st.columns(2)
        mp1.metric("Producción total (obs.)", f"{int(prod_total):,}")
        mp2.metric("Defectuosos detectados",  f"{int(prod_def):,}")
    else:
        if not datos_ok and fuente == "Usar datos cargados en la aplicación":
            caja("No hay datos cargados. Complete la sección **📥 Ingreso de datos** primero, "
                 "o use el modo manual.", tipo="warning")

        bp1, bp2 = st.columns(2)
        with bp1:
            prod_total = st.number_input(
                "🏭 Producción total (unidades)",
                min_value=1.0, value=1000.0, step=10.0,
                format="%.0f", key="cq_prod_total",
                help="Total de unidades producidas en el período analizado.",
            )
        with bp2:
            prod_def = st.number_input(
                "❌ Productos defectuosos (unidades)",
                min_value=0.0, value=30.0, step=1.0,
                format="%.0f", key="cq_prod_def",
                help="Unidades que no cumplen las especificaciones de calidad.",
            )

    # Calcular PNC
    res_p = _cq_calcular_pnc(prod_total, prod_def)
    if "error" in res_p:
        caja(f"Error en producción: {res_p['error']}", tipo="warning")
        return

    pnc     = res_p["pnc_pct"]
    lbl_pnc, col_pnc, ico_pnc = _cq_nivel_pnc(pnc)

    # Tarjetas PNC
    tp1, tp2, tp3, tp4 = st.columns(4)
    tp1.metric("Producción total",    f"{int(res_p['produccion']):,} uds.")
    tp2.metric("Unidades conformes",  f"{int(res_p['conformes']):,} uds.",
               delta=f"{100 - pnc:.2f}%", delta_color="normal")
    tp3.metric("No conformes",        f"{int(res_p['defectuosos']):,} uds.",
               delta=f"{pnc:.2f}%", delta_color="inverse")
    tp4.metric("Nivel PNC",           f"{lbl_pnc}",
               help=f"{ico_pnc} {pnc:.3f}%")

    # Interpretación automática PNC
    if pnc < 1.0:
        st.success(f"✅ Excelente: solo el {pnc:.3f}% de productos no conformes. El proceso presenta buena calidad.")
    elif pnc < 3.0:
        st.success(f"✅ Aceptable: {pnc:.2f}% PNC. Los costos de fallas son relativamente bajos.")
    elif pnc < 5.0:
        st.warning(f"⚠️ El {pnc:.2f}% de PNC requiere atención. Revisar causas de variabilidad del proceso.")
    elif pnc < 10.0:
        st.error(f"❌ El {pnc:.2f}% de PNC es crítico. Los costos de falla impactan significativamente la rentabilidad.")
    else:
        st.error(
            f"🔴 El {pnc:.2f}% de PNC es muy elevado. El proceso genera un volumen inaceptable de defectos. "
            "Se recomienda fortalecer actividades de prevención de forma urgente."
        )

    sep()

    # ══════════════════════════════════════════════════════════════════════════
    # BLOQUE C – Ingreso de costos de calidad
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("### 💵 Costos de calidad (período analizado)")
    caja(
        "Ingrese los costos en la moneda de su operación (COP, USD, etc.). "
        "Los cálculos son proporcionales a la unidad elegida.",
        tipo="info",
    )

    with st.expander("🛡️ Costos de Prevención", expanded=True):
        caja(
            "Inversión para **evitar** que ocurran defectos: capacitación, "
            "mantenimiento preventivo, mejora de procesos, calibración de equipos.",
            tipo="info",
        )
        pc1, pc2, pc3 = st.columns(3)
        with pc1:
            c_capacitacion = st.number_input(
                "Capacitación operarios ($)", min_value=0.0,
                value=500_000.0, step=10_000.0, format="%.0f", key="cq_cap")
        with pc2:
            c_mantenimiento = st.number_input(
                "Mantenimiento preventivo ($)", min_value=0.0,
                value=800_000.0, step=10_000.0, format="%.0f", key="cq_mant")
        with pc3:
            c_ctrl_proceso = st.number_input(
                "Control estadístico del proceso ($)", min_value=0.0,
                value=300_000.0, step=10_000.0, format="%.0f", key="cq_ctrl")
        costo_prev = c_capacitacion + c_mantenimiento + c_ctrl_proceso

    with st.expander("🔎 Costos de Evaluación", expanded=True):
        caja(
            "Costos de **detectar** defectos: inspección, ensayos de laboratorio, "
            "auditorías internas, calibración de instrumentos de medición.",
            tipo="info",
        )
        ec1, ec2, ec3 = st.columns(3)
        with ec1:
            c_inspeccion = st.number_input(
                "Inspección en proceso ($)", min_value=0.0,
                value=600_000.0, step=10_000.0, format="%.0f", key="cq_insp")
        with ec2:
            c_ensayos = st.number_input(
                "Ensayos de laboratorio ($)", min_value=0.0,
                value=400_000.0, step=10_000.0, format="%.0f", key="cq_ens")
        with ec3:
            c_auditorias = st.number_input(
                "Auditorías de calidad ($)", min_value=0.0,
                value=200_000.0, step=10_000.0, format="%.0f", key="cq_aud")
        costo_eval = c_inspeccion + c_ensayos + c_auditorias

    with st.expander("⚠️ Costos de Fallas Internas", expanded=True):
        caja(
            "Pérdidas **antes** de entregar al cliente: retrabajos, desperdicios, "
            "productos rechazados en línea, tiempo de parada por defectos.",
            tipo="warning",
        )
        fi1, fi2, fi3 = st.columns(3)
        with fi1:
            c_retrabajo = st.number_input(
                "Retrabajos y reprocesos ($)", min_value=0.0,
                value=1_200_000.0, step=10_000.0, format="%.0f", key="cq_ret")
        with fi2:
            c_scrap = st.number_input(
                "Scrap / material desechado ($)", min_value=0.0,
                value=900_000.0, step=10_000.0, format="%.0f", key="cq_scrap")
        with fi3:
            c_rechazo_int = st.number_input(
                "Rechazo en línea / paradas ($)", min_value=0.0,
                value=400_000.0, step=10_000.0, format="%.0f", key="cq_rech")
        costo_fi = c_retrabajo + c_scrap + c_rechazo_int

    with st.expander("❌ Costos de Fallas Externas", expanded=True):
        caja(
            "Pérdidas **después** de entregar al cliente: devoluciones, reclamos, "
            "garantías, penalizaciones contractuales, pérdida de clientes.",
            tipo="warning",
        )
        fe1, fe2, fe3 = st.columns(3)
        with fe1:
            c_devoluciones = st.number_input(
                "Devoluciones de clientes ($)", min_value=0.0,
                value=700_000.0, step=10_000.0, format="%.0f", key="cq_dev")
        with fe2:
            c_garantias = st.number_input(
                "Garantías y reclamos ($)", min_value=0.0,
                value=500_000.0, step=10_000.0, format="%.0f", key="cq_gar")
        with fe3:
            c_perd_cliente = st.number_input(
                "Pérdida de clientes / penalizaciones ($)", min_value=0.0,
                value=300_000.0, step=10_000.0, format="%.0f", key="cq_perd")
        costo_fe = c_devoluciones + c_garantias + c_perd_cliente

    # ── Calcular costos ───────────────────────────────────────────────────────
    res_c = _cq_calcular_costos(costo_prev, costo_eval, costo_fi, costo_fe)
    if "error" in res_c:
        caja(f"Error en costos: {res_c['error']}", tipo="warning")
        return

    sep()

    # ══════════════════════════════════════════════════════════════════════════
    # BLOQUE D – Dashboard de métricas clave
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("### 📊 Dashboard de indicadores")

    dm1, dm2, dm3, dm4 = st.columns(4)
    dm1.metric("Costo total de calidad",    f"${res_c['costo_total']:,.0f}")
    dm2.metric("Costos de control",         f"${res_c['costo_control']:,.0f}",
               delta=f"{res_c['pct_control']:.1f}% del total",
               delta_color="normal")
    dm3.metric("Costos de falla",           f"${res_c['costo_falla']:,.0f}",
               delta=f"{res_c['pct_falla']:.1f}% del total",
               delta_color="inverse")
    dm4.metric("Ahorro potencial (90% falla)", f"${res_c['ahorro_potencial']:,.0f}",
               help="Si se elimina el 90% de los costos de falla actuales.")

    dm5, dm6, dm7, dm8 = st.columns(4)
    dm5.metric("Prevención",       f"${res_c['prev']:,.0f}",
               delta=f"{res_c['pct_prev']:.1f}%", delta_color="normal")
    dm6.metric("Evaluación",       f"${res_c['eval_']:,.0f}",
               delta=f"{res_c['pct_eval']:.1f}%", delta_color="normal")
    dm7.metric("Fallas internas",  f"${res_c['fi']:,.0f}",
               delta=f"{res_c['pct_fi']:.1f}%", delta_color="inverse")
    dm8.metric("Fallas externas",  f"${res_c['fe']:,.0f}",
               delta=f"{res_c['pct_fe']:.1f}%", delta_color="inverse")

    # Si existe información de capacidad del proceso, mostrar vinculación
    if cap_res.get("cpk"):
        cpk_val = cap_res["cpk"]
        lbl_cpk = "Capaz" if cpk_val >= 1.33 else ("Marginal" if cpk_val >= 1.0 else "No capaz")
        col_cpk = _CQ_GREEN if cpk_val >= 1.33 else (_CQ_YELLOW if cpk_val >= 1.0 else _CQ_RED)
        caja(
            f"Vinculación con CEP: el proceso tiene Cpk = **{cpk_val:.3f}** ({lbl_cpk}). "
            "Un proceso con Cpk bajo genera más defectos y, por tanto, mayores costos de falla.",
            tipo="info",
        )

    sep()

    # ══════════════════════════════════════════════════════════════════════════
    # BLOQUE E – Gráficos profesionales
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("### 📈 Visualización de costos de calidad")

    # Fila 1: barras + dona
    g1, g2 = st.columns([3, 2])
    with g1:
        fig_barras = _cq_fig_barras_costos(res_c)
        st.pyplot(fig_barras, use_container_width=True)
        plt.close(fig_barras)
    with g2:
        fig_dona = _cq_fig_dona_costos(res_c)
        st.pyplot(fig_dona, use_container_width=True)
        plt.close(fig_dona)

    # Fila 2: control vs. falla + dona PNC
    g3, g4 = st.columns([3, 2])
    with g3:
        st.markdown("#### ⚖️ Control vs. Falla")
        fig_cf = _cq_fig_control_vs_falla(res_c)
        st.pyplot(fig_cf, use_container_width=True)
        plt.close(fig_cf)
    with g4:
        st.markdown("#### 🏭 Conformes vs. No conformes")
        fig_pnc = _cq_fig_pnc_dona(res_p)
        st.pyplot(fig_pnc, use_container_width=True)
        plt.close(fig_pnc)

    sep()

    # ══════════════════════════════════════════════════════════════════════════
    # BLOQUE F – Tabla resumen exportable
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("### 📋 Tabla resumen de indicadores")

    lbl_f_tab, _, ico_f_tab = _cq_nivel_falla(res_c["pct_falla"])

    df_tabla = pd.DataFrame([
        {"Categoría": "PRODUCCIÓN",             "Indicador": "Producción total",             "Valor": f"{int(res_p['produccion']):,} uds.",     "Estado": "—"},
        {"Categoría": "PRODUCCIÓN",             "Indicador": "Unidades conformes",           "Valor": f"{int(res_p['conformes']):,} uds.",      "Estado": "—"},
        {"Categoría": "PRODUCCIÓN",             "Indicador": "Unidades no conformes",        "Valor": f"{int(res_p['defectuosos']):,} uds.",    "Estado": "—"},
        {"Categoría": "PRODUCCIÓN",             "Indicador": "% PNC",                        "Valor": f"{pnc:.3f}%",                           "Estado": f"{ico_pnc} {lbl_pnc}"},
        {"Categoría": "COSTOS DE CONTROL",      "Indicador": "Prevención",                   "Valor": f"${costo_prev:,.0f}",                   "Estado": f"{res_c['pct_prev']:.1f}%"},
        {"Categoría": "COSTOS DE CONTROL",      "Indicador": "Evaluación",                   "Valor": f"${costo_eval:,.0f}",                   "Estado": f"{res_c['pct_eval']:.1f}%"},
        {"Categoría": "COSTOS DE CONTROL",      "Indicador": "Total control",                "Valor": f"${res_c['costo_control']:,.0f}",        "Estado": f"{res_c['pct_control']:.1f}%"},
        {"Categoría": "COSTOS DE FALLA",        "Indicador": "Fallas internas",              "Valor": f"${costo_fi:,.0f}",                     "Estado": f"{res_c['pct_fi']:.1f}%"},
        {"Categoría": "COSTOS DE FALLA",        "Indicador": "Fallas externas",              "Valor": f"${costo_fe:,.0f}",                     "Estado": f"{res_c['pct_fe']:.1f}%"},
        {"Categoría": "COSTOS DE FALLA",        "Indicador": "Total fallas",                 "Valor": f"${res_c['costo_falla']:,.0f}",          "Estado": f"{ico_f_tab} {lbl_f_tab}"},
        {"Categoría": "RESUMEN ECONÓMICO",      "Indicador": "Costo total de calidad",       "Valor": f"${res_c['costo_total']:,.0f}",          "Estado": "—"},
        {"Categoría": "RESUMEN ECONÓMICO",      "Indicador": "Ahorro potencial (90% falla)", "Valor": f"${res_c['ahorro_potencial']:,.0f}",     "Estado": "—"},
        {"Categoría": "RESUMEN ECONÓMICO",      "Indicador": "Ratio Prevención / Control",   "Valor": f"{res_c['ratio_prev_ctrl']:.1f}%",      "Estado": "—"},
    ])
    st.dataframe(df_tabla, use_container_width=True, hide_index=True)

    # Botón de descarga CSV
    csv_bytes = df_tabla.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Descargar tabla CSV",
        data=csv_bytes,
        file_name="calidad_costos_cep.csv",
        mime="text/csv",
    )

    sep()

    # ══════════════════════════════════════════════════════════════════════════
    # BLOQUE G – Interpretación automática y recomendaciones
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("### 🧠 Interpretación automática y recomendaciones")
    _cq_panel_interpretacion(res_p, res_c)


# ─────────────────────────────────────────────────────────────────────────────
# Fin SECCIÓN 13 – Calidad y Costos
# ─────────────────────────────────────────────────────────────────────────────

SECCIONES = {
    "🏠  Introducción & Calidad":   seccion_introduccion,
    "📥  Ingreso de datos":         seccion_ingreso_datos,
    "🔍  Validación estadística":   seccion_validacion,
    "📊  Fase 1 – Estabilización":  seccion_fase1,
    "📈  Fase 2 – Monitoreo":       seccion_fase2,
    "🔢  Control por atributos":    seccion_atributos,
    "⚙️  Capacidad del proceso":    seccion_capacidad,
    "💰  Calidad y Costos":         seccion_calidad_costos,
    "🏭  Desempeño del sistema":    seccion_desempeno,
    "📦  Muestreo por aceptación":   seccion_muestreo,
    "🔎  Análisis de causas":       seccion_causas,
    "📋  Dashboard general":        seccion_dashboard,
    "💡  Recomendaciones":          seccion_recomendaciones,
}


def main():
    # Estilos y estado
    aplicar_estilos()
    inicializar_estado()

    # ── Recolectar estado global para el sidebar ───────────────────────────────
    ss          = st.session_state
    datos_ok    = bool(ss.get("datos_cargados", False))
    df_sg       = ss.get("df_subgrupos")
    f1          = ss.get("fase1", {})
    cap         = ss.get("capacidad", {})
    f1_ok       = f1.get("calculado", False)
    estable     = f1.get("proceso_estable", None)
    cpk_val     = cap.get("cpk")
    pnc_val     = cap.get("pnc_pct")
    n_obs       = len(df_sg) if (datos_ok and df_sg is not None) else 0

    # Score global (reutiliza la función del dashboard)
    try:
        e_sb = _db_recolectar_estado()
        score_sb, lbl_sb, col_sb, ico_sb = _db_score_salud(e_sb)
    except Exception:
        score_sb, lbl_sb, col_sb, ico_sb = 0.0, "Sin datos", "#64748b", "⚪"

    # ── Sidebar ────────────────────────────────────────────────────────────────
    with st.sidebar:

        # ── Marca del sistema ──────────────────────────────────────────────────
        st.markdown(
            f"""
            <div class="sb-brand">
                <div class="sb-logo-img">
                    <img src="data:image/png;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/4gHYSUNDX1BST0ZJTEUAAQEAAAHIAAAAAAQwAABtbnRyUkdCIFhZWiAH4AABAAEAAAAAAABhY3NwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAA9tYAAQAAAADTLQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAlkZXNjAAAA8AAAACRyWFlaAAABFAAAABRnWFlaAAABKAAAABRiWFlaAAABPAAAABR3dHB0AAABUAAAABRyVFJDAAABZAAAAChnVFJDAAABZAAAAChiVFJDAAABZAAAAChjcHJ0AAABjAAAADxtbHVjAAAAAAAAAAEAAAAMZW5VUwAAAAgAAAAcAHMAUgBHAEJYWVogAAAAAAAAb6IAADj1AAADkFhZWiAAAAAAAABimQAAt4UAABjaWFlaIAAAAAAAACSgAAAPhAAAts9YWVogAAAAAAAA9tYAAQAAAADTLXBhcmEAAAAAAAQAAAACZmYAAPKnAAANWQAAE9AAAApbAAAAAAAAAABtbHVjAAAAAAAAAAEAAAAMZW5VUwAAACAAAAAcAEcAbwBvAGcAbABlACAASQBuAGMALgAgADIAMAAxADb/2wBDAAUDBAQEAwUEBAQFBQUGBwwIBwcHBw8LCwkMEQ8SEhEPERETFhwXExQaFRERGCEYGh0dHx8fExciJCIeJBweHx7/2wBDAQUFBQcGBw4ICA4eFBEUHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh7/wAARCAQABgADASIAAhEBAxEB/8QAHQABAAICAwEBAAAAAAAAAAAAAAcIBQYBAwQCCf/EAFsQAQABAwMBBAYFBwgFBQ8DBQABAgMEBQYRIQcSMUEIE1FhcYEUIjKRoRUjQlKxwdEWM0NicoKS0iSUwuHwdJOisvEXJTQ1NkRGU1RVVnOEldMYY3VkZYOFo//EABwBAQACAwEBAQAAAAAAAAAAAAAEBQIDBgEHCP/EAEIRAQABAwICBQoFAgUDAwUAAAABAgMEBREhMQYSQVGhEyJhcYGRscHR8BQVMlLhI0IHM2KS8RYkolOC0hc0Q2Ny/9oADAMBAAIRAxEAPwCmQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA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AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD/9k=" alt="InsigmaFlow" />
                </div>
                <div>
                    <div class="sb-title">CEP Sistema</div>
                    <div class="sb-sub">Bloques de Concreto</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ── Píldora de estado de datos ─────────────────────────────────────────
        if datos_ok:
            st.markdown(
                f"""
                <div class="sb-data-pill ok">
                    <span class="sb-pulse"></span>
                    {n_obs:,} observaciones activas
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
                <div class="sb-data-pill nok">
                    <span class="sb-pulse"></span>
                    Sin datos cargados
                </div>
                """,
                unsafe_allow_html=True,
            )

        # ── Panel de KPIs del sidebar ──────────────────────────────────────────
        def _sb_kpi(lbl: str, val: str, col: str):
            st.markdown(
                f"""
                <div class="sb-kpi-row">
                    <span class="sb-kpi-lbl">{lbl}</span>
                    <span class="sb-kpi-val" style="color:{col}">{val}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Score global
        st.markdown(
            f"""
            <div class="sb-status-panel">
                <div class="sb-status-title">Estado del proceso</div>
            """,
            unsafe_allow_html=True,
        )

        _sb_kpi("Score global",
                f"{score_sb:.0f}/100",
                col_sb)

        _sb_kpi("Estabilidad",
                "✅ Estable" if estable is True
                else ("❌ Inestable" if estable is False else "—"),
                "#10b981" if estable is True
                else ("#ef4444" if estable is False else "#64748b"))

        _sb_kpi("Cpk",
                f"{cpk_val:.3f}" if cpk_val is not None else "—",
                "#10b981" if (cpk_val or 0) >= 1.33
                else ("#f59e0b" if (cpk_val or 0) >= 1.00 else "#ef4444"))

        _sb_kpi("% PNC",
                f"{pnc_val:.2f}%" if pnc_val is not None else "—",
                "#10b981" if (pnc_val or 99) < 1.0
                else ("#f59e0b" if (pnc_val or 99) < 5.0 else "#ef4444"))

        _sb_kpi("Fase 1",
                "✅ OK" if f1_ok else "⏳ Pendiente",
                "#10b981" if f1_ok else "#64748b")

        st.markdown("</div>", unsafe_allow_html=True)

        # ── Navegación ─────────────────────────────────────────────────────────
        st.markdown("<p class='sb-nav-lbl'>Módulos</p>", unsafe_allow_html=True)

        seccion_activa = st.radio(
            label="nav",
            options=list(SECCIONES.keys()),
            index=0,
            label_visibility="collapsed",
        )

        # ── Footer ─────────────────────────────────────────────────────────────
        st.markdown(
            """
            <div class="sb-footer">
                <span class="sb-ver">v2.0</span> · CEP Industrial<br>
                Manufactura de Bloques
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── Renderizar sección activa ──────────────────────────────────────────────
    SECCIONES[seccion_activa]()


# ══════════════════════════════════════════════════════════════════════════════
# PUNTO DE ENTRADA
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    main()
else:
    # Streamlit ejecuta el módulo directamente (no como __main__),
    # por lo que también llamamos a main() en ese caso.
    main()