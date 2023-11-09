import streamlit as st
import pandas as pd

# Conexão com o banco

@st.cache_resource()
def db_connect():
  return st.experimental_connection('producao', type='sql')

# Datafetching - Publicações

@st.cache_data(hash_funcs={db_connect: id})
def load_data_publicacoes(_conn):
  data = _conn.query("""
    select distinct (a.coi_artigo), a.stv_idioma, a.stc_procedencia, a.stc_autor_internacional as autor_internacional, year(p.dat_inicio) as ano_publicacao, ctv.stv_descricao as veiculo, ctv.stc_sigla as sigla_veiculo, ctp.coi_tpesquisa, ctp.stv_descricao as tipo_pesquisa, crc.stc_peso,crc.stv_descricao as peso, gp.stv_descricao as programa
    from cad_artigos a
    left join cad_periodos p on p.coi_indice = a.coi_periodo
    left join cad_tipo_veiculos ctv on ctv.coi_veiculo = a.coi_veiculo_avaliado
    left join cad_tipo_pesquisa ctp on ctp.coi_tpesquisa = a.coi_tipo_pesquisa
    left join cad_ranking_coppe crc on crc.coi_ranking = a.coi_ranking
    left join cad_autores ca on ca.coi_artigo = a.coi_artigo
    left join view_cad_usuario vcu on vcu.cos_matricula_cad = ca.cos_docente
    left join coppe11.gbl_programas gp on gp.cos_programa = vcu.cos_programa
    left join cad_categoria cc on cc.coi_categoria = vcu.coi_categoria
    where stc_situacao = 'Avaliado'
    and a.coi_veiculo_avaliado <> ''
    # and a.coi_veiculo_avaliado = 1
  """, ttl=600)
  return data

@st.cache_data(hash_funcs={db_connect: id})
def organize_data_publicacoes(df):
  # garantindo os nomes das colunas
  df.rename(columns={
    'stv_idioma': 'idioma', 'stc_procedencia': 'fruto', 'stc_autor_internacional': 'autor_internacional', 'year(p.dat_inicio)': 'ano_publicacao', 'stv_descricao': 'veiculo', 'stc_sigla': 'sigla_veiculo', 'coi_tpesquisa': 'coi_tpesquisa', 'stv_descricao': 'tipo_pesquisa', 'stv_descricao': 'peso', 'stv_descricao': 'programa', 'coi_perfil': 'perfil', 'stv_nome': 'docente', 'stc_cargo': 'cargo'
  }, inplace=True)
  # normalizando dados: remove nulls e dados inválidos, padroniza capital case
  df['idioma'] = df['idioma'].fillna('').str.capitalize().str.strip().str.replace('N/a', '')
  # Substitui dados com erros de digitação
  replace_words_ingles = ['Ingles', 'Inglés']
  replace_words_port = ['Portugues']
  valid_languages = ("Inglês", "Português", "Francês", "Espanhol", "Italiano", "Alemão", "Bretão", "Russo", "Polonês", "Chinês")
  df['idioma'] = (df['idioma']
                  .replace(dict.fromkeys(replace_words_ingles, 'Inglês'))
                  .replace(dict.fromkeys(replace_words_port, 'Português'))
                  )
  # Substitui todos os dados inválidos na coluna idioma e classifica como Não informado
  df['idioma'] = ['Não informado' if idioma not in valid_languages else idioma for idioma in df['idioma']]
  # Substitui todos os dados inválidos na coluna fruto e classifica como Outros
  invalid_values_fruto = ['', None]
  df['fruto'] = df['fruto'].replace(dict.fromkeys(invalid_values_fruto, 'Outros'))
  df['fruto'] = df['fruto'].replace({
                  'DM': 'Dissertação de Mestrado', 
                  'TD': 'Tese de Doutorado', 
                  'PD': 'Pós Doutorado', 
                  'FC': 'Trabalho Final de Curso', 
                  'IC': 'Iniciação Científica'
                  })
  # Junto todos os congressos em ANAIS DE CONGRESSO
  normalized_terms = ['CONGRESSOS INTERNACIONAIS', 'CONGRESSOS NACIONAIS']
  df['veiculo'] = df['veiculo'].replace(dict.fromkeys(normalized_terms, 'ANAIS DE CONGRESSO'))
  return df

