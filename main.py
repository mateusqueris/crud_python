import streamlit as st
import webbrowser

def abrir_arquivo1():
    webbrowser.open("http://localhost:8505/#adicionar-vaga")

def abrir_arquivo2():
    # Substitua "caminho_do_arquivo2.py" pelo caminho real do seu segundo arquivo
    webbrowser.open("caminho_do_arquivo2.py")

def abrir_arquivo3():
    # Substitua "caminho_do_arquivo3.py" pelo caminho real do seu terceiro arquivo
    webbrowser.open("caminho_do_arquivo3.py")

# Título do aplicativo
st.title("Exemplo de GUI em Python com Streamlit")

# Botões para abrir arquivos
if st.button("Abrir Arquivo 1"):
    abrir_arquivo1()

if st.button("Abrir Arquivo 2"):
    abrir_arquivo2()

if st.button("Abrir Arquivo 3"):
    abrir_arquivo3()
