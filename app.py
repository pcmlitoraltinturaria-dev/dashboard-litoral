import streamlit as st
import requests
from datetime import datetime
import re

# 1. Configurações de UI - Limpo e Focado
st.set_page_config(page_title="Monitoramento Litoral", layout="wide")

st.markdown("""
    <style>
    .block-container { padding: 0.5rem !important; max-width: 100% !important; }
    .stApp { background-color: #0b0e14; overflow: hidden; }
    
    /* STOP: Pisca Robusto (10px) */
    @keyframes piscar-robusto { 
        0% { border-top-color: #ff0000; } 
        50% { border-top-color: #660000; } 
        100% { border-top-color: #ff0000; } 
    }

    /* AVISO: Farol Branco Lento (3s) */
    @keyframes efeito-farol-lento { 
        0% { background-position: -200% 0; } 
        100% { background-position: 200% 0; } 
    }

    .card {
        background-color: #1a1f29; 
        padding: 15px 5px; 
        border-radius: 4px;
        text-align: center; 
        margin-bottom: 10px; 
        min-height: 170px; 
        border-top: 10px solid; 
        display: flex; 
        flex-direction: column;
        justify-content: space-between;
        border: 1px solid #232a37;
    }

    .blink-top { 
        border-top: 10px solid #ff0000 !important; 
        animation: piscar-robusto 0.8s infinite; 
    }

    .farol-branco { 
        border-top: 10px solid transparent !important;
        background-image: linear-gradient(#1a1f29, #1a1f29), 
                          linear-gradient(90deg, #ff8c00 35%, #ffffff 50%, #ff8c00 65%);
        background-origin: border-box;
        background-clip: padding-box, border-box;
        background-size: 200% 100%;
        animation: efeito-farol-lento 3s linear infinite; 
    }

    /* Tipografia: Foco no ID */
    .nome-topo { color: #a0aec0; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; }
    .id-container { color: #ffffff; line-height: 1; margin: 5px 0; }
    .id-letras { font-size: 1.2rem; font-weight: 700; opacity: 0.5; margin-right: 3px; }
    .id-numeros { font-size: 3.2rem; font-weight: 900; }
    
    .status-area { font-weight: 900; font-size: 1.1rem; text-transform: uppercase; }
    .tag-servico { 
        color: #ffffff !important; font-weight: bold; font-size: 0.85rem; 
        background: #334155; border-radius: 3px; padding: 5px 0;
    }
    
    .kpi-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; padding: 0 10px; }
    .kpi-unit { background: #1a1f29; padding: 10px 25px; border-radius: 6px; border: 1px solid #2d3748; display: flex; gap: 15px; }

    [data-testid="column"] { padding: 3px !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Lista de Ativos
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
        letras = f'<span class="id-letras">{match.group(1)}</span>' if match.group(1) else ""
        return f'{letras}<span class="id-numeros">{match.group(2)}</span>'
    return f'<span class="id-numeros">{limpo}</span>'

def buscar_dados():
    try:
        r = requests.get("https://dashboard-manutencao-ef55f-default-rtdb.firebaseio.com/manutencao.json")
        return r.text.upper() if r.text else ""
    except: return ""

string_bruta = buscar_dados()
resumo = {"OK": 0, "AVISO": 0, "STOP": 0}
processados = []

for at in ativos:
    pos = string_bruta.rfind(at['id'])
    status, cor, classe, icon, servico = "NORMAL", "#2ecc71", "", "✅", "EM OPERAÇÃO"
    if at['id'] == "QUIMICO_1602": pos = -1 

    if pos != -1:
        ctx = string_bruta[pos : pos + 200]
        tipo_base = "MANUTENÇÃO"
        if "CONSERTO" in ctx: tipo_base = "CONSERTO"
        elif "ADEQUAÇÃO" in ctx: tipo_base = "ADEQUAÇÃO"
        elif "CIVIL" in ctx: tipo_base = "CIVIL"
        elif "ELETRICA" in ctx: tipo_base = "ELÉTRICA"
        elif "MECANICA" in ctx: tipo_base = "MECÂNICA"

        if "MÁQUINA PARADA" in ctx:
            status, cor, classe, icon, servico = "PARADA", "#ff0000", "blink-top", "🛑", tipo_base
            resumo["STOP"] += 1
        elif any(x in ctx for x in ["MÁQ.PAR.PARCIAL", "PARCIAL"]):
            status, cor, icon, classe, servico = "AVISO", "#ff8c00", "⚠️", "farol-branco", f"PARCIAL/{tipo_base.capitalize()}"
            resumo["AVISO"] += 1
        else: resumo["OK"] += 1
    else: resumo["OK"] += 1

    processados.append({
        "id_html": formatar_id_visual(at['id']), "n": at['n'], 
        "status": status, "cor": cor, "classe": classe, "icon": icon, "servico": servico
    })

# 3. Cabeçalho e Grid
st.markdown(f"""
    <div class="kpi-row">
        <div style="display: flex; gap: 20px;">
            <div class="kpi-unit"><b style="color:#2ecc71; font-size:1.6rem;">{resumo['OK']}</b> <small style="color:#a0aec0;">OK</small></div>
            <div class="kpi-unit"><b style="color:#ff8c00; font-size:1.6rem;">{resumo['AVISO']}</b> <small style="color:#a0aec0;">AVISO</small></div>
            <div class="kpi-unit"><b style="color:#ff0000; font-size:1.6rem;">{resumo['STOP']}</b> <small style="color:#a0aec0;">STOP</small></div>
        </div>
        <div style="color: #90cdf4; font-weight: 800; font-size: 2rem;">{datetime.now().strftime("%H:%M:%S")}</div>
    </div>
    """, unsafe_allow_html=True)

cols = st.columns(8)
for idx, m in enumerate(processados):
    with cols[idx % 8]:
        st.markdown(f"""
            <div class="card {m['classe']}" style="border-top-color: {m['cor'] if not m['classe'] else 'transparent'};">
                <div class="nome-topo">{m['n']}</div>
                <div class="id-container">{m['id_html']}</div>
                <div class="status-area" style="color: {m['cor']};">{m['icon']} {m['status']}</div>
                <div class="tag-servico">{m['servico']}</div>
            </div>
        """, unsafe_allow_html=True)
