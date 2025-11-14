# TelaBanco.py
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from openpyxl import Workbook


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)

        # ===== LAYOUT PRINCIPAL (VERTICAL) =====
        self.layout_principal = QtWidgets.QVBoxLayout(self.centralwidget)
        self.layout_principal.setContentsMargins(10, 10, 10, 10)
        self.layout_principal.setSpacing(10)

        # ===== PRIMEIRA LINHA: TÍTULO =====
        self.label = QtWidgets.QLabel("BANCO DE DADOS")
        fonte_titulo = QtGui.QFont()
        fonte_titulo.setFamily("Arial")
        fonte_titulo.setPointSize(16)
        fonte_titulo.setBold(True)
        self.label.setFont(fonte_titulo)
        self.layout_principal.addWidget(self.label)

        # ===== SEGUNDA LINHA: COMBO + BOTÃO =====
        self.linha_superior = QtWidgets.QHBoxLayout()
        self.linha_superior.setSpacing(10)

        self.combo_tabelas = QtWidgets.QComboBox()
        self.combo_tabelas.setMinimumWidth(220)
        self.combo_tabelas.setObjectName("combo_tabelas")

        self.btn_exportar = QtWidgets.QPushButton("Exportar Excel")
        self.btn_exportar.setObjectName("btn_exportar")
        self.btn_exportar.setMinimumWidth(150)

        self.linha_superior.addWidget(QtWidgets.QLabel("Tabelas:"))
        self.linha_superior.addWidget(self.combo_tabelas)
        self.linha_superior.addStretch()
        self.linha_superior.addWidget(self.btn_exportar)

        self.layout_principal.addLayout(self.linha_superior)

        # ===== TABELA PRINCIPAL =====
        self.tabela = QtWidgets.QTableWidget()
        self.tabela.setObjectName("tabela_dados")
        self.tabela.setAlternatingRowColors(True)  # estilo B
        self.tabela.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # só visualização
        self.tabela.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tabela.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tabela.horizontalHeader().setStretchLastSection(True)
        self.tabela.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        fonte_cabecalho = self.tabela.horizontalHeader().font()
        fonte_cabecalho.setBold(True)
        self.tabela.horizontalHeader().setFont(fonte_cabecalho)

        self.layout_principal.addWidget(self.tabela)

        # MENUBAR / STATUSBAR
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Conexão pyodbc será setada depois pela tela de login
        self.conexao = None

        # Eventos
        self.combo_tabelas.currentTextChanged.connect(self.on_tabela_trocada)
        self.btn_exportar.clicked.connect(self.exportar_tabela_para_excel)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Banco de Dados"))

    # ========= MÉTODOS PARA INTEGRAR COM A TELA DE LOGIN =========

    def configurar_conexao(self, conexao):
        """Recebe a conexão pyodbc vinda da tela de conexão."""
        self.conexao = conexao

    def carregar_tabelas(self, lista_tabelas: list):
        self.combo_tabelas.clear()
        self.combo_tabelas.addItems(lista_tabelas)

    # ========= CARREGAR DADOS NA TABELA =========

    def on_tabela_trocada(self, nome_tabela: str):
        if not nome_tabela:
            return
        if not self.conexao:
            self.mensagem("Nenhuma conexão ativa.")
            return

        try:
            cursor = self.conexao.cursor()
            cursor.execute(f"SELECT * FROM [{nome_tabela}]")
            colunas = [desc[0] for desc in cursor.description]
            linhas = cursor.fetchall()

            # Configura tabela
            self.tabela.clear()
            self.tabela.setColumnCount(len(colunas))
            self.tabela.setRowCount(len(linhas))
            self.tabela.setHorizontalHeaderLabels(colunas)

            # Preenche linhas
            for i, row in enumerate(linhas):
                for j, valor in enumerate(row):
                    item = QtWidgets.QTableWidgetItem(str(valor))
                    # Deixa o texto levemente mais moderno (opcional)
                    item.setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
                    self.tabela.setItem(i, j, item)

            self.tabela.resizeColumnsToContents()

        except Exception as e:
            self.mensagem(f"Erro ao carregar dados da tabela '{nome_tabela}':\n{e}")

    # ========= EXPORTAR PARA EXCEL (.XLSX) =========

    def exportar_tabela_para_excel(self):
        nome_tabela = self.combo_tabelas.currentText()
        if not nome_tabela:
            self.mensagem("Selecione uma tabela para exportar.")
            return
        if not self.conexao:
            self.mensagem("Nenhuma conexão ativa.")
            return

        # Escolher arquivo .xlsx
        caminho, _ = QtWidgets.QFileDialog.getSaveFileName(
            None,
            "Salvar tabela como Excel",
            f"{nome_tabela}.xlsx",
            "Arquivos Excel (*.xlsx)"
        )

        if not caminho:
            return  # usuário cancelou

        try:
            cursor = self.conexao.cursor()
            cursor.execute(f"SELECT * FROM [{nome_tabela}]")
            colunas = [desc[0] for desc in cursor.description]
            linhas = cursor.fetchall()

            wb = Workbook()
            ws = wb.active
            ws.title = nome_tabela[:31]  # Excel limita o nome da planilha a 31 caracteres

            # Cabeçalho
            ws.append(colunas)

            # Dados
            for row in linhas:
                ws.append(list(row))

            wb.save(caminho)

            self.mensagem(f"Tabela '{nome_tabela}' exportada com sucesso para:\n{caminho}")

        except Exception as e:
            self.mensagem(f"Erro ao exportar para Excel:\n{e}")

    # ========= MENSAGEM POP-UP =========

    def mensagem(self, texto: str):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Aviso")
        msg.setText(texto)
        msg.exec_()


# Teste isolado da tela (sem conexão)
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
