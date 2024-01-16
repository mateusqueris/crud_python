import streamlit as st
import pyodbc

# Defina os detalhes da conexão
server = 'servidor'
database = 'banco'
username = 'usuario'
password = 'senha'
driver = '{ODBC Driver 17 for SQL Server}'

# Crie a string de conexão
conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

# Conecte-se ao SQL Server
try:
    conn = pyodbc.connect(conn_str)
    print("Conexão bem-sucedida!")

    # Execute consultas ou operações no banco de dados aqui

except pyodbc.Error as ex:
    print(f"Erro na conexão: {ex}")

def adicionar_registro():
    """Adiciona um novo registro à tabela vagas."""

    funcao = st.text_input("Função")
    setor = st.text_input("Setor")
    gestor = st.text_input("Gestor")
    salario_previsto = st.number_input("Salário previsto", min_value=0)
    entrada_prevista = st.date_input("Entrada prevista")
    aprovado = st.checkbox("Aprovado")

    if st.button("Adicionar registro"):
        cursor = conn.cursor()

        # Utilizando interpolação segura para evitar SQL injection
        query = """
            INSERT INTO SolicitacaoVagas (funcao, setor, gestor, salario_previsto, entrada_prevista, aprovado)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        # Passando diretamente o valor booleano para o parâmetro
        cursor.execute(query, funcao, setor, gestor, salario_previsto, entrada_prevista, aprovado)
        conn.commit()
        st.success("Registro adicionado com sucesso!")

        # Resetar os campos após a inclusão dos dados
        st.session_state.input_values = {}

st.title("Adicionar Vaga")
adicionar_registro()

 

conn.close()