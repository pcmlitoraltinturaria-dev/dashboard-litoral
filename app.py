import streamlit as st
import requests
from datetime import datetime
import re

# 1. Configuração de Layout
st.set_page_config(page_title="Monitoramento Litoral", layout="wide")

st.markdown("""
    <style>
    .block-container { 
        padding-top: 0.5rem !important; 
        padding-bottom: 0rem !important; 
        padding-left: 0.5rem !important; 
        padding-right: 0.5rem !important; 
        max-width: 100% !important;
    }
    .stApp { background-color: #0b0e14; overflow: hidden; }
    
    @keyframes piscar-topo {
        0% { border-top-color: #e74c3c; }
        50% { border-top-color: #1a1f29; }
        100% { border-top-color: #e74c3c; }
    }

    @keyframes fluxo-circular {
        0% { background-position: 0% 50%; }
        100% { background-position: 200% 50%; }
    }

    .card {
        background-color: #1a1f29; 
        padding: 10px 5px; 
        border-radius: 4px;
        text-align: center; 
        margin-bottom: 5px; 
        min-height: 155px; 
        border-top: 8px solid;
        display: flex; 
        flex-direction: column;
        justify-content: space-between;
        border-right: 1px solid #232a37;
        border-left: 1px solid #232a37;
        border-bottom: 1px solid #232a37;
        position: relative;
    }

    .blink-top { animation: piscar-topo 0.8s infinite; }

    .flow-top { 
        border-top: 8px solid transparent !important;
        background-image: linear-gradient(#1a1f29, #1a1f29), 
                          linear-gradient(90deg, #f1c40f, #eaff00, #f1c40f);
        background-origin: border-box;
        background-clip: padding-box, border-box;
        background-size: 200% 100%;
        animation: fluxo-circular 1.5s linear infinite;
    }

    .id-container { color: #ffffff; line-height: 1; margin: 5px 0; }
    .id-letras { font-size: 1.1rem; font-weight: 700; vertical-align: baseline; opacity: 0.8; margin-right: 2px; }
    .id-numeros { font-size: 2.7rem; font-weight: 900; vertical-align: baseline; }
    
    .nome-maquina { color: #a0aec0; font-size: 0.7rem; font-weight: 700; text-transform: uppercase; }
    .status-texto { font-weight: 900; font-size: 0.9rem; text-transform: uppercase; }
    .tag-manutencao { 
        color: #a0aec0 !important; font-weight: bold; font-size: 0.75rem; 
        background: #232a37; border-radius: 3px; padding: 2px 0;
    }
    
    .kpi-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
    .kpi-unit { background: #1a1f29; padding: 4px 12px; border-radius: 6px; border: 1px solid #2d3748; display: flex; gap: 8px; align-items: center; }

    [data-testid="column"] { padding: 2px !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Lista de Ativos - ATUALIZADA (HT 1316 no lugar da Empilhadeira)
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

def formatar_id_visual(id_bruto):
    limpo = id_bruto.replace("_", "").replace("QUIMICO", "")
    match = re.match(r"([a-zA-Z]+)?(\d+)", limpo)
    if match:
        letras = match.group(1) if match.group(1) else ""
        numeros = match.group(2)
        return f'<span class="id-letras">{letras}</span><span class="id-numeros">{numeros}</span>'
    return f'<span class="id-numeros">{limpo}</span>'

def buscar_dados():
    try:
        r = requests.get("https://dashboard-manutencao-ef55f-default-rtdb.firebaseio.com/manutencao.json")
        return r.text.upper() if r.text else ""
    except: return ""

string_bruta = buscar_dados()
total, paradas, parciais = 0, 0, 0
lista_final = []

for at in ativos:
    total += 1
    pos = string_bruta.rfind(at['id'])
    status, cor, classe, icon, s_nome = "NORMAL", "#2ecc71", "", "✅", "OPERANDO"
    
    if pos != -1:
        ctx = string_bruta[pos : pos + 80]
        # Lógica de prioridade: Parada > Parcial
        if "PARADA" in ctx or "MÁQUINA PARADA" in ctx:
            status, cor, classe, icon, paradas = "PARADA", "#e74c3c", "blink-top", "🛑", paradas + 1
        elif any(x in ctx for x in ["CIVIL", "PARCIAL", "MÁQ.PAR.PARCIAL"]):
            status, cor, icon, parciais, classe = "AVISO", "#f1c40f", "⚠️", parciais + 1, "flow-top"
        
        if "CIVIL" in ctx: s_nome = "CIVIL"
        elif "ELETRICA" in ctx: s_nome = "ELÉTRICA"
        elif "MECANICA" in ctx: s_nome = "MECÂNICA"

    lista_final.append({
        "id_html": formatar_id_visual(at['id']),
        "n": at['n'], "status": status, "cor": cor, 
        "classe": classe, "icon": icon, "s_nome": s_nome
    })

# 3. Cabeçalho e Grid
agora = datetime.now().strftime("%H:%M:%S")
st.markdown(f"""
    <div class="kpi-row">
        <div style="display: flex; gap: 10px;">
            <div class="kpi-unit"><b style="color:#2ecc71;">{total-paradas-parciais}</b> <small style="color:#a0aec0;">OK</small></div>
            <div class="kpi-unit"><b style="color:#f1c40f;">{parciais}</b> <small style="color:#a0aec0;">AVISO</small></div>
            <div class="kpi-unit"><b style="color:#e74c3c;">{paradas}</b> <small style="color:#a0aec0;">STOP</small></div>
        </div>
        <div style="color: #90cdf4; font-weight: 800; font-size: 1.5rem;">{agora}</div>
    </div>
    """, unsafe_allow_html=True)

cols = st.columns(8)
for idx, m in enumerate(lista_final):
    with cols[idx % 8]:
        st.markdown(f"""
            <div class="card {m['classe']}" style="border-top-color: {m['cor']};">
                <div class="nome-maquina">{m['n']}</div>
                <div class="id-container">{m['id_html']}</div>
                <div class="status-texto" style="color: {m['cor']};">{m['icon']} {m['status']}</div>
                <div class="tag-manutencao">{m['s_nome'] if m['status'] != 'NORMAL' else 'EM OPERAÇÃO'}</div>
            </div>
        """, unsafe_allow_html=True)
