import streamlit as st
import requests

# 1. Configuração de Layout e Estilo (Original Litoral)
st.set_page_config(page_title="Monitor de Manutenção", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    h1 {
        color: #4a5568;
        font-family: 'Arial Black', Gadget, sans-serif;
        border-bottom: 2px solid #2d3748;
        padding-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>MONITOR DE MANUTENÇÃO :: LITORAL</h1>", unsafe_allow_html=True)

# 2. Conexão com o Firebase
FIREBASE_URL = "https://dashboard-manutencao-ef55f-default-rtdb.firebaseio.com/manutencao.json"

def buscar_dados():
    try:
        response = requests.get(FIREBASE_URL)
        if response.status_code == 200:
            return str(response.json()).upper() if response.json() else ""
        return ""
    except:
        return ""

texto_sistema = buscar_dados()

# 3. Lista de Ativos conforme o sistema da fábrica
maquinas = [
    {"id": "1311", "nome": "2 - HT_1311"},
    {"id": "701", "nome": "25 - Abridor Bianco_701"},
    {"id": "1501", "nome": "26 - Abridor de malha Brastec 1_1501"},
    {"id": "1502", "nome": "27 - Abridor de malha Brastec 2_1502"},
    {"id": "1504", "nome": "28 - Abridor de malha Brastec 4_1504"},
    {"id": "26030", "nome": "29 - Secador de malha Hercules_26030"},
    {"id": "1503", "nome": "30 - Abridor de malha Brastec 3_1503"},
    {"id": "803", "nome": "31 - Calandra Lafer_803"},
    {"id": "804", "nome": "32 - Calandra Albrecht _804"},
    {"id": "9010", "nome": "33 - Embaladeira IBM_9010"},
    {"id": "10010", "nome": "34 - Felpadeira Lafer_10010"},
    {"id": "10020", "nome": "35 - Felpadeira Lafer_10020"},
    {"id": "14030", "nome": "36 - Hidro Albrecht HP-100_14030"},
    {"id": "14010", "nome": "37 - Hidro Tubula Indsteel 1_14010"},
    {"id": "12020", "nome": "39 - Rama LK _12020"},
    {"id": "12010", "nome": "40 - Rama Unitech_12010"},
    {"id": "13060", "nome": "44 - HT_13060"},
    {"id": "13140", "nome": "49 - HT_13140"},
    {"id": "13240", "nome": "59 - HT_13240"},
    {"id": "16010", "nome": "223 - COZINHA AUXILIAR DE CORANTE_16010"},
    {"id": "16020", "nome": "224 - COZINHA AUXILIAR DE QUIMICO_16020"},
    {"id": "1506", "nome": "235 - Abridor de malha Brastec 5_1506"},
    {"id": "14040", "nome": "329 - Hidrorelaxadora 14040"}
]

# 4. Exibição das Máquinas em Grid
cols = st.columns(5)  # Ajustado para 5 colunas para melhor visualização dos nomes longos

for i, mq in enumerate(maquinas):
    status = "NORMAL"
    cor = "#28a745"  # Verde
    
    # Lógica de busca no texto bruto do Firebase
    if texto_sistema and (mq['nome'].upper() in texto_sistema or mq['id'] in texto_sistema):
        pos = texto_sistema.find(mq['nome'].upper()) if mq['nome'].upper() in texto_sistema else texto_sistema.find(mq['id'])
        trecho = texto_sistema[pos:pos+200]
        
        if "MÁQUINA PARADA" in trecho:
            status = "PARADA"
            cor = "#dc3545"  # Vermelho
        elif "MÁQ.PAR.PARCIAL" in trecho:
            status = "PARCIAL"
            cor = "#ff8c00"  # Laranja (Dark Orange)

    with cols[i % 5]:
        st.markdown(f"""
            <div style="background-color:#1e2530; padding:15px; border-radius:10px; 
                        border-top: 8px solid {cor}; text-align:center; color:white; 
                        margin-bottom:15px; min-height:160px;">
                <p style="font-size:11px; color:#a0aec0; margin:0;">ID SISTEMA: {mq['id']}</p>
                <h4 style="margin:10px 0; font-size:14px; height:50px; display:flex; align-items:center; justify-content:center;">
                    {mq['nome']}
                </h4>
                <p style="font-size:18px; font-weight:bold; color:{cor}; margin:0;">{status}</p>
            </div>
        """, unsafe_allow_html=True)

# Botão de atualização manual
if st.button('🔄 ATUALIZAR STATUS AGORA'):
    st.rerun()
