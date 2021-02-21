import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QTableWidgetItem, \
    QStackedWidget, QMessageBox
from PyQt5 import uic


class ChangeDialog(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        uic.loadUi('change_dialog.ui', self)
        self.pushButton.clicked.connect(self.save_changes)
        self.pushButton_2.clicked.connect(self.close)

    def save_changes(self):
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        passed_id = self.lineEdit.text()
        params = {
            'title': self.rw_1,
            'roast_degree': self.rw_2,
            'type': self.rw_3,
            'taste': self.rw_4,
            'price': self.rw_5,
            'liters': self.rw_6
        }
        for key in params:
            if params[key].text() == '':
                continue
            cur.execute(f'''
                        UPDATE capuchino
                        SET {key} = "{params[key].text()}"
                        WHERE id = {passed_id}''')
        con.commit()
        con.close()
        # ex.second_form.get_data()
        # ex.second_form.tbl_init()
        ex.widget.get_data()
        ex.widget.tbl_init()
        self.close()


class AddDialog(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        uic.loadUi('add_dialog.ui', self)
        self.pushButton.clicked.connect(self.save_changes)
        self.pushButton_2.clicked.connect(self.close)

    def save_changes(self):
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        params = {
            'title': self.rw_1,
            'roast_degree': self.rw_2,
            'type': self.rw_3,
            'taste': self.rw_4,
            'price': self.rw_5,
            'V (Liters)': self.rw_6
        }
        for key in params:
            if params[key].text() == '':
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle("Информация")
                msg.setText("Не все поля заполнены.")
                okButton = msg.addButton('Закрыть', QMessageBox.AcceptRole)
                msg.exec()
                return
        length_of_data = len(cur.execute(""" SELECT * FROM capuchino""").fetchall())

        cur.execute(f"""
        INSERT INTO capuchino
VALUES({length_of_data + 1}, '{self.rw_1.text()}', '{self.rw_2.text()}', '{self.rw_3.text()}',
'{self.rw_4.text()}', '{self.rw_5.text()}', '{self.rw_6.text()}')
                    """)
        con.commit()
        con.close()
        # ex.second_form.get_data()
        # ex.second_form.tbl_init()
        ex.widget.get_data()
        ex.widget.tbl_init()
        self.close()


class SecondForm(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        uic.loadUi('addEditCoffeeForm.ui', self)
        # self.get_data()
        # self.tbl_init()
        self.change_btn.clicked.connect(self.open_change_dialog)
        self.add_btn.clicked.connect(self.open_add_dialog)

    def open_change_dialog(self):
        self.change_dialog = ChangeDialog()
        self.change_dialog.show()

    def open_add_dialog(self):
        self.add_dialog = AddDialog()
        self.add_dialog.show()


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        uic.loadUi('main.ui', self)
        self.get_data()
        self.tbl_init()

    def tbl_init(self):
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels([
            'ID', 'title', 'roast_degree', 'type', 'taste', 'price', 'V (Liters)'
        ])
        self.tableWidget.setRowCount(0)
        for row in range(len(self.data)):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for col in range(self.tableWidget.columnCount()):
                self.tableWidget.setItem(row, col, QTableWidgetItem(str(self.data[row][col])))

    def get_data(self):
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        self.data = cur.execute("""
        SELECT * FROM capuchino
        """).fetchall()
        con.close()


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Капучино')
        self.statusBar().showMessage("Две разные формы реализованы внутри одного окна qmainwindow.")
        self.setGeometry(300, 100, 800, 800)
        self.stack = QStackedWidget()
        self.widget = MyWidget()
        self.second_form = SecondForm()
        self.stack.addWidget(self.widget)
        self.stack.addWidget(self.second_form)
        self.setCentralWidget(self.stack)
        self.stack.setCurrentWidget(self.widget)
        self.widget.pushButton.clicked.connect(self.change_form)
        self.second_form.pushButton.clicked.connect(self.change_form)

    def change_form(self):
        if self.stack.currentWidget() == self.widget:
            self.stack.setCurrentWidget(self.second_form)
        else:
            self.stack.setCurrentWidget(self.widget)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