df_publicacoes = organize_data_publicacoes(load_data_publicacoes(db_connect()))

# TESES

@st.cache_data(hash_funcs={db_connect: id})
def load_data_teses(_conn):
  data = _conn.query("""
    select p.stc_periodobase, ctf.stv_titulo, ctf.stv_autor, ctf.dat_defesa, ctf.stv_local_defesa, ctc.stv_descricao desc_curso, ctc.stc_sigla, co.num_percentual, vcu.stv_nome, gp.stv_descricao desc_programa
    from cad_trab_final ctf
    inner join cad_periodos p on p.coi_indice = ctf.coi_periodo
    left join cad_tipo_cursos ctc on ctc.coi_curso= ctf.coi_curso
    inner join cad_orientadores co on co.coi_trabalho = ctf.coi_trabalho
    inner join view_cad_usuario vcu on vcu.cos_matricula_cad = co.cos_docente
    inner join coppe11.gbl_programas gp on gp.cos_programa = vcu.cos_programa
  """, ttl=600)
  return data

@st.cache_data(hash_funcs={db_connect: id})
def organize_data_teses(df):
  # renomeando os nomes das colunas
  df.rename(columns={
      'stc_periodobase': 'periodo_base', 'stv_titulo': 'titulo', 'stv_autor': 'autor', 'ctf.dat_defesa': 'dat_defesa',
      'stv_local_defesa': 'local_defesa', 'ctc.stv_descricao': 'desc_curso', 'ctc.stc_sigla': 'sigla', 'co.num_percentual': 'percentual', 'vcu.stv_nome': 'nome', 'gp.stv_descricao': 'desc_programa'
    }, inplace=True)
  replace_period = {'8788': '87-88','8889': '88-89','8990': '89-90','9091': '90-91','9192': '91-92','9293': '92-93',
                    '9394': '93-94','9495': '94-95','9596': '95-96','9697': '96-97','9798': '97-98','9899': '98-99',
                    '9900': '99-00','0001': '00-01','0102': '01-02','0203': '02-03','0304': '03-04','0405': '04-05',
                    '0506': '05-06','0607': '06-07','0708': '07-08'}
  df['periodo_base'] = df['periodo_base'].replace(replace_period)
  return df

df_teses = organize_data_teses(load_data_teses(db_connect()))


# DISCIPLINAS

@st.cache_data(hash_funcs={db_connect: id})
def load_data_disciplinas(_conn):
  data = _conn.query("""
    select p.stc_periodobase, p.stc_periodoavaliado, ct.stv_disciplina, ct.stc_curso, ct.stv_local, ct.stc_ano_ministrado, vcu.stv_nome, gp.stc_sigla, gp.stv_descricao 
    from cad_turmas ct
    inner join cad_periodos p on p.coi_indice = ct.coi_periodo
    left join cad_ensino ce on ce.coi_turma = ct.coi_turma
    left join view_cad_usuario vcu on vcu.cos_matricula_cad = ce.cos_docente
    left join coppe11.gbl_programas gp on gp.cos_programa = vcu.cos_programa
  """, ttl=600)
  return data

