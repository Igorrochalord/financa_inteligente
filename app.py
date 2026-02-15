import streamlit as st
from src.views import login, dashboard

# Configurações globais da página
st.set_page_config(
    page_title="Finança Inteligente 3.0",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def load_css():
    try:
        with open("assets/style.css") as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        pass

# Carrega Estilos
load_css()

# Gestão de Sessão
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['user'] = None

def main():
    if not st.session_state['logged_in']:
        login.show_login()
    else:
        # Botão de Logout na Sidebar
        with st.sidebar:
            st.write(f"Usuário: **{st.session_state['user']['username']}**")
            if st.button("Sair 🚪"):
                st.session_state['logged_in'] = False
                st.session_state['user'] = None
                st.rerun()
        
        # Renderiza Dashboard Principal
        dashboard.show_dashboard(st.session_state['user'])

if __name__ == "__main__":
    main()