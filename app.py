import streamlit as st
import requests
from datetime import datetime
import re

# Configuração de UI
st.set_page_config(page_title="Monitoramento Litoral", layout="wide")

# CSS Ajustado para tamanho de letras e alinhamento
st.markdown(f"""
    <style>
    .block-container {{ padding-top: 2rem !important; max-width: 98% !important; }}
    .stApp {{ background-color: #0b0e14; }}
    
    .card {{
        background-color: #1a1f29; 
        padding: 8px 3px; 
        border-radius: 4px;
        text-align: center; 
        margin-bottom: 5px; 
        min-height: 140px; 
        display: flex; 
        flex-direction: column;
        justify-content: space-between; 
        align-items: center; 
        border: 1px solid #232a37;
        border-top: 7px solid;
    }}

    /* Ajuste de tamanho de letras para evitar sobreposição */
    .nome-topo {{ 
        color: #a0aec0; 
        font-size: 0.65rem; /* Letras menores no topo */
        font-weight: 700; 
        text-transform: uppercase;
        white-space: nowrap;
        overflow: hidden;
    }}
    
    .id-container {{ 
        color: #ffffff; 
        margin: 2px 0;
        width: 100%;
    }}
    
    .id-numeros {{ 
        font-size: 2.2rem; /* Reduzido de 3rem para 2.2rem para caber no card */
        font-weight: 900;
        letter-spacing: -1px;
    }}

    .status-area {{ 
        font-weight: 800; 
        font-size: 0.8rem; /* Letras do status (NORMAL/PARADA) */
        text-transform: uppercase;
    }}

    .tag-servico {{ 
        color: #ffffff !important; 
        font-weight: bold; 
        font-size: 0.7rem; /* Letra da base (EM OPERAÇÃO) */
        background: #334155; 
        border-radius: 3px; 
        padding: 2px 0; 
        width: 95%;
        text-transform: uppercase;
    }}

    /* Classes de bordas */
    .border-normal {{ border-top-color: #2ecc71 !important; }}
    .border-parada {{ border-top-color: #ff0000 !important; }}
    .farol-aviso {{ border-top-color: #ff8c00 !important; }}

    [data-testid="column"] {{ padding: 2px !important; }}
    </style>
    """, unsafe_allow_html=True)

# Lógica de processamento (Dados do texto como prioridade)
def buscar_dados():
    try:
        r = requests.get("https://dashboard-manutencao-ef55f-default-rtdb.firebaseio.com/manutencao.json")
        return r.text.upper() if r.text else ""
    except: return ""

ativos = [
    {"id": "701", "n": "BIANCO"}, {"id": "1501", "n": "BRASTEC 1"}, {"id": "1502", "n": "BRASTEC 2"},
    {"id": "1503", "n": "BRASTEC 3"}, {"id": "1504", "n": "BRASTEC 4"}, {"id": "1506", "n": "BRASTEC 6"},
    {"id": "804", "n": "ALBRECHT"}, {"id": "803", "n": "LAFER"}, {"id": "1201", "n": "UNITECH"},
    {"id": "_1202", "n": "LK"}, {"id": "1404", "n": "HIDRORELAX"}, {"id": "1601", "n": "CORANTE"},
    {"id": "QUIMICO_1602", "n": "QUÍMICO"}, {"id": "1306", "n": "HT 1306"}, {"id": "1311", "n": "HT 1311"},
    {"id": "1314", "n": "HT 1314"}, {"id": "HT_1324", "n": "HT 1324"}, {"id": "HT_1308", "n": "HT 1308"},
    {"id": "HT_1303", "n": "HT 1303"}, {"id": "HT_1313", "n": "HT 1313"}, {"id": "1001", "n": "FELP 1"},
    {"id": "1002", "n": "FELP 2"}, {"id": "2603", "n": "SECADOR"}, {"id": "HT_1316", "n": "HT 1316"}
]

string_bruta = buscar_dados()
cols = st.columns(8)

for idx, at in enumerate(ativos):
    pos = string_bruta.rfind(at['id'])
    # REGRA: Se não disser parada ou parcial no texto, é VERDE
    status, cor, classe, icon, servico = "NORMAL", "#2ecc71", "border-normal", "✅", "EM OPERAÇÃO"
    
    if pos != -1:
        ctx = string_bruta[pos : pos + 300]
        if "MÁQUINA PARADA" in ctx:
            status, cor, classe, icon, servico = "PARADA", "#ff0000", "border-parada", "🛑", "CORRETIVA"
        elif "MÁQ.PAR.PARCIAL" in ctx:
            status, cor, classe, icon, servico = "AVISO", "#ff8c00", "farol-aviso", "⚠️", "PARCIAL"

    # ID limpo para exibição
    id_visivel = at['id'].replace("_", "").replace("QUIMICO", "")

    with cols[idx % 8]:
        st.markdown(f"""
            <div class="card {classe}">
                <div class="nome-topo">{at['n']}</div>
                <div class="id-container">
                    <span class="id-numeros">{id_visivel}</span>
                </div>
                <div class="status-area" style="color: {cor};">{icon} {status}</div>
                <div class="tag-servico">{servico}</div>
            </div>
        """, unsafe_allow_html=True)
