import streamlit as st
import pandas as pd

# 1. Configuração de Layout e Estilo (Mantendo o padrão Litoral das imagens)
st.set_page_config(page_title="Monitor de Manutenção", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    h1 { color: #4a5568; font-family: 'Arial Black'; border-bottom: 2px solid #2d3748; padding-bottom: 10px; }
    
    .card {
        background-color: #1f2937;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 15px;
        height: 180px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        border-top: 8px solid; /* A cor será dinâmica */
    }
    .maquina-id { color: #9ca3af; font-size: 0.8em; margin-bottom: 5px; }
    .maquina-nome { color: white; font-weight: bold; font-size: 1.1em; margin-bottom: 15px; }
    .status-texto { font-weight: bold; font-size: 1.2em; text-transform: uppercase; }
    .motivo-sub { color: #d1d5db; font-size: 0.85em; margin-top: 10px; border-top: 1px solid #374151; padding-top: 8px; }
    </style>
    """, unsafe_allow_html=True)

st.title("MONITOR DE MANUTENÇÃO :: LITORAL")

# 2. Função para ler os dados (Ajuste o caminho para o seu CSV real)
# Supondo que as colunas sejam: ID, Máquina, O.S., Status
def carregar_dados():
    try:
        # Substitua 'dados_manutencao.csv' pelo nome correto do seu arquivo
        df = pd.read_csv('dados_manutencao.csv') 
        return df
    except:
        # Dados de fallback caso o arquivo não carregue para não quebrar o layout
        return pd.DataFrame([
            {"ID": "1202", "Maquina": "Rama LK_1202", "OS": "2548", "Status": "Finalizada"},
            {"ID": "1311", "Maquina": "2 - HT_1311", "OS": "-", "Status": "Normal"}
        ])

df = carregar_dados()

# 3. Exibição em Grid (5 colunas como na sua foto)
cols = st.columns(5)
idx_col = 0

for index, row in df.iterrows():
    status_raw = str(row['Status']).strip().lower()
    os_num = str(row['OS'])
    
    # Lógica de Cores e Motivos (Sua solicitação)
    if status_raw in ['aberta', 'em execução', 'execução']:
        cor_borda = "#f1c40f" # Amarelo
        status_label = "ATENÇÃO"
        motivo = f"🛠️ O.S. {os_num} em andamento"
    elif status_raw in ['finalizada', 'normal', 'operando', '']:
        cor_borda = "#2ecc71" # Verde
        status_label = "NORMAL"
        motivo = "✅ Equipamento Operando"
    else:
        cor_borda = "#e74c3c" # Vermelho
        status_label = "PARADA"
        motivo = "⚠️ Manutenção Corretiva"

    with cols[idx_col]:
        st.markdown(f"""
            <div class="card" style="border-top-color: {cor_borda};">
                <div class="maquina-id">ID SISTEMA: {row['ID']}</div>
                <div class="maquina-nome">{row['Maquina']}</div>
                <div class="status-texto" style="color: {cor_borda};">{status_label}</div>
                <div class="motivo-sub">{motivo}</div>
            </div>
        """, unsafe_allow_html=True)
    
    idx_col = (idx_col + 1) % 5
