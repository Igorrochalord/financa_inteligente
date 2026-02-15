from yahooquery import Ticker
import pandas as pd
from datetime import datetime, timedelta
from src.database import db

def get_market_movers():
    """Busca as maiores altas e baixas com cache no MongoDB."""
    cache_col = db.get_collection('market_cache')
    cached_data = cache_col.find_one({"type": "market_movers"})
    
    if cached_data and (datetime.now() < cached_data.get('updated_at') + timedelta(minutes=15)):
        return pd.DataFrame(cached_data['altas']), pd.DataFrame(cached_data['baixas'])

    tickers_list = ["PETR4.SA", "VALE3.SA", "ITUB4.SA", "ABEV3.SA", "BBDC4.SA", "BBAS3.SA", "MGLU3.SA"]
    try:
        t = Ticker(tickers_list)
        data = t.price
        
        data_list = []
        for ticker in tickers_list:
            details = data.get(ticker, {})
            if isinstance(details, dict):
                current = details.get('regularMarketPrice')
                change = details.get('regularMarketChangePercent', 0) * 100
                
                if current:
                    data_list.append({
                        "Ativo": ticker.replace(".SA", ""),
                        "Preço": round(current, 2),
                        "Variação (%)": round(change, 2)
                    })
        
        if data_list:
            df = pd.DataFrame(data_list)
            altas = df.sort_values(by="Variação (%)", ascending=False).head(3)
            baixas = df.sort_values(by="Variação (%)", ascending=True).head(3)
            
            cache_col.update_one({"type": "market_movers"}, {"$set": {
                "altas": altas.to_dict('records'), "baixas": baixas.to_dict('records'), "updated_at": datetime.now()
            }}, upsert=True)
            return altas, baixas
    except:
        if cached_data: return pd.DataFrame(cached_data['altas']), pd.DataFrame(cached_data['baixas'])
    return None, None

def get_stock_data(ticker, period="1mo"):
    """Busca dados para o gráfico de velas (Candlestick)."""
    if not ticker.endswith(".SA"): ticker = f"{ticker}.SA"
    try:
        t = Ticker(ticker)
        hist = t.history(period=period)
        return hist if not hist.empty else None
    except:
        return None