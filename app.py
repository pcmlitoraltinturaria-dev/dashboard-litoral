import streamlit as st
import requests
from datetime import datetime

# 1. Configuração de Layout - Grade Limpa e Contínua
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
    
    /* Animação EXCLUSIVA para a borda superior vermelha */
    @keyframes piscar-topo {
        0% { border-top-color: #e74c3c; }
        50% { border-top-color: #1a1f29; }
        100% { border-top-color: #e74c3c; }
    }

    .card {
        background-color: #1a1f29; 
        padding: 12px 5px; 
        border-radius: 4px;
        text-align: center; 
        margin-bottom: 8px; 
        min-height: 160px; /* Altura para preencher bem a tela em 3 linhas */
        border-top: 8px solid; 
        display: flex; 
        flex-direction: column;
        justify-content: space-between;
        border-right: 1px solid #232a37;
        border-left: 1px solid #232a37;
        border-bottom: 1px solid #232a37;
    }

    .blink-top { animation: piscar-topo 0.8s infinite; }

    /* Design Moderno: Foco no ID */
    .id-grande { color: #ffffff; font-size: 2.5rem; font-weight: 900; line-height: 1; margin: 5px 0; }
    .nome-maquina { color: #a0aec0; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; }
    .status-texto { font-weight: 900; font-size: 1rem; text-transform: uppercase; }
    .tag-manutencao { 
        color: #a0aec0 !important; font-weight: bold; font-size: 0.75rem; 
        background: #232a37; border-radius: 3px; padding: 2px 0;
    }
    
    /* Placar Superior */
    .kpi-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
    .kpi-unit { background: #1a1f29; padding: 5px 15px; border-radius: 6px; border: 1px solid #2d3748; display: flex; gap: 10px; align-items: center; }

    [data-testid="column"] { padding: 3px !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Lista de Ativos (Ordem sequencial)
ativos = [
    {"id": "701", "n": "BIANCO"}, {"id": "1501", "n": "BRASTEC 1"}, {"id": "1502", "n": "BRASTEC 2"},
    {"id": "1503", "n": "BRASTEC 3"}, {"id": "1504", "n": "BRASTEC 4"}, {"id": "1506", "n": "BRASTEC 6"},
    {"id": "804", "n": "ALBRECHT"}, {"id": "803", "n": "LAFER"}, {"id": "1201", "n": "UNITECH"},
    {"id": "_1202", "n": "LK"}, {"id": "1404", "n": "HIDRORELAX"}, {"id": "1601", "n": "CORANTE"},
    {"id": "QUIMICO_1602", "n": "QUÍMICO"}, {"id": "1306", "n": "HT 1306"}, {"id": "1311", "n": "HT 1311"},
    {"id": "1314", "n": "HT 1314"}, {"id": "HT_1324", "n": "HT 1324"}, {"id": "HT_1308", "n": "HT 1308"},
    {"id": "HT_1303", "n": "HT 1303"}, {"id": "HT_1313", "n": "HT 1313"}, {"id": "1001", "n": "FELP 1"},
    {"id": "1002", "n": "FELP 2"}, {"id": "2603", "n": "SECADOR"}, {"id": "EMPILHADEIRA 26", "n": "EMPILHA 26"}
]

# 3. Busca de Dados
def buscar_dados():
    try:
        r = requests.get("https://dashboard-manutencao-ef55f-default-rtdb.firebaseio.com/manutencao.json")
        return r.text.upper() if r.text else ""
    except: return ""

string_bruta = buscar_dados()
total, paradas, parciais = 0, 0, 0
lista_processada = []

for at in ativos:
    total += 1
    pos = string_bruta.rfind(at['id'])
    status, cor, classe, icon, s_nome = "NORMAL", "#2ecc71", "", "✅", "OPERANDO"
    
    if pos != -1:
        ctx = string_bruta[pos : pos + 80]
        if any(x in ctx for x in ["CIVIL", "PARCIAL", "MÁQ.PAR.PARCIAL"]):
            status, cor, icon, parciais = "AVISO", "#f1c40f", "⚠️", parciais + 1
        elif "PARADA" in ctx:
            status, cor, classe, icon, paradas = "PARADA", "#e74c3c", "blink-top", "🛑", paradas + 1
        
        if "CIVIL" in ctx: s_nome = "CIVIL"
        elif "ELETRICA" in ctx: s_nome = "ELÉTRICA"
        elif "MECANICA" in ctx: s_nome = "MECÂNICA"

    lista_processada.append({
        "id": at['id'].replace("_","").replace("EMPILHADEIRA ",""), 
        "n": at['n'], "status": status, "cor": cor, 
        "classe": classe, "icon": icon, "s_nome": s_nome
    })

# 4. Cabeçalho
agora = datetime.now().strftime("%H:%M:%S")
st.markdown(f"""
    <div class="kpi-row">
        <div style="display: flex; gap: 12px;">
            <div class="kpi-unit"><b style="color:#2ecc71; font-size:1.4em;">{total-paradas-parciais}</b> <small style="color:#a0aec0; font-weight:bold;">OK</small></div>
            <div class="kpi-unit"><b style="color:#f1c40f; font-size:1.4em;">{parciais}</b> <small style="color:#a0aec0; font-weight:bold;">AVISO</small></div>
            <div class="kpi-unit"><b style="color:#e74c3c; font-size:1.4em;">{paradas}</b> <small style="color:#a0aec0; font-weight:bold;">STOP</small></div>
        </div>
        <div style="color: #90cdf4; font-weight: 900; font-size: 1.8em;">{agora}</div>
    </div>
    """, unsafe_allow_html=True)

# 5. Renderização em Grade (8 colunas)
cols = st.columns(8)
for idx, m in enumerate(lista_processada):
    with cols[idx % 8]:
        st.markdown(f"""
            <div class="card {m['classe']}" style="border-top-color: {m['cor']};">
                <div class="nome-maquina">{m['n']}</div>
                <div class="id-grande">{m['id']}</div>
                <div class="status-texto" style="color: {m['cor']};">{m['icon']} {m['status']}</div>
                <div class="tag-manutencao">{m['s_nome'] if m['status'] != 'NORMAL' else 'EM OPERAÇÃO'}</div>
            </div>
        """, unsafe_allow_html=True)
