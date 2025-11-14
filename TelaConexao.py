# TelaConexao.py  (ou o nome que você já usa)
from PyQt5 import QtCore, QtGui, QtWidgets
from TelaBanco import Ui_MainWindow
from conexao import conectar
import sys


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        self.dialog = Dialog
        Dialog.setObjectName("Dialog")
        Dialog.resize(411, 409)

        # LABEL TÍTULO
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(60, 30, 300, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setObjectName("label")

        # CAMPOS
        self.line_driver = QtWidgets.QLineEdit(Dialog)
        self.line_driver.setGeometry(QtCore.QRect(140, 110, 151, 20))
        self.line_driver.setObjectName("line_driver")

        self.line_server = QtWidgets.QLineEdit(Dialog)
        self.line_server.setGeometry(QtCore.QRect(140, 140, 151, 20))
        self.line_server.setObjectName("line_server")

        self.line_database = QtWidgets.QLineEdit(Dialog)
        self.line_database.setGeometry(QtCore.QRect(140, 170, 151, 20))
        self.line_database.setObjectName("line_database")

        self.line_password = QtWidgets.QLineEdit(Dialog)
        self.line_password.setGeometry(QtCore.QRect(140, 200, 151, 20))
        self.line_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.line_password.setObjectName("line_password")

        # BOTÕES
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(120, 260, 101, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.pegar_dados)

        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(240, 260, 101, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(Dialog.close)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Conexão"))
        self.label.setText(_translate("Dialog", "CADASTRO NO BANCO DE DADOS"))

        self.line_driver.setPlaceholderText(_translate("Dialog", "DRIVER (ex: {SQL Server})"))
        self.line_server.setPlaceholderText(_translate("Dialog", "SERVER (ex: DESKTOP\\SQLEXPRESS)"))
        self.line_database.setPlaceholderText(_translate("Dialog", "DATABASE"))
        self.line_password.setPlaceholderText(_translate("Dialog", "PASSWORD (deixe vazio p/ Trusted)"))

        # Já preenche driver padrão escolhido (A)
        self.line_driver.setText("{SQL Server}")

        self.pushButton.setText(_translate("Dialog", "CONECTAR"))
        self.pushButton_2.setText(_translate("Dialog", "SAIR"))

    def pegar_dados(self):
        driver = self.line_driver.text().strip() or "{SQL Server}"
        server = self.line_server.text().strip()
        database = self.line_database.text().strip()
        senha = self.line_password.text().strip()

        if not server or not database:
            self.mensagem("Preencha pelo menos SERVER e DATABASE.")
            return

        trusted = (senha == "")
        username = None
        if not trusted:
            # Como você escolheu A, vou assumir o usuário 'sa' quando usar senha
            username = "sa"

        try:
            banco, tabelas, nome_db = conectar(
                driver=driver,
                server=server,
                database=database,
                username=username,
                password=senha if not trusted else None,
                trusted=trusted
            )

        except Exception as e:
            self.mensagem(f"Erro na conexão:\n{e}")
            return

        self.mensagem(f"Conexão com '{nome_db}' bem-sucedida!")

        # Abre a segunda janela (TelaBanco)
        self.segunda = QtWidgets.QMainWindow()
        self.ui_segunda = Ui_MainWindow()
        self.ui_segunda.setupUi(self.segunda)
        self.ui_segunda.configurar_conexao(banco)
        self.ui_segunda.carregar_tabelas(tabelas)
        self.segunda.show()

        # Fecha a tela de conexão
        self.dialog.close()

    def mensagem(self, texto: str):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Aviso")
        msg.setText(texto)
        msg.exec_()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(dialog)
    dialog.show()
    sys.exit(app.exec_())
