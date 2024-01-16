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

# Função para conectar ao SQL Server
def connect_to_database():
    try:
        conn = pyodbc.connect(conn_str)
        return conn
    except pyodbc.Error as ex:
        st.error(f"Erro na conexão: {ex}")
        return None

# Função para deletar registro
def deletar_registro():
    conn = connect_to_database()

    if conn:
        cursor = conn.cursor()

        # Consulta para obter os registros existentes
        query_select = "SELECT * FROM SolicitacaoVagas"
        result = cursor.execute(query_select).fetchall()

        # Lista de IDs dos registros existentes
        registros_ids = [str(row[0]) for row in result]

        if not registros_ids:
            st.warning("Não há registros para deletar.")
            return

        # Dropdown para selecionar o registro a ser deletado
        registro_id = st.selectbox("Selecione o ID do registro a ser deletado:", registros_ids)

        # Consulta para obter os detalhes do registro selecionado
        query_select_registro = f"SELECT * FROM SolicitacaoVagas WHERE id = {registro_id}"
        result_registro = cursor.execute(query_select_registro).fetchone()

        # Exibir os detalhes do registro atual
        st.subheader(f"Detalhes do Registro #{registro_id}")

        # Criar um dicionário com os detalhes do registro
        detalhes_registro = {
            "Função": result_registro.funcao,
            "Setor": result_registro.setor,
            "Gestor": result_registro.gestor,
            "Salário Previsto": result_registro.salario_previsto,
            "Entrada Prevista": result_registro.entrada_prevista.strftime('%Y-%m-%d') if result_registro.entrada_prevista else None,
            "Aprovado": "Sim" if result_registro.aprovado else "Não"
        }

        # Exibir os detalhes usando st.dataframe
        st.dataframe([detalhes_registro])

        # Botão para deletar o registro
        if st.button("Deletar Registro"):
            # Query para deletar o registro
            query_delete = "DELETE FROM SolicitacaoVagas WHERE id = ?"
            # Executar a query de exclusão
            cursor.execute(query_delete, registro_id)
            conn.commit()
            st.success("Registro deletado com sucesso!")

            # Atualizar a tela
            st.rerun()

# Título do Streamlit
st.title("Deletar Registro")
deletar_registro()