@st.cache_data(hash_funcs={db_connect: id})
def organize_data_disciplinas(df):
  # renomeando os nomes das colunas
  df.rename(columns={
    'stc_periodobase': 'periodo_base', 'stc_periodoavaliado': 'periodo_avaliado', 'stv_disciplina': 'disciplina', 'stc_curso': 'curso', 'stv_local': 'local', 'stc_ano_ministrado': 'ano_ministrado','stv_nome': 'nome', 
    'stc_sigla': 'sigla', 'stv_descricao': 'programa',
  }, inplace=True)
  replace_period = {'8687': '86-87', '8788': '87-88', '8889': '88-89', '8990': '89-90', '9091': '90-91', '9192': '91-92', 
                    '9293': '92-93', '9394': '93-94', '9495': '94-95', '9596': '95-96', '9697': '96-97', '9798': '97-98', 
                    '9899': '98-99', '9900': '99-00', '0001': '00-01', '0102': '01-02', '0203': '02-03', '0304': '03-04', 
                    '0405': '04-05', '0506': '05-06', '0607': '06-07', '0708': '07-08'}
  df['periodo_base'] = df['periodo_base'].replace(replace_period)
  # removendo nulls e strings em branco
  df['curso'].fillna('EP', inplace=True)
  df['curso'].replace('', 'EP', inplace=True)
  df['local'].fillna('COPPE', inplace=True)
  df['local'].replace('', 'COPPE', inplace=True)
  # Substitui dados com erros de digitação e normaliza categorias
  replace_words_escola_poli = ('DEE - POLI','DEE / POLI - UFRJ','DEE-POLI','DEE-POLI/UFRJ','DEE/POLI/UFRJ','DEE/UFRJ','DEI/POLI','DEL','DEL - POLI','DEL-POLI/UFRJ','DEL/POLI','DEL/POLI/UFRJ','DEM','DEM-ESCOLA POLITECNICA','DEN/UFRJ','DENO - ESCOLA POLITECNICA','DENO/POLI','DENO/POLI/UFRJ','DMM','DMM PEMM','DMM/UFRJ','DNC/POLI','DNC/POLI/UFRJ','DRHIMA/POLI/UFRJ','ESCOLA POLITÉCNIA','ESCOLA POLITECNICA','ESCOLA POLITÉCNICA','ESCOLA POLITÈCNICA','ESCOLA POLITÉCNICA ','ESCOLA POLITËCNICA ','ESCOLA POLITECNICA - DRHIMA','ESCOLA POLITÉCNICA - PROG ENG URBANA','ESCOLA POLITÉCNICA - UFRJ','ESCOLA POLITÉCNICA DA UFRJ','ESCOLA POLITÉCNICA UFRJ','ESCOLA POLITECNICA, UFRJ','ESCOLA POLITÉCNICA/CT/UFRJ','ESCOLA POLITÉCNICA/DMM','ESOLA POLITECNICA', 'PEN/POLI/UFRJ','PEU - POLI','POLI','POLI ','POLI - CURSO ENGENHARIA DA COMPUTAÇÃO','POLI - DEI - ENGENHARIA INDUSTRIAL','POLI - REMOTA','POLI - UFRJ','POLI UFRJ','POLI-ENGENAHRIA MECÂNICA','POLI-UFRJ','POLI, H-230B','POLI/DEL','POLI/PEN/UFRJ','POLI/UFRJ','POLITÉCNICA','POLIUFRJ','PPGCAL / IQ / UFRJ','UFRJ - EPOLI - DEL','UFRJ|POLI','ECI','ECI - ESCOLA POLITÉCNICA','ECI/POLI','EPT/POLI'
)
  replace_words_escola_coppe = ('BLOCO I-2000 SALA 036', 'COPPE/UFRJ', 'COPPE/UFRJ - CEDERJ EAD')
  df['local'] = (df['local'].replace(replace_words_escola_coppe, 'COPPE')
                 .replace(replace_words_escola_poli, 'Escola Politécnica')
                )
  df['curso'] = df['curso'].replace({'EG': 'Ensino de Graduação', 'EP': 'Ensino de Pós-Graduação'})
# C205B
# CAMPUS CAXIAS
# CCMN/IM/DCC
# CCST/INPE
# CEDERJ
# CEFET RJ - CAMPUS MARACANA
# CLASSROOM
# CT - BLOCO H - 2º ANDAR
# CT-POLI-UFRJ
# CT/UFRJ
# DEPARTAMENTO DE ELETRÔNICA E COMPUTAÇÃO
# DEPARTAMENTO DE ELETRÔNICA E DE COMPUTAÇÃO
# DEPARTAMENTO DE ENGENHARIA INDUSTRIAL/POLI
# DEPARTAMENTO DE EXPRESSÃO GRÁFICA
# DEPARTAMENTO DE EXPRESSÃO GRÁFICA/POLI
# EAD/CEDERJ
# ECA
# ENG. CONTROLE E AUTOMAÇÃO
# ENGENHARIA DE COMPUTAÇÃO E INFORMAÇÃO 
# ENGENHARIA ELETRÔNICA E COMPUTACAO
# ENGENHARIA MECÂNICA - POLI/UFRJ
# ENGENHARIA MECÂNICA POLI/UFRJ
# ENGENHARIA NAVAL/ SALA I-207
# EP/UFRJ
# EPQB / EQ / UFRJ
# EQ / UFRJ
# EQ/UFRJ
# ESCOLA DE BELAS ARTES
# ESCOLA DE BELAS ARTES / COMUNICAÇÃO VISUAL
# ESCOLA DE QUIMICA
# ESCOLA DE QUÍMICA
# ESCOLA DE QUÍMICA - UFRJ
# FAO/UFRJ
# FAU/UFRJ
# IC/CCMN
# IM
# IMA/UFRJ
# INSTITUTO DE BIOFÍSICA
# INSTITUTO DE BIOFÍSICA CARLOS CHAGAS FILHO
# INSTITUTO DE COMPUTAÇÃO
# INSTITUTO DE FÍSICA
# INSTITUTO DE FÍSICA (FÍSICA MÉDICA)
# INSTITUTO DE MACROLOLÉCULAS
# INSTITUTO DE MACROMOLÉCULAS
# INSTITUTO DE MACROMOLOLÉCULAS
# INSTITUTO DE MATEMATICA
# INSTITUTO DE QUÍMICA
# IQ/UERJ
# IQ/UFRJ - PPGBQ
# LABORATÓRIO DE ESTRUTURAS
# METEOROLOGIA
# PEN/COPPE
# PPGEQ/IQ/UERJ
# PRAIA VERMELHA
# PROG. PÓS-GRAD. CIÊNCIAS CIRÚRGICAS - 
# UFF
# VIRTUAL - ESCOLA POLITENICA

  return df

df_disciplinas = organize_data_disciplinas(load_data_disciplinas(db_connect()))

# CITAÇÕES

@st.cache_data(hash_funcs={db_connect: id})
def load_data_citacoes(_conn):
  data = _conn.query("""
    select cp.stc_periodobase periodo_base, cp.stc_periodoavaliado, cc.num_total, cc.num_trabalho, cc.num_fatorH, cb.stv_descricao banco, vcu.stv_nome, gp.stv_descricao, gp.stc_sigla  
    from cad_citacoes cc, cad_basebibliografica cb, view_cad_usuario vcu, cad_periodos cp, coppe11.gbl_programas gp  
    where cp.coi_indice = cc.coi_periodo
    and cc.coi_base = cb.coi_base
    and cc.cos_docente = vcu.cos_matricula_cad
    and vcu.cos_programa = gp.cos_programa
  """, ttl=600)
  return data

@st.cache_data(hash_funcs={db_connect: id})
def organize_data_citacoes(df):
  # renomeando os nomes das colunas
  df.rename(columns={
    'stc_periodobase': 'periodo_base', 'stc_periodoavaliado': 'periodo_avaliado', 'num_total': 'num_total', 'num_trabalho': 'num_trabalho', 'num_fatorH': 'fatorH', 'banco': 'banco','stv_nome': 'nome', 
    'stc_sigla': 'sigla', 'stv_descricao': 'programa','stc_sigla': 'programa_sigla'
  }, inplace=True)
  return df

df_citacoes = organize_data_citacoes(load_data_citacoes(db_connect()))

# PROJETOS COPPETEC

@st.cache_data(hash_funcs={db_connect: id})
def load_data_proj_coppetec(_conn):
  data = _conn.query("""
    select cp.stc_periodobase, cp.stc_periodoavaliado , cp2.stc_sigla, cp2.stv_projeto, gp.stc_sigla as programa_docente, gp2.stc_sigla as programa_projeto
    from cad_projetos cp2
    left join view_cad_usuario vcu on vcu.cos_matricula_cad = cp2.cos_docente
    left join coppe11.gbl_programas gp on gp.cos_programa = vcu.cos_programa
    left join coppe11.gbl_programas gp2 on gp2.cos_programa = cp2.coi_programa
    , cad_periodos cp
    where cp.coi_indice = cp2.coi_periodo  
  """, ttl=600)
  return data

@st.cache_data(hash_funcs={db_connect: id})
def organize_data_proj_coppetec(df):
  # renomeando os nomes das colunas
  df.rename(columns={
    'stc_periodobase': 'periodo_base', 'stc_periodoavaliado': 'periodo_avaliado','stc_sigla': 'sigla', 'stv_projeto': 'projeto', 'programa_docente': 'programa_docente', 'programa_projeto': 'programa_projeto'
  }, inplace=True)
  replace_period = {'8687': '86-87', '8788': '87-88', '8889': '88-89', '8990': '89-90', '9091': '90-91', '9192': '91-92', 
                    '9293': '92-93', '9394': '93-94', '9495': '94-95', '9596': '95-96', '9697': '96-97', '9798': '97-98', 
                    '9899': '98-99', '9900': '99-00', '0001': '00-01', '0102': '01-02', '0203': '02-03', '0304': '03-04', 
                    '0405': '04-05', '0506': '05-06', '0607': '06-07', '0708': '07-08'}
  df['periodo_base'] = df['periodo_base'].replace(replace_period)
  return df

