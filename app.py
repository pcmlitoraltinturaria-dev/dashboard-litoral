import streamlit as st
import requests
from datetime import datetime

# 1. Configuração de Layout
st.set_page_config(page_title="Central de Monitoramento Litoral", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; }
    .block-container { padding-top: 1.5rem !important; }
    
    .setor-header {
        color: #90cdf4; font-size: 1.1rem; font-weight: bold;
        border-bottom: 2px solid #2d3748; margin: 15px 0 8px 0;
        padding-bottom: 3px; text-transform: uppercase; letter-spacing: 1px;
    }

    @keyframes piscar-critico {
        0% { opacity: 1; border-top-color: #e74c3c; box-shadow: 0 0 12px #e74c3c; }
        50% { opacity: 0.5; border-top-color: transparent; box-shadow: none; }
        100% { opacity: 1; border-top-color: #e74c3c; box-shadow: 0 0 12px #e74c3c; }
    }

    .card {
        background-color: #1a1f29; padding: 8px; border-radius: 6px;
        text-align: center; margin-bottom: 6px; min-height: 110px;
        border-top: 5px solid; display: flex; flex-direction: column;
        justify-content: space-between; border-right: 1px solid #2d3748;
        border-left: 1px solid #2d3748; border-bottom: 1px solid #2d3748;
    }

    .blink-red { animation: piscar-critico 1s infinite; background-color: #2d1616 !important; }

    .maquina-id { color: #90cdf4; font-size: 0.7em; font-weight: bold; }
    .maquina-nome { color: #ffffff; font-weight: 800; font-size: 0.8em; min-height: 28px; display: flex; align-items: center; justify-content: center; }
    .status-texto { font-weight: 900; font-size: 0.9em; text-transform: uppercase; }
    .texto-destaque { color: #a0aec0 !important; font-weight: bold; font-size: 0.7em; background: #2d3748; border-radius: 4px; padding: 1px 0; }
    
    .kpi-box { text-align: center; background: #1a1f29; padding: 8px; border-radius: 8px; border: 1px solid #2d3748; min-width: 120px; }
    [data-testid="column"] { padding: 2px !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Definição dos Setores (IMPORTANTE: Deve vir antes do processamento)
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

# 3. Busca de Dados
def buscar_dados():
    try:
        r = requests.get("https://dashboard-manutencao-ef55f-default-rtdb.firebaseio.com/manutencao.json")
        return r.text.upper() if r.text else ""
    except: return ""

string_bruta = buscar_dados()

# 4. Processamento de Status
total, paradas, parciais = 0, 0, 0
lista_final = []

for nome_setor, ativos_do_setor in setores.items():
    for at in ativos_do_setor:
        total += 1
        pos = string_bruta.rfind(at['id'])
        status, cor, classe, s_nome = "NORMAL", "#2ecc71", "", "MANUTENÇÃO"
        
        if pos != -1:
            ctx = string_bruta[pos : pos + 80]
            if "CIVIL" in ctx: s_nome = "CIVIL"
            elif "ELETRICA" in ctx: s_nome = "ELÉTRICA"
            elif "MECANICA" in ctx: s_nome = "MECÂNICA"

            if "NORMAL" in ctx: 
                status, cor = "NORMAL", "#2ecc71"
            elif any(x in ctx for x in ["CIVIL", "PARCIAL", "MÁQ.PAR.PARCIAL"]):
                status, cor = "PARCIAL", "#f1c40f"
                parciais += 1
            elif "PARADA" in ctx:
                status, cor, classe = "PARADA", "#e74c3c", "blink-red"
                paradas += 1
        
        # Unir dados da máquina com status processado
        dados_maquina = at.copy()
        dados_maquina.update({
            "status": status, "cor": cor, "classe": classe, 
            "setor_pai": nome_setor, "s_nome": s_nome
        })
        lista_final.append(dados_maquina)

# 5. Cabeçalho (KPIs e Relógio)
agora = datetime.now().strftime("%H:%M:%S")
st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
        <div style="display: flex; gap: 10px;">
            <div class="kpi-box"><span style="color:#a0aec0; font-size:0.7em;">TOTAL</span><br><b style="font-size:1.2em; color:white;">{total}</b></div>
            <div class="kpi-box"><span style="color:#2ecc71; font-size:0.7em;">OPERANDO</span><br><b style="font-size:1.2em; color:#2ecc71;">{total-paradas-parciais}</b></div>
            <div class="kpi-box"><span style="color:#f1c40f; font-size:0.7em;">ATENÇÃO</span><br><b style="font-size:1.2em; color:#f1c40f;">{parciais}</b></div>
            <div class="kpi-box"><span style="color:#e74c3c; font-size:0.7em;">PARADAS</span><br><b style="font-size:1.2em; color:#e74c3c;">{paradas}</b></div>
        </div>
        <div class="kpi-box" style="border-color: #90cdf4;">
            <span style="color:#90cdf4; font-size:0.7em;">HORÁRIO</span><br><b style="font-size:1.2em; color:white;">{agora}</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 6. Exibição por Setores
for nome_setor in setores.keys():
    st.markdown(f"<div class='setor-header'>{nome_setor}</div>", unsafe_allow_html=True)
    cols = st.columns(6)
    
    # Filtra máquinas deste setor específico
    maquinas_setor = [m for m in lista_final if m['setor_pai'] == nome_setor]
    
    for idx, m in enumerate(maquinas_setor):
        with cols[idx % 6]:
            st.markdown(f"""
                <div class="card {m['classe']}" style="border-top-color: {m['cor']};">
                    <div class="maquina-id">{m['id']}</div>
                    <div class="maquina-nome">{m['n']}</div>
                    <div class="status-texto" style="color: {m['cor']};">{m['status']}</div>
                    <div class='texto-destaque'>{m['s_nome'] if m['status'] != 'NORMAL' else '✅ OPERANDO'}</div>
                </div>
            """, unsafe_allow_html=True)
