import os
import sqlite3
import sys
import webbrowser
from PIL import Image
from PyQt5 import uic
from PyQt5.QtGui import QImage, QPalette, QBrush, QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout,\
    QDialog, QMessageBox, QFileDialog, QTableWidgetItem, QAbstractItemView
from PyQt5.QtCore import Qt, QCoreApplication, QDate


class EmptinessError(Exception):
    pass


class MyWidget(QMainWindow): #основное окно
    def __init__(self):
        super().__init__()
        uic.loadUi('UI_files/main.ui', self)
        self.initUI()

    def initUI(self):
        self.pushButton_2.clicked.connect(self.zak_b)
        self.pushButton.clicked.connect(self.new_win)
        self.pushButton_3.clicked.connect(self.new_win)
        self.pushButton_4.clicked.connect(self.new_win)
        self.pushButton_5.clicked.connect(self.info)
        self.tools_win = Tools()
        self.rectification_win = Rectification('my_rect')
        self.recipe_win = Recipe('recipe')
        self.setFixedSize(865, 637)
        fon(self)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            QCoreApplication.instance().quit()

    def zak_b(self):
        webbrowser.open_new_tab('https://киквидзенский.34.мвд.рф/news/item/8632979')

    def new_win(self):
        if self.sender() == self.pushButton_3:
            self.tools_win.show()
        elif self.sender() == self.pushButton:
            self.recipe_win.show()
        elif self.sender() == self.pushButton_4:
            self.rectification_win.show()
        self.hide()

    def info(self):
        self.inf_win = Info()
        self.inf_win.show()


