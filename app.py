import streamlit as st

# Exemplo de como processar os dados (ajuste para a sua leitura de CSV)
def render_maquina_card(nome, os, status):
    status_limpo = str(status).strip().lower()
    
    # Lógica de Cores e Motivos
    if status_limpo in ['aberta', 'em execução']:
        cor = "#f1c40f"  # Amarelo
        texto_cor = "#2c3e50"
        motivo = f"🛠️ O.S. {os} {status}"
    elif status_limpo in ['finalizada', '', 'operando']:
        cor = "#2ecc71"  # Verde
        texto_cor = "white"
        motivo = "✅ Equipamento Operando"
    else:
        cor = "#e74c3c"  # Vermelho
        texto_cor = "white"
        motivo = "⚠️ Manutenção Corretiva"

    # HTML do Card
    card_html = f"""
    <div style="
        background-color: {cor};
        color: {texto_cor};
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    ">
        <h3 style="margin: 0; font-size: 1.2em;">{nome}</h3>
        <hr style="border: 0.5px solid rgba(255,255,255,0.3); margin: 10px 0;">
        <p style="margin: 0; font-size: 0.9em; font-weight: bold;">{motivo}</p>
    </div>
    """
    return st.markdown(card_html, unsafe_allow_html=True)

# --- EXECUÇÃO NO STREAMLIT ---
st.title("Painel de Manutenção")

# Exemplo com a Rama LK _1202
# Aqui você substituiria pela leitura do seu arquivo CSV
dados_exemplo = [
    {"nome": "Rama LK _1202", "os": "2548", "status": "Finalizada"},
    {"nome": "Tear Circular 01", "os": "2550", "status": "Em Execução"},
    {"nome": "Compressor Central", "os": "2551", "status": "Crítica"}
]

col1, col2, col3 = st.columns(3)

with col1:
    render_maquina_card("Rama LK _1202", "2548", "Finalizada")
with col2:
    render_maquina_card("Tear Circular 01", "2550", "Em Execução")
with col3:
    render_maquina_card("Compressor Central", "2551", "Crítica")
