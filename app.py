import streamlit as st
import requests

# 1. Configuração de Layout
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
        color: #e5e7eb; font-size: 0.85em; font-weight: bold; 
        background-color: #374151; border-radius: 3px;
        display: inline-block; padding: 2px 8px; margin-bottom: 2px;
    }
    .maquina-nome { color: #9ca3af; font-weight: bold; font-size: 0.85em; margin-bottom: 5px; }
    .status-texto { font-weight: bold; font-size: 1.1em; text-transform: uppercase; margin-bottom: 2px; }
    .texto-destaque { color: #FFFFFF !important; font-weight: bold; font-size: 0.9em; margin-top: 6px; }
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
    {"id": "803", "n": "CALANDRA LAFER"}, {"id": "_1202", "n": "RAMA LK"},
    {"id": "1201", "n": "RAMA UNITECH"}, {"id": "1601", "n": "COZINHA CORANTE"},
    {"id": "QUIMICO_1602", "n": "COZINHA QUÍMICO"}, {"id": "1001", "n": "FELPADEIRA 1"},
    {"id": "1002", "n": "FELPADEIRA 2"}, {"id": "HT_1324", "n": "HT 1324"},
    {"id": "1306", "n": "HT 1306"}, {"id": "1311", "n": "HT 1311"},
    {"id": "1314", "n": "HT 1314"}, {"id": "2603", "n": "SECADOR"}, 
    {"id": "EMPILHADEIRA 26", "n": "EMPILHADEIRA 26"}, {"id": "HT_1308", "n": "HT 1308"},
    {"id": "HT_1303", "n": "HT 1303"}, {"id": "HT_1313", "n": "HT 1313"}
]

# 4. Processamento e Exibição
cols = st.columns(5)
for i, at in enumerate(ativos):
    # rfind garante que pegamos a ocorrência mais recente (evita cabeçalhos)
    pos = string_bruta.rfind(at['id'])
    
    if pos != -1:
        # Janela de segurança de apenas 60 caracteres (curtíssima)
        # Isso garante que ele leia o setor e o status da própria linha
        ctx = string_bruta[pos : pos + 60]
        
        # Identificação de Setor (Priorizando Civil que é Amarelo fixo)
        setor = "MANUTENÇÃO"
        if "CIVIL" in ctx: setor = "CIVIL"
        elif "ELETRICA" in ctx: setor = "ELÉTRICA"
        elif "MECANICA" in ctx: setor = "MECÂNICA"

        # Lógica de Cores
        if setor == "CIVIL":
            cor, lbl = "#f1c40f", "PARCIAL" # Civil sempre amarelo
        elif "PARADA" in ctx:
            cor, lbl = "#e74c3c", "PARADA"   # Vermelho se houver Parada no contexto curto
        elif "PARCIAL" in ctx:
            cor, lbl = "#f1c40f", "PARCIAL"  # Amarelo se for Parcial
        else:
            cor, lbl = "#2ecc71", "NORMAL"
        
        info = f"<div class='texto-destaque'>{setor if lbl != 'NORMAL' else '✅ OPERANDO'}</div>"
    else:
        cor, lbl, info = "#2ecc71", "NORMAL", "<div class='texto-destaque'>✅ OPERANDO</div>"

    with cols[i % 5]:
        st.markdown(f"""
            <div class="card" style="border-top-color: {cor};">
                <div class="maquina-id">ID: {at['id']}</div>
                <div class="maquina-nome">{at['n']}</div>
                <div class="status-texto" style="color: {cor};">{lbl}</div>
                {info}
            </div>
        """, unsafe_allow_html=True)
