# --- LÓGICA DE DECISÃO DE CORES ---
for at in ativos:
    pos = string_bruta.rfind(at['id'])
    
    # REGRA DE OURO: O padrão é sempre VERDE (Normal)
    status, cor, classe, icon, servico = "NORMAL", "#2ecc71", "border-normal", "✅", "EM OPERAÇÃO"
    
    if pos != -1:
        # Analisamos apenas as informações próximas ao ID da máquina no texto
        ctx = string_bruta[pos : pos + 350]
        
        # 1. Só fica VERMELHO se o texto disser explicitamente "MÁQUINA PARADA"
        if "MÁQUINA PARADA" in ctx:
            status, cor, classe, icon, servico = "PARADA", "#ff0000", "border-parada", "🛑", "CORRETIVA"
        
        # 2. Só fica LARANJA se o texto disser explicitamente "MÁQ.PAR.PARCIAL"
        elif "MÁQ.PAR.PARCIAL" in ctx:
            status, cor, classe, icon, servico = "AVISO", "#ff8c00", "farol-aviso", "⚠️", "PARCIAL"
            
        # 3. Caso contrário (como o Químico 1602 que é "Normal"), cai no padrão VERDE.
