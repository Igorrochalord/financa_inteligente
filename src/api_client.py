import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from src.database import db

def get_market_movers():
    """
    Busca as maiores altas/baixas com cache persistente no MongoDB.
    """
    cache_col = db.get_collection('market_cache')
    
    # 1. Tenta buscar o cache no banco
    cached_data = cache_col.find_one({"type": "market_movers"})
    
    # 2. Verifica se o cache existe e se tem menos de 15 minutos (900 segundos)
    if cached_data:
        updated_at = cached_data.get('updated_at')
        if datetime.now() < updated_at + timedelta(minutes=15):
            # Retorna os dados convertendo de volta para DataFrame
            altas = pd.DataFrame(cached_data['altas'])
            baixas = pd.DataFrame(cached_data['baixas'])
            return altas, baixas

    # 3. Se não houver cache ou estiver expirado, consulta a API
    tickers = ["PETR4.SA", "VALE3.SA", "ITUB4.SA", "ABEV3.SA", "BBDC4.SA", 
               "BBAS3.SA", "MGLU3.SA", "WEGE3.SA", "HAPV3.SA", "RENT3.SA"]
    
    data_list = []
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            current = info.get('currentPrice')
            prev_close = info.get('previousClose')
            
            if current and prev_close:
                change = ((current - prev_close) / prev_close) * 100
                data_list.append({
                    "Ativo": ticker.replace(".SA", ""),
                    "Preço": current,
                    "Variação (%)": round(change, 2)
                })
        except:
            continue
    
    df = pd.DataFrame(data_list)
    if not df.empty:
        altas = df.sort_values(by="Variação (%)", ascending=False).head(3)
        baixas = df.sort_values(by="Variação (%)", ascending=True).head(3)
        
        # 4. Salva/Atualiza o cache no MongoDB para a próxima requisição
        cache_col.update_one(
            {"type": "market_movers"},
            {"$set": {
                "altas": altas.to_dict('records'),
                "baixas": baixas.to_dict('records'),
                "updated_at": datetime.now()
            }},
            upsert=True
        )
        return altas, baixas
        
    return None, None

def get_stock_data(ticker, period="1mo"):
    """Mantém a função de busca de gráficos candlestick."""
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)
        return (hist, stock.info) if not hist.empty else (None, None)
    except:
        return None, None