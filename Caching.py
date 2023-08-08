import streamlit as st
import pandas as pd
import numpy as np

# ESSE SCRIPT SERVE DE EXEMPLO PARA ENTENDER COMO FUNCIONA O CACHING DO STREAMLIT
# https://docs.streamlit.io/library/advanced-features/caching

# Primeiro exemplo, o cache_data salva os parametros e o que está na função para poder reutilizar
# O cache_data vai reutilizar os códigos comuns do python, tabelas, chamadas API
# Já o cache_resources vai lidar com tudo que não pode ser salvo em um database, como modelos de ML, DB Connections
# @st.cache_data
# def long_running_function(param1, param2):
#     return …
##################################################################################################

# Aqui é dado um exemplo de download de um arquivo csv de mais ou menos 50mb, para comparar o tempo de carregamento sem o cache e com o cache.
# No primeiro carregamento levou uns 3 a 5 segundos e no segundo após incluir o cache foi instantâneo
@st.cache_data # 👈 Aqui foi incluido na segunda vez que carregou os dados
def load_data(url):
    df = pd.read_csv(url)  # 👈 Download the data
    return df

df = load_data("https://github.com/plotly/datasets/raw/master/uber-rides-data1.csv")
st.dataframe(df)
st.button("Rerun")

# Exemplo do uso para transformação de array
@st.cache_data
def transform(df):
    df = df.filter(items=['one', 'three'])
    df = df.apply(np.sum, axis=0)
    return df

transformar = transform(df)
st.dataframe(df)

@st.cache_data
def add(arr1, arr2):
    return arr1 + arr2
##################################################################################################

# Exemplo para fazer uma leitura de uma seleção de tabela no database SQL
connection = database.connect()

@st.cache_data
def query():
    return pd.read_sql_query("SELECT * from table", connection)
##################################################################################################
# Exemplo de uma chamada API
@st.cache_data
def api_call():
    response = requests.get('https://jsonplaceholder.typicode.com/posts/1')
    return response.json()
##################################################################################################
# Esse é um exemplo do uso do cache_data para ML, que pode ser usado para que não precise usar os recursos computacionais repetidamente
@st.cache_data
def run_model(inputs):
    return model(inputs)

# Ainda teria o cache_resource para explorar, porém envolveria alguns conceitos ainda não estudado. Alguns desses exemplos seriam custosos de se aplicar, pois teria que ter a criação de um SQL e/ou montar uma conexão API.













