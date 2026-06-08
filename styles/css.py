import streamlit as st


def cargar_css():
    st.markdown("""
    <style>

        :root {
            --dh-bg: #F5F7FA;
            --dh-surface: #FFFFFF;
            --dh-surface-soft: #F8FAFC;
            --dh-sidebar: #0F172A;
            --dh-sidebar-2: #111827;
            --dh-primary: #0EA5A4;
            --dh-primary-dark: #0F766E;
            --dh-primary-soft: #ECFEFF;
            --dh-text: #1E293B;
            --dh-muted: #64748B;
            --dh-border: #E2E8F0;
            --dh-danger: #DC2626;
            --dh-success: #059669;
            --dh-warning: #D97706;
            --dh-shadow: 0 14px 34px rgba(15, 23, 42, 0.08);
            --dh-shadow-sm: 0 8px 20px rgba(15, 23, 42, 0.06);
            --dh-radius-xl: 28px;
            --dh-radius-lg: 20px;
            --dh-radius-md: 14px;
        }

        html, body, [class*="css"] {
            font-family: "Inter", "Segoe UI", system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
        }

        .stApp {
            background:
                radial-gradient(circle at top right, rgba(14, 165, 164, 0.08), transparent 30%),
                var(--dh-bg);
        }

        .main .block-container {
            padding-top: 1.7rem;
            padding-bottom: 3rem;
            max-width: 1280px;
        }

        h1 {
            color: var(--dh-text) !important;
            font-weight: 850 !important;
            letter-spacing: -0.045em !important;
        }

        h2, h3 {
            color: var(--dh-text) !important;
            font-weight: 780 !important;
            letter-spacing: -0.025em !important;
        }

        p, label, span, div {
            color: var(--dh-text);
        }

        /* ===================== Sidebar ===================== */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0F172A 0%, #111827 58%, #0B3B44 100%);
            border-right: 1px solid rgba(255,255,255,0.08);
        }

        [data-testid="stSidebar"] * {
            color: #F8FAFC !important;
        }

        .dh-sidebar-brand {
            padding: 12px 8px 18px 8px;
            border-bottom: 1px solid rgba(255,255,255,0.10);
            margin-bottom: 14px;
        }

        .dh-logo-mark {
            width: 46px;
            height: 46px;
            border-radius: 14px;
            background: linear-gradient(135deg, #0EA5A4 0%, #38BDF8 100%);
            display: inline-flex;
            align-items: center;
            justify-content: center;
            color: white !important;
            font-size: 1.05rem;
            font-weight: 900;
            margin-bottom: 10px;
            box-shadow: 0 10px 24px rgba(14,165,164,0.26);
        }

        .dh-sidebar-title {
            font-size: 0.95rem;
            font-weight: 850;
            letter-spacing: -0.04em;
            color: white !important;
            margin: 0;
            line-height: 1.1;
        }
                
        .dh-sidebar-subtitle {
            color: rgba(248,250,252,0.68) !important;
            font-size: 0.72rem;
            margin-top: 4px;
            line-height: 1.3;
        }

        .dh-user-chip {
            background: rgba(14,165,164,0.13);
            border: 1px solid rgba(14,165,164,0.22);
            border-radius: 999px;
            padding: 7px 11px;
            font-size: 0.82rem;
            font-weight: 750;
            margin: 8px 0 12px 0;
            color: #CCFBF1 !important;
        }
                    
        .dh-brand-row {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        /* Menú lateral con st.radio */
        [data-testid="stSidebar"] [role="radiogroup"] {
            margin-top: 10px;
        }

        [data-testid="stSidebar"] [role="radiogroup"] label {
            border-radius: 13px;
            padding: 0.42rem 0.55rem;
            margin-bottom: 0.25rem;
            transition: all 0.18s ease;
        }

        [data-testid="stSidebar"] [role="radiogroup"] label:hover {
            background: rgba(14, 165, 164, 0.16);
            transform: translateX(2px);
        }

        [data-testid="stSidebar"] [role="radiogroup"] label p {
            font-size: 0.92rem !important;
            font-weight: 650 !important;
            color: #E2E8F0 !important;
        }

        /* ===================== Inputs / buttons ===================== */
        .stButton button,
        .stDownloadButton button,
        .stFormSubmitButton button {
            border-radius: 13px !important;
            border: 1px solid var(--dh-border) !important;
            font-weight: 780 !important;
            transition: all 0.2s ease !important;
            min-height: 2.45rem;
        }

        .stButton button:hover,
        .stDownloadButton button:hover,
        .stFormSubmitButton button:hover {
            border-color: var(--dh-primary) !important;
            color: var(--dh-primary-dark) !important;
            box-shadow: 0 10px 22px rgba(14, 165, 164, 0.14) !important;
            transform: translateY(-1px);
        }

        /* Botón cerrar sesión del sidebar: oscuro y siempre legible */
        [data-testid="stSidebar"] .stButton button {
            background: #1E293B !important;
            color: #F8FAFC !important;
            border: 1px solid rgba(34,224,208,0.28) !important;
            border-radius: 13px !important;
            font-weight: 800 !important;
            box-shadow: none !important;
        }

        [data-testid="stSidebar"] .stButton button:hover {
            background: #0EA5A4 !important;
            color: #FFFFFF !important;
            border-color: #0EA5A4 !important;
        }

        .stTextInput input,
        .stNumberInput input,
        .stDateInput input,
        .stSelectbox div[data-baseweb="select"] {
            border-radius: 12px !important;
        }

        hr {
            border-color: rgba(148, 163, 184, 0.22) !important;
        }

        /* ===================== Métricas ===================== */
        .stMetric {
            background: var(--dh-surface);
            padding: 18px 20px;
            border-radius: var(--dh-radius-lg);
            box-shadow: var(--dh-shadow-sm);
            border: 1px solid var(--dh-border);
        }

        [data-testid="stMetricLabel"] {
            color: var(--dh-muted) !important;
            font-size: 0.82rem !important;
            font-weight: 700 !important;
        }

        [data-testid="stMetricValue"] {
            color: var(--dh-text) !important;
            font-size: 1.75rem !important;
            font-weight: 850 !important;
            letter-spacing: -0.045em;
        }

        /* ===================== Componentes propios ===================== */
        .dh-page-hero {
            background:
                radial-gradient(circle at top right, rgba(14, 165, 164, 0.18), transparent 34%),
                linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 48%, #ECFEFF 100%);
            border: 1px solid var(--dh-border);
            border-radius: 32px;
            padding: 30px 34px;
            box-shadow: var(--dh-shadow);
            margin-bottom: 24px;
            overflow: hidden;
        }

        .dh-page-eyebrow {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 7px 12px;
            border-radius: 999px;
            background: rgba(14, 165, 164, 0.10);
            color: var(--dh-primary-dark) !important;
            font-weight: 850;
            font-size: 0.80rem;
            margin-bottom: 14px;
            border: 1px solid rgba(14, 165, 164, 0.18);
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }

        .dh-page-title {
            font-size: 2.35rem;
            line-height: 1.05;
            font-weight: 880;
            letter-spacing: -0.06em;
            color: var(--dh-text) !important;
            margin: 0 0 8px 0;
        }

        .dh-page-subtitle {
            color: var(--dh-muted) !important;
            font-size: 1.02rem;
            line-height: 1.62;
            max-width: 840px;
            margin: 0;
        }

        .dh-panel {
            background: rgba(255,255,255,0.92);
            border: 1px solid var(--dh-border);
            border-radius: var(--dh-radius-xl);
            padding: 22px 24px;
            box-shadow: var(--dh-shadow-sm);
            margin-bottom: 20px;
        }

        .dh-panel-title {
            font-size: 1.05rem;
            font-weight: 850;
            color: var(--dh-text) !important;
            margin: 0 0 6px 0;
            letter-spacing: -0.02em;
        }

        .dh-panel-caption {
            color: var(--dh-muted) !important;
            font-size: 0.92rem;
            line-height: 1.55;
            margin: 0 0 14px 0;
        }

        .dh-kpi-card {
            background: var(--dh-surface);
            border: 1px solid var(--dh-border);
            border-radius: 22px;
            padding: 20px 21px;
            box-shadow: var(--dh-shadow-sm);
            height: 100%;
            position: relative;
            overflow: hidden;
        }

        .dh-kpi-card:before {
            content: "";
            position: absolute;
            inset: 0 auto 0 0;
            width: 4px;
            background: linear-gradient(180deg, var(--dh-primary), #38BDF8);
        }

        .dh-kpi-label {
            color: var(--dh-muted) !important;
            font-size: 0.78rem;
            font-weight: 850;
            text-transform: uppercase;
            letter-spacing: 0.065em;
            margin-bottom: 9px;
        }

        .dh-kpi-value {
            color: var(--dh-text) !important;
            font-size: 1.9rem;
            font-weight: 900;
            letter-spacing: -0.06em;
            margin-bottom: 4px;
            line-height: 1.05;
        }

        .dh-kpi-note {
            color: var(--dh-muted) !important;
            font-size: 0.86rem;
            line-height: 1.45;
        }

        .dh-pill {
            display: inline-block;
            padding: 7px 12px;
            border-radius: 999px;
            background: var(--dh-primary-soft);
            color: var(--dh-primary-dark) !important;
            border: 1px solid rgba(14,165,164,0.18);
            font-size: 0.80rem;
            font-weight: 850;
            margin-right: 7px;
            margin-bottom: 7px;
        }

        .dh-pill-muted {
            background: #F8FAFC;
            color: var(--dh-text) !important;
            border-color: var(--dh-border);
        }

        .dh-quick-card {
            background: var(--dh-surface);
            border: 1px solid var(--dh-border);
            border-radius: 22px;
            padding: 20px;
            box-shadow: var(--dh-shadow-sm);
            height: 100%;
        }

        .dh-quick-card h4 {
            margin: 0 0 6px 0;
            color: var(--dh-text) !important;
            font-size: 1.02rem;
            font-weight: 850;
        }

        .dh-quick-card p {
            color: var(--dh-muted) !important;
            margin: 0;
            font-size: 0.9rem;
            line-height: 1.45;
        }

        .dh-status-list {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 10px;
        }

        .dh-status-ok {
            color: #047857 !important;
            background: #ECFDF5;
            border: 1px solid #BBF7D0;
            border-radius: 999px;
            padding: 6px 12px;
            font-size: 0.78rem;
            font-weight: 850;
            display: inline-flex;
            align-items: center;
        }
                
        .dh-danger-note {
            color: var(--dh-danger) !important;
            font-weight: 800;
        }

        .dh-code-formula {
            background: #0F172A;
            color: #E2E8F0 !important;
            border-radius: 18px;
            padding: 18px 20px;
            border: 1px solid rgba(255,255,255,0.08);
            font-family: Consolas, Monaco, monospace;
            line-height: 1.5;
            box-shadow: var(--dh-shadow-sm);
        }

        div[data-testid="stDataFrame"] {
            border-radius: 18px;
            overflow: hidden;
            border: 1px solid var(--dh-border);
            box-shadow: var(--dh-shadow-sm);
        }

        @media (max-width: 900px) {
            .dh-page-title { font-size: 1.9rem; }
            .dh-page-hero { padding: 24px 22px; }
        }
    </style>
    """, unsafe_allow_html=True)
