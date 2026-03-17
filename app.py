import streamlit as st
import requests

# 1. Configuração de Layout e Estilo com Animações de Teste
st.set_page_config(page_title="Monitor Litoral", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    
    /* Animação para o status PARADA (Vermelho) - Mais intensa */
    @keyframes piscar-critico {
        0% { opacity: 1; border-top-color: #e74c3c; }
        50% { opacity: 0.4; border-top-color: transparent; }
        100% { opacity: 1; border-top-color: #e74c3c; }
    }

    /* Animação para o status PARCIAL (Amarelo) - Teste */
    @keyframes piscar-alerta {
        0% { opacity: 1; border-top-color: #f1c40f; }
        50% { opacity: 0.6; border-top-color: #374151; }
        100% { opacity: 1; border-top-color: #f1c40f; }
    }

    .card {
        background-color: #1f2937; 
        padding: 5px;
        border-radius: 4px;
        text-align: center; 
        margin-bottom: 5px; 
        min-height: 100px;
        border-top: 4px solid;
        display: flex; 
        flex-direction: column;
        justify-content: center;
    }

    /* Classes de animação */
    .blink-red { animation: piscar-critico 1s infinite; border-top-width: 5px !important; }
    .blink-yellow { animation: piscar-alerta 1.5s infinite; border-top-width: 5px !important; }

    .maquina-id { 
        color: #e5e7eb; font-size: 0.75em; font-weight: bold; 
        background-color: #374151; border-radius: 2px;
        display: inline-block; padding: 1px 6px; margin-bottom: 2px;
    }
    .maquina-nome { 
        color: #9ca3af; font-weight: bold; font-size: 0.75em; 
        margin-bottom: 2px; line-height: 1;
    }
    .status-texto { 
        font-weight: bold; font-size: 0.9em; 
        text-transform: uppercase; margin-bottom: 1px; 
    }
    .texto-destaque { 
        color: #FFFFFF !important; font-weight: bold; font-size: 0.8em; 
        margin-top: 2px; 
    }

    [data-testid="column"] { padding-left: 3px !important; padding-right: 3px !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Busca de Dados
def buscar_dados():
    try:
        r = requests.get("https://dashboard-manutencao-ef55f-default-rtdb.firebaseio.com/manutencao.json")
        return r.text.upper() if r.text else ""
    except: 
        return ""

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

        # TESTE: Ambos piscando
        if "NORMAL" in ctx:
            cor, lbl = "#2ecc71", "NORMAL"
        elif "CIVIL" in ctx or "PARCIAL" in ctx or "MÁQ.PAR.PARCIAL" in ctx:
            cor, lbl = "#f1c40f", "PARCIAL"
            extra_class = "blink-yellow" # Amarelo piscando para teste
        elif "PARADA" in ctx or "MÁQUINA PARADA" in ctx:
            cor, lbl = "#e74c3c", "PARADA"
            extra_class = "blink-red"    # Vermelho piscando
        else:
            cor, lbl = "#2ecc71", "NORMAL"
        
        info = f"<div class='texto-destaque'>{setor if lbl != 'NORMAL' else '✅ OPERANDO'}</div>"
    else:
        cor, lbl, info = "#2ecc71", "NORMAL", "<div class='texto-destaque'>✅ OPERANDO</div>"

    with cols[i % 6]:
        st.markdown(f"""
            <div class="card {extra_class}" style="border-top-color: {cor};">
                <div class="maquina-id">ID: {at['id']}</div>
                <div class="maquina-nome">{at['n']}</div>
                <div class="status-texto" style="color: {cor};">{lbl}</div>
                {info}
            </div>
        """, unsafe_allow_html=True)
