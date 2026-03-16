import streamlit as st
import requests
import pandas as pd

# 1. Configuração de Layout Original (Litoral Tinturaria)
st.set_page_config(page_title="Monitor de Manutenção Litoral", layout="wide")

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
        min-height: 190px;
        border-top: 5px solid; 
    }
    .maquina-id { color: #9ca3af; font-size: 0.7em; margin-bottom: 5px; text-transform: uppercase; }
    .maquina-nome { color: white; font-weight: bold; font-size: 1.1em; margin-bottom: 10px; min-height: 45px; display: flex; align-items: center; justify-content: center; }
    .status-texto { font-weight: bold; font-size: 1.2em; text-transform: uppercase; }
    
    .motivo-sub { 
        color: #d1d5db; 
        font-size: 0.85em; 
        margin-top: 15px; 
        border-top: 1px solid #374151; 
        padding-top: 10px;
        font-style: italic;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("MONITOR DE MANUTENÇÃO :: LITORAL")

# 2. Conexão com Firebase (Dados Reais)
def buscar_dados_firebase():
    url = "https://dashboard-manutencao-ef55f-default-rtdb.firebaseio.com/manutencao.json"
    try:
        response = requests.get(url)
        return response.text.upper() # Transformamos em maiúsculo para facilitar a busca
    except:
        return ""

string_bruta = buscar_dados_firebase()

# 3. Lista Oficial de Ativos (Conforme seu Script de Recuperação)
ativos = [
    {"id": "701", "nome": "ABRIDOR BIANCO"},
    {"id": "1501", "nome": "ABRIDOR BRASTEC 1"},
    {"id": "1502", "nome": "ABRIDOR BRASTEC 2"},
    {"id": "1503", "nome": "ABRIDOR BRASTEC 3"},
    {"id": "1504", "nome": "ABRIDOR BRASTEC 4"},
    {"id": "1506", "nome": "ABRIDOR BRASTEC 6"},
    {"id": "1404", "nome": "HIDRORELAXADORA"},
    {"id": "804", "nome": "CALANDRA ALBRECHT"},
    {"id": "803", "nome": "CALANDRA LAFER"},
    {"id": "1202", "nome": "RAMA LK"},
    {"id": "1201", "nome": "RAMA UNITECH"},
    {"id": "1601", "nome": "COZINHA CORANTE"},
    {"id": "1602", "nome": "COZINHA QUÍMICO"},
    {"id": "1001", "nome": "FELPADEIRA 1"},
    {"id": "1002", "nome": "FELPADEIRA 2"},
    {"id": "59", "nome": "HT 1324"},
    {"id": "1306", "nome": "HT 1306"},
    {"id": "1311", "nome": "HT 1311"},
    {"id": "1314", "nome": "HT 1314"},
    {"id": "2603", "nome": "SECADOR"},
    {"id": "26", "nome": "EMPILHADEIRA"}
]

# 4. Renderização do Grid
cols = st.columns(5)

for i, ativo in enumerate(ativos):
    # Lógica de Busca de Status na String do Firebase
    posicao = string_bruta.find(ativo['id'])
    contexto = string_bruta[posicao:posicao+150] if posicao != -1 else ""
    
    # DEFINIÇÃO DE CORES E MOTIVOS
    if "MÁQUINA PARADA" in contexto:
        cor = "#e74c3c" # Vermelho
        label = "PARADA"
        motivo = "⚠️ Manutenção Corretiva"
    elif "ABERTA" in contexto or "EXECUÇÃO" in contexto:
        cor = "#f1c40f" # Amarelo (NOVO)
        label = "ATENÇÃO"
        motivo = "🛠️ O.S. em Andamento"
    elif "MÁQ.PAR.PARCIAL" in contexto:
        cor = "#e67e22" # Laranja
        label = "ALERTA"
        motivo = "🟠 Parada Parcial"
    else:
        cor = "#2ecc71" # Verde
        label = "NORMAL"
        motivo = "✅ Equipamento Operando"

    with cols[i % 5]:
        st.markdown(f"""
            <div class="card" style="border-top-color: {cor};">
                <div class="maquina-id">ID SISTEMA: {ativo['id']}</div>
                <div class="maquina-nome">{ativo['nome']}</div>
                <div class="status-texto" style="color: {cor};">{label}</div>
                <div class="motivo-sub">{motivo}</div>
            </div>
        """, unsafe_allow_html=True)
