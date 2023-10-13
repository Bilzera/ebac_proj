
# Imports
import pandas            as pd
import streamlit         as st
import seaborn           as sns
import matplotlib.pyplot as plt





# Título da aplicação
st.title("Análise de Marketing")


############## CARREGANDO A BASE DE DADOS ########################################################
# Sidebar para fazer upload do arquivo CSV
st.sidebar.header("Upload do Arquivo CSV")
uploaded_file = st.sidebar.file_uploader("Faça o upload do arquivo CSV", type=["csv"])

# Função para carregar o DataFrame a partir do arquivo CSV
@st.cache_data
def carregar_dados(uploaded_file):
    if uploaded_file is not None:
        return pd.read_csv(uploaded_file, delimiter=';')
    return None

df = carregar_dados(uploaded_file)


# Verifica se o arquivo foi carregado com sucesso
if df is None:
    st.info("Por favor, faça o upload de um arquivo CSV para carregar os dados.")
    st.stop()  # Para a execução do código
###################################################################################################



##################### FILTRANDO OS DADOS ##########################################################
# Sidebar para filtros
st.sidebar.header("Filtros")
# Listando algumas variáveis explicativas (age vai ser feito separadamente)
colunas_explicativas = ['job', 'marital', 'education', 'housing', 'loan', 'contact', 'month']
valores_filtros = {}
for coluna in colunas_explicativas:
    valores_filtros[coluna] = st.sidebar.multiselect(f"Selecione valores para {coluna}", df[coluna].unique())


# Controle deslizante para selecionar um intervalo de idade
min_age = int(df['age'].min())
max_age = int(df['age'].max())
# Botão do Idades slidebar
idades = st.sidebar.slider(label='Idade', min_value=min_age, max_value=max_age, value=(min_age, max_age), step=1)

# Função para filtrar o DataFrame
@st.cache_data
def filtrar_dados(df, valores_filtros, idades):
    df_filtrado = df.copy()
    for coluna, valores in valores_filtros.items():
        if valores:
            df_filtrado = df_filtrado[df_filtrado[coluna].isin(valores)]
    df_filtrado = df_filtrado[(df_filtrado['age'] >= idades[0]) & (df_filtrado['age'] <= idades[1])]
    return df_filtrado

df_filtrado = filtrar_dados(df, valores_filtros, idades)

# Exibir os dados filtrados
st.subheader("Dados Filtrados")
st.write(df_filtrado)
# Exibir o número de linhas selecionadas
st.write(f"Total de {df_filtrado.shape[0]} pessoas selecionadas.")

# Gráficos na parte principal da aplicação
st.header("Gráficos")
# Escolhendo o tipo de gráfico
tipo_grafico = st.selectbox("Escolha o tipo de gráfico", ["Gráfico de Barras", "Gráfico de Pizza"])
if tipo_grafico == "Gráfico de Barras":
    # Gráfico de barras
    plt.figure(figsize=(4, 3))
    sns.countplot(data=df_filtrado, x='y')
    st.pyplot()
else:
    # Gráfico de pizza
    plt.figure(figsize=(2,2))
    df_filtrado['y'].value_counts().plot.pie(autopct='%1.1f%%')
    st.pyplot()
# Removendo msg de erro (devido a não passar fig como parâmetro) mas não interferiu no resultado
st.set_option('deprecation.showPyplotGlobalUse', False)


##################### SALVANDO O DATA-FRAME FILTRADO ##########################################
# Botão para salvar o DataFrame filtrado em CSV
if st.button('Salvar como CSV'):
    df_filtrado.to_csv('dados_filtrados.csv', index=False)
    st.success('DataFrame filtrado salvo em CSV com sucesso!')

# Adicione um botão para salvar o DataFrame filtrado em XLSX
if st.button('Salvar como XLSX'):
    df_filtrado.to_excel('dados_filtrados.xlsx', index=False)
    st.success('DataFrame filtrado salvo em XLSX com sucesso!')