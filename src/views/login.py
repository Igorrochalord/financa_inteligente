import streamlit as st
from src.auth import login_user, register_user

def show_login():
    # Centralização usando colunas
    col_l, col_main, col_r = st.columns([1, 1.5, 1])
    
    with col_main:
        # Espaçamento vertical
        st.write("") 
        st.write("") 
        
        # Container com borda para destacar o login
        with st.container(border=True):
            st.markdown("<h1 style='text-align: center;'>🚀 Finança Pro</h1>", unsafe_allow_html=True)
            st.caption("Gestão Inteligente de Ativos e Renda")
            
            tab_login, tab_registro = st.tabs(["Acessar Conta", "Criar Nova Conta"])
            
            # --- TAB LOGIN ---
            with tab_login:
                st.write("")
                user = st.text_input("Usuário", placeholder="Digite seu usuário", key="log_u")
                pwd = st.text_input("Senha", type="password", placeholder="Digite sua senha", key="log_p")
                
                st.write("")
                if st.button("Entrar no Sistema", type="primary", use_container_width=True):
                    u = login_user(user, pwd)
                    if u:
                        st.session_state['logged_in'] = True
                        st.session_state['user'] = u
                        st.rerun()
                    else:
                        st.error("Credenciais inválidas.")

            # --- TAB REGISTRO ---
            with tab_registro:
                st.write("")
                new_u = st.text_input("Escolha um Usuário", key="reg_u")
                new_p = st.text_input("Escolha uma Senha", type="password", key="reg_p")
                new_n = st.text_input("Nome Completo", key="reg_n")
                new_s = st.number_input("Salário Mensal (R$)", min_value=0.0, step=100.0, key="reg_s")
                
                st.write("")
                if st.button("Cadastrar e Entrar", type="secondary", use_container_width=True):
                    user_created, msg = register_user(new_u, new_p, new_n, new_s)
                    if user_created:
                        st.success("Conta criada!")
                        st.session_state['logged_in'] = True
                        st.session_state['user'] = user_created
                        st.rerun()
                    else:
                        st.error(msg)