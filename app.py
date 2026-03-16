import streamlit as st
import requests

# 1. Layout Original Litoral (Fundo Escuro)
st.set_page_config(page_title="Monitor Litoral", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .card {
        background-color: #1f2937;
        padding: 12px;
        border-radius: 5px;
        text-align: center;
        margin-bottom: 10px;
        min-height: 190px;
        border-top: 6px solid;
    }
    .maquina-id { color: #9ca3af; font-size: 0.65em; text-transform: uppercase; }
    .maquina-nome { color: white; font-weight: bold; font-size: 1em; margin: 8px 0; min-height: 40px; display: flex; align-items: center; justify-content: center; }
    .status-texto { font-weight: bold; font-size: 1.1em; text-transform: uppercase; }
    
    /* Motivo Ultra-Resumido */
    .motivo-sub { 
        color: #d1d5db; 
        font-size: 0.8em; 
        margin-top: 10px; 
        border-top: 1px solid #374151; 
        padding-top: 8px;
    }
    .desc-curta { color: #fbbf24; font-weight: bold; display: block; margin-top: 2px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Conexão Firebase
def buscar_dados():
    try:
        r = requests.get("https://dashboard-manutencao-ef55f-default-rtdb.firebaseio.com/manutencao.json")
        return r.text.upper()
    except: return ""

string_bruta = buscar_dados()

# 3. Lista de Ativos (Resumida para o código)
ativos = [
    {"id": "701", "n": "ABRIDOR BIANCO"}, {"id": "1501", "n": "ABRIDOR BRASTEC 1"},
    {"id": "1502", "n": "ABRIDOR BRASTEC 2"}, {"id": "1503", "n": "ABRIDOR BRASTEC 3"},
    {"id": "1504", "n": "ABRIDOR BRASTEC 4"}, {"id": "1506", "n": "ABRIDOR BRASTEC 6"},
    {"id": "1404", "n": "HIDRORELAXADORA"}, {"id": "804", "n": "CALANDRA ALBRECHT"},
    {"id": "803", "n": "CALANDRA LAFER"}, {"id": "1202", "n": "RAMA LK"},
    {"id": "1201", "n": "RAMA UNITECH"}, {"id": "1601", "n": "COZINHA CORANTE"},
    {"id": "1602", "n": "COZINHA QUÍMICO"}, {"id": "1001", "n": "FELPADEIRA 1"},
    {"id": "1002", "n": "FELPADEIRA 2"}, {"id": "59", "n": "HT 1324"},
    {"id": "1306", "n": "HT 1306"}, {"id": "1311", "n": "HT 1311"},
    {"id": "1314", "n": "HT 1314"}, {"id": "2603", "n": "SECADOR"}, {"id": "26", "n": "EMPILHADEIRA"}
]

# 4. Exibição
cols = st.columns(5)
for i, at in enumerate(ativos):
    pos = string_bruta.find(at['id'])
    ctx = string_bruta[pos:pos+150] if pos != -1 else ""
    
    # Extrai descritivo e limita a 2-3 palavras
    desc = ""
    if "DESC:" in ctx:
        desc = ctx.split("DESC:")[1].split("|")[0].split()[:3]
        desc = " ".join(desc)

    if "MÁQUINA PARADA" in ctx:
        cor, lbl, mot = "#e74c3c", "PARADA", f"CORRETIVA <span class='desc-curta'>{desc}</span>"
    elif "ABERTA" in ctx or "EXECUÇÃO" in ctx:
        cor, lbl, mot = "#f1c40f", "ATENÇÃO", f"EM CURSO <span class='desc-curta'>{desc}</span>"
    elif "MÁQ.PAR.PARCIAL" in ctx:
        cor, lbl, mot = "#e67e22", "ALERTA", "PARCIAL"
    else:
        cor, lbl, mot = "#2ecc71", "NORMAL", "OPERANDO"

    with cols[i % 5]:
        st.markdown(f"""
            <div class="card" style="border-top-color: {cor};">
                <div class="maquina-id">ID: {at['id']}</div>
                <div class="maquina-nome">{at['n']}</div>
                <div class="status-texto" style="color: {cor};">{lbl}</div>
                <div class="motivo-sub">{mot}</div>
            </div>
        """, unsafe_allow_html=True)
