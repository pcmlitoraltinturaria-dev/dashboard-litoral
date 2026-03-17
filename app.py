import streamlit as st
import requests
from datetime import datetime

# 1. Configuração de Layout
st.set_page_config(page_title="Central Litoral", layout="wide")

st.markdown("""
    <style>
    /* Remove margens laterais e superiores do Streamlit */
    .block-container { 
        padding-top: 1rem !important; 
        padding-bottom: 0rem !important; 
        padding-left: 0.5rem !important; 
        padding-right: 0.5rem !important; 
        max-width: 100% !important;
    }
    .stApp { background-color: #0b0e14; overflow: hidden; }
    
    /* Títulos de Setor compactos */
    .setor-header {
        color: #90cdf4; font-size: 0.85rem; font-weight: bold;
        border-left: 4px solid #90cdf4; margin: 10px 0 5px 0;
        padding-left: 8px; text-transform: uppercase; background: #1a1f29;
    }

    /* Animação APENAS para a LINHA SUPERIOR (Borda) */
    @keyframes piscar-linha {
        0% { border-top-color: #e74c3c; box-shadow: 0 -2px 10px rgba(231, 76, 60, 0.6); }
        50% { border-top-color: #374151; box-shadow: none; }
        100% { border-top-color: #e74c3c; box-shadow: 0 -2px 10px rgba(231, 76, 60, 0.6); }
    }

    .card {
        background-color: #1a1f29; 
        padding: 6px 2px; 
        border-radius: 4px;
        text-align: center; 
        margin-bottom: 4px; 
        min-height: 110px; /* Altura mantida para leitura boa */
        border-top: 6px solid; /* Linha de cima mais grossa para destacar o pisca */
        display: flex; 
        flex-direction: column;
        justify-content: space-between;
        border-right: 1px solid #232a37;
        border-left: 1px solid #232a37;
        border-bottom: 1px solid #232a37;
    }

    /* Classe aplicada apenas quando o status é PARADA */
    .blink-top-only { animation: piscar-linha 0.8s infinite; }

    .maquina-id { color: #90cdf4; font-size: 0.7em; font-weight: bold; }
    .maquina-nome { 
        color: #ffffff; font-weight: 800; font-size: 0.85em; 
        min-height: 35px; line-height: 1.1; 
        display: flex; align-items: center; justify-content: center;
    }
    .status-texto { font-weight: 900; font-size: 0.95em; text-transform: uppercase; }
    .texto-destaque { 
        color: #a0aec0 !important; font-weight: bold; font-size: 0.7em; 
        background: #232a37; border-radius: 3px; margin: 0 4px;
    }
    
    /* Placar Superior */
    .kpi-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
    .kpi-unit { background: #1a1f29; padding: 4px 12px; border-radius: 5px; border: 1px solid #2d3748; display: flex; gap: 10px; align-items: center; }

    [data-testid="column"] { padding: 1px !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Definição dos Setores
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

# 3. Busca e Processamento
def buscar_dados():
    try:
        r = requests.get("https://dashboard-manutencao-ef55f-default-rtdb.firebaseio.com/manutencao.json")
        return r.text.upper() if r.text else ""
    except: return ""

string_bruta = buscar_dados()

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

            if "NORMAL" in ctx: status, cor = "NORMAL", "#2ecc71"
            elif any(x in ctx for x in ["CIVIL", "PARCIAL", "MÁQ.PAR.PARCIAL"]):
                status, cor, parciais = "PARCIAL", "#f1c40f", parciais + 1
            elif "PARADA" in ctx:
                status, cor, classe, paradas = "PARADA", "#e74c3c", "blink-top-only", paradas + 1
        
        m = at.copy()
        m.update({"status": status, "cor": cor, "classe": classe, "setor_pai": nome_setor, "s_nome": s_nome})
        lista_final.append(m)

# 4. Cabeçalho KPIs
agora = datetime.now().strftime("%H:%M:%S")
st.markdown(f"""
    <div class="kpi-row">
        <div style="display: flex; gap: 10px;">
            <div class="kpi-unit"><b style="color:#2ecc71; font-size:1.2em;">{total-paradas-parciais}</b> <span style="color:#a0aec0; font-size:0.8em;">OPERANDO</span></div>
            <div class="kpi-unit"><b style="color:#f1c40f; font-size:1.2em;">{parciais}</b> <span style="color:#a0aec0; font-size:0.8em;">ATENÇÃO</span></div>
            <div class="kpi-unit"><b style="color:#e74c3c; font-size:1.2em;">{paradas}</b> <span style="color:#a0aec0; font-size:0.8em;">PARADAS</span></div>
        </div>
        <div style="color: #90cdf4; font-weight: bold; font-size: 1.3em; background: #1a1f29; padding: 4px 15px; border-radius: 5px; border: 1px solid #2d3748;">{agora}</div>
    </div>
    """, unsafe_allow_html=True)

# 5. Exibição (12 COLUNAS)
for nome_setor in setores.keys():
    st.markdown(f"<div class='setor-header'>{nome_setor}</div>", unsafe_allow_html=True)
    cols = st.columns(12) # Layout esticado na horizontal
    maquinas = [m for m in lista_final if m['setor_pai'] == nome_setor]
    
    for idx, m in enumerate(maquinas):
        with cols[idx % 12]:
            st.markdown(f"""
                <div class="card {m['classe']}" style="border-top-color: {m['cor']};">
                    <div class="maquina-id">{m['id']}</div>
                    <div class="maquina-nome">{m['n']}</div>
                    <div class="status-texto" style="color: {m['cor']};">{m['status']}</div>
                    <div class='texto-destaque'>{m['s_nome'] if m['status'] != 'NORMAL' else '✅'}</div>
                </div>
            """, unsafe_allow_html=True)
