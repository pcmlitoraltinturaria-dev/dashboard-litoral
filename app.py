# 3. Processamento de Status para o Placar
total, paradas, parciais = 0, 0, 0
lista_final = []

for setor_nome, ativos_setor in setores.items():
    for at in ativos_setor:
        total += 1
        pos = string_bruta.rfind(at['id'])
        status, cor, classe, s_nome = "NORMAL", "#2ecc71", "", "MANUTENÇÃO"
        
        if pos != -1:
            ctx = string_bruta[pos : pos + 80]
            if "CIVIL" in ctx: s_nome = "CIVIL"
            elif "ELETRICA" in ctx: s_nome = "ELÉTRICA"
            elif "MECANICA" in ctx: s_nome = "MECÂNICA"

            if "NORMAL" in ctx: 
                status, cor = "NORMAL", "#2ecc71"
            elif any(x in ctx for x in ["CIVIL", "PARCIAL", "MÁQ.PAR.PARCIAL"]):
                status, cor = "PARCIAL", "#f1c40f"
                parciais += 1
            elif "PARADA" in ctx:
                status, cor, classe = "PARADA", "#e74c3c", "blink-red"
                paradas += 1
        
        # Correção da Sintaxe Python para unir dicionários
        dados_atualizados = at.copy()
        dados_atualizados.update({
            "status": status, 
            "cor": cor, 
            "classe": classe, 
            "setor": setor_nome, 
            "s_nome": s_nome
        })
        lista_final.append(dados_atualizados)
