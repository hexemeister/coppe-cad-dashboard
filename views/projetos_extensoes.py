import streamlit as st
import plotly.express as px

def createPage(df, ano):
  st.empty()

  st.header("Projetos de Extensões", divider='red', anchor=False)

  df = df.query("periodo_base == @ano")
  # st.dataframe(df, use_container_width=True)
  
  df_programa_counts = df.groupby(by=['programa']).size().reset_index(name='counts')

  vbar_chart = px.bar(
    df_programa_counts,
    title='Quantidade de Programas',
    x='programa',
    y='counts',
    # color='programa_projeto',
    orientation='v',
    text_auto=True,
    labels={'counts': 'Quantidade de Projetos', 'programa': 'Programas'},
    color_discrete_sequence=px.colors.sequential.Reds_r,
    )
  st.plotly_chart(vbar_chart, theme="streamlit", use_container_width=True)