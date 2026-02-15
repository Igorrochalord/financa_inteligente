import pandas as pd
import plotly.express as px

def get_fire_stats(patrimonio, aporte, gasto_mensal, taxa_anual=0.08):
    """Calcula a meta FIRE: $$Meta = (Gasto \times 12) \times 25$$"""
    meta_fire = (gasto_mensal * 12) * 25
    taxa_mensal = (1 + taxa_anual)**(1/12) - 1
    
    meses = 0
    saldo = patrimonio
    while saldo < meta_fire and meses < 600:
        saldo = saldo * (1 + taxa_mensal) + aporte
        meses += 1
    
    return {"meta": meta_fire, "anos": round(meses/12, 1), "progresso": min(patrimonio/meta_fire, 1.0)}

def get_projection_data(patrimonio, aporte, meses_proj, taxa_anual=0.10):
    taxa_mensal = (1 + taxa_anual)**(1/12) - 1
    dados = []
    saldo = patrimonio
    for m in range(meses_proj + 1):
        dados.append({"Mês": m, "Patrimônio": round(saldo, 2)})
        saldo = saldo * (1 + taxa_mensal) + aporte
    return pd.DataFrame(dados)