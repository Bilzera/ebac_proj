import streamlit as st
import pandas as pd
import numpy as np

st.title('Uber pickups in NYC')


# Carregando os dados do Uber de New York City
DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')
@st.cache_data # Adicionado posteriormente para mostrar o poder do cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data
########################################################################################################

# Cria um texto que mostra que o elemento está carregando
data_load_state = st.text('Loading data...')

# Carrega 10000 linhas do DF passando o parametro pra função criada anteriormente
data = load_data(10000)
    

    
# Avisa que carregou com sucesso!
# data_load_state.text('Loading data...done!')  trocado pela linha de baixo
data_load_state.text("Done! (using st.cache_data)")


# Verificando o conjunto de dados
#st.subheader('Raw data') Comentado para usar o novo exemplo abaixo
#st.write(data)
# Esse IF faz com que possa ser escolhido entre tabela e gráfico com checkbox
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

# Verificando o número de viagens por hora
st.subheader('Number of pickups by hour')
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
# Esse comando vai dar o plot no histograma
st.bar_chart(hist_values)


# Mostra um mapa de todas viagens iniciadas
#st.subheader('Map of all pickups') # Comentado os dois códigos para prosseguir com o código abaixo
#st.map(data)

# Aqui vai mostrar a concentração do mapa no horário das 17h, que é o horário mais movimentado
# hour_to_filter = 17 substituido pelo código abaixo
hour_to_filter = st.slider('hour', 0, 23, 17) # Escolhendo horário pelo filtro 0-23, o 17 é padrão antes de escolher
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)

























