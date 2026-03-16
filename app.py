import streamlit as st
import pandas as pd

# 1. Configuração de Layout e Estilo Original Litoral
st.set_page_config(page_title="Monitor de Manutenção", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    h1 { color: #4a5568; font-family: 'Arial Black', sans-serif; border-bottom: 2px solid #2d3748; padding-bottom: 10px; }
    
    /* Layout dos Cards que você usa */
    .card {
        background-color: #1f2937;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 15px;
        min-height: 160px;
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

# 2. Carregar os dados (Ajuste o caminho para o seu CSV ou Google Sheets)
@st.cache_data(ttl=60) # Atualiza a cada 1 minuto
def carregar_dados():
    # Se você usa Google Sheets ou CSV local, coloque o link/caminho aqui
    # df = pd.read_csv("SEU_ARQUIVO.csv") 
    
    # Exemplo baseado no seu print (Rama LK_1202, HT_1311, etc)
    # Certifique-se de que essas colunas existem no seu arquivo!
    dados = [
        {"ID": "1311", "Maquina": "2 - HT_1311", "OS": "-", "Status": "Normal"},
        {"ID": "701", "Maquina": "25 - Abridor Bianco_701", "OS": "-", "Status": "Normal"},
        {"ID": "1501", "Maquina": "26 - Abridor de malha Brastec 1_1501", "OS": "-", "Status": "Normal"},
        {"ID": "1202", "Maquina": "39 - Rama LK_1202", "OS": "2548", "Status": "Finalizada"},
        {"ID": "2550", "Maquina": "Tear Circular 01", "OS": "2550", "Status": "Em Execução"},
    ]
    return pd.DataFrame(dados)

df = carregar_dados()

# 3. Gerar o Grid de 5 colunas (para caber todas na tela como no seu print)
cols = st.columns(5)
idx_col = 0

for index, row in df.iterrows():
    # Lógica de processamento de status
    status_raw = str(row['Status']).strip().lower()
    os_atual = str(row['OS'])
    
    # Definição de Cores e Mensagens
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

    # Renderização no Grid
    with cols[idx_col]:
        st.markdown(f"""
            <div class="card" style="border-top-color: {cor};">
                <div class="maquina-id">ID SISTEMA: {row['ID']}</div>
                <div class="maquina-nome">{row['Maquina']}</div>
                <div class="status-texto" style="color: {cor};">{label}</div>
                <div class="motivo-sub">{motivo}</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Controla a quebra de colunas (5 por linha)
    idx_col = (idx_col + 1) % 5
