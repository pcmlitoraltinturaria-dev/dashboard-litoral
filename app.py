import streamlit as st
import requests

# 1. Configuração de Layout e Estilo Litoral
st.set_page_config(page_title="Monitor Litoral", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .card {
        background-color: #1f2937;
        padding: 15px;
        border-radius: 5px;
        text-align: center;
        margin-bottom: 10px;
        min-height: 240px;
        border-top: 6px solid;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .maquina-id { color: #9ca3af; font-size: 0.7em; text-transform: uppercase; }
    .maquina-nome { color: white; font-weight: bold; font-size: 1.1em; margin: 5px 0; }
    .status-texto { font-weight: bold; font-size: 1.2em; text-transform: uppercase; margin: 10px 0; }
    .footer-area { border-top: 1px solid #374151; padding-top: 10px; margin-top: auto; }
    .tipo-manut { color: #d1d5db; font-size: 0.85em; font-weight: bold; display: block; margin-bottom: 4px; }
    .desc-texto { color: #fbbf24; font-weight: bold; font-size: 0.85em; text-transform: uppercase; line-height: 1.2; display: block; }
    </style>
    """, unsafe_allow_html=True)

# 2. Captura de Dados
def buscar_dados():
    try:
        r = requests.get("https://dashboard-manutencao-ef55f-default-rtdb.firebaseio.com/manutencao.json")
        return r.text.upper()
    except: return ""

string_bruta = buscar_dados()

# 3. Lista de Ativos (Foco no ID para evitar erros)
ativos = [
    {"id": "1202", "n": "RAMA LK"}, {"id": "1404", "n": "HIDRORELAXADORA"}, 
    {"id": "804", "n": "CALANDRA ALBRECHT"}, {"id": "803", "n": "CALANDRA LAFER"},
    {"id": "1602", "n": "COZINHA QUÍMICO"}, {"id": "59", "n": "HT 1324"},
    {"id": "701", "n": "ABRIDOR BIANCO"}, {"id": "1501", "n": "ABRIDOR BRASTEC 1"},
    {"id": "1502", "n": "ABRIDOR BRASTEC 2"}, {"id": "1503", "n": "ABRIDOR BRASTEC 3"}
]

# 4. Exibição Dinâmica
cols = st.columns(5)
for i, at in enumerate(ativos):
    # Localiza a última atualização pelo ID numérico
    pos = string_bruta.rfind(at['id']) 
    ctx = string_bruta[pos:pos+350] if pos != -1 else ""
    
    # Extração da descrição (Ex: RESETAR INVERSOR...)
    desc_real = ""
    if "DESC:" in ctx:
        desc_real = ctx.split("DESC:")[1].split("|")[0].strip()
    
    # Define visual baseado no status
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
