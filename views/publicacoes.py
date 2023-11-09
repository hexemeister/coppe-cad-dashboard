import streamlit as st
import plotly.express as px

def createPage(df, ano):
  st.empty()
  
  st.header("Publicações", divider='red', anchor=False)

  df_ano = df.query("ano_publicacao == @ano")
  
  # Seção de indicadores
  col_ind_1, col_ind_2, col_ind_3 = st.columns(3)

  total_artigos_anoselecionado = df_ano['coi_artigo'].count()
  total_artigos_anoanterior = df.query("ano_publicacao == @ano-1")['coi_artigo'].count()
  diferenca_qtd_artigos = total_artigos_anoselecionado - total_artigos_anoanterior

  col_ind_1.metric(
    f"Publicações em {ano}", 
    total_artigos_anoselecionado, 
    f"{diferenca_qtd_artigos}",
    help=f"Quantidade de Publicações publicados em {ano} e a diferença em relação à quantidade no ano anterior."
  )


  total_ri_anoselecionado = (df_ano['veiculo'] == 'REVISTA INTERNACIONAL').sum()
  total_ri_anoanterior = (
     df[['veiculo', 'ano_publicacao']]
     .query("ano_publicacao == @ano-1 & veiculo == 'REVISTA INTERNACIONAL'")['veiculo']
     .count()
  )
  diferenca_ri = total_ri_anoselecionado - total_ri_anoanterior

  col_ind_2.metric(
      f"RI em {ano}", 
      total_ri_anoselecionado, 
      f"{diferenca_ri}",
      help=f"Quantidade de Publicações publicados em {ano} e a diferença em relação à quantidade no ano anterior."
  )


  qt_autores_internacionais_anoselecionado = len(df_ano[df_ano
  ['autor_internacional']=='S'])
  qt_autores_inter_anoanterior = df[['autor_internacional', 'ano_publicacao']].query("ano_publicacao == @ano-1 & autor_internacional == 'S'")['autor_internacional'].count()
  diferenca_autores_inter = qt_autores_internacionais_anoselecionado - qt_autores_inter_anoanterior


  col_ind_3.metric(
      f"Autores Internacionais em {ano}", 
      len(df_ano[df_ano['autor_internacional']=='S']), 
      f"{diferenca_autores_inter}",
      help=f"Quantidade de Publicações publicados em {ano} e a taxa em relação ao ano anterior.",
  )

  dflang_artigo = df_ano[['idioma', 'coi_artigo']].groupby("idioma").count().sort_values(by="coi_artigo", ascending=False).reset_index()
  # total = len(df_ano)
  dfveiculo_artigo = df_ano[['veiculo', 'coi_artigo']].groupby("veiculo").count().reset_index()
  dfartigo_fruto = df_ano[['programa','fruto', 'coi_artigo']].groupby(["programa", 'fruto']).count().reset_index()


  # Seção de gráficos

  st.subheader("Gráficos")
  col1, col2 = st.columns(2)
  with col1:
    pie_chart = px.pie(
      dflang_artigo,
      title='Publicações por Idioma',
      values="coi_artigo",
      names="idioma",
      color_discrete_sequence=px.colors.sequential.Reds_r
    ).update_layout(title_x=0.27)

    st.plotly_chart(pie_chart, theme="streamlit", use_container_width=True)

  with col2:
    pie_chart = px.pie (
      dfveiculo_artigo,
      title="Publicações por Tipo de veículo",
      values="coi_artigo",
      names="veiculo",
      color_discrete_sequence=px.colors.sequential.Reds_r
    ).update_layout(title_x=0.17)
    st.plotly_chart(pie_chart, theme="streamlit", use_container_width=True)

    df_prog_veiculo = (
      df_ano[['veiculo', 'coi_artigo', 'programa']]
      .groupby(['veiculo', 'programa']).count()
      .sort_values(by="coi_artigo", ascending=False).reset_index()
    )

  hbar_chart = px.bar (
    df_prog_veiculo,
    title="Publicações por Programa e Tipo de veículo",
    x='coi_artigo',
    y='programa',
    color="veiculo",
    orientation='h',
    text_auto=True,
    labels={'coi_artigo': 'Quantidade de Publicações', 'programa': 'Programa', 'veiculo': 'Veículo'},
    color_discrete_sequence=px.colors.sequential.Reds_r,
  )
  st.plotly_chart(hbar_chart, theme="streamlit", use_container_width=True)

  vbar_chart=px.bar(
      dfartigo_fruto,
      title='Publicações por Programa e Origem',
      x='programa',
      y='coi_artigo',
      color="fruto",
      orientation='v',
      text_auto=True,
      labels={'coi_artigo': 'Quantidade de Publicações', 'programa': 'Programa', 'veiculo': 'Veículo', 'fruto': 'Origem'},
      color_discrete_sequence=px.colors.sequential.Reds_r,
      category_orders={"fruto":['Dissertação de Mestrado',
                           'Tese de Doutorado', 
                           'Pós Doutorado', 
                           'Trabalho Final de Curso', 
                           'Iniciação Científica']
                           }
  )
  st.plotly_chart(vbar_chart, theme="streamlit", use_container_width=True)

  return True