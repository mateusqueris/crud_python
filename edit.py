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

# Função para editar registro
def editar_registro():
    conn = connect_to_database()

    if conn:
        cursor = conn.cursor()

        # Consulta para obter os registros existentes
        query_select = "SELECT * FROM SolicitacaoVagas"
        result = cursor.execute(query_select).fetchall()

        # Lista de IDs dos registros existentes
        registros_ids = [str(row[0]) for row in result]

        # Dropdown para selecionar o registro a ser editado
        registro_id = st.selectbox("Selecione o ID do registro a ser editado:", registros_ids)

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

        # Obter novos valores para atualização
        novo_funcao = st.text_input("Nova Função", value=result_registro.funcao)
        novo_setor = st.text_input("Novo Setor", value=result_registro.setor)
        novo_gestor = st.text_input("Novo Gestor", value=result_registro.gestor)
        # Convertendo para float
        novo_salario_previsto = st.number_input("Novo Salário Previsto", value=float(result_registro.salario_previsto), min_value=0.0, step=1.0)
        novo_entrada_prevista = st.date_input("Nova Entrada Prevista", value=result_registro.entrada_prevista)
        novo_aprovado = st.checkbox("Aprovado", value=result_registro.aprovado)

        # Botão para realizar a atualização
        if st.button("Atualizar Registro"):
            # Query para atualizar o registro
            query_update = """
                UPDATE SolicitacaoVagas
                SET funcao=?, setor=?, gestor=?, salario_previsto=?, entrada_prevista=?, aprovado=?
                WHERE id=?
            """
            # Executar a query de atualização
            cursor.execute(query_update, novo_funcao, novo_setor, novo_gestor,
                           novo_salario_previsto, novo_entrada_prevista, novo_aprovado, registro_id)
            conn.commit()
            st.success("Registro atualizado com sucesso!")

            # Refresh da página
            st.rerun()

# Título do Streamlit
st.title("Editar Registro")
editar_registro()
