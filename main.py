import streamlit as st
from streamlit_option_menu import option_menu

from utils import app_config
app_config.set_page_config()
app_config.set_styles()

from views import (publicacoes, 
                   teses,
                   disciplinas,
                   citacoes,
                   projetos_coppetec,
                   projetos_extensoes)
from utils.datafetch import *


st.title(":bar_chart: COPPE/CAD Dashboard")

menu_itens = ["Publicações", "Teses", "Disciplinas", "Citações", "Projetos Coppetec", "Projetos de Extensões"]

with st.sidebar:
    logo_col1, logo_col2 = st.columns(2)
    logo_col1.markdown(
      '<a href="https://www.coppe.ufrj.br/" target="_blank"><img src="app/static/coppe-white.png" class="logocoppe img-fluid" alt="Logotipo da COPPE"></a>', unsafe_allow_html=True
      )
    logo_col2.markdown(
      '<a href="https://cad.coppe.ufrj.br/" target="_blank"><img src="app/static/logo_cad.png" class="logocad img-fluid" alt="Logotipo da CAD"></a>', unsafe_allow_html=True
      )
    
    st.divider()

    st.subheader("Seleção de Filtros")

    ano_selecao_dropdown = st.empty()
    drop_disciplinas = st.empty()
    drop_teses = st.empty()
    
    st.session_state.dropdown_value = ano_selecao_dropdown.selectbox(
      "Selecione o ano",
      sorted(list(df_publicacoes["ano_publicacao"].unique()), reverse=True)
    )
    
    st.divider()

    item_selected = option_menu(
      menu_title = "Menu",  # required
      options = menu_itens,  # required
      icons = None,  # optional
      # menu_icon = "menu-down",  # optional
      default_index = 0,  # optional
      styles={
        "nav-link-selected": {"background-color": "#822433"},
        "nav-link": {"--hover-color": "#822443"},
        }
    )
    if item_selected == "Teses":
      ano_selecao_dropdown.empty()
      st.session_state.dropdown_value = drop_teses.selectbox(
          "Selecione o período", list(df_teses['periodo_base'].unique()[::-1])
          )
    if item_selected == "Disciplinas":
      ano_selecao_dropdown.empty()
      st.session_state.dropdown_value = drop_disciplinas.selectbox(
          "Selecione o período", list(df_disciplinas["periodo_base"].unique()[::-1])
          )
    if item_selected == "Citações":
      ano_selecao_dropdown.empty()
      st.session_state.dropdown_value = drop_disciplinas.selectbox(
          "Selecione o período", list(df_citacoes["periodo_base"].unique()[::-1])
          )
    if item_selected == "Projetos Coppetec":
      ano_selecao_dropdown.empty()
      st.session_state.dropdown_value = drop_disciplinas.selectbox(
          "Selecione o período", list(df_proj_coppetec["periodo_base"].unique()[::-1])
          )
    if item_selected == "Projetos de Extensões":
      ano_selecao_dropdown.empty()
      st.session_state.dropdown_value = drop_disciplinas.selectbox(
          "Selecione o período", list(df_proj_extensoes["periodo_base"].unique()[::-1])
          )


if item_selected == "Publicações":
    publicacoes.createPage(df_publicacoes, ano=st.session_state.dropdown_value)
if item_selected == "Teses":
    teses.createPage(df_teses, ano=st.session_state.dropdown_value)
if item_selected == "Disciplinas":
    disciplinas.createPage(df_disciplinas, ano=st.session_state.dropdown_value)
if item_selected == "Citações":
    citacoes.createPage(df_citacoes, ano=st.session_state.dropdown_value)
if item_selected == "Projetos Coppetec":
    projetos_coppetec.createPage(df_proj_coppetec, ano=st.session_state.dropdown_value)
if item_selected == "Projetos de Extensões":
    projetos_extensoes.createPage(df_proj_extensoes, ano=st.session_state.dropdown_value)

st.divider()
st.markdown("###### :gray[Copyright® 2023 - Todos os direitos reservados ao [CISI](https://www.cisi.coppe.ufrj.br/) - [Coppe](https://www.coppe.ufrj.br/)/[UFRJ](https://ufrj.br/).]")
