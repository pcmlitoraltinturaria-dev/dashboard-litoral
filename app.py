import streamlit as st
import requests

# 1. Configuração de Layout e Estilo Litoral
st.set_page_config(page_title="Monitor Litoral", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .card {
        background-color: #1f2937;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        margin-bottom: 8px;
        min-height: 140px; 
        border-top: 6px solid;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
    }
    .maquina-id { color: #9ca3af; font-size: 0.6em; text-transform: uppercase; margin-bottom: 2px; }
    .maquina-nome { color: #9ca3af; font-weight: bold; font-size: 0.85em; margin-bottom: 5px; text-transform: uppercase; }
    .status-texto { font-weight: bold; font-size: 1.1em; text-transform: uppercase; margin-bottom: 2px; }
    
    .texto-destaque { 
        color: #FFFFFF !important; 
        font-weight: bold; 
        font-size: 0.85em; 
        text-transform: uppercase; 
        line-height: 1.2;
        margin-top: 6px;
        display: block;
    }
    
    .status-normal-container {
        margin-top: 5px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 4px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Busca de Dados
def buscar_dados():
    try:
        r = requests.get("https://dashboard-manutencao-ef55f-default-rtdb.firebaseio.com/manutencao.json")
        return r.text.upper()
    except: return ""

string_bruta = buscar_dados()

# 3. Lista de Ativos (21 Máquinas)
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

# 4. Exibição com Lógica de Captura Final
cols = st.columns(5)
for i, at in enumerate(ativos):
    # Busca pela última ocorrência do ID
    pos = string_bruta.rfind(f'"{at["id"]}"')
    if pos == -1: pos = string_bruta.rfind(at['id'])
    
    ctx = string_bruta[pos:pos+500] if pos != -1 else ""
    
    # LÓGICA DE CAPTURA DA DESCRIÇÃO FINAL:
    # Como a descrição é a última parte antes do fechamento do registro (normalmente uma aspa ou barra)
    desc_real = ""
    if "MÁQUINA PARADA" in ctx or "ABERTA" in ctx:
        # Tenta quebrar a string por palavras-chave que vêm antes da descrição final
        # Exemplo: NARCISO FLORENCIO[DESCRICAO]
        partes = ctx.split("CONSERTO") # "CONSERTO" costuma vir antes do nome e da descrição
        if len(partes) > 1:
            # Pega a parte após "CONSERTO", remove o nome do técnico (opcional) e limpa
            sujo = partes[1].split('"')[0].strip()
            # Remove números iniciais que sobraram do fatiamento e pega o texto final
            desc_real = "".join([c for c in sujo if not c.isdigit()]).strip()
            # Se ainda houver o nome do técnico grudado, aqui ele busca a descrição real:
            # (Ajuste manual simples: pega as últimas palavras)
            palavras = desc_real.split()
            if len(palavras) > 2:
                desc_real = " ".join(palavras[2:]) # Pula o Nome/Sobrenome do técnico

    # Fallback caso a lógica acima falhe em algum formato novo
    if not desc_real and "DESC:" in ctx:
        desc_real = ctx.split("DESC:")[1].split("|")[0].split('"')[0].strip()

    # Renderização
    if "MÁQUINA PARADA" in ctx:
        cor, lbl = "#e74c3c", "PARADA"
        info = f"<div class='texto-destaque'>{desc_real}</div>"
    elif "ABERTA" in ctx or "EXECUÇÃO" in ctx:
        cor, lbl = "#f1c40f", "ATENÇÃO"
        info = f"<div class='texto-destaque'>{desc_real}</div>"
    else:
        cor, lbl = "#2ecc71", "NORMAL"
        info = "<div class='status-normal-container'><span style='color:#2ecc71'>✅</span><span class='texto-destaque'>OPERANDO</span></div>"

    with cols[i % 5]:
        st.markdown(f"""
            <div class="card" style="border-top-color: {cor};">
                <div class="maquina-id">ID: {at['id']}</div>
                <div class="maquina-nome">{at['n']}</div>
                <div class="status-texto" style="color: {cor};">{lbl}</div>
                {info}
            </div>
        """, unsafe_allow_html=True)
