print(f"SCRIPT CLARO AJUSTADO DEEPSEEK")

import streamlit as st
from rag_engine import ask, retrieve
import os

# ==========================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Assistente SEAD-GO", 
    page_icon="🤖", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# CSS PERSONALIZADO - LIMPO E EFICIENTE
# ==========================================
st.markdown("""
    <style>
    /* Configurações gerais */
    .stApp {
        background: #F9F9F9;
        color: #000000;
        font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    }
    
    /* Remove elementos padrão do Streamlit */
    .stApp > header {
        background-color: transparent;
    }
    
    [data-testid="stHeader"] {
        display: none !important;
    }
    
    .stSidebar {
        display: none !important;
    }
    
    section[data-testid="stSidebar"] {
        display: none !important;
    }
    
    /* Header principal - LIMPO E DIRETO */
    .main-header {
        background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%);
        padding: 3rem 0 2rem 0;
        margin: -1rem -1rem 3rem -1rem;
        border-bottom: 3px solid #1E3C72;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        position: relative;
        overflow: hidden;
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
        padding: 0 3rem;
        display: flex;
        align-items: center;
        gap: 3rem;
    }
    
    .logo-container {
        flex-shrink: 0;
        padding: 2rem;
        background: white;
        border-radius: 16px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.12);
        border: 2px solid #E8E8E8;
    }
    
    .logo-img {
        height: 240px;
        border-radius: 12px;
        filter: drop-shadow(0 4px 16px rgba(0,0,0,0.15));
    }
    
    .title-container {
        flex-grow: 1;
        padding: 1rem 0;
    }
    
    .main-title {
        font-size: 3.5rem;
        font-weight: 800;
        color: #1E3C72;
        margin: 0 0 1rem 0;
        line-height: 1.1;
        letter-spacing: -0.02em;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        background: linear-gradient(135deg, #1E3C72, #2A5298);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .department {
        font-size: 1.8rem;
        color: #000000;
        margin: 1rem 0 0 0;
        font-weight: 600;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        background: linear-gradient(135deg, #1E3C72, #2A5298);
        color: white;
        padding: 1.2rem 2rem;
        border-radius: 12px;
        display: inline-block;
        box-shadow: 0 6px 20px rgba(30, 60, 114, 0.3);
    }
    
    /* Container principal */
    .main-container {
        max-width: 1000px;
        margin: 0 auto;
        padding: 0 2rem;
    }
    
    /* Área de input */
    .input-container {
        background: #FFFFFF;
        padding: 2.5rem;
        border-radius: 16px;
        box-shadow: 0 6px 24px rgba(0,0,0,0.1);
        margin-bottom: 2.5rem;
        border: 2px solid #1E3C72;
    }
    
    /* Histórico de chat */
    .chat-history-container {
        margin-bottom: 3rem;
    }
    
    .chat-container {
        margin-bottom: 1.5rem;
    }
    
    .user-message {
        background: linear-gradient(135deg, #1E3C72 0%, #2A5298 100%);
        color: #FFFFFF;
        padding: 1.8rem;
        margin: 0 0 0.8rem 0;
        border-radius: 18px 18px 6px 18px;
        box-shadow: 0 4px 16px rgba(30, 60, 114, 0.3);
        border: 2px solid #1E3C72;
        max-width: 80%;
        margin-left: auto;
    }
    
    .assistant-message {
        background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%);
        color: #000000;
        padding: 1.8rem;
        margin: 0 0 0.8rem 0;
        border-radius: 18px 18px 18px 6px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        border: 2px solid #E0E0E0;
        max-width: 80%;
    }
    
    .message-sender {
        font-weight: 700;
        font-size: 1rem;
        color: #1E3C72;
        margin-bottom: 0.8rem;
        display: block;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    .user-sender {
        color: #FFFFFF;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }
    
    .message-content {
        font-size: 1.1rem;
        line-height: 1.6;
        color: #000000;
        margin: 0;
        font-weight: 500;
    }
    
    .user-content {
        color: #FFFFFF;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }
    
    /* Input styling */
    .stTextInput>div>div>input {
        background-color: #FFFFFF;
        color: #000000;
        border: 2px solid #1E3C72;
        border-radius: 12px;
        padding: 16px 20px;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        font-weight: 500;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #2A5298;
        box-shadow: 0 0 0 3px rgba(30, 60, 114, 0.15);
        outline: none;
    }
    
    .stTextInput>div>div>input::placeholder {
        color: #666666;
        font-weight: 400;
    }
    
    /* Botões */
    .stButton>button {
        background: linear-gradient(135deg, #1E3C72 0%, #2A5298 100%);
        color: #FFFFFF;
        border: 2px solid #1E3C72;
        border-radius: 12px;
        padding: 16px 28px;
        font-weight: 700;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 4px 12px rgba(30, 60, 114, 0.3);
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #2A5298 0%, #3B6FD9 100%);
        border-color: #2A5298;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(42, 82, 152, 0.4);
    }
    
    .secondary-button>button {
        background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%);
        color: #1E3C72;
        border: 2px solid #1E3C72;
        border-radius: 12px;
        padding: 16px 28px;
        font-weight: 700;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .secondary-button>button:hover {
        background: linear-gradient(135deg, #F0F7FF 0%, #E8F2FF 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(30, 60, 114, 0.2);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #000000;
        margin-top: 4rem;
        padding: 2.5rem;
        border-top: 2px solid #1E3C72;
        font-size: 1rem;
        background: #FFFFFF;
        border-radius: 16px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.08);
        font-weight: 600;
    }
    
    /* Estado vazio */
    .empty-state {
        text-align: center;
        padding: 4rem 3rem;
        color: #000000;
        background: #FFFFFF;
        border-radius: 16px;
        border: 2px solid #1E3C72;
        box-shadow: 0 6px 24px rgba(0,0,0,0.1);
        margin: 2rem 0;
    }
    
    .empty-state h3 {
        color: #1E3C72;
        margin-bottom: 2rem;
        font-size: 1.8rem;
        font-weight: 700;
    }
    
    .empty-state p {
        font-size: 1.1rem;
        margin-bottom: 2rem;
        font-weight: 500;
    }
    
    .empty-state ul {
        text-align: left;
        display: inline-block;
        color: #000000;
        max-width: 500px;
    }
    
    .empty-state li {
        margin-bottom: 1rem;
        line-height: 1.5;
        padding: 0.8rem 1.2rem;
        background: rgba(30, 60, 114, 0.05);
        border-radius: 8px;
        border-left: 4px solid #1E3C72;
        font-weight: 500;
    }
    
    /* Títulos */
    .section-title {
        color: #1E3C72;
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        padding-bottom: 0.8rem;
        border-bottom: 2px solid #1E3C72;
    }
    
    /* Emoji ajustado */
    .welcome-emoji {
        font-size: 2.5rem;
        filter: grayscale(0.3);
        display: block;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# FUNÇÃO PARA EXIBIR A LOGO
# ==========================================
def display_logo(logo_path="seadgo_logo.png", width=240):
    """
    Tenta carregar e exibir a logo da SEAD-GO
    """
    try:
        if os.path.exists(logo_path):
            st.image(logo_path, width=width)
        else:
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #1E3C72, #2A5298); 
                            width: {width}px; height: {width}px; 
                            border-radius: 16px; 
                            display: flex; 
                            align-items: center; 
                            justify-content: center;
                            font-weight: 700;
                            color: white;
                            font-size: 28px;
                            box-shadow: 0 8px 32px rgba(0,0,0,0.15);">
                    SEAD-GO
                </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        st.markdown(f"""
            <div style="background: #1E3C72; 
                        width: {width}px; height: {width}px; 
                        border-radius: 16px; 
                        display: flex; 
                        align-items: center; 
                        justify-content: center;
                        font-weight: 700;
                        color: white;
                        font-size: 24px;
                        box-shadow: 0 8px 32px rgba(0,0,0,0.15);">
                SEAD-GO
            </div>
        """, unsafe_allow_html=True)

# ==========================================
# HEADER SIMPLIFICADO
# ==========================================
st.markdown("""
    <div class="main-header">
        <div class="header-content">
            <div class="logo-container">
""", unsafe_allow_html=True)

# Exibe a logo
display_logo("seadgo_logo.png", width=240)

# Header simplificado - SEM texto repetido
st.markdown("""
            </div>
            <div class="title-container">
                <h1 class="main-title">Assistente SEAD-GO</h1>
                <p class="department">Secretaria de Estado de Administração - Governo de Goiás</p>
                <!-- REMOVIDO: "Assistente Inteligente de Documentos Institucionais" -->
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# INICIALIZAÇÃO DO HISTÓRICO
# ==========================================
if "history" not in st.session_state:
    st.session_state.history = []

# ==========================================
# CONTEÚDO PRINCIPAL
# ==========================================
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Área de input - SEM bloco vazio centralizado
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
    if st.button("🚀 Enviar Pergunta", use_container_width=True) and query:
        with st.spinner("🔍 Buscando informações nos documentos..."):
            try:
                resposta = ask(query)
            except Exception as e:
                resposta = f"❌ Erro ao gerar resposta: {e}"
        st.session_state.history.append((query, resposta))
        st.rerun()

with col_btn2:
    if st.button("🗑️ Limpar Histórico", use_container_width=True, key="clear_btn"):
        st.session_state.history = []
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Histórico de conversas
st.markdown("### 📝 Histórico da Conversa")

if not st.session_state.history:
    # Estado vazio melhorado - EMOJI AJUSTADO
    st.markdown("""
        <div class="empty-state">
            <span class="welcome-emoji">👋</span>
            <h3>Bem-vindo ao Assistente SEAD-GO</h3>
            <p>Faça sua primeira pergunta para começar a conversa com nosso assistente inteligente.</p>
            <p><strong>Exemplos de perguntas:</strong></p>
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
    st.markdown('<div class="chat-history-container">', unsafe_allow_html=True)
    
    # Exibe o histórico de conversas
    for q, r in st.session_state.history:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        # Mensagem do usuário
        st.markdown(f'''
            <div class="user-message">
                <span class="message-sender user-sender">👤 Você</span>
                <div class="message-content user-content">{q}</div>
            </div>
        ''', unsafe_allow_html=True)
        
        # Mensagem do assistente
        st.markdown(f'''
            <div class="assistant-message">
                <span class="message-sender">🤖 Assistente SEAD-GO</span>
                <div class="message-content">{r}</div>
            </div>
        ''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Fecha main-container

# ==========================================
# FOOTER
# ==========================================
st.markdown("""
    <div class="footer">
        <p><strong>Assistente SEAD-GO</strong> • Desenvolvido para a Secretaria de Estado de Administração de Goiás</p>
        <p>Tecnologia: Gemini AI + Busca Semântica</p>
    </div>
""", unsafe_allow_html=True)