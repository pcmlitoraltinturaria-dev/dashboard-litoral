import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. Configuração de Layout e Estilo (Fundo Escuro Original)
st.set_page_config(page_title="Monitor de Manutenção", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    h1 { color: #4a5568; font-family: 'Arial Black', sans-serif; border-bottom: 2px solid #2d3748; padding-bottom: 10px; }
    
    .card {
        background-color: #1f2937;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 15px;
        min-height: 180px;
        border-top: 8px solid; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .maquina-id { color: #9ca3af; font-size: 0.75em; margin-bottom: 8px; }
    .maquina-nome { color: white; font-weight: bold; font-size: 1em; margin-bottom: 15px; height: 40px; display: flex; align-items: center; justify-content: center; }
    .status-texto { font-weight: bold; font-size: 1.1em; text-transform: uppercase; }
    .motivo-sub { color: #d1d5db; font-size: 0.8em; margin-top: 10px; border-top: 1px solid #374151; padding-top: 8px; }
    </style>
    """, unsafe_allow_html=True)

st.title("MONITOR DE MANUTENÇÃO :: LITORAL")

# 2. Função para carregar dados reais (URL da sua planilha)
@st.cache_data(ttl=30)
def carregar_dados():
    # COLOQUE O SEU LINK DO GOOGLE SHEETS ABAIXO
    url = "SUA_URL_DO_GOOGLE_SHEETS_AQUI"
    try:
        response = requests.get(url)
        df = pd.read_csv(StringIO(response.text))
        return df
    except:
        return pd.DataFrame()

df = carregar_dados()

# 3. Renderização de todos os itens da planilha
if not df.empty:
    # Definindo 5 colunas para o grid
    cols = st.columns(5)
    
    for index, row in df.iterrows():
        # Lógica de Cores e Status
        status_raw = str(row['Status']).strip().lower()
        os_atual = str(row['OS'])
        
        # AMARELO: Aberta ou Em Execução
        if status_raw in ['aberta', 'em execução', 'execução']:
            cor = "#f1c40f"
            label = "ATENÇÃO"
            motivo = f"🛠️ O.S. {os_atual} em andamento"
        
        # VERDE: Finalizada, Normal ou Operando
        elif status_raw in ['finalizada', 'normal', 'operando', '']:
            cor = "#2ecc71"
            label = "NORMAL"
            motivo = "✅ Equipamento Operando"
        
        # VERMELHO: Qualquer outro estado (Parada/Crítica)
        else:
            cor = "#e74c3c"
            label = "PARADA"
            motivo = "⚠️ Manutenção Corretiva"

        # Distribui os cards nas colunas
        with cols[index % 5]:
            st.markdown(f"""
                <div class="card" style="border-top-color: {cor};">
                    <div class="maquina-id">ID SISTEMA: {row['ID']}</div>
                    <div class="maquina-nome">{row['Maquina']}</div>
                    <div class="status-texto" style="color: {cor};">{label}</div>
                    <div class="motivo-sub">{motivo}</div>
                </div>
            """, unsafe_allow_html=True)
else:
    st.error("Erro: Verifique se o link da planilha no código está correto.")
