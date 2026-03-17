import streamlit as st
import requests
from datetime import datetime

# 1. Configuração de Layout para Tela Única
st.set_page_config(page_title="Central Litoral", layout="wide")

st.markdown("""
    <style>
    /* Força o conteúdo a ocupar o topo e remove scrolls desnecessários */
    .block-container { padding-top: 1rem !important; padding-bottom: 0rem !important; }
    .stApp { background-color: #0b0e14; overflow: hidden; }
    
    /* Cabeçalho de Setor mais fino */
    .setor-header {
        color: #90cdf4; font-size: 0.9rem; font-weight: bold;
        border-bottom: 1px solid #2d3748; margin: 8px 0 4px 0;
        text-transform: uppercase; letter-spacing: 1px;
    }

    /* Animação APENAS para a borda superior */
    @keyframes piscar-borda {
        0% { border-top-color: #e74c3c; box-shadow: 0 -4px 8px -2px rgba(231, 76, 60, 0.5); }
        50% { border-top-color: #374151; box-shadow: none; }
        100% { border-top-color: #e74c3c; box-shadow: 0 -4px 8px -2px rgba(231, 76, 60, 0.5); }
    }

    .card {
        background-color: #1a1f29; padding: 5px; border-radius: 4px;
        text-align: center; margin-bottom: 4px; 
        min-height: 85px; /* Altura reduzida para caber tudo na janela */
        border-top: 5px solid; display: flex; flex-direction: column;
        justify-content: space-between; border-right: 1px solid #2d3748;
        border-left: 1px solid #2d3748; border-bottom: 1px solid #2d3748;
    }

    /* Aplica animação apenas na borda superior se estiver PARADA */
    .blink-top { animation: piscar-borda 0.8s infinite; }

    .maquina-id { color: #90cdf4; font-size: 0.65em; font-weight: bold; }
    .maquina-nome { color: #ffffff; font-weight: 700; font-size: 0.75em; min-height: 22px; line-height: 1.1; display: flex; align-items: center; justify-content: center; }
    .status-texto { font-weight: 800; font-size: 0.85em; text-transform: uppercase; }
    .texto-destaque { color: #a0aec0 !important; font-weight: bold; font-size: 0.65em; background: #2d3748; border-radius: 3px; }
    
    .kpi-box { text-align: center; background: #1a1f29; padding: 5px 10px; border-radius: 6px; border: 1px solid #2d3748; }
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

# 3. Busca de Dados
def buscar_dados():
    try:
        r = requests.get("https://dashboard-manutencao-ef55f-default-rtdb.firebaseio.com/manutencao.json")
        return r.text.upper() if r.text else ""
    except: return ""

string_bruta = buscar_dados()

# 4. Processamento
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
                status, cor = "PARCIAL", "#f1c40f"
                parciais += 1
            elif "PARADA" in ctx:
                status, cor, classe = "PARADA", "#e74c3c", "blink-top"
                paradas += 1
        
        m = at.copy()
        m.update({"status": status, "cor": cor, "classe": classe, "setor_pai": nome_setor, "s_nome": s_nome})
        lista_final.append(m)

# 5. Cabeçalho Compacto
agora = datetime.now().strftime("%H:%M:%S")
st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
        <div style="display: flex; gap: 8px;">
            <div class="kpi-box"><b style="color:#2ecc71;">{total-paradas-parciais}</b> <span style="color:#a0aec0; font-size:0.7em;">OK</span></div>
            <div class="kpi-box"><b style="color:#f1c40f;">{parciais}</b> <span style="color:#a0aec0; font-size:0.7em;">AVISO</span></div>
            <div class="kpi-box"><b style="color:#e74c3c;">{paradas}</b> <span style="color:#a0aec0; font-size:0.7em;">STOP</span></div>
        </div>
        <div style="color: #90cdf4; font-weight: bold; font-size: 1.1em;">{agora}</div>
    </div>
    """, unsafe_allow_html=True)

# 6. Renderização por Setores
for nome_setor in setores.keys():
    st.markdown(f"<div class='setor-header'>{nome_setor}</div>", unsafe_allow_html=True)
    cols = st.columns(9) # Aumentado para 9 colunas para achatar os grupos
    maquinas = [m for m in lista_final if m['setor_pai'] == nome_setor]
    
    for idx, m in enumerate(maquinas):
        with cols[idx % 9]:
            st.markdown(f"""
                <div class="card {m['classe']}" style="border-top-color: {m['cor']};">
                    <div class="maquina-id">{m['id']}</div>
                    <div class="maquina-nome">{m['n']}</div>
                    <div class="status-texto" style="color: {m['cor']};">{m['status']}</div>
                    <div class='texto-destaque'>{m['s_nome'] if m['status'] != 'NORMAL' else '✅'}</div>
                </div>
            """, unsafe_allow_html=True)
