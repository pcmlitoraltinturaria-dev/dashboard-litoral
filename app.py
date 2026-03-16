import streamlit as st
import requests
import unicodedata

# 1. Configuração de Layout
st.set_page_config(page_title="Monitor de Manutenção", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    h1 { color: #4a5568; font-family: 'Arial Black'; border-bottom: 2px solid #2d3748; padding-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>MONITOR DE MANUTENÇÃO :: LITORAL</h1>", unsafe_allow_html=True)

FIREBASE_URL = "https://dashboard-manutencao-ef55f-default-rtdb.firebaseio.com/manutencao.json"

def buscar_dados():
    try:
        response = requests.get(FIREBASE_URL)
        if response.status_code == 200:
            texto = str(response.json())
            # Remove acentos
            texto = "".join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
            return texto.upper()
        return ""
    except:
        return ""

texto_sistema = buscar_dados()

# 3. LISTA OTIMIZADA
maquinas = [
    {"id": "1311", "exibicao": "2 - HT_1311", "busca": "1311"},
    {"id": "701", "exibicao": "25 - Abridor Bianco_701", "busca": "701"},
    {"id": "1501", "exibicao": "26 - Abridor de malha Brastec 1_1501", "busca": "1501"},
    {"id": "1502", "exibicao": "27 - Abridor de malha Brastec 2_1502", "busca": "1502"},
    {"id": "1504", "exibicao": "28 - Abridor de malha Brastec 4_1504", "busca": "1504"},
    {"id": "2603", "exibicao": "29 - Secador de malha Hercules_26030", "busca": "2603"},
    {"id": "1503", "exibicao": "30 - Abridor de malha Brastec 3_1503", "busca": "1503"},
    {"id": "803", "exibicao": "31 - Calandra Lafer_803", "busca": "803"},
    {"id": "804", "exibicao": "32 - Calandra Albrecht _804", "busca": "804"},
    {"id": "901", "exibicao": "33 - Embaladeira IBM_9010", "busca": "901"},
    {"id": "1001", "exibicao": "34 - Felpadeira Lafer_10010", "busca": "1001"},
    {"id": "1002", "exibicao": "35 - Felpadeira Lafer_10020", "busca": "1002"},
    {"id": "1403", "exibicao": "36 - Hidro Albrecht HP-100_14030", "busca": "1403"},
    {"id": "1401", "exibicao": "37 - Hidro Tubula Indsteel 1_14010", "busca": "1401"},
    {"id": "1202", "exibicao": "39 - Rama LK _12020", "busca": "1202"},
    {"id": "1201", "exibicao": "40 - Rama Unitech_12010", "busca": "1201"},
    {"id": "1306", "exibicao": "44 - HT_13060", "busca": "1306"},
    {"id": "1314", "exibicao": "49 - HT_13140", "busca": "1314"},
    {"id": "1324", "exibicao": "59 - HT_13240", "busca": "1324"},
    {"id": "1601", "exibicao": "223 - COZINHA AUXILIAR DE CORANTE_16010", "busca": "1601"},
    {"id": "1602", "exibicao": "224 - COZINHA AUXILIAR DE QUIMICO_16020", "busca": "1602"},
    {"id": "1506", "exibicao": "235 - Abridor de malha Brastec 5_1506", "busca": "1506"},
    {"id": "1404", "exibicao": "329 - Hidrorelaxadora 14040", "busca": "1404"}
]

cols = st.columns(5)
for i, mq in enumerate(maquinas):
    status, cor = "NORMAL", "#28a745"
    
    if texto_sistema and mq['busca'] in texto_sistema:
        pos = texto_sistema.find(mq['busca'])
        trecho = texto_sistema[pos:pos+300]
        
        if "MAQUINA PARADA" in trecho:
            status, cor = "PARADA", "#dc3545"
        elif "MAQ.PAR.PARCIAL" in trecho:
            status, cor = "PARCIAL", "#ff8c00"

    with cols[i % 5]:
        st.markdown(f"""
            <div style="background-color:#1e2530; padding:15px; border-radius:10px; 
                        border-top: 8px solid {cor}; text-align:center; color:white; 
                        margin-bottom:15px; min-height:160px;">
                <p style="font-size:11px; color:#a0aec0; margin:0;">BUSCA ID: {mq['busca']}</p>
                <h4 style="margin:10px 0; font-size:14px; height:50px; display:flex; align-items:center; justify-content:center;">
                    {mq['exibicao']}
                </h4>
                <p style="font-size:18px; font-weight:bold; color:{cor}; margin:0;">{status}</p>
            </div>
            """, unsafe_allow_html=True)

if st.button('🔄 ATUALIZAR STATUS'):
    st.rerun()
