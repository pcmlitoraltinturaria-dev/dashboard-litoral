import streamlit as st
import requests

# 1. Configuração de Layout e Estilo (Design Compacto Litoral)
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
        min-height: 140px; 
        border-top: 6px solid;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
    }
    .maquina-id { color: #9ca3af; font-size: 0.6em; text-transform: uppercase; margin-bottom: 2px; }
    .maquina-nome { color: #9ca3af; font-weight: bold; font-size: 0.85em; margin-bottom: 5px; text-transform: uppercase; }
    .status-texto { font-weight: bold; font-size: 1.1em; text-transform: uppercase; margin-bottom: 2px; }
    
    /* TEXTO EM BRANCO E NEGRITO PARA OPERANDO E TIPO DE MANUTENÇÃO */
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

# 3. Lista Completa de Ativos (21 Máquinas)
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
    pos = string_bruta.rfind(f'"{at["id"]}"')
    if pos == -1: pos = string_bruta.rfind(at['id'])
    
    ctx = string_bruta[pos:pos+500] if pos != -1 else ""
    
    # Lógica de Identificação do Tipo (Independente da posição na string)
    if at['id'] == "26":
        tipo_servico = "MECÂNICA"
    elif "ELETRICA" in ctx or "ELÉTRICA" in ctx:
        tipo_servico = "ELÉTRICA"
    elif "MECANICA" in ctx or "MECÂNICA" in ctx:
        tipo_servico = "MECÂNICA"
    else:
        tipo_servico = "MANUTENÇÃO" # Caso não encontre as palavras chave

    # Definição de Cores e Status
    is_parada = "MÁQUINA PARADA" in ctx
    is_atencao = "ABERTA" in ctx or "EXECUÇÃO" in ctx or "MÁQ.PAR.PARCIAL" in ctx

    if is_parada:
        cor, lbl = "#e74c3c", "PARADA"
        info = f"<div class='texto-destaque'>{tipo_servico}</div>"
    elif is_atencao:
        cor, lbl = "#f1c40f", "ATENÇÃO"
        info = f"<div class='texto-destaque'>{tipo_servico}</div>"
    else:
        cor, lbl = "#2ecc71", "NORMAL"
        info = "<div class='status-normal-container'><span style='color:#2ecc71'>✅</span><span class='texto-destaque'>OPERANDO</span></div>"

    with cols[i % 5]:
        st.markdown(f"""
            <div class="card" style="border-top-color: {cor};">
                <div class="maquina-id">ID: {at['id']}</div>
                <div class="maquina-nome">{at['n']}</div>
                <div class="status-texto" style="color: {cor};">{lbl}</div>
                {info}
            </div>
        """, unsafe_allow_html=True)
