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
        border-top: 5px solid; 
    }
    .maquina-id { color: #9ca3af; font-size: 0.7em; margin-bottom: 5px; text-transform: uppercase; }
    .maquina-nome { color: white; font-weight: bold; font-size: 1.1em; margin-bottom: 15px; }
    .status-texto { font-weight: bold; font-size: 1.2em; text-transform: uppercase; }
    
    /* Linha do motivo que você pediu */
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

# 2. Carregamento de Dados (Mantenha o seu método de leitura original aqui)
# Se você usa pd.read_csv("nome_do_arquivo.csv"), mantenha-o.
def carregar_dados():
    try:
        # Tenta ler o seu CSV original
        df = pd.read_csv('dados_manutencao.csv') 
        return df
    except:
        # Fallback apenas para não dar erro de tela vazia se o arquivo sumir
        return pd.DataFrame([
            {"ID": "1311", "Maquina": "2 - HT_1311", "OS": "-", "Status": "Normal"},
            {"ID": "1202", "Maquina": "39 - Rama LK_1202", "OS": "2548", "Status": "Finalizada"}
        ])

df = carregar_dados()

# 3. Grid de Colunas (Restaurando o layout de 5 colunas dos seus prints)
if not df.empty:
    cols = st.columns(5)
    
    for index, row in df.iterrows():
        status_raw = str(row['Status']).strip().lower()
        os_atual = str(row['OS'])
        
        # LÓGICA DE CORES E MOTIVOS
        # AMARELO: Aberta ou Em Execução
        if status_raw in ['aberta', 'em execução', 'execução']:
            cor = "#f1c40f"
            label = "ATENÇÃO"
            motivo = f"🛠️ O.S. {os_atual} em andamento"
        
        # VERDE: Finalizada ou Normal (Equipamento Operando)
        elif status_raw in ['finalizada', 'normal', 'operando', '']:
            cor = "#2ecc71"
            label = "NORMAL"
            motivo = "✅ Equipamento Operando"
        
        # VERMELHO: Parada
        else:
            cor = "#e74c3c"
            label = "PARADA"
            motivo = "⚠️ Manutenção Corretiva"

        # Renderização do Card no estilo exato da sua imagem b87e7b.png
        with cols[index % 5]:
            st.markdown(f"""
                <div class="card" style="border-top-color: {cor};">
                    <div class="maquina-id">ID SISTEMA: {row['ID']}</div>
                    <div class="maquina-nome">{row['Maquina']}</div>
                    <div class="status-texto" style="color: {cor};">{label}</div>
                    <div class="motivo-sub">{motivo}</div>
                </div>
            """, unsafe_allow_html=True)
