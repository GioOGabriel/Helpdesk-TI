import sqlite3
#biblioteca de conexao com o banco de dados

def CriarBanco():
    #conecta com o arquivo do banco de dados, caso não exista ele cria
    conn = sqlite3.connect('helpdesk.db') 
    #cria a conexão com o banco de dados caso o arquivo helpdesk.db 
    #não exista, ele será criado automaticamente

    cursor = conn.cursor()
    #o cursor é usado para executar comandos SQL no banco de dados               

    #comando SQL para criar a tabela de chamados
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chamados ( 
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        solicitante TEXT NOT NULL,
        categoria TEXT NOT NULL,
        descricao TEXT NOT NULL,
        prioridade TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Aberto',
        data_abertura DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()  #salva as alterações fisicamente no arquivo do banco de dados
    conn.close()  #fecha a conexão com o banco de dados e libera pra outros programas accessarem
    print("Banco de dados e tabela 'chamados' criados com sucesso!")

    if __name__ == "__main__":
        CriarBanco()  #chama a função para criar o banco de dados e a tabela