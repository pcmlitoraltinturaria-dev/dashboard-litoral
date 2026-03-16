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

# 2. Conexão com o Banco de Dados (Firebase)
FIREBASE_URL = "https://dashboard-manutencao-ef55f-default-rtdb.firebaseio.com/manutencao.json"

def buscar_dados():
    try:
        res = requests.get(FIREBASE_URL)
        return str(res.json()).upper() if res.json() else ""
    except:
        return ""

texto_sistema = buscar_dados()

# 3. Lista Completa de Máquinas (IDs e Nomes Conforme solicitado)
maquinas = [
    {"id": "701", "nome": "ABRIDOR BIANCO"},
    {"id": "1501", "nome": "ABRIDOR BRASTEC 1"},
    {"id": "1502", "nome": "ABRIDOR BRASTEC 2"},
    {"id": "1503", "nome": "ABRIDOR BRASTEC 3"},
    {"id": "1504", "nome": "ABRIDOR BRASTEC 4"},
    {"id": "1506", "nome": "ABRIDOR BRASTEC 5"},
    {"id": "804", "nome": "CALANDRA ALBRECHT"},
    {"id": "803", "nome": "CALANDRA LAFER"},
    {"id": "1202", "nome": "RAMA LK"},
    {"id": "1201", "nome": "RAMA UNITECH"},
    {"id": "1404", "nome": "HIDRORELAXADORA"},
    {"id": "1403", "nome": "HIDRO ALBRECHT"},
    {"id": "1401", "nome": "HIDRO INDSTEEL"},
    {"id": "59", "nome": "HT 1324"},
    {"id": "1306", "nome": "HT 1306"},
    {"id": "1311", "nome": "HT 1311"},
    {"id": "1314", "nome": "HT 1314"},
    {"id": "1601", "nome": "COZINHA CORANTE"},
    {"id": "1602", "nome": "COZINHA QUIMICO"},
    {"id": "1001", "nome": "FELPADEIRA 1"},
    {"id": "1002", "nome": "FELPADEIRA 2"},
    {"id": "901", "nome": "EMBALADEIRA IBM"},
    {"id": "2603", "nome": "SECADOR HERCULES"},
    {"id": "26", "nome": "EMPILHADEIRA 26"}
]

# 4. Criação do Painel de Cards (Grid)
cols = st.columns(6)

for i, mq in enumerate(maquinas):
    status = "NORMAL"
    cor_borda = "#28a745" # Verde (Padrão)
    
    if texto_sistema:
        # Busca pelo Nome ou ID no texto bruto
        if mq['nome'] in texto_sistema or mq['id'] in texto_sistema:
            # Pega um trecho de 150 caracteres após o nome da máquina para ver o status dela
            pos = texto_sistema.find(mq['nome']) if mq['nome'] in texto_sistema else texto_sistema.find(mq['id'])
            contexto = texto_sistema[pos:pos+150]
            
            if "MÁQUINA PARADA" in contexto:
                status = "PARADA"
                cor_borda = "#dc3545" # Vermelho
            elif "MÁQ.PAR.PARCIAL" in contexto:
                status = "PARCIAL"
                cor_borda = "#ff8c00" # Laranja

    with cols[i % 6]:
        st.markdown(f"""
            <div style="background-color:#1e2530; padding:12px; border-radius:8px; 
                        border-top: 6px solid {cor_borda}; text-align:center; 
                        color:white; margin-bottom:12px; min-height: 130px;">
                <p style="font-size:10px; color:#a0aec0; margin:0;">ID {mq['id']}</p>
                <h4 style="margin:8px 0; font-size:13px; height:35px; overflow:hidden;">{mq['nome']}</h4>
                <p style="font-size:15px; font-weight:bold; color:{cor_borda}; margin:0;">{status}</p>
            </div>
        """, unsafe_allow_html=True)

# Rodapé com botão de atualização
st.write("---")
if st.button('🔄 ATUALIZAR STATUS AGORA'):
    st.rerun()
