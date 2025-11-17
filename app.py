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
# CSS PERSONALIZADO - DESIGN ESCURO ELEGANTE
# ==========================================
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f1f5f9;
    }
    
    /* Remove qualquer barra azul padrão do Streamlit */
    .stApp > header {
        background-color: transparent;
    }
    
    .decoration {
        display: none;
    }
    
    /* Header principal */
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 2.5rem 0;
        margin: -1rem -1rem 3rem -1rem;
        border-radius: 0 0 25px 25px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent 0%, rgba(255,255,255,0.1) 100%);
        pointer-events: none;
    }
    
    .header-content {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 2rem;
        display: flex;
        align-items: center;
        gap: 2.5rem;
        position: relative;
        z-index: 2;
    }
    
    .logo-container {
        flex-shrink: 0;
    }
    
    .logo-img {
        height: 120px;
        border-radius: 16px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        border: 2px solid rgba(255,255,255,0.1);
    }
    
    .title-container {
        flex-grow: 1;
    }
    
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        color: white;
        margin: 0;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.4);
        line-height: 1.1;
        letter-spacing: -0.5px;
    }
    
    .subtitle {
        font-size: 1.4rem;
        color: #e2e8f0;
        margin: 0.8rem 0 0 0;
        font-weight: 400;
        text-shadow: 1px 1px 4px rgba(0,0,0,0.3);
    }
    
    .department {
        font-size: 1.1rem;
        color: #94a3b8;
        margin: 0.3rem 0 0 0;
        font-weight: 300;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    
    /* Container principal */
    .main-container {
        max-width: 900px;
        margin: 0 auto;
        padding: 0 1rem;
    }
    
    /* Área de input */
    .input-container {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        margin-bottom: 2.5rem;
        border: 1px solid #475569;
        backdrop-filter: blur(10px);
    }
    
    /* Histórico de chat */
    .chat-container {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border-radius: 20px;
        padding: 0;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        border: 1px solid #475569;
        overflow: hidden;
        backdrop-filter: blur(10px);
    }
    
    .user-message {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 1.8rem;
        margin: 0;
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }
    
    .assistant-message {
        background: rgba(30, 41, 59, 0.7);
        padding: 1.8rem;
        margin: 0;
        color: #f1f5f9;
        border-left: 4px solid #3b82f6;
    }
    
    /* Input styling */
    .stTextInput>div>div>input {
        background-color: #0f172a;
        color: #f1f5f9;
        border: 2px solid #475569;
        border-radius: 12px;
        padding: 16px 20px;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        background-color: #1e293b;
    }
    
    .stTextInput>div>div>input::placeholder {
        color: #94a3b8;
    }
    
    /* Botões */
    .stButton>button {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 16px 32px;
        font-weight: 600;
        font-size: 16px;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 4px 15px rgba(30, 60, 114, 0.3);
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #2a5298 0%, #3b6fd9 100%);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(42, 82, 152, 0.4);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #94a3b8;
        margin-top: 4rem;
        padding: 2.5rem;
        border-top: 1px solid #334155;
        font-size: 0.9rem;
        background: rgba(15, 23, 42, 0.8);
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
    }
    
    /* Estado vazio */
    .empty-state {
        text-align: center;
        padding: 4rem 2rem;
        color: #94a3b8;
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border-radius: 20px;
        border: 1px solid #475569;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    
    .empty-state h3 {
        color: #e2e8f0;
        margin-bottom: 1.5rem;
        font-size: 1.5rem;
    }
    
    .empty-state ul {
        text-align: left;
        display: inline-block;
        color: #cbd5e1;
    }
    
    .empty-state li {
        margin-bottom: 0.5rem;
    }
    
    /* Remove sidebar completamente */
    .stSidebar {
        display: none !important;
    }
    
    section[data-testid="stSidebar"] {
        display: none !important;
    }
    
    /* Remove qualquer barra azul residual */
    [data-testid="stHeader"] {
        display: none !important;
    }
    
    /* Melhora a tipografia */
    h1, h2, h3, h4, h5, h6 {
        color: #f1f5f9 !important;
    }
    
    .stMarkdown {
        color: #f1f5f9;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# FUNÇÃO PARA EXIBIR A LOGO
# ==========================================
def display_logo(logo_path="seadgo_logo.png", width=120):
    """
    Tenta carregar e exibir a logo da SEAD-GO
    """
    try:
        if os.path.exists(logo_path):
            st.image(logo_path, width=width)
        else:
            # Placeholder estilizado se a logo não for encontrada
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #1e3c72, #2a5298); 
                            width: {width}px; height: {width}px; 
                            border-radius: 16px; 
                            display: flex; 
                            align-items: center; 
                            justify-content: center;
                            font-weight: bold;
                            color: white;
                            font-size: 16px;
                            box-shadow: 0 8px 25px rgba(0,0,0,0.3);
                            border: 2px solid rgba(255,255,255,0.1);">
                    SEAD-GO
                </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        # Fallback em caso de erro
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1e3c72, #2a5298); 
                        width: {width}px; height: {width}px; 
                        border-radius: 16px; 
                        display: flex; 
                        align-items: center; 
                        justify-content: center;
                        font-weight: bold;
                        color: white;
                        font-size: 14px;
                        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
                        border: 2px solid rgba(255,255,255,0.1);">
                LOGO<br>SEAD-GO
            </div>
        """, unsafe_allow_html=True)

# ==========================================
# HEADER COM LOGO E TÍTULO
# ==========================================
st.markdown("""
    <div class="main-header">
        <div class="header-content">
            <div class="logo-container">
""", unsafe_allow_html=True)

# Exibe a logo
display_logo("seadgo_logo.png", width=120)

# Continuação do header com título
st.markdown("""
            </div>
            <div class="title-container">
                <h1 class="main-title">Assistente SEAD-GO</h1>
                <p class="subtitle">Assistente Inteligente de Documentos</p>
                <p class="department">Secretaria de Estado de Administração - Goiás</p>
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

# Área de input
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
        with st.spinner("🔍 Buscando informações nos documentos da SEAD-GO..."):
            try:
                resposta = ask(query)
            except Exception as e:
                resposta = f"❌ Erro ao gerar resposta: {e}"
        st.session_state.history.append((query, resposta))
        st.rerun()

with col_btn2:
    if st.button("🗑️ Limpar Histórico", use_container_width=True):
        st.session_state.history = []
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Histórico de conversas
st.markdown("### 📝 Conversa")

if not st.session_state.history:
    st.markdown("""
        <div class="empty-state">
            <h3>👋 Bem-vindo ao Assistente SEAD-GO!</h3>
            <p>Faça sua primeira pergunta para começar a conversa.</p>
            <p><strong>Exemplos de perguntas:</strong></p>
            <ul>
                <li>Quais são os procedimentos administrativos?</li>
                <li>Como funciona o processo de licitação?</li>
                <li>Quais documentos são necessários para abertura de processo?</li>
                <li>Quais são as normas de conduta da secretaria?</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

# Exibe o histórico de conversas
for q, r in st.session_state.history:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    st.markdown(f'<div class="user-message"><strong>👤 Você:</strong> {q}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="assistant-message"><strong>🤖 Assistente SEAD-GO:</strong> {r}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Fecha main-container

# ==========================================
# FOOTER
# ==========================================
st.markdown("""
    <div class="footer">
        <p><strong>Assistente SEAD-GO</strong> • Desenvolvido para a Secretaria de Estado de Administração de Goiás</p>
        <p>Tecnologia: Gemini AI + Busca Semântica • Versão 1.0</p>
    </div>
""", unsafe_allow_html=True)