import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
import os
from src.database import db
from src.api_client import get_stock_data, get_market_movers
from src.news import get_financial_news
from src.reports import generate_pdf

# --- [FUNÇÕES AUXILIARES] ---

def interleave_news(news_list):
    """Organiza as notícias intercalando as fontes (1 Poder, 1 CNN...)"""
    poder = [n for n in news_list if 'Poder' in n['source']]
    cnn = [n for n in news_list if 'CNN' in n['source']]
    final_list = []
    max_len = max(len(poder), len(cnn))
    for i in range(max_len):
        if i < len(poder): final_list.append(poder[i])
        if i < len(cnn): final_list.append(cnn[i])
    return final_list

def get_logo(source):
    """Busca o caminho dos arquivos locais na pasta assets/"""
    path = "assets/poder_5.svg" if 'Poder' in source else "assets/log-cnn-money.svg"
    return path if os.path.exists(path) else None

# --- [DASHBOARD] ---

def show_dashboard(user):
    # --- SIDEBAR (Configuração 2026) ---
    with st.sidebar:
        st.markdown(f"### 🚀 Finança Pro")
        st.write(f"Engenheiro: **{user['name']}**")
        st.divider()
        page = st.radio("Navegação", ["🏠 Principal", "📈 Mercado", "📰 Notícias"], label_visibility="collapsed")
        st.divider()
        # Ajuste de largura para versoes atuais do Streamlit
        if st.button("Sair do Sistema", type="secondary", use_container_width=True):
            st.session_state['logged_in'] = False
            st.rerun()

    # Conexões MongoDB
    trans_col = db.get_collection('transactions')
    port_col = db.get_collection('portfolio')
    
    # Cálculos Financeiros
    res = list(trans_col.aggregate([
        {"$match": {"username": user['username']}}, 
        {"$group": {"_id": "$tipo", "total": {"$sum": "$valor"}}}
    ]))
    rec = next((x['total'] for x in res if x['_id'] == 'Receita'), 0.0)
    des = next((x['total'] for x in res if x['_id'] == 'Despesa'), 0.0)
    saldo_total = (user.get('salario', 0.0) + rec) - des
    stocks = list(port_col.find({'username': user['username']}))

    # 🏠 TELA 1: PRINCIPAL (Visão Geral & Recomendações)
    if page == "🏠 Principal":
        st.title("Visão Geral")
        
        # --- [BLOCO 1: RECOMENDAÇÕES INTELIGENTES] ---
        if saldo_total > 100:
            st.success(f"💡 **Oportunidade de Aporte:** Você tem R$ {saldo_total:.2f} sobrando. Que tal analisar **MXRF11.SA** ou **ITSA4.SA**?")
        elif saldo_total < 0:
            st.error("🚨 **Atenção ao Saldo:** Seus gastos superaram sua renda. Evite novos aportes este mês.")

        # --- [BLOCO 2: MAIORES ALTAS E BAIXAS] ---
        st.subheader("📊 Movimentações do Dia (B3)")
        altas, baixas = get_market_movers()
        
        if altas is not None and baixas is not None:
            col_u, col_d = st.columns(2)
            with col_u:
                with st.container(border=True):
                    st.markdown("🚀 **Top Altas**")
                    for _, row in altas.iterrows():
                        st.write(f"**{row['Ativo']}**: :green[+{row['Variação (%)']}%] (R$ {row['Preço']})")
            with col_d:
                with st.container(border=True):
                    st.markdown("📉 **Top Baixas**")
                    for _, row in baixas.iterrows():
                        st.write(f"**{row['Ativo']}**: :red[{row['Variação (%)']}%] (R$ {row['Preço']})")

        st.divider()

        # Ações Rápidas
        c_btn1, c_btn2, _ = st.columns([2, 2, 4])
        with c_btn1:
            with st.popover("➕ Nova Renda"):
                with st.form("add_inc"):
                    v = st.number_input("Valor R$", min_value=0.0)
                    d = st.text_input("Origem")
                    if st.form_submit_button("Lançar", type="primary"):
                        trans_col.insert_one({'username': user['username'], 'valor': v, 'tipo': 'Receita', 'descricao': d, 'data': datetime.now()})
                        st.rerun()
        with c_btn2:
            if st.button("📄 Gerar Relatório", type="secondary", use_container_width=True):
                path = generate_pdf(user, saldo_total, rec, des, stocks)
                with open(path, "rb") as f:
                    st.download_button("Clique para Baixar", f, file_name="relatorio.pdf")

        # KPIs Principais
        st.write("")
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Saldo Líquido", f"R$ {saldo_total:,.2f}")
        k2.metric("Despesas", f"R$ {des:,.2f}", delta_color="inverse")
        inv_total = sum([s['qtd'] * s['preco_medio'] for s in stocks])
        k3.metric("Em Ações", f"R$ {inv_total:,.2f}")
        k4.metric("Salário Base", f"R$ {user.get('salario', 0):,.2f}")

        st.divider()
        
        # Conteúdo Inferior
        cl, cr = st.columns([2, 1])
        with cl:
            st.subheader("💼 Patrimônio Atual")
            t1, t2 = st.tabs(["Ativos", "Histórico"])
            with t1:
                if stocks:
                    st.dataframe(pd.DataFrame(stocks)[['ticker', 'qtd', 'preco_medio']], width="stretch", hide_index=True)
                else: st.info("Carteira vazia.")
            with t2:
                df_t = pd.DataFrame(list(trans_col.find({'username': user['username']}).limit(5).sort('data', -1)))
                if not df_t.empty:
                    df_t['data'] = pd.to_datetime(df_t['data']).dt.strftime('%d/%m %H:%M')
                    st.dataframe(df_t[['data', 'descricao', 'valor', 'tipo']], width="stretch", hide_index=True)

        with cr:
            st.subheader("📰 Radar")
            news = interleave_news(get_financial_news())
            for n in news[:3]:
                with st.container(border=True):
                    logo = get_logo(n['source'])
                    if logo: st.image(logo, width=70)
                    st.markdown(f"**[{n['title']}]({n['link']})**")

    # 📈 TELA 2: MERCADO (Negociação)
    elif page == "📈 Mercado":
        st.title("Negociação em Tempo Real")
        col_l, col_r = st.columns([1, 2])
        with col_l:
            with st.container(border=True):
                st.subheader("Boleta")
                with st.form("order"):
                    tik = st.text_input("Ticker (Ex: PETR4.SA)").upper()
                    q = st.number_input("Qtd", 1)
                    p = st.number_input("Preço", 0.01)
                    side = st.radio("Operação", ["Comprar", "Vender"], horizontal=True)
                    if st.form_submit_button("Executar Ordem", type="primary"):
                        total = q * p
                        if side == "Comprar":
                            if saldo_total >= total:
                                port_col.update_one({'username': user['username'], 'ticker': tik}, {'$inc': {'qtd': q}, '$set': {'preco_medio': p}}, upsert=True)
                                trans_col.insert_one({'username': user['username'], 'valor': total, 'tipo': 'Despesa', 'descricao': f'Compra {tik}', 'data': datetime.now()})
                                st.success("Ordem enviada!")
                                st.rerun()
                            else: st.error("Saldo insuficiente")
                        else:
                            exist = port_col.find_one({'username': user['username'], 'ticker': tik})
                            if exist and exist['qtd'] >= q:
                                port_col.update_one({'_id': exist['_id']}, {'$inc': {'qtd': -q}})
                                trans_col.insert_one({'username': user['username'], 'valor': total, 'tipo': 'Receita', 'descricao': f'Venda {tik}', 'data': datetime.now()})
                                st.rerun()

        with col_r:
            with st.container(border=True):
                s_tik = st.text_input("Visualizar Gráfico", "PETR4.SA").upper()
                h = get_stock_data(s_tik, "1mo")
                if h is not None:
                    fig = go.Figure(data=[go.Candlestick(x=h.index, open=h['open'], high=h['high'], low=h['low'], close=h['close'])])
                    fig.update_layout(height=400, template="none", margin=dict(l=0,r=0,t=0,b=0))
                    st.plotly_chart(fig, use_container_width=True)

    # 📰 TELA 3: NOTÍCIAS (Feed Intercalado)
    elif page == "📰 Notícias":
        st.title("Notícias do Mercado")
        news = interleave_news(get_financial_news())
        for n in news:
            with st.container(border=True):
                c1, c2 = st.columns([1, 4])
                with c1: 
                    if n.get('img'): st.image(n['img'], use_container_width=True)
                with c2:
                    logo = get_logo(n['source'])
                    if logo: st.image(logo, width=120)
                    st.markdown(f"### [{n['title']}]({n['link']})")