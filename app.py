import streamlit as st
import requests

# 1. Configuração de Layout e Estilo
st.set_page_config(page_title="Monitor Litoral", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .card {
        background-color: #1f2937;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        margin-bottom: 8px;
        min-height: 145px; 
        border-top: 6px solid;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
    }
    .maquina-id { 
        color: #e5e7eb; 
        font-size: 0.95em; 
        font-weight: bold; 
        text-transform: uppercase; 
        margin-bottom: 2px;
        background-color: #374151;
        border-radius: 3px;
        display: inline-block;
        padding: 2px 10px;
    }
    .maquina-nome { color: #9ca3af; font-weight: bold; font-size: 0.85em; margin-bottom: 5px; text-transform: uppercase; }
    .status-texto { font-weight: bold; font-size: 1.1em; text-transform: uppercase; margin-bottom: 2px; }
    .texto-destaque { 
        color: #FFFFFF !important; 
        font-weight: bold; 
        font-size: 0.9em; 
        text-transform: uppercase; 
        line-height: 1.2;
        margin-top: 6px;
        display: block;
    }
    .status-normal-container {
        margin-top: 5px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 4px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Busca de Dados
def buscar_dados():
    try:
        r = requests.get("https://dashboard-manutencao-ef55f-default-rtdb.firebaseio.com/manutencao.json")
        return r.text.upper()
    except: return ""

string_bruta = buscar_dados()

# 3. Lista de Ativos
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
    # rfind garante que pegamos a informação mais recente (final do arquivo)
    pos = string_bruta.rfind(at['id']) 
    # REDUZIDO para 150 para não "vazar" dados da máquina ao lado
    ctx = string_bruta[pos:pos+150] if pos != -1 else ""
    
    # Tipo de Manutenção
    if at['id'] == "26": tipo_servico = "MECÂNICA"
    elif "ELETRICA" in ctx: tipo_servico = "ELÉTRICA"
    elif "MECANICA" in ctx: tipo_servico = "MECÂNICA"
    elif "CIVIL" in ctx: tipo_servico = "CIVIL"
    else: tipo_servico = "MANUTENÇÃO"

    # --- LÓGICA DE ALTA CONFIANÇA ---
    
    # 1. Se contém a palavra PARCIAL, o status é Amarelo.
    if "PARCIAL" in ctx:
        cor, lbl = "#f1c40f", "PARCIAL"
        info = f"<div class='texto-destaque'>{tipo_servico}</div>"
    
    # 2. Se não tem Parcial, mas tem PARADA, o status é Vermelho Absoluto.
    elif "PARADA" in ctx:
        cor, lbl = "#e74c3c", "PARADA"
        info = f"<div class='texto-destaque'>{tipo_servico}</div>"
    
    # 3. Caso contrário, Operando (Verde).
    else:
        cor, lbl = "#2ecc71", "NORMAL"
        info = "<div class='status-normal-container'><span style='color:#2ecc71'>✅</span><span class='texto-destaque'>OPERANDO</span></div>"

    with cols[i % 5]:
        st.markdown(f"""
            <div class="card" style="border-top-color: {cor};">
                <div>
                    <div class="maquina-id">ID: {at['id']}</div>
                    <div class="maquina-nome">{at['n']}</div>
                </div>
                <div class="status-texto" style="color: {cor};">{lbl}</div>
                {info}
            </div>
        """, unsafe_allow_html=True)
