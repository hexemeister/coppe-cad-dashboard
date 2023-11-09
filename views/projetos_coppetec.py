import streamlit as st
import plotly.express as px

def createPage(df, ano):
  st.empty()
  st.header("Projetos Coppetec", divider='red', anchor=False)

  df = df.query("periodo_base == @ano")
  df_sigla_counts = df.groupby(by=['sigla', 'programa_projeto']).size().reset_index(name='counts')
  # st.dataframe(df, use_container_width=True)

  vbar_chart = px.bar(
    df_sigla_counts,
    title='Quantidade de siglas',
    x='sigla',
    y='counts',
    color='programa_projeto',
    orientation='v',
    text_auto=True,
    labels={'num_total': 'Quantidade de Citações', 'programa': 'Programas'},
    color_discrete_sequence=px.colors.sequential.Reds_r,
    )
  st.plotly_chart(vbar_chart, theme="streamlit", use_container_width=True)