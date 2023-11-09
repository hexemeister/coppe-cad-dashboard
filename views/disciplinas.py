import streamlit as st
import plotly.express as px

def createPage(df, ano):
  st.empty()
  st.header("Disciplinas", divider='red', anchor=False)
  
  df = df.query("periodo_base == @ano")
  # st.dataframe(df['local'].unique(), use_container_width=True)

  df_curso_programa = df.groupby(by=['programa', 'curso']).size().reset_index(name='counts')

  # # Tipo de curso : ct.stc_curso (EG - Ensino de Graduação; EP e NULL - Ensino de Pós) ( por programa)
  vbar_chart = px.bar(
        df_curso_programa,
        title='Tipo de Curso por Programa',
        x='programa',
        y='counts',
        color='curso',
        orientation='v',
        text_auto=True,
        labels={'counts': 'Quantidade de Publicações', 'programa': 'Programa', 'curso': 'Nível'},
        color_discrete_sequence=px.colors.sequential.Reds_r,
        )
  st.plotly_chart(vbar_chart, theme="streamlit", use_container_width=True)


  # Local : ct.stv_local ( entende tudo like 'coppe' or NULL = COPPE) (por ct.stv_local)
  df_local_programa = df.groupby(by=['programa', 'local']).size().reset_index(name='counts')
  vbar_chart=px.bar(
          df_local_programa,
          title='Local por Tipo de Curso e Programa',
          x='programa',
          y='counts',
          color='local',
          orientation='v',
          text_auto=True,
          labels={'counts': 'Quantidade de Publicações', 'programa': 'Programa', 'curso': 'Veículo'},
          color_discrete_sequence=px.colors.sequential.Reds_r,
          )
  st.plotly_chart(vbar_chart, theme="streamlit", use_container_width=True)