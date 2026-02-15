import requests
from bs4 import BeautifulSoup
import streamlit as st

@st.cache_data(ttl=600)
def get_financial_news():
    news_list = []
    
    # Headers completos para evitar bloqueio
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Referer": "https://www.google.com/"
    }
    
    default_img = "https://via.placeholder.com/300x200.png?text=Noticia"

    # --- 1. CNN BRASIL (Baseado no seu HTML: <figure class="group ...">) ---
    try:
        url = "https://www.cnnbrasil.com.br/economia/macroeconomia/"
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Busca cada bloco de notícia
            items = soup.find_all('figure', class_='group')
            
            for item in items:
                # Título está no h3
                title_tag = item.find('h3')
                if not title_tag: continue
                title = title_tag.get_text().strip()
                
                # Link está no 'a' pai do h3 ou da imagem
                link_tag = item.find('a', href=True)
                link = link_tag['href'] if link_tag else '#'
                
                # Imagem
                img_tag = item.find('img')
                img_src = default_img
                if img_tag:
                    # Tenta pegar src. Se não tiver, tenta data-src
                    img_src = img_tag.get('src') or img_tag.get('data-src') or default_img
                
                if len(title) > 5:
                    news_list.append({
                        'source': 'CNN Money',
                        'title': title,
                        'link': link,
                        'img': img_src
                    })
    except Exception as e:
        print(f"Erro CNN: {e}")

    # --- 2. PODER360 (Baseado no seu HTML: <div class="box-news-list__news ...">) ---
    try:
        url = "https://www.poder360.com.br/poder-economia/"
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Busca os blocos específicos
            articles = soup.find_all('div', class_='box-news-list__news')
            
            for article in articles:
                # Título está no h2 com a classe subhead
                title_tag = article.find('h2', class_='box-news-list__subhead')
                if not title_tag: continue
                
                title = title_tag.get_text().strip()
                
                # Link dentro do h2
                link_tag = title_tag.find('a')
                link = link_tag['href'] if link_tag else '#'
                
                # Imagem
                img_tag = article.find('img')
                img_src = default_img
                if img_tag:
                    # Poder360 usa srcset. Vamos pegar a melhor resolução (última do split) ou o src normal
                    if img_tag.get('src'):
                        img_src = img_tag['src']
                    elif img_tag.get('srcset'):
                        # Ex: "url-pq 195w, url-gr 405w" -> pega o url-gr
                        srcs = img_tag['srcset'].split(',')
                        if srcs:
                            # Pega a parte da URL do último item (maior qualidade)
                            img_src = srcs[-1].strip().split(' ')[0]

                if len(title) > 5:
                    news_list.append({
                        'source': 'Poder360',
                        'title': title,
                        'link': link,
                        'img': img_src
                    })
    except Exception as e:
        print(f"Erro Poder360: {e}")

    return news_list