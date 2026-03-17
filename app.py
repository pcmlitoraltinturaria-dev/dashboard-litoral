import streamlit as st
import requests
from datetime import datetime

# 1. Configuração de Layout e Estilo
st.set_page_config(page_title="Central de Monitoramento Litoral", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; }
    .block-container { padding-top: 1rem !important; }
    
    /* Estilo dos Títulos de Setor */
    .setor-header {
        color: #90cdf4; font-size: 1.2rem; font-weight: bold;
        border-bottom: 2px solid #2d3748; margin: 15px 0 10px 0;
        padding-bottom: 5px; text-transform: uppercase; letter-spacing: 2px;
    }

    /* Animação Crítica */
    @keyframes piscar-critico {
        0% { opacity: 1; border-top-color: #e74c3c; box-shadow: 0 0 15px #e74c3c; }
        50% { opacity: 0.5; border-top-color: transparent; box-shadow: none; }
        100% { opacity: 1; border-top-color: #e74c3c; box-shadow: 0 0 15px #e74c3c; }
    }

    .card {
        background-color: #1a1f29; padding: 10px; border-radius: 6px;
        text-align: center; margin-bottom: 10px; min-height: 115px;
        border-top: 5px solid; display: flex; flex-direction: column;
        justify-content: space-between; border: 1px solid #2d3748;
    }

    .blink-red { animation: piscar-critico 1s infinite; background-color: #2d1616 !important; }

    .maquina-id { color: #90cdf4; font-size: 0.75em; font-weight: bold; }
    .maquina-nome { color: #ffffff; font-weight: 800; font-size: 0.85em; min-height: 30px; display: flex; align-items: center; justify-content: center; }
    .status-texto { font-weight: 900; font-size: 1em; text-transform: uppercase; }
    .texto-destaque { color: #a0aec0 !important; font-weight: bold; font-size: 0.75em; background: #2d3748; border-radius: 4px; }
    
    /* Estilo do Placar (KPIs) */
    .kpi-box { text-align: center; background: #1a1f29; padding: 10px; border-radius: 8px; border: 1px solid #2d3748; min-width: 150px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Dados e Ativos Agrupados por Setor
setores = {
    "🛠️ PREPARAÇÃO": [
        {"id": "701", "n": "ABRIDOR BIANCO"}, {"id": "1501", "n": "ABRIDOR BRASTEC 1"},
        {"id": "1502", "n": "ABRIDOR BRASTEC 2"}, {"id": "1503", "n": "ABRIDOR BRASTEC 3"},
        {"id": "1504", "n": "ABRIDOR BRASTEC 4"}, {"id": "1506", "n": "ABRIDOR BRASTEC 6"}
    ],
    "🔥 ACABAMENTO": [
        {"id": "804", "n": "CALANDRA ALBRECHT"}, {"id": "803", "n": "CALANDRA LAFER"},
        {"id": "1201", "n": "RAMA UNITECH"}, {"id": "_1202", "n": "RAMA LK"},
        {"id": "1404", "n": "HIDRORELAXADORA"}
    ],
    "🧪 TINTURARIA": [
        {"id": "1601", "n": "COZINHA CORANTE"}, {"id": "QUIMICO_1602", "n": "COZINHA QUÍMICO"},
        {"id": "1306", "n": "HT 1306"}, {"id": "1311", "n": "HT 1311"},
        {"id": "1314", "n": "HT 1314"}, {"id": "HT_1324", "n": "HT 1324"},
        {"id": "HT_1308", "n": "HT 1308"}, {"id": "HT_1303", "n": "HT 1303"},
        {"id": "HT_1313", "n": "HT 1313"}
    ],
    "💨 SECAGEM E FELPAGEM": [
        {"id": "1001", "n": "FELPADEIRA 1"}, {"id": "1002", "n": "FELPADEIRA 2"},
        {"id": "2603", "n": "SECADOR"}
    ],
    "📦 LOGÍSTICA": [
        {"id": "EMPILHADEIRA 26", "n": "EMPILHADEIRA 26"}
    ]
}

def buscar_dados():
    try:
        r = requests.get("https://dashboard-manutencao-ef55f-default-rtdb.firebaseio.com/manutencao.json")
        return r.text.upper() if r.text else ""
    except: return ""

string_bruta = buscar_dados()

# 3. Processamento de Status para o Placar
total, paradas, parciais = 0, 0, 0
lista_final = []

for setor_nome, ativos in setores.items():
    for at in ativos:
        total += 1
        pos = string_bruta.rfind(at['id'])
        status, cor, classe, s_nome = "NORMAL", "#2ecc71", "", "MANUTENÇÃO"
        
        if pos != -1:
            ctx = string_bruta[pos : pos + 80]
            if "CIVIL" in ctx: s_nome = "CIVIL"
            elif "ELETRICA" in ctx: s_nome = "ELÉTRICA"
            elif "MECANICA" in ctx: s_nome = "MECÂNICA"

            if "NORMAL" in ctx: status, cor = "NORMAL", "#2ecc71"
            elif any(x in ctx for x in ["CIVIL", "PARCIAL", "MÁQ.PAR.PARCIAL"]):
                status, cor, parciais = "PARCIAL", "#f1c40f", parciais + 1
            elif "PARADA" in ctx:
                status, cor, classe, paradas = "PARADA", "#e74c3c", "blink-red", paradas + 1
        
        lista_final.append({...at, "status": status, "cor": cor, "classe": classe, "setor": setor_nome, "s_nome": s_nome})

# 4. Cabeçalho Visual (Placar e Relógio)
agora = datetime.now().strftime("%H:%M:%S")
st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
        <div style="display: flex; gap: 15px;">
            <div class="kpi-box"><span style="color:#a0aec0">TOTAL</span><br><b style="font-size:1.5em; color:white;">{total}</b></div>
            <div class="kpi-box"><span style="color:#2ecc71">OPERANDO</span><br><b style="font-size:1.5em; color:#2ecc71;">{total-paradas-parciais}</b></div>
            <div class="kpi-box"><span style="color:#f1c40f">ATENÇÃO</span><br><b style="font-size:1.5em; color:#f1c40f;">{parciais}</b></div>
            <div class="kpi-box"><span style="color:#e74c3c">PARADAS</span><br><b style="font-size:1.5em; color:#e74c3c;">{paradas}</b></div>
        </div>
        <div class="kpi-box" style="border-color: #90cdf4;">
            <span style="color:#90cdf4">HORÁRIO</span><br><b style="font-size:1.5em; color:white;">{agora}</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 5. Renderização por Setores
for setor_nome, ativos_setor in setores.items():
    st.markdown(f"<div class='setor-header'>{setor_nome}</div>", unsafe_allow_html=True)
    cols = st.columns(6)
    
    # Filtra os dados processados que pertencem a este setor
    dados_setor = [d for d in lista_final if d['setor'] == setor_nome]
    
    for idx, d in enumerate(dados_setor):
        with cols[idx % 6]:
            st.markdown(f"""
                <div class="card {d['classe']}" style="border-top-color: {d['cor']};">
                    <div class="maquina-id">{d['id']}</div>
                    <div class="maquina-nome">{d['n']}</div>
                    <div class="status-texto" style="color: {d['cor']};">{d['status']}</div>
                    <div class='texto-destaque'>{d['s_nome'] if d['status'] != 'NORMAL' else '✅ OPERANDO'}</div>
                </div>
            """, unsafe_allow_html=True)
