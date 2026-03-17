import streamlit as st
import requests
from datetime import datetime

# 1. Configuração e Estilo "Card Moderno"
st.set_page_config(page_title="Central Litoral V3", layout="wide")

st.markdown("""
    <style>
    .block-container { padding: 0.5rem !important; max-width: 100% !important; }
    .stApp { background-color: #0b0e14; overflow: hidden; }
    
    /* Rótulo do Setor integrado */
    .setor-label {
        color: #90cdf4; font-size: 0.6rem; font-weight: 800;
        text-transform: uppercase; margin-bottom: -10px; margin-left: 10px;
        position: relative; z-index: 99; background-color: #0b0e14;
        padding: 0 5px; display: inline-block; letter-spacing: 1px;
    }

    @keyframes piscar-linha {
        0% { border-top-color: #e74c3c; }
        50% { border-top-color: #1a1f29; }
        100% { border-top-color: #e74c3c; }
    }

    .card {
        background-color: #1a1f29; border-radius: 4px;
        text-align: center; margin-bottom: 5px; min-height: 150px;
        border-top: 8px solid; border-right: 1px solid #232a37;
        border-left: 1px solid #232a37; border-bottom: 1px solid #232a37;
        display: flex; flex-direction: column; justify-content: space-around;
        padding: 10px 5px;
    }

    .blink-top { animation: piscar-linha 0.8s infinite; }

    /* Tipografia sugerida: ID Grande e focado */
    .id-destaque { color: #ffffff; font-size: 2.2rem; font-weight: 900; line-height: 1; margin: 5px 0; }
    .nome-sub { color: #a0aec0; font-size: 0.7rem; font-weight: 600; text-transform: uppercase; }
    .status-badge { font-weight: 900; font-size: 0.9rem; padding: 2px 8px; border-radius: 10px; }
    
    /* Placar Superior */
    .kpi-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
    .kpi-unit { background: #1a1f29; padding: 5px 15px; border-radius: 6px; border: 1px solid #2d3748; }

    [data-testid="column"] { padding: 2px !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Dados e Processamento (Mantendo sua estrutura)
setores = {
    "PREPARAÇÃO": ["701", "1501", "1502", "1503", "1504", "1506"],
    "ACABAMENTO": ["804", "803", "1201", "_1202", "1404"],
    "TINTURARIA": ["1601", "QUIMICO_1602", "1306", "1311", "1314", "HT_1324", "HT_1308", "HT_1303", "HT_1313"],
    "SECAGEM/FELP": ["1001", "1002", "2603"],
    "LOGÍSTICA": ["EMPILHADEIRA 26"]
}

# Dicionário de nomes para legenda menor
nomes_curtos = {
    "701": "BIANCO", "1501": "BRASTEC 1", "1502": "BRASTEC 2", "1503": "BRASTEC 3", 
    "1504": "BRASTEC 4", "1506": "BRASTEC 6", "804": "ALBRECHT", "803": "LAFER",
    "1201": "UNITECH", "_1202": "LK", "1404": "HIDRORELAX", "1601": "CORANTE",
    "QUIMICO_1602": "QUÍMICO", "1306": "HT 1306", "1311": "HT 1311", "1314": "HT 1314",
    "HT_1324": "HT 1324", "HT_1308": "HT 1308", "HT_1303": "HT 1303", "HT_1313": "HT 1313",
    "1001": "FELP 1", "1002": "FELP 2", "2603": "SECADOR", "EMPILHADEIRA 26": "EMPILHA 26"
}

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
        status, cor, classe, icon, s_nome = "NORMAL", "#2ecc71", "", "✅", "OPERANDO"
        
        if pos != -1:
            ctx = string_bruta[pos : pos + 80]
            if "NORMAL" in ctx: pass
            elif any(x in ctx for x in ["CIVIL", "PARCIAL", "MÁQ.PAR.PARCIAL"]):
                status, cor, icon, parciais = "AVISO", "#f1c40f", "⚠️", parciais + 1
            elif "PARADA" in ctx:
                status, cor, classe, icon, paradas = "PARADA", "#e74c3c", "blink-top", "🛑", paradas + 1
            
            if "CIVIL" in ctx: s_nome = "CIVIL"
            elif "ELETRICA" in ctx: s_nome = "ELÉTRICA"
            elif "MECANICA" in ctx: s_nome = "MECÂNICA"

        lista_final.append({
            "id": id_maq.replace("_",""), "n": nomes_curtos.get(id_maq, "MAQ"), 
            "status": status, "cor": cor, "classe": classe, "icon": icon,
            "setor": nome_setor, "s_nome": s_nome, "primeira": (i == 0)
        })

# 3. Renderização
agora = datetime.now().strftime("%H:%M:%S")
st.markdown(f"""
    <div class="kpi-row">
        <div style="display: flex; gap: 10px;">
            <div class="kpi-unit"><b style="color:#2ecc71; font-size:1.2rem;">{total-paradas-parciais}</b> <small style="color:#a0aec0;">OK</small></div>
            <div class="kpi-unit"><b style="color:#f1c40f; font-size:1.2rem;">{parciais}</b> <small style="color:#a0aec0;">AVISO</small></div>
            <div class="kpi-unit"><b style="color:#e74c3c; font-size:1.2rem;">{paradas}</b> <small style="color:#a0aec0;">STOP</small></div>
        </div>
        <div style="color: #90cdf4; font-weight: 800; font-size: 1.5rem;">{agora}</div>
    </div>
    """, unsafe_allow_html=True)

cols = st.columns(8)
for idx, m in enumerate(lista_final):
    with cols[idx % 8]:
        label = f"<span class='setor-label'>{m['setor']}</span>" if m['primeira'] else "<div style='height:14px;'></div>"
        st.markdown(f"""
            {label}
            <div class="card {m['classe']}" style="border-top-color: {m['cor']};">
                <div class="nome-sub">{m['n']}</div>
                <div class="id-destaque">{m['id']}</div>
                <div style="color: {m['cor']}; font-size: 1.1rem;">{m['icon']}</div>
                <div class="status-badge" style="color: {m['cor']};">{m['status']}</div>
                <div style="font-size:0.6rem; color:#a0aec0; font-weight:bold;">{m['s_nome']}</div>
            </div>
        """, unsafe_allow_html=True)
