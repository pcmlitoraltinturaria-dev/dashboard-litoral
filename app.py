import streamlit as st
import requests
from datetime import datetime

# 1. Configuração e Refresh
st.set_page_config(page_title="Monitoramento Litoral", layout="wide")
st.components.v1.html("<script>setTimeout(function(){window.location.reload();}, 30000);</script>", height=0)

# 2. CSS (Ajuste de letras e posição)
st.markdown("""
    <style>
    .block-container { padding-top: 5.5rem !important; max-width: 98% !important; margin: 0 auto; }
    .stApp { background-color: #0b0e14; }
    header { visibility: hidden; }
    .card {
        background-color: #1a1f29; padding: 12px 5px; border-radius: 5px;
        text-align: center; margin-bottom: 8px; min-height: 155px; 
        display: flex; flex-direction: column; justify-content: space-between; 
        align-items: center; border: 1px solid #232a37; border-top: 7px solid;
    }
    .nome-topo { color: #a0aec0; font-size: 0.65rem; font-weight: 700; text-transform: uppercase; }
    .id-numeros { font-size: 2.3rem; font-weight: 900; color: #ffffff; line-height: 1; letter-spacing: -1px; }
    .status-area { font-weight: 800; font-size: 0.85rem; text-transform: uppercase; margin: 6px 0; }
    .tag-servico { color: #ffffff; font-weight: bold; font-size: 0.7rem; background: #334155; border-radius: 3px; padding: 3px 0; width: 92%; }
    .border-normal { border-top-color: #2ecc71 !important; }
    .border-parada { border-top-color: #ff0000 !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. Busca de Dados
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
# Quebra o texto por linhas para não misturar informações de máquinas diferentes
linhas_texto = string_bruta.split("\\N") 

cols = st.columns(8)

for idx, at in enumerate(ativos):
    # PADRÃO É SEMPRE VERDE
    status, cor, classe, icon, servico = "NORMAL", "#2ecc71", "border-normal", "✅", "EM OPERAÇÃO"
    
    # Busca a linha específica que contém o ID da máquina
    linha_da_maquina = ""
    for linha in linhas_texto:
        if at['id'] in linha:
            linha_da_maquina = linha
            break
    
    # SE encontrar a linha, verifica SE nela está escrito MÁQUINA PARADA
    if linha_da_maquina:
        if "MÁQUINA PARADA" in linha_da_maquina:
            status, cor, classe, icon, servico = "PARADA", "#ff0000", "border-parada", "🛑", "CORRETIVA"
        # Note que se na linha estiver "NORMAL" ou "PARCIAL", ele ignora e mantém VERDE

    id_exibicao = at['id'].replace("_", "").replace("QUIMICO", "")

    with cols[idx % 8]:
        st.markdown(f"""
            <div class="card {classe}">
                <div class="nome-topo">{at['n']}</div>
                <div class="id-numeros">{id_exibicao}</div>
                <div class="status-area" style="color: {cor};">{icon} {status}</div>
                <div class="tag-servico">{servico}</div>
            </div>
        """, unsafe_allow_html=True)
