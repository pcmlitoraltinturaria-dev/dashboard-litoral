import streamlit as st
import requests
from datetime import datetime

# 1. Configuração de Layout para Máxima Otimização de Tela
st.set_page_config(page_title="Central Litoral", layout="wide")

st.markdown("""
    <style>
    /* Remove margens do Streamlit para preencher a tela */
    .block-container { 
        padding-top: 0.2rem !important; 
        padding-bottom: 0rem !important; 
        padding-left: 0.5rem !important; 
        padding-right: 0.5rem !important; 
        max-width: 100% !important;
    }
    .stApp { background-color: #0b0e14; overflow: hidden; }
    
    /* SETOR: Grudado na linha. O fundo do texto "corta" a linha de cor */
    .setor-label {
        color: #90cdf4; 
        font-size: 0.65rem; 
        font-weight: 800;
        text-transform: uppercase;
        margin-bottom: -10px; /* Puxa o card para "dentro" do texto */
        margin-left: 12px;
        position: relative;
        z-index: 99; 
        background-color: #0b0e14; /* Cor do fundo da página para o efeito de corte */
        padding: 0 5px;
        display: inline-block;
        letter-spacing: 0.5px;
    }

    /* Animação EXCLUSIVA para a borda superior (Pisca sem contorno) */
    @keyframes piscar-topo-apenas {
        0% { border-top-color: #e74c3c; }
        50% { border-top-color: #1a1f29; }
        100% { border-top-color: #e74c3c; }
    }

    .card {
        background-color: #1a1f29; 
        padding: 6px 2px; 
        border-radius: 2px;
        text-align: center; 
        margin-bottom: 0px; /* Elimina espaço extra entre linhas verticalmente */
        min-height: 140px; 
        border-top: 8px solid; 
        display: flex; 
        flex-direction: column;
        justify-content: space-between;
        border-right: 1px solid #232a37;
        border-left: 1px solid #232a37;
        border-bottom: 1px solid #232a37;
    }

    /* Gatilho para o pisca APENAS na linha superior */
    .blink-top { 
        animation: piscar-topo-apenas 0.8s infinite; 
    }

    .maquina-id { color: #90cdf4; font-size: 0.75em; font-weight: bold; opacity: 0.6; }
    .maquina-nome { 
        color: #ffffff; font-weight: 800; font-size: 0.85em; 
        min-height: 38px; line-height: 1.1; 
        display: flex; align-items: center; justify-content: center;
    }
    .status-texto { font-weight: 900; font-size: 1.05em; text-transform: uppercase; }
    .texto-destaque { 
        color: #a0aec0 !important; font-weight: bold; font-size: 0.7em; 
        background: #232a37; border-radius: 2px; padding: 1px 0;
    }
    
    /* Cabeçalho compactado ao máximo */
    .kpi-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 2px; }
    .kpi-unit { background: #1a1f29; padding: 2px 10px; border-radius: 4px; border: 1px solid #2d3748; display: flex; gap: 8px; align-items: center; }

    /* Ajuste para aproximar as colunas horizontalmente */
    [data-testid="column"] { padding: 1px !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Definição de Dados
setores = {
    "PREPARAÇÃO": ["701", "1501", "1502", "1503", "1504", "1506"],
    "ACABAMENTO": ["804", "803", "1201", "_1202", "1404"],
    "TINTURARIA": ["1601", "QUIMICO_1602", "1306", "1311", "1314", "HT_1324", "HT_1308", "HT_1303", "HT_1313"],
    "SECAGEM/FELP": ["1001", "1002", "2603"],
    "LOGÍSTICA": ["EMPILHADEIRA 26"]
}

# 3. Processamento
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
            if "NORMAL" in ctx: status, cor = "NORMAL", "#2ecc71"
            elif any(x in ctx for x in ["CIVIL", "PARCIAL", "MÁQ.PAR.PARCIAL"]):
                status, cor, parciais = "PARCIAL", "#f1c40f", parciais + 1
            elif "PARADA" in ctx:
                status, cor, classe, paradas = "PARADA", "#e74c3c", "blink-top", paradas + 1
            
            # Sub-status
            if "CIVIL" in ctx: s_nome = "CIVIL"
            elif "ELETRICA" in ctx: s_nome = "ELÉTRICA"
            elif "MECANICA" in ctx: s_nome = "MECÂNICA"

        lista_final.append({"id": id_maq, "status": status, "cor": cor, "classe": classe, "setor": nome_setor, "s_nome": s_nome, "primeira": (i == 0)})

# 4. Cabeçalho KPIs
agora = datetime.now().strftime("%H:%M:%S")
st.markdown(f"""
    <div class="kpi-row">
        <div style="display: flex; gap: 8px;">
            <div class="kpi-unit"><b style="color:#2ecc71;">{total-paradas-parciais}</b> <span style="color:#a0aec0; font-size:0.65em;">OK</span></div>
            <div class="kpi-unit"><b style="color:#f1c40f;">{parciais}</b> <span style="color:#a0aec0; font-size:0.65em;">AVISO</span></div>
            <div class="kpi-unit"><b style="color:#e74c3c;">{paradas}</b> <span style="color:#a0aec0; font-size:0.65em;">STOP</span></div>
        </div>
        <div style="color: #90cdf4; font-weight: 800; font-size: 1.1em;">{agora}</div>
    </div>
    """, unsafe_allow_html=True)

# 5. Grid de 8 Colunas (Aproveitamento Total)
cols = st.columns(8)
for idx, m in enumerate(lista_final):
    with cols[idx % 8]:
        # Título do Setor (visível apenas na primeira máquina de cada grupo)
        label_html = f"<span class='setor-label'>{m['setor']}</span>" if m['primeira'] else "<span class='setor-label' style='color:transparent;'>.</span>"
        
        st.markdown(f"""
            {label_html}
            <div class="card {m['classe']}" style="border-top-color: {m['cor']};">
                <div class="maquina-id">ID {m['id']}</div>
                <div class="maquina-nome">MÁQUINA {m['id']}</div>
                <div class="status-texto" style="color: {m['cor']};">{m['status']}</div>
                <div class='texto-destaque'>{m['s_nome'] if m['status'] != 'NORMAL' else '✅ OPERANDO'}</div>
            </div>
        """, unsafe_allow_html=True)
