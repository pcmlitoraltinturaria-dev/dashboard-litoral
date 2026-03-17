import streamlit as st
import requests
from datetime import datetime

# 1. Configuração de Layout para Tela Única
st.set_page_config(page_title="Central Litoral", layout="wide")

st.markdown("""
    <style>
    /* Reset de margens para aproveitar 100% da tela vertical */
    .block-container { 
        padding-top: 0.5rem !important; 
        padding-bottom: 0rem !important; 
        padding-left: 0.5rem !important; 
        padding-right: 0.5rem !important; 
    }
    .stApp { background-color: #0b0e14; overflow: hidden; }
    
    /* Nome do setor grudado na linha de cor */
    .setor-label {
        color: #90cdf4; 
        font-size: 0.65rem; 
        font-weight: 800;
        text-transform: uppercase;
        margin-bottom: -3px;
        margin-left: 5px;
        display: block;
        text-align: left;
    }

    /* Animação EXCLUSIVA para a borda superior (sem contorno lateral) */
    @keyframes piscar-apenas-linha {
        0% { border-top-color: #e74c3c; }
        50% { border-top-color: #374151; }
        100% { border-top-color: #e74c3c; }
    }

    .card {
        background-color: #1a1f29; 
        padding: 8px 4px; 
        border-radius: 3px;
        text-align: center; 
        margin-bottom: 5px; 
        min-height: 155px; /* Altura reduzida para caber 3 linhas na tela */
        border-top: 7px solid; 
        display: flex; 
        flex-direction: column;
        justify-content: space-between;
        border-right: 1px solid #232a37;
        border-left: 1px solid #232a37;
        border-bottom: 1px solid #232a37;
    }

    /* Aplica o pisca apenas na linha vermelha */
    .blink-line-only { 
        animation: piscar-apenas-linha 0.8s infinite; 
    }

    .maquina-id { color: #90cdf4; font-size: 0.8em; font-weight: bold; opacity: 0.7; }
    .maquina-nome { 
        color: #ffffff; font-weight: 800; font-size: 0.95em; 
        min-height: 40px; line-height: 1.1; 
        display: flex; align-items: center; justify-content: center;
    }
    .status-texto { font-weight: 900; font-size: 1.15em; text-transform: uppercase; }
    .texto-destaque { 
        color: #a0aec0 !important; font-weight: bold; font-size: 0.75em; 
        background: #232a37; border-radius: 3px; padding: 2px 0;
    }
    
    /* Placar Compacto */
    .kpi-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
    .kpi-unit { background: #1a1f29; padding: 4px 15px; border-radius: 6px; border: 1px solid #2d3748; display: flex; gap: 10px; align-items: center; }

    [data-testid="column"] { padding: 3px !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Dados (Setores e Ativos)
setores = {
    "PREPARAÇÃO": ["701", "1501", "1502", "1503", "1504", "1506"],
    "ACABAMENTO": ["804", "803", "1201", "_1202", "1404"],
    "TINTURARIA": ["1601", "QUIMICO_1602", "1306", "1311", "1314", "HT_1324", "HT_1308", "HT_1303", "HT_1313"],
    "SECAGEM/FELP": ["1001", "1002", "2603"],
    "LOGÍSTICA": ["EMPILHADEIRA 26"]
}

nomes_maquinas = {
    "701": "ABRIDOR BIANCO", "1501": "ABRIDOR BRASTEC 1", "1502": "ABRIDOR BRASTEC 2",
    "1503": "ABRIDOR BRASTEC 3", "1504": "ABRIDOR BRASTEC 4", "1506": "ABRIDOR BRASTEC 6",
    "804": "CALANDRA ALBRECHT", "803": "CALANDRA LAFER", "1201": "RAMA UNITECH",
    "_1202": "RAMA LK", "1404": "HIDRORELAXADORA", "1601": "COZINHA CORANTE",
    "QUIMICO_1602": "COZINHA QUÍMICO", "1306": "HT 1306", "1311": "HT 1311",
    "1314": "HT 1314", "HT_1324": "HT 1324", "HT_1308": "HT 1308", "HT_1303": "HT 1303",
    "HT_1313": "HT 1313", "1001": "FELPADEIRA 1", "1002": "FELPADEIRA 2",
    "2603": "SECADOR", "EMPILHADEIRA 26": "EMPILHADEIRA 26"
}

# 3. Integração
def buscar_dados():
    try:
        r = requests.get("https://dashboard-manutencao-ef55f-default-rtdb.firebaseio.com/manutencao.json")
        return r.text.upper() if r.text else ""
    except: return ""

string_bruta = buscar_dados()
total, paradas, parciais = 0, 0, 0
lista_final = []

for nome_setor, ids in setores.items():
    for i, id_maq in enumerate(ids):
        total += 1
        pos = string_bruta.rfind(id_maq)
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
                status, cor, classe, paradas = "PARADA", "#e74c3c", "blink-line-only", paradas + 1
        
        lista_final.append({
            "id": id_maq, "n": nomes_maquinas[id_maq], "status": status, 
            "cor": cor, "classe": classe, "setor": nome_setor, 
            "s_nome": s_nome, "primeira": (i == 0)
        })

# 4. Exibição KPIs
agora = datetime.now().strftime("%H:%M:%S")
st.markdown(f"""
    <div class="kpi-row">
        <div style="display: flex; gap: 10px;">
            <div class="kpi-unit"><b style="color:#2ecc71; font-size:1.3em;">{total-paradas-parciais}</b> <span style="color:#a0aec0; font-size:0.7em;">OPERANDO</span></div>
            <div class="kpi-unit"><b style="color:#f1c40f; font-size:1.3em;">{parciais}</b> <span style="color:#a0aec0; font-size:0.7em;">AVISO</span></div>
            <div class="kpi-unit"><b style="color:#e74c3c; font-size:1.3em;">{paradas}</b> <span style="color:#a0aec0; font-size:0.7em;">PARADAS</span></div>
        </div>
        <div style="color: #90cdf4; font-weight: 800; font-size: 1.5em; letter-spacing: 1px;">{agora}</div>
    </div>
    """, unsafe_allow_html=True)

# 5. Grid de 8 Colunas (3 Linhas para 24 Ativos)
cols = st.columns(8)
for idx, m in enumerate(lista_final):
    with cols[idx % 8]:
        label = f"<span class='setor-label'>{m['setor']}</span>" if m['primeira'] else "<span class='setor-label' style='color:transparent;'>.</span>"
        
        st.markdown(f"""
            {label}
            <div class="card {m['classe']}" style="border-top-color: {m['cor']};">
                <div class="maquina-id">ID {m['id']}</div>
                <div class="maquina-nome">{m['n']}</div>
                <div class="status-texto" style="color: {m['cor']};">{m['status']}</div>
                <div class='texto-destaque'>{m['s_nome'] if m['status'] != 'NORMAL' else '✅ EM OPERAÇÃO'}</div>
            </div>
        """, unsafe_allow_html=True)
