import streamlit as st
import requests

# Configuração da página para usar toda a largura disponível
st.set_page_config(page_title="Monitor Litoral", layout="wide")

st.markdown("""
    <style>
    /* Remove as margens e paddings padrões do Streamlit para ganhar espaço */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    
    .stApp { background-color: #0b0e14; }
    
    /* Animação para status PARADA */
    @keyframes piscar-critico {
        0% { opacity: 1; border-top-color: #e74c3c; box-shadow: 0 0 8px #e74c3c; }
        50% { opacity: 0.5; border-top-color: transparent; box-shadow: none; }
        100% { opacity: 1; border-top-color: #e74c3c; box-shadow: 0 0 8px #e74c3c; }
    }

    /* Card ultra-compacto conforme o recuadro vermelho solicitado */
    .card {
        background-color: #1a1f29; 
        padding: 4px;
        border-radius: 4px;
        text-align: center; 
        min-height: 90px; /* Altura reduzida para caber na vertical */
        border-top: 4px solid;
        display: flex; 
        flex-direction: column;
        justify-content: space-between;
        border-right: 1px solid #2d3748;
        border-left: 1px solid #2d3748;
        border-bottom: 1px solid #2d3748;
    }

    .blink-red { 
        animation: piscar-critico 1s infinite; 
        background-color: #2d1616 !important; 
    }

    .maquina-id { 
        color: #90cdf4; font-size: 0.7em; font-weight: bold; 
        margin-bottom: 2px;
    }
    .maquina-nome { 
        color: #ffffff; font-weight: 700; font-size: 0.8em; 
        line-height: 1; min-height: 24px;
        display: flex; align-items: center; justify-content: center;
    }
    .status-texto { 
        font-weight: 800; font-size: 0.9em; 
        text-transform: uppercase;
    }
    .texto-destaque { 
        color: #a0aec0 !important; font-weight: bold; font-size: 0.7em; 
        background: #2d3748; border-radius: 3px; padding: 1px 0;
    }

    /* Reduz o espaço entre as colunas do Streamlit */
    [data-testid="column"] { 
        padding: 1px !important; 
    }
    </style>
    """, unsafe_allow_html=True)

# Lógica de busca e lista de ativos permanece a mesma
def buscar_dados():
    try:
        r = requests.get("https://dashboard-manutencao-ef55f-default-rtdb.firebaseio.com/manutencao.json")
        return r.text.upper() if r.text else ""
    except: 
        return ""

string_bruta = buscar_dados()

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

# Exibição em 6 colunas para garantir que caiba na largura da tela
cols = st.columns(6)
for i, at in enumerate(ativos):
    pos = string_bruta.rfind(at['id'])
    extra_class = ""
    
    if pos != -1:
        ctx = string_bruta[pos : pos + 80]
        setor = "MANUTENÇÃO"
        if "CIVIL" in ctx: setor = "CIVIL"
        elif "ELETRICA" in ctx: setor = "ELÉTRICA"
        elif "MECANICA" in ctx: setor = "MECÂNICA"

        if "NORMAL" in ctx:
            cor, lbl = "#2ecc71", "NORMAL"
        elif "CIVIL" in ctx or "PARCIAL" in ctx or "MÁQ.PAR.PARCIAL" in ctx:
            cor, lbl = "#f1c40f", "PARCIAL"
        elif "PARADA" in ctx or "MÁQUINA PARADA" in ctx:
            cor, lbl = "#e74c3c", "PARADA"
            extra_class = "blink-red"
        else:
            cor, lbl = "#2ecc71", "NORMAL"
        
        info = f"<div class='texto-destaque'>{setor if lbl != 'NORMAL' else '✅ OPERANDO'}</div>"
    else:
        cor, lbl, info = "#2ecc71", "NORMAL", "<div class='texto-destaque'>✅ OPERANDO</div>"

    with cols[i % 6]:
        st.markdown(f"""
            <div class="card {extra_class}" style="border-top-color: {cor};">
                <div class="maquina-id">{at['id']}</div>
                <div class="maquina-nome">{at['n']}</div>
                <div class="status-texto" style="color: {cor};">{lbl}</div>
                {info}
            </div>
        """, unsafe_allow_html=True)
