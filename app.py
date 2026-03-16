import streamlit as st
import pandas as pd

# 1. Configuração de Layout Original (Fundo Escuro)
st.set_page_config(page_title="Monitor de Manutenção", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    h1 { color: #4a5568; font-family: 'Arial Black', sans-serif; border-bottom: 2px solid #2d3748; padding-bottom: 10px; }
    
    .card {
        background-color: #1f2937;
        padding: 15px;
        border-radius: 5px;
        text-align: center;
        margin-bottom: 15px;
        min-height: 180px;
        border-top: 5px solid; 
    }
    .maquina-id { color: #9ca3af; font-size: 0.7em; margin-bottom: 5px; text-transform: uppercase; }
    .maquina-nome { color: white; font-weight: bold; font-size: 1.1em; margin-bottom: 15px; min-height: 45px; display: flex; align-items: center; justify-content: center; }
    .status-texto { font-weight: bold; font-size: 1.2em; text-transform: uppercase; }
    
    .motivo-sub { 
        color: #d1d5db; 
        font-size: 0.85em; 
        margin-top: 15px; 
        border-top: 1px solid #374151; 
        padding-top: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("MONITOR DE MANUTENÇÃO :: LITORAL")

# 2. Carregamento de Dados (Lendo o arquivo local do GitHub)
@st.cache_data(ttl=10)
def carregar_dados():
    try:
        # IMPORTANTE: mude 'manutencao.csv' para o nome real do seu arquivo no GitHub
        return pd.read_csv('manutencao.csv') 
    except Exception as e:
        st.error(f"Erro ao ler arquivo: {e}")
        return pd.DataFrame()

df = carregar_dados()

# 3. Exibição de TODAS as máquinas do arquivo
if not df.empty:
    # Cria o grid de 5 colunas para caber todas na tela
    cols = st.columns(5)
    
    for index, row in df.iterrows():
        # Limpeza e lógica de status
        status_raw = str(row['Status']).strip().lower()
        os_atual = str(row['OS'])
        
        # Cores e Labels
        if status_raw in ['aberta', 'em execução', 'execução']:
            cor = "#f1c40f" # Amarelo
            label = "ATENÇÃO"
            motivo = f"🛠️ O.S. {os_atual} em andamento"
        elif status_raw in ['finalizada', 'normal', 'operando', '']:
            cor = "#2ecc71" # Verde
            label = "NORMAL"
            motivo = "✅ Equipamento Operando"
        else:
            cor = "#e74c3c" # Vermelho
            label = "PARADA"
            motivo = "⚠️ Manutenção Corretiva"

        # Coloca cada máquina em uma coluna (distribuição automática)
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
    st.warning("Aguardando carregamento de dados ou arquivo vazio.")
