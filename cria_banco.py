import sqlite3

# Caminho completo onde o banco de dados será criado
caminho_banco = r'C:\Users\lfsoares\OneDrive - Sistema FIEMG\Área de Trabalho\LUIZ\8.Cursos\2.REST_APIs_Flask\app\banco.db'

# Estabelece a conexão com o banco de dados SQLite.
# O arquivo 'banco.db' será criado no caminho especificado, caso não exista.
connection = sqlite3.connect(caminho_banco)

# Cria um cursor para executar comandos SQL.
cursor = connection.cursor()

# Comando SQL para criar a tabela 'hoteis', caso ela ainda não exista.
cria_tabela = """
CREATE TABLE IF NOT EXISTS hoteis (
    hotel_id TEXT PRIMARY KEY,  -- Identificador único do hotel (chave primária)
    nome TEXT NOT NULL,         -- Nome do hotel
    estrelas REAL NOT NULL,     -- Avaliação em estrelas
    diaria REAL NOT NULL,       -- Valor da diária
    cidade TEXT NOT NULL        -- Cidade do hotel
)
"""

# Comando SQL para inserir um hotel na tabela 'hoteis'
cria_hotel = """
INSERT OR IGNORE INTO hoteis (hotel_id, nome, estrelas, diaria, cidade)
VALUES ('alpha', 'Alpha Hotel', 4.3, 345.30, 'Rio de Janeiro')
"""

# Executa o comando SQL para criar a tabela
cursor.execute(cria_tabela)

# Executa o comando SQL para inserir dados, garantindo que não haverá duplicação de registros
cursor.execute(cria_hotel)

# Confirma as alterações no banco de dados.
connection.commit()

# Fecha a conexão com o banco de dados.
connection.close()

# Exibe uma mensagem informando que o processo foi concluído.
print(f"Banco de dados e tabela 'hoteis' configurados com sucesso no caminho: {caminho_banco}")
