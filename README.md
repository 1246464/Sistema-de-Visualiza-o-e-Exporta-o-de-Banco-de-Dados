# 📊 Sistema de Consulta e Exportação de Banco de Dados

### Desenvolvido em Python, PyQt5 e SQL Server

Este projeto é um aplicativo desktop criado para realizar **conexão com SQL Server**, visualizar tabelas do banco de dados e exportar dados diretamente para **Excel (.xlsx)**.

Com uma interface moderna desenvolvida em **PyQt5**, o sistema é ideal para estudantes, analistas ou qualquer pessoa que precise consultar um banco rapidamente de forma visual.

---

## 🚀 Funcionalidades

### 🔌 1. Conexão com SQL Server

* Digite:

  * DRIVER
  * SERVER
  * DATABASE
  * PASSWORD (opcional)
* Suporta:

  * **Trusted Connection**
  * **Login e senha**

### 📁 2. Listagem de tabelas

* O sistema carrega automaticamente todas as tabelas do banco conectado.
* Exibe no ComboBox para fácil seleção.

### 📋 3. Visualização moderna de dados

* Exibição em **QTableWidget** com:

  * Linhas alternadas (estilo moderno)
  * Cabeçalhos destacados
  * Rolagem vertical/horizontal
  * Seleção por linha
  * Tabela responsiva ao tamanho da tela

### 📤 4. Exportação real para Excel (.xlsx)

* Exporta a tabela selecionada usando **openpyxl**
* Mantém estrutura e colunas do banco
* Compatível com:

  * Microsoft Excel
  * Google Sheets
  * LibreOffice

---

## 🛠️ Tecnologias utilizadas

| Tecnologia     | Uso                       |
| -------------- | ------------------------- |
| **Python 3**   | Linguagem principal       |
| **PyQt5**      | Interface gráfica         |
| **pyodbc**     | Conexão com SQL Server    |
| **openpyxl**   | Exportar dados para Excel |
| **SQL Server** | Banco de dados            |

---

## 📦 Instalação

### 1️⃣ Instale as dependências

```bash
pip install pyqt5 pyodbc openpyxl
```

### 2️⃣ Execute o programa

```bash
python TelaConexao.py
```

---

## 🖼️ Como usar

1. Abra o programa
2. Na primeira tela, informe:

   * DRIVER (ex: `{SQL Server}`)
   * SERVER (ex: `DESKTOP\SQLEXPRESS`)
   * DATABASE
   * PASSWORD (somente se não quiser Trusted Connection)
3. Clique em **Conectar**
4. A segunda tela abrirá automaticamente
5. Escolha uma tabela
6. Veja os dados na tabela interativa
7. Clique em **Exportar Excel** para salvar como `.xlsx`

---

## 🌐 Acesso remoto

O programa funciona com bancos locais e remotos, desde que:

* O servidor permita conexões externas
* Porta 1433 esteja liberada
* LOGIN + SENHA estejam ativos
* `Trusted_Connection` não seja usada remotamente

---

## 📂 Estrutura do projeto

```
📁 MeuProjetoBancoDeDados
│
├── TelaConexao.py     # Tela de conexão
├── TelaBanco.py       # Tela principal com visualização e exportação
├── conexao.py         # Módulo de conexão reaproveitável
├── README.md          # Este arquivo
│
└── requirements.txt   # (opcional)
```


## ⭐ Gostou do projeto?

Deixe uma estrela no repositório 😊
