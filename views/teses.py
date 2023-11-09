import streamlit as st
import plotly.express as px

def createPage(df, ano):
  st.empty()
  st.header("Teses", divider='red', anchor=False)

  df = df.query("periodo_base == @ano")
  # st.dataframe(df, use_container_width=True)

  df_teses_programa = df.groupby(by=['desc_programa', 'desc_curso']).size().reset_index(name='counts')
  
  vbar_chart = px.bar(
      df_teses_programa,
      title='Tipo de Teses por Programa',
      x='desc_programa',
      y='counts',
      color="desc_curso",
      barmode='overlay',
      orientation='v',
      # text_auto=True,
      labels={'counts': 'Quantidade de Teses', 'desc_programa': 'Programa', 'desc_curso': 'Tipo de Tese'},
      color_discrete_sequence=px.colors.sequential.Reds_r,
      # category_orders={"fruto":['Dissertação de Mestrado',
      #                      'Tese de Doutorado', 
      #                      'Pós Doutorado', 
      #                      'Trabalho Final de Curso', 
      #                      'Iniciação Científica']
      #                      }
      )
  
  st.plotly_chart(vbar_chart, theme="streamlit", use_container_width=True)
  
  
  # Local-defesa -> ctf.stv_local_defesa ( entende tudo like '*coppe*' = COPPE) (por programas)
  df_local_programa = df.groupby(by=['desc_programa', 'local_defesa']).size().reset_index(name='counts')
  
  vbar_chart = px.bar(
      df_local_programa,
      title='Local de Defesa por Programa',
      x='desc_programa',
      y='counts',
      color="local_defesa",
      barmode='overlay', text='counts',
      orientation='v',
      text_auto=True,
      labels={'counts': 'Quantidade de Teses', 'desc_programa': 'Programa', 'local_defesa': 'Local de Defesa'},
      color_discrete_sequence=px.colors.sequential.Reds_r,
      )
  
  st.plotly_chart(vbar_chart, theme="streamlit", use_container_width=True)