import streamlit as st
import requests
from datetime import datetime

# 1. Configuração da Página
st.set_page_config(page_title="Monitoramento Litoral", layout="wide")

# Auto-refresh de 30 segundos
st.components.v1.html(
    "<script>setTimeout(function(){window.location.reload();}, 30000);</script>",
    height=0,
)

agora = datetime.now().strftime("%H:%M:%S")

# 2. CSS com Correção de Letras, Espaçamento Superior e Cores
st.markdown(f"""
    <style>
    .block-container {{ 
        padding-top: 5rem !important; 
        max-width: 98% !important; 
        margin: 0 auto; 
    }}
    
    .stApp {{ background-color: #0b0e14; }}
    header {{ visibility: hidden; }}

    .timer-container {{
        position: absolute; top: 10px; right: 20px; color: #718096;
        font-family: monospace; font-size: 0.8rem; background: rgba(26, 31, 41, 0.9);
        padding: 4px 12px; border-radius: 20px; border: 1px solid #2d3748;
    }}

    .card {{
        background-color: #1a1f29; 
        padding: 12px 5px; 
        border-radius: 5px;
        text-align: center; 
        margin-bottom: 8px; 
        min-height: 155px; 
        display: flex; 
        flex-direction: column;
        justify-content: space-between; 
        align-items: center; 
        border: 1px solid #232a37;
        box-sizing: border-box;
        border-top: 7px solid;
    }}

    .nome-topo {{ 
        color: #a0aec0; 
        font-size: 0.65rem; 
        font-weight: 700; 
        text-transform: uppercase;
        margin-bottom: 4px;
    }}
    
    .id-numeros {{ 
        font-size: 2.3rem; 
        font-weight: 900;
        color: #ffffff;
        line-height: 1;
        letter-spacing: -1px;
    }}

    .status-area {{ 
        font-weight: 800; 
        font-size: 0.85rem; 
        text-transform: uppercase;
        margin: 6px 0;
    }}

    .tag-servico {{ 
        color: #ffffff !important; 
        font-weight: bold; 
        font-size: 0.7rem; 
        background: #334155; 
        border-radius: 3px; 
        padding: 3px 0; 
        width: 92%; 
    }}

    /* Cores das Bordas */
    .border-normal {{ border-top-color: #2ecc71 !important; }}
    .border-parada {{ border-top-color: #ff0000 !important; }}
    .farol-aviso {{ border-top-color: #ff8c00 !important; }}

    [data-testid="column"] {{ padding: 3px !important; }}
    </style>
    <div class="timer-container">⏱️ ATUALIZADO EM: {agora}</div>
    """, unsafe_allow_html=True)

# 3. Função de Busca de Dados
def buscar_dados():
    try:
        r = requests.get("https://dashboard-manutencao-ef55f-default-rtdb.firebaseio.com/manutencao.json")
        return r.text.upper() if r.text else ""
    except:
        return ""

# Lista de Ativos
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
cols = st.columns(8)

# 4. Processamento com Filtragem Estrita
for idx, at in enumerate(ativos):
    pos = string_bruta.rfind(at['id'])
    
    # PADRÃO É SEMPRE VERDE
    status, cor, classe, icon, servico = "NORMAL", "#2ecc71", "border-normal", "✅", "EM OPERAÇÃO"
    
    if pos != -1:
        # Analisamos apenas as informações de prioridade próximas ao ID
        ctx = string_bruta[pos : pos + 400]
        
        # VERIFICAÇÃO DE PRIORIDADE EXATA
        if "MÁQUINA PARADA" in ctx:
            status, cor, classe, icon, servico = "PARADA", "#ff0000", "border-parada", "🛑", "CORRETIVA"
        elif "MÁQ.PAR.PARCIAL" in ctx:
            status, cor, classe, icon, servico = "AVISO", "#ff8c00", "farol-aviso", "⚠️", "PARCIAL"
        # Se for "Normal" ou "Alta" (CIPA), ignora os IFs e permanece VERDE

    id_limpo = at['id'].replace("_", "").replace("QUIMICO", "")

    with cols[idx % 8]:
        st.markdown(f"""
            <div class="card {classe}">
                <div class="nome-topo">{at['n']}</div>
                <div class="id-container">
                    <span class="id-numeros">{id_exibicao if 'id_exibicao' in locals() else id_limpo}</span>
                </div>
                <div class="status-area" style="color: {cor};">{icon} {status}</div>
                <div class="tag-servico">{servico}</div>
            </div>
        """, unsafe_allow_html=True)
