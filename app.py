import streamlit as st
import requests
from datetime import datetime
import re

# 1. Configuração de Layout e Animações
st.set_page_config(page_title="Monitoramento Litoral", layout="wide")

st.markdown("""
    <style>
    .block-container { padding: 0.5rem !important; max-width: 100% !important; }
    .stApp { background-color: #0b0e14; overflow: hidden; }
    
    /* VERMELHO: Pisca (Parada Total) */
    @keyframes piscar-topo { 
        0% { border-top-color: #e74c3c; } 
        50% { border-top-color: #1a1f29; } 
        100% { border-top-color: #e74c3c; } 
    }

    /* EFEITO FAROL: Linha Vermelha cruzando o Laranja (Parcial) */
    @keyframes efeito-farol {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }

    .card {
        background-color: #1a1f29; 
        padding: 10px 5px; 
        border-radius: 4px;
        text-align: center; 
        margin-bottom: 5px; 
        min-height: 160px; 
        border-top: 8px solid;
        display: flex; 
        flex-direction: column;
        justify-content: space-between;
        border-right: 1px solid #232a37;
        border-left: 1px solid #232a37;
        border-bottom: 1px solid #232a37;
    }

    .blink-top { animation: piscar-topo 0.8s infinite; }

    /* Classe do Farol (Aviso/Parcial) */
    .farol-top { 
        border-top: 8px solid transparent !important;
        /* Fundo Laranja com o "feixe" Vermelho cruzando */
        background-image: linear-gradient(#1a1f29, #1a1f29), 
                          linear-gradient(90deg, #ff8c00 30%, #ff0000 50%, #ff8c00 70%);
        background-origin: border-box;
        background-clip: padding-box, border-box;
        background-size: 200% 100%;
        animation: efeito-farol 1.2s linear infinite;
    }

    /* Tipografia: Números em evidência e Letras menores */
    .nome-topo { color: #a0aec0; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; }
    .id-container { color: #ffffff; line-height: 1; margin: 2px 0; }
    .id-letras { font-size: 1.1rem; font-weight: 700; vertical-align: middle; opacity: 0.7; }
    .id-numeros { font-size: 2.8rem; font-weight: 900; vertical-align: middle; }
    
    .status-area { font-weight: 900; font-size: 1rem; text-transform: uppercase; margin-top: 5px; }
    .tag-manutencao { 
        color: #a0aec0 !important; font-weight: bold; font-size: 0.8rem; 
        background: #232a37; border-radius: 3px; padding: 4px 0;
    }
    
    .kpi-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
    .kpi-unit { background: #1a1f29; padding: 6px 15px; border-radius: 6px; border: 1px solid #2d3748; display: flex; gap: 10px; }

    [data-testid="column"] { padding: 2px !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Ativos (HT 1316 já incluída)
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

# 3. Lógica de Status
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
    status, cor, classe, icon, tag = "NORMAL", "#2ecc71", "", "✅", "EM OPERAÇÃO"
    
    if pos != -1:
        ctx = string_bruta[pos : pos + 150]
        if "MÁQUINA PARADA" in ctx:
            status, cor, classe, icon, tag = "PARADA", "#e74c3c", "blink-top", "🛑", "MECÂNICA"
            resumo["STOP"] += 1
        elif any(x in ctx for x in ["MÁQ.PAR.PARCIAL", "EM EXECUÇÃO", "PARCIAL"]):
            status, cor, icon, tag, classe = "AVISO", "#ff8c00", "⚠️", "ATENÇÃO", "farol-top"
            resumo["AVISO"] += 1
        else: resumo["OK"] += 1
        
        # Ajuste de tag por equipe
        if "CIVIL" in ctx: tag = "CIVIL"
        elif "ELETRICA" in ctx: tag = "ELÉTRICA"
    else: resumo["OK"] += 1

    processados.append({
        "id_html": formatar_id_visual(at['id']), "n": at['n'], 
        "status": status, "cor": cor, "classe": classe, "icon": icon, "tag": tag
    })

# 4. Renderização
st.markdown(f"""
    <div class="kpi-row">
        <div style="display: flex; gap: 12px;">
            <div class="kpi-unit"><b style="color:#2ecc71;">{resumo['OK']}</b> <small style="color:#a0aec0;">OK</small></div>
            <div class="kpi-unit"><b style="color:#ff8c00;">{resumo['AVISO']}</b> <small style="color:#a0aec0;">AVISO</small></div>
            <div class="kpi-unit"><b style="color:#e74c3c;">{resumo['STOP']}</b> <small style="color:#a0aec0;">STOP</small></div>
        </div>
        <div style="color: #90cdf4; font-weight: 800; font-size: 1.6rem;">{datetime.now().strftime("%H:%M:%S")}</div>
    </div>
    """, unsafe_allow_html=True)

cols = st.columns(8)
for idx, m in enumerate(processados):
    with cols[idx % 8]:
        st.markdown(f"""
            <div class="card {m['classe']}" style="border-top-color: {m['cor']};">
                <div class="nome-topo">{m['n']}</div>
                <div class="id-container">{m['id_html']}</div>
                <div class="status-area" style="color: {m['cor']};">{m['icon']} {m['status']}</div>
                <div class="tag-manutencao">{m['tag']}</div>
            </div>
        """, unsafe_allow_html=True)
