# conexao.py
import pyodbc


def conectar(driver: str,
             server: str,
             database: str,
             username: str | None = None,
             password: str | None = None,
             trusted: bool = True,
             timeout: int = 5):
    """
    Faz a conexão com o SQL Server e retorna:
      - conexao (pyodbc.Connection)
      - lista de tabelas (list[str])
      - nome do banco (str)
    """

    if trusted:
        conn_str = (
            f"DRIVER={driver};"
            f"SERVER={server};"
            f"DATABASE={database};"
            "Trusted_Connection=yes;"
        )
    else:
        conn_str = (
            f"DRIVER={driver};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"UID={username};"
            f"PWD={password};"
        )

    banco = pyodbc.connect(conn_str, timeout=timeout)
    cursor = banco.cursor()

    # Nome do banco atual
    cursor.execute("SELECT DB_NAME()")
    nome_db = cursor.fetchone()[0]

    # Lista de tabelas
    tabelas = [row.table_name for row in cursor.tables(tableType='TABLE')]

    return banco, tabelas, nome_db