df_proj_coppetec = organize_data_proj_coppetec(load_data_proj_coppetec(db_connect()))


# PROJETOS DE EXTENSÕES - WIP

@st.cache_data(hash_funcs={db_connect: id})
def load_data_proj_extensoes(_conn):
  data = _conn.query("""
    select cp.stc_periodobase, cp.stc_periodoavaliado , cp2.stv_instituicao, vcu.stv_nome , gp.stv_descricao, gp.stc_sigla  
    from cad_projetosextensao cp2 , view_cad_usuario vcu, cad_periodos cp, coppe11.gbl_programas gp  
    where cp.coi_indice = cp2.coi_periodo 
    and cp2.cos_docente = vcu.cos_matricula_cad
    and vcu.cos_programa = gp.cos_programa
    and cp2.num_pontos > 0
  """, ttl=600)
  return data

@st.cache_data(hash_funcs={db_connect: id})
def organize_data_proj_extensoes(df):
  # renomeando os nomes das colunas
  df.rename(columns={
    'stc_periodobase': 'periodo_base', 'stc_periodoavaliado': 'periodo_avaliado', 'stv_instituicao': 'instituicao','stv_nome': 'nome', 'stv_descricao': 'programa' , 'stc_sigla': 'sigla'
  }, inplace=True)
  # replace_period = {'8687': '86-87', '8788': '87-88', '8889': '88-89', '8990': '89-90', '9091': '90-91', '9192': '91-92', 
  #                   '9293': '92-93', '9394': '93-94', '9495': '94-95', '9596': '95-96', '9697': '96-97', '9798': '97-98', 
  #                   '9899': '98-99', '9900': '99-00', '0001': '00-01', '0102': '01-02', '0203': '02-03', '0304': '03-04', 
  #                   '0405': '04-05', '0506': '05-06', '0607': '06-07', '0708': '07-08'}
  # df['periodo_base'] = df['periodo_base'].replace(replace_period)
  return df

df_proj_extensoes = organize_data_proj_extensoes(load_data_proj_extensoes(db_connect()))



# Citações

# select cp.stc_periodobase, cp.stc_periodoavaliado , cc.num_total , cc.num_trabalho , cc.num_fatorH , cb.stv_descricao, vcu.stv_nome , gp.stv_descricao, gp.stc_sigla  
# from cad_citacoes cc, cad_basebibliografica cb, view_cad_usuario vcu, cad_periodos cp, coppe11.gbl_programas gp  
# where cp.coi_indice = cc.coi_periodo
# and cc.coi_base = cb.coi_base
# and cc.cos_docente = vcu.cos_matricula_cad
# and vcu.cos_programa = gp.cos_programa

# por programas

# =================================
# Projetos COPPETEC
# select cp.stc_periodobase, cp.stc_periodoavaliado , cp2.stc_sigla,  cp2.stv_projeto, gp.stc_sigla as programa_docente , gp2.stc_sigla as programa_projeto
# from cad_projetos cp2
# left join view_cad_usuario vcu on vcu.cos_matricula_cad = cp2.cos_docente
# left join coppe11.gbl_programas gp on gp.cos_programa = vcu.cos_programa
# left join coppe11.gbl_programas gp2 on gp2.cos_programa = cp2.coi_programa
# , cad_periodos cp
# where cp.coi_indice = cp2.coi_periodo  


# por programas

# Quando "programa_projeto" = null usa "programa_docente"



# Projetos de Extensões

# select cp.stc_periodobase, cp.stc_periodoavaliado , cp2.stv_instituicao, vcu.stv_nome , gp.stv_descricao, gp.stc_sigla  
# from cad_projetosextensao cp2 , view_cad_usuario vcu, cad_periodos cp, coppe11.gbl_programas gp  
# where cp.coi_indice = cp2.coi_periodo 
# and cp2.cos_docente = vcu.cos_matricula_cad
# and vcu.cos_programa = gp.cos_programa
# and cp2.num_pontos > 0
