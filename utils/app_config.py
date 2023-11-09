import streamlit as st
from locale import setlocale, LC_ALL

def set_page_config():
  st.set_page_config(
    page_title="COPPE/CAD Dashboard",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="auto",
    # menu_items={
    #     'Get Help': 'https://www.extremelycoolapp.com/help',
    #     'Report a bug': "https://www.extremelycoolapp.com/bug",
    #     'About': "# This is a header. This is an *extremely* cool app!"
    # }
  )

setlocale(LC_ALL, 'pt_BR.UTF-8')

# Carrega estilos personalizados
def set_styles():
  with open ('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# set_page_config()