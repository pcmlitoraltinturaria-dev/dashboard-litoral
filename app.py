import streamlit as st
import requests

# 1. Configuração de Layout e Estilo (Original Litoral)
st.set_page_config(page_title="Monitor Litoral", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .card {
        background-color: #1f2937;
        padding: 15px;
        border-radius: 5px;
        text-align: center;
        margin-bottom: 15px;
        min-height: 250px;
        border-top: 6px solid;
        display: flex;
        flex-direction: column;
    }
    .maquina-id { color: #9ca3af; font-size: 0.7em; }
    .maquina-nome { color: white; font-weight: bold; font-size: 1.1em; margin-top: 5px; height: 45px; display: flex; align-items: center; justify-content: center; }
    .status-texto { font-weight: bold; font-size: 1.2em; text-transform: uppercase; margin: 15px 0; }
    .footer-area { border-top: 1px solid #374151; padding-top: 10px; margin-top: auto; text-align: center; }
    .tipo-manut { color: #d1d5db; font-size: 0.8em; font-weight: bold; display: block; margin-bottom: 5px; }
    .desc-texto { color: #fbbf24; font-weight: bold; font-size: 0.85em; text-transform: uppercase; line-height: 1.2; }
    </style>
    """, unsafe_allow_html=True)

# 2. Busca de Dados
def buscar_dados():
    try:
        r = requests.get("https://dashboard-manutencao-ef55f-default-rtdb.firebaseio.com/manutencao.json")
        return r.text.upper()
    except: return ""

string_bruta = buscar_dados()

# 3. LISTA COMPLETA DE ATIVOS (Garantindo que todas apareçam)
ativos = [
    {"id": "701", "n": "ABRIDOR BIANCO"}, {"id": "1501", "n": "ABRIDOR BRASTEC 1"},
    {"id": "1502", "n": "ABRIDOR BRASTEC 2"}, {"id": "1503", "n": "ABRIDOR BRASTEC 3"},
    {"id": "1504", "n": "ABRIDOR BRASTEC 4"}, {"id": "1506", "n": "ABRIDOR BRASTEC 6"},
    {"id": "1404", "n": "HIDRORELAXADORA"}, {"id": "804", "n": "CALANDRA ALBRECHT"},
    {"id": "803", "n": "CALANDRA LAFER"}, {"id": "1202", "n": "RAMA LK"},
    {"id": "1201", "n": "RAMA UNITECH"}, {"id": "1601", "n": "COZINHA CORANTE"},
    {"id": "1602", "n": "COZINHA QUÍMICO"}, {"id": "1001", "n": "FELPADEIRA 1"},
    {"id": "1002", "n": "FELPADEIRA 2"}, {"id": "59", "n": "HT 1324"},
    {"id": "1306", "n": "HT 1306"}, {"id": "1311", "n": "HT 1311"},
    {"id": "1314", "n": "HT 1314"}, {"id": "2603", "n": "SECADOR"}, {"id": "26", "n": "EMPILHADEIRA"}
]

# 4. Renderização em Grade (5 colunas)
cols = st.columns(5)
for i, at in enumerate(ativos):
    # Busca a última posição do ID na string
    pos = string_bruta.rfind(f'"{at["id"]}"') # Busca exata pelo ID entre aspas
    if pos == -1: pos = string_bruta.rfind(at['id']) # Busca secundária
    
    ctx = string_bruta[pos:pos+400] if pos != -1 else ""
    
    # Extração Limpa da Descrição
    desc_real = ""
    if "DESC:" in ctx:
        desc_real = ctx.split("DESC:")[1].split("|")[0].split('"')[0].strip()

    # Lógica de Status e Cores
    if "MÁQUINA PARADA" in ctx:
        cor, status, tipo = "#e74c3c", "PARADA", "MANUT. CORRETIVA"
        detalhe = f"<span class='desc-texto'>{desc_real}</span>"
    elif "ABERTA" in ctx or "EXECUÇÃO" in ctx:
        cor, status, tipo = "#f1c40f", "ATENÇÃO", "O.S. EM CURSO"
        detalhe = f"<span class='desc-texto'>{desc_real}</span>"
    else:
        cor, status, tipo = "#2ecc71", "NORMAL", ""
        detalhe = "✅ EQUIPAMENTO OPERANDO"

    with cols[i % 5]:
        st.markdown(f"""
            <div class="card" style="border-top-color: {cor};">
                <div>
                    <div class="maquina-id">ID: {at['id']}</div>
                    <div class="maquina-nome">{at['n']}</div>
                    <div class="status-texto" style="color: {cor};">{status}</div>
                </div>
                <div class="footer-area">
                    <span class="tipo-manut">{tipo}</span>
                    {detalhe}
                </div>
            </div>
        """, unsafe_allow_html=True)