class Info(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI_files/info.ui', self)
        self.initUI()

    def initUI(self):
        self.setModal(True)
        self.setFixedSize(865, 637)
        fon(self)
        with open('readmy.txt', 'r', encoding='utf8') as info_text:
            self.textBrowser.setText(f'{info_text.read()}')


class Tools(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI_files/tools.ui', self)
        self.initUI()

    def initUI(self):
        fon(self)
        self.pushButton.clicked.connect(self.run)
        self.pushButton_2.clicked.connect(self.run)
        self.pushButton_3.clicked.connect(self.run)
        self.pushButton_4.clicked.connect(self.run)
        self.pushButton_6.clicked.connect(self.run)
        self.pushButton_5.clicked.connect(self.breac)
        self.setFixedSize(1112, 687)

    def run(self):
        if self.sender() == self.pushButton:
            self.win = AlcAndWat('UI_files/alcohol_and_water.ui')
        elif self.sender() == self.pushButton_3:
            self.win = SugarHeads('UI_files/sugar_heads.ui')
        elif self.sender() == self.pushButton_4:
            self.win = HydrometerReadings('UI_files/hydrometer_readings.ui')
        elif self.sender() == self.pushButton_2:
            self.win = Alco1AndAlco2('UI_files/alcohol1_and_alcohol2.ui')
        elif self.sender() == self.pushButton_6:
            self.win = AbsAlcHeads('UI_files/heads_by_absolute_alcohol.ui')
        self.win.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.breac()

    def breac(self):
        self.hide()
        global form
        form.show()


class AlcAndWat(QDialog): #калькулятор разбавления водой
    def __init__(self, form):
        super().__init__()
        uic.loadUi(form, self)
        self.initUI()

    def initUI(self):
        self.setFixedSize(359, 603)
        self.setModal(True)
        fon(self)
        self.pushButton.clicked.connect(self.run)

    def run(self):
        try:
            s, k, v = float(self.lineEdit_2.text()), float(self.lineEdit_3.text()), \
                      float(self.lineEdit.text())
            x = s / k * v
            self.textBrowser.setText(f'Для получения {x} л. {"{:.2f}".format(k)} % расствора, '
                                     f'необходимо добавить {x - v} л. воды.')
        except ValueError:
            QMessageBox.critical(self, "Ошибка", "Недопустимый формат данных", QMessageBox.Ok)


class Alco1AndAlco2(AlcAndWat): #калькулятор смешивания 2х жидкостей
    def run(self):
        try:
            v1, c1 = float(self.lineEdit.text()), float(self.lineEdit_2.text())
            v2, c2 = float(self.lineEdit_3.text()), float(self.lineEdit_4.text())
            c = (c1 * v1 + c2 * v2) / (v1 + v2)
            self.textBrowser.setText(f'В результате смешивания мы получим {v1 + v2}л.'
                                     f' {"{:.2f}".format(c)}% расствора.')
        except ValueError:
            QMessageBox.critical(self, "Ошибка", "Недопустимый формат данных", QMessageBox.Ok)


class SugarHeads(AlcAndWat): #калькулятор голов по сахару
    def run(self):
        try:
            self.textBrowser_3.setText(f'Необходимо отобрать '
                                       f'{float(self.lineEdit_7.text()) * 50} мл. голов.')
        except ValueError:
            QMessageBox.critical(self, "Ошибка", "Недопустимый формат данных", QMessageBox.Ok)


class AbsAlcHeads(AlcAndWat): #калькулятор голов по абсолютному спирту
    def initUI(self):
        self.setFixedSize(359, 603)
        self.setModal(True)
        fon(self)
        self.pushButton.clicked.connect(self.run)
        self.comboBox.addItem('10')
        self.comboBox.addItem('15')
        self.comboBox.addItem('20')
        self.comboBox_2.addItem('10')
        self.comboBox_2.addItem('15')
        self.comboBox_2.addItem('20')

    def run(self):
        try:
            v, f = float(self.lineEdit.text()), float(self.lineEdit_2.text())
            sa = v * f / 100
            head = sa * int(self.comboBox.currentText()) / 100
            tails = sa * int(self.comboBox_2.currentText()) / 100
            k = float(self.lineEdit_3.text())
            t = sa - head - tails
            x = 100 / k * t
            self.textBrowser.setText(f'Абс. спирта: {sa} литров\nГоловы: {head} литров\n'
                                     f'Хвосты: {tails} литров\nВыход продукта крепостью'
                                     f' {self.lineEdit_3.text()}%: {"{:.2f}".format(x)} литров')
        except ValueError:
            QMessageBox.critical(self, "Ошибка", "Недопустимый формат данных", QMessageBox.Ok)


class HydrometerReadings(AlcAndWat): #Коррекция показаний ареометра
    def run(self):
        try:
            a, b = float(self.lineEdit_11.text()), float(self.lineEdit_10.text())
            self.textBrowser_4.setText(f'Реальное содержание спирта в '
                                       f'растворе равно {a + (20 - b) * 0.3} %')
        except ValueError:
            QMessageBox.critical(self, "Ошибка", "Недопустимый формат данных", QMessageBox.Ok)


class Recipe(QWidget):
    def __init__(self, tabel):
        super().__init__()
        self.tabel = tabel
        uic.loadUi('UI_files/2wid.ui', self)
        self.initUI()

    def initUI(self):
        self.setFixedSize(1166, 846)
        fon(self)
        self.pushButton.clicked.connect(self.breac)
        self.pushButton_2.clicked.connect(self.add_record)
        self.widget = QWidget(self)
        self.vbox = QVBoxLayout(self.widget)
        self.scroll.setWidget(self.widget)
        con = sqlite3.connect('rectification.db')
        cur = con.cursor()
        result = cur.execute(f"""SELECT name FROM {self.tabel} """).fetchall()
        for elem in result:
            a = QPushButton(f'{elem[0]}')
            a.setStyleSheet('background-color: rgba(59, 0, 89, 200)')
            a.setFixedHeight(33)
            a.clicked.connect(self.inf)
            self.vbox.addWidget(a)
        con.close()

    def inf(self):
        self.inf_win = InfoWin(self.sender())
        self.inf_win.show()

    def add_record(self):
        self.win = AddRecipe(self, 'UI_files/2add_win.ui')
        self.win.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            Tools.breac(self)

    def breac(self):
        Tools.breac(self)


class Rectification(Recipe):
    def add_record(self):
        self.win = AddRect(self, 'UI_files/rect_add_win.ui')
        self.win.show()

    def inf(self):
        self.inf_win = RectInfoWin(self.sender())
        self.inf_win.show()


class AddRecipe(QDialog):
    def __init__(self, parents, ui_name):
        super().__init__()
        self.parents = parents
        self.setModal(True)
        uic.loadUi(ui_name, self)
        self.initUI()

    def initUI(self):
        fon(self)
        self.setFixedSize(812, 448)
        self.pixmap = QPixmap('Picture_files/default.png')
        self.label_3.setPixmap(self.pixmap)
        self.pushButton.clicked.connect(self.add_record)
        self.pushButton_2.clicked.connect(self.add_pic)

    def add_record(self):
        try:
            self.pixmap = QPixmap('Picture_files/default.png')
            self.label_3.setPixmap(self.pixmap)
            con = sqlite3.connect('rectification.db')
            cur = con.cursor()
            name = self.lineEdit.text()
            text = self.textEdit.toPlainText()
            if not name or not text:
                raise EmptinessError
            cur.execute("""INSERT INTO recipe VALUES(?, ?)""", (name, text))
            con.commit()
            c = QPushButton(name)
            c.setStyleSheet('background-color: rgba(59, 0, 89, 200)')
            c.setFixedHeight(33)
            c.clicked.connect(self.inf)
            self.parents.vbox.addWidget(c)
            self.close()
            self.im.save(f'Picture_files/{name}.png')
        except sqlite3.IntegrityError:
            QMessageBox.critical(self, "Ошибка", "Такое название существует", QMessageBox.Ok)
        except EmptinessError:
            QMessageBox.critical(self, "Ошибка", "Недопустимый формат данных", QMessageBox.Ok)
        except AttributeError as a:
            Image.open('Picture_files/default.png').save(f'Picture_files/{name}.png')

    def add_pic(self):
        try:
            self.pic_name = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '',
                                                        'Картинка (*.jpg);;Картинка (*.png)')[0]
            self.im = Image.open(self.pic_name).resize((311, 341))
            self.im.save('Picture_files/test.png')
            self.pixmap = QPixmap('Picture_files/test.png')
            self.label_3.setPixmap(self.pixmap)
        except AttributeError:
            pass

    def inf(self):
        Recipe.inf(self)


class AddRect(AddRecipe):
    def initUI(self):
        self.setFixedSize(821, 342)
        fon(self)
        self.pushButton.clicked.connect(self.add_record)

    def add_record(self):
        try:
            con = sqlite3.connect('rectification.db')
            cur = con.cursor()
            name = self.lineEdit.text()
            date = self.dateEdit.dateTime().toString('dd-MM-yyyy')
            value1 = self.spinBox.value()
            alcohol_content1 = self.spinBox_2.value()
            time = self.spinBox_3.value()
            value2 = self.doubleSpinBox.value()
            alcohol_content2 = self.spinBox_4.value()
            cur.execute("""INSERT INTO my_rect VALUES(?, ?, ?, ?, ?, ?, ?)""", (name,
                                                                                date,
                                                                                value1,
                                                                                alcohol_content1,
                                                                                time,
                                                                                value2,
                                                                                alcohol_content2))
            con.commit()
            c = QPushButton(name)
            c.setStyleSheet('background-color: rgba(59, 0, 89, 200)')
            c.setFixedHeight(33)
            c.clicked.connect(self.inf)
            self.parents.vbox.addWidget(c)
            self.close()
        except sqlite3.IntegrityError:
            QMessageBox.critical(self, "Ошибка", "Такое название существует", QMessageBox.Ok)

    def inf(self):
        Rectification.inf(self)


class InfoWin(QDialog): #информация о рецептах
    def __init__(self, but):
        super().__init__()
        self.but = but
        uic.loadUi('UI_files/info_win.ui', self)
        self.initUI()

    def initUI(self):
        self.setFixedSize(810, 498)
        self.setModal(True)
        fon(self)
        self.pushButton_3.hide()
        self.pushButton_4.hide()
        self.pushButton_2.clicked.connect(self.delite)
        self.pushButton.clicked.connect(self.change)
        self.pushButton_4.clicked.connect(self.confirm)
        self.pushButton_3.clicked.connect(self.cancellation)
        self.pushButton_5.clicked.connect(self.add_pic)
        self.pushButton_5.hide()


        self.lineEdit.setText(self.but.text())
        con = sqlite3.connect('rectification.db')
        cur = con.cursor()
        result = cur.execute(f"""SELECT recipe FROM recipe
                        WHERE name = '{self.but.text()}'""").fetchall()
        con.close()
        self.textEdit.setText(result[0][0])
        self.pixmap = QPixmap(f'../Picture_files/{self.but.text()}.png')
        self.label_3.setPixmap(self.pixmap)

    def delite(self):
        a = 'Вы действительно хотите удалить этот рецепт?'
        if QMessageBox.question(self, ' ', a, QMessageBox.Yes,
                                QMessageBox.No) == QMessageBox.Yes:
            self.but.setParent(None)
            self.close()
            con = sqlite3.connect('rectification.db')
            cur = con.cursor()
            cur.execute(f"DELETE FROM recipe WHERE name = '{self.but.text()}'")
            con.commit()
            os.remove(f'../Picture_files/{self.but.text()}.png')

    def change(self):
        self.pushButton.hide()
        self.pushButton_2.hide()
        self.pushButton_3.show()
        self.pushButton_4.show()
        self.pushButton_5.show()
        self.lineEdit.setEnabled(True)
        self.textEdit.setEnabled(True)

    def confirm(self):
        try:
            con = sqlite3.connect('rectification.db')
            cur = con.cursor()
            name = self.lineEdit.text()
            description = self.textEdit.toPlainText()
            if not name or not description:
                raise EmptinessError
            cur.execute(f"""UPDATE recipe 
                            SET name = '{name}', recipe = '{description}'
                             WHERE name = '{self.but.text()}'""")
            con.commit()
            a = self.but.text()
            self.but.setText(self.lineEdit.text())
            self.close()
            self.im.save(f'Picture_files/{name}.png')
        except EmptinessError:
            QMessageBox.critical(self, "Ошибка", "Недопустимый формат данных", QMessageBox.Ok)
        except sqlite3.IntegrityError:
            QMessageBox.critical(self, "Ошибка", "Такое название существует", QMessageBox.Ok)
        except AttributeError:
            os.rename(f'../Picture_files/{a}.png', f'../Picture_files/{self.lineEdit.text()}.png')

    def cancellation(self):
        self.pushButton.show()
        self.pushButton_2.show()
        self.pushButton_3.hide()
        self.pushButton_4.hide()
        self.pushButton_5.hide()
        self.lineEdit.setEnabled(False)
        self.textEdit.setEnabled(False)
        self.lineEdit.setText(self.but.text())
        con = sqlite3.connect('rectification.db')
        cur = con.cursor()
        result = cur.execute(f"""SELECT recipe FROM recipe
                                WHERE name = '{self.but.text()}'""").fetchall()

        con.close()
        self.textEdit.setText(result[0][0])
        self.pixmap = QPixmap(f'../Picture_files/{self.but.text()}.png')
        self.label_3.setPixmap(self.pixmap)

    def add_pic(self):
        AddRecipe.add_pic(self)


class RectInfoWin(QDialog):
    def __init__(self, but):
        super().__init__()
        self.but = but
        uic.loadUi('UI_files/rect_info_win.ui', self)
        self.initUI()

    def initUI(self):
        self.setFixedSize(874, 366)
        self.pushButton_2.clicked.connect(self.delite)
        self.pushButton.clicked.connect(self.change)

        con = sqlite3.connect('rectification.db')
        cur = con.cursor()
        result = cur.execute(f"""SELECT * FROM my_rect 
                                WHERE name = '{self.but.text()}'""").fetchall()[0]
        self.lineEdit.setText(result[0])
        self.dateEdit.setDate(QDate(*map(int, result[1].split('-'))))
        self.spinBox.setValue(result[2])
        self.spinBox_2.setValue(result[3])
        self.spinBox_3.setValue(result[4])
        self.doubleSpinBox.setValue(result[5])
        self.spinBox_4.setValue(result[6])
        self.tableWidget.setRowCount(1)
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(['название', 'дата', 'Объём сырья',
                                                    'спиртуозность сырья (%)', 'время ректификации',
                                                    'Объём дистилята', '  спиртуозность дистилята (%)'])
        for i, elem in enumerate(result):
            self.tableWidget.setItem(0, i, QTableWidgetItem(str(elem)))
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)

    def delite(self):
        a = 'Вы действительно хотите удалить эту запись?'
        if QMessageBox.question(self, ' ', a, QMessageBox.Yes,
                                QMessageBox.No) == QMessageBox.Yes:
            self.but.setParent(None)
            con = sqlite3.connect('rectification.db')
            cur = con.cursor()
            cur.execute(f"DELETE FROM my_rect WHERE name = '{self.but.text()}'")
            con.commit()
            self.close()

    def change(self):
        a = 'Вы действительно хотите изменить эту запись?'
        if QMessageBox.question(self, ' ', a, QMessageBox.Yes,
                                QMessageBox.No) == QMessageBox.Yes:
            con = sqlite3.connect('rectification.db')
            cur = con.cursor()
            cur.execute(f"""UPDATE my_rect 
                            SET name = ?,
                                date = ?,
                                volume = ?,
                                alcohol_content = ?,
                                time = ?,
                                volume_2 = ?,
                                alcohol_content_2 = ?
                            WHERE name = ?""", (self.lineEdit.text(),
                                                self.dateEdit.dateTime().toString('dd-MM-yyyy'),
                                                self.spinBox.value(),
                                                self.spinBox_2.value(),
                                                self.spinBox_3.value(),
                                                self.doubleSpinBox.value(),
                                                self.spinBox_4.value(),
                                                self.but.text()))
            con.commit()
            self.but.setText(self.lineEdit.text())
            self.close()


def fon(self): #делает фон
    oImage = QImage("Picture_files/fon.jpg")
    sImage = oImage.scaled(self.size())
    palette = QPalette()
    palette.setBrush(QPalette.Window, QBrush(sImage))
    self.setPalette(palette)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('Picture_files/kolba.ico'))

    form = MyWidget()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())