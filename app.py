import streamlit as st
import requests
from datetime import datetime
import re

# 1. Configuração de UI
st.set_page_config(page_title="Monitoramento Litoral", layout="wide")

st.components.v1.html(
    "<script>setTimeout(function(){window.location.reload();}, 30000);</script>",
    height=0,
)

agora = datetime.now().strftime("%H:%M:%S")

st.markdown(f"""
    <style>
    .timer-container {{
        position: absolute; top: -35px; right: 20px; color: #718096;
        font-family: monospace; font-size: 0.85rem; background: rgba(26, 31, 41, 0.9);
        padding: 4px 12px; border-radius: 20px; border: 1px solid #2d3748; z-index: 999;
    }}
    .block-container {{ padding-top: 4rem !important; max-width: 95% !important; margin: 0 auto; }}
    .stApp {{ background-color: #0b0e14; }}
    header {{ visibility: hidden; }}

    @keyframes efeito-farol {{ 0% {{ background-position: -200% 0; }} 100% {{ background-position: 200% 0; }} }}
    @keyframes piscar-vermelho {{ 0% {{ border-top-color: #ff0000; }} 50% {{ border-top-color: #440000; }} 100% {{ border-top-color: #ff0000; }} }}

    .card {{
        background-color: #1a1f29; padding: 10px 5px; border-radius: 4px;
        text-align: center; margin-bottom: 10px; min-height: 155px; 
        display: flex; flex-direction: column;
        justify-content: space-between; align-items: center; 
        border: 1px solid #232a37;
        box-sizing: border-box;
        border-top: 7px solid;
    }}

    .border-normal {{ border-top-color: #2ecc71 !important; }}
    .border-parada {{ border-top-color: #ff0000 !important; animation: piscar-vermelho 0.8s infinite; }}
    .farol-aviso {{
        border-top-color: transparent !important;
        background-image: linear-gradient(#1a1f29, #1a1f29), linear-gradient(90deg, #ff8c00 30%, #ffffff 50%, #ff8c00 70%);
        background-origin: border-box; background-clip: padding-box, border-box;
        background-size: 200% 100%; animation: efeito-farol 3s linear infinite;
    }}

    .nome-topo {{ color: #a0aec0; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; }}
    .id-container {{ color: #ffffff; line-height: 1; margin: 5px 0; }}
    .id-letras {{ font-size: 1.1rem; font-weight: 700; opacity: 0.5; }}
    .id-numeros {{ font-size: 3rem; font-weight: 900; }}
    .status-area {{ font-weight: 900; font-size: 0.9rem; text-transform: uppercase; margin: 4px 0; }}
    .tag-servico {{ color: #ffffff !important; font-weight: bold; font-size: 0.75rem; background: #334155; border-radius: 3px; padding: 3px 0; width: 90%; }}
    </style>
    <div class="timer-container">⏱️ ATUALIZADO EM: {agora}</div>
    """, unsafe_allow_html=True)

def buscar_dados():
    try:
        r = requests.get("https://dashboard-manutencao-ef55f-default-rtdb.firebaseio.com/manutencao.json")
        return r.text.upper() if r.text else ""
    except: return ""

# Lista oficial de ativos
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
processados = []

for at in ativos:
    # Busca a posição do ID no texto
    pos = string_bruta.rfind(at['id'])
    
    # PADRÃO: Se não achar no texto ou não disser parada/parcial, é VERDE
    status, cor, classe, icon, servico = "NORMAL", "#2ecc71", "border-normal", "✅", "EM OPERAÇÃO"
    
    if pos != -1:
        # Pega o contexto daquela máquina (as próximas informações após o ID)
        ctx = string_bruta[pos : pos + 300]
        
        # VERIFICAÇÃO RIGOROSA CONFORME SOLICITADO
        if "MÁQUINA PARADA" in ctx:
            status, cor, classe, icon, servico = "PARADA", "#ff0000", "border-parada", "🛑", "CORRETIVA"
        elif "MÁQ.PAR.PARCIAL" in ctx:
            status, cor, classe, icon, servico = "AVISO", "#ff8c00", "farol-aviso", "⚠️", "PARCIAL"
        # Qualquer outro termo (Execução, Aberta, Cipa, Normal) cai no padrão VERDE

    processados.append({
        "id_html": at['id'].replace("_", "").replace("QUIMICO", ""), 
        "n": at['n'], "status": status, "cor": cor, "classe": classe, 
        "icon": icon, "servico": servico
    })

# Renderização
cols = st.columns(8)
for idx, m in enumerate(processados):
    with cols[idx % 8]:
        st.markdown(f"""
            <div class="card {m['classe']}">
                <div class="nome-topo">{m['n']}</div>
                <div class="id-container"><span class='id-numeros'>{m['id_html']}</span></div>
                <div class="status-area" style="color: {m['cor']};">{m['icon']} {m['status']}</div>
                <div class="tag-servico">{m['servico']}</div>
            </div>
        """, unsafe_allow_html=True)
