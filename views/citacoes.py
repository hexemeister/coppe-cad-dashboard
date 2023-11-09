import streamlit as st
import plotly.express as px

def createPage(df, ano):
  st.empty()
  st.header("Citações", divider='red', anchor=False)

  df = df.query("periodo_base == @ano")
  # st.dataframe(df, use_container_width=True)

  df_total_programa = df.groupby(by='programa')['num_total'].sum().reset_index()

  # num_total = Citações e a quantidades de vezes buscado ( Google)

  # num_trabalho = Número de trabalho e o número de trabalhos que ele tem

  vbar_chart = px.bar(
        df_total_programa,
        title='Quantidade de Buscas no Google por Publicações de Programa',
        x='programa',
        y='num_total',
        # color='curso',
        orientation='v',
        text_auto=True,
        labels={'num_total': 'Quantidade de Citações', 'programa': 'Programas'},
        color_discrete_sequence=px.colors.sequential.Reds_r,
        )
  st.plotly_chart(vbar_chart, theme="streamlit", use_container_width=True)