print("SCRIPT FINAL — LOGO GRANDE + INPUT MAIOR + CORRIGIDO")

import streamlit as st
from rag_engine import ask, retrieve
import os

# ==========================================
# CONFIG DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Assistente SEAD-GO",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# CSS AJUSTADO
# ==========================================
st.markdown("""
    <style>
    .stApp {
        background: #F9F9F9;
        color: #000000;
        font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    }

    [data-testid="stHeader"], .stSidebar, section[data-testid="stSidebar"] {
        display: none !important;
    }

    .main-header {
        background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%);
        padding: 1rem 0 0.5rem 0;
        margin: 0 -1rem 1.5rem -1rem;
        border-bottom: 3px solid #1E3C72;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        position: relative;
    }

    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #1E3C72, #2A5298, #1E3C72);
    }

    .header-content {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 2rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 3rem;
    }

    /* LOGO AUMENTADA */
    .logo-container {
        flex-shrink: 0;
        padding: 0;
        margin: 0;
        background: white;
        border-radius: 16px;
        box-shadow: 0 6px 24px rgba(0,0,0,0.12);
        border: 2px solid #E8E8E8;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .logo-img {
        height: 300px;
        border-radius: 12px;
        filter: drop-shadow(0 4px 16px rgba(0,0,0,0.15));
    }

    .title-container {
        flex-grow: 1;
        text-align: left;
    }

    .main-title {
        font-size: 3.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #1E3C72, #2A5298);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
    }

    .department {
        font-size: 1.4rem;
        color: #fff;
        padding: 0.9rem 1.6rem;
        background: linear-gradient(135deg, #1E3C72, #2A5298);
        border-radius: 10px;
        display: inline-block;
        box-shadow: 0 4px 12px rgba(30,60,114,0.3);
    }

    .main-container {
        max-width: 900px;
        margin: 0 auto;
        padding: 0 2rem;
        text-align: center;
    }

    /* CAMPO DE PERGUNTA MAIOR */
    .input-container {
        background: #FFFFFF;
        padding: 3rem 2.5rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        margin-bottom: 3rem;
        border: 2px solid #1E3C72;
        position: relative;
    }

    .input-container input {
        font-size: 1.2rem !important;
        padding: 1.2rem 1rem !important;
        border-radius: 12px !important;
    }

    .input-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #1E3C72, #2A5298);
        border-radius: 20px 20px 0 0;
    }

    .stButton>button {
        background: linear-gradient(135deg, #1E3C72 0%, #2A5298 100%);
        color: #FFFFFF !important;
        border: 3px solid #1E3C72;
        border-radius: 12px;
        padding: 18px 32px;
        font-weight: 700;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 6px 20px rgba(30,60,114,0.3);
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }

    .stButton>button:hover {
        background: linear-gradient(135deg, #2A5298 0%, #3B6FD9 100%);
        transform: translateY(-2px);
    }

    .secondary-button>button {
        background: #F8FAFC;
        color: #1E3C72 !important;
        border: 3px solid #1E3C72;
        font-weight: 700;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }

    .secondary-button>button:hover {
        background: #E8F2FF;
        transform: translateY(-2px);
    }

    .empty-state {
        text-align: center;
        padding: 4rem 3rem;
        background: #FFFFFF;
        border-radius: 20px;
        border: 3px solid #1E3C72;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        margin: 3rem auto;
        max-width: 700px;
    }

    .footer {
        text-align: center;
        color: #000000;
        margin-top: 4rem;
        padding: 2rem;
        border-top: 3px solid #1E3C72;
        background: #FFFFFF;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# FUNÇÃO LOGO
# ==========================================
def display_logo(logo_path="seadgo_logo.png", width=300):
    try:
        if os.path.exists(logo_path):
            st.image(logo_path, width=width)
        else:
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #1E3C72, #2A5298);
                            width: {width}px; height: {width}px;
                            border-radius: 16px;
                            display: flex; align-items: center; justify-content: center;
                            font-weight: 700; color: white; font-size: 30px;">
                    SEAD-GO
                </div>
            """, unsafe_allow_html=True)
    except Exception:
        st.markdown(f"""
            <div style="background:#1E3C72;width:{width}px;height:{width}px;
                        border-radius:16px;display:flex;align-items:center;
                        justify-content:center;font-weight:700;color:white;
                        font-size:28px;">SEAD-GO</div>
        """, unsafe_allow_html=True)

# ==========================================
# HEADER
# ==========================================
st.markdown("""
    <div class="main-header">
        <div class="header-content">
            <div class="logo-container">
""", unsafe_allow_html=True)

display_logo("seadgo_logo.png", width=300)

st.markdown("""
            </div>
            <div class="title-container">
                <h1 class="main-title">Assistente SEAD-GO</h1>
                <p class="department">Secretaria de Estado de Administração - Governo de Goiás</p>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# CONTEÚDO PRINCIPAL
# ==========================================
if "history" not in st.session_state:
    st.session_state.history = []

st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.markdown('<div class="input-container">', unsafe_allow_html=True)
st.markdown("### 💬 Faça sua pergunta")

query = st.text_input(
    "Digite sua pergunta sobre os documentos:",
    key="input",
    placeholder="Ex: Quais são os procedimentos administrativos da SEAD-GO?",
    label_visibility="collapsed"
)

col_btn1, col_btn2 = st.columns([1, 1])
with col_btn1:
    if st.button("🚀 Enviar Pergunta", use_container_width=True):
        if query:
            resposta = ask(query)
            st.session_state.history.append((query, resposta))
            st.rerun()

with col_btn2:
    if st.button("🗑️ Limpar Histórico", use_container_width=True, key="clear_btn"):
        st.session_state.history = []
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
st.markdown("### 📝 Histórico da Conversa")

# ==========================================
# HISTÓRICO OU MENSAGEM INICIAL
# ==========================================
if not st.session_state.history:
    st.markdown("""
        <div class="empty-state">
            <h3>👋 Bem-vindo ao Assistente SEAD-GO</h3>
            <p>Faça sua primeira pergunta para começar a conversa com nosso assistente inteligente.</p>
            <ul>
                <li>Quais são os procedimentos administrativos da secretaria?</li>
                <li>Como funciona o processo de licitação na SEAD-GO?</li>
                <li>Quais documentos são necessários para abertura de processo?</li>
                <li>Quais são as normas de conduta e ética institucional?</li>
                <li>Como acessar os manuais de procedimentos?</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
else:
    for q, r in st.session_state.history:
        st.markdown(f"""
            <div style="text-align:left;background:#1E3C72;color:white;
                padding:1.5rem;border-radius:12px;margin-bottom:1rem;">
                <strong>👤 Você:</strong><br>{q}
            </div>
            <div style="text-align:left;background:#F8FAFC;
                padding:1.5rem;border-radius:12px;margin-bottom:2rem;border:1px solid #DDD;">
                <strong>🤖 Assistente SEAD-GO:</strong><br>{r}
            </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# FOOTER
# ==========================================
st.markdown("""
    <div class="footer">
        <p><strong>Assistente SEAD-GO</strong> • Desenvolvido para a Secretaria de Estado de Administração de Goiás</p>
        <p>Tecnologia: Gemini AI + Busca Semântica • Conforme padrões WCAG AA de acessibilidade</p>
    </div>
""", unsafe_allow_html=True)
