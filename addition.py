import sys
import sqlite3
from PIL import Image

from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QFileDialog, QInputDialog, QDialog, QVBoxLayout,
                             QColorDialog)
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtGui import QIcon, QPixmap, QImage, QTransform
from PyQt5 import QtCore


def middle_color(name_im):
    im = Image.open(name_im)
    pixels = im.load()
    x, y = im.size
    totalr, totalg, totalb = 0, 0, 0
    for i in range(x):
        for j in range(y):
            r, g, b = pixels[i, j]
            totalr += r
            totalb += b
            totalg += g
    return totalr // (x * y), totalg // (x * y), totalb // (x * y)


class AddWindow(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('add_window.ui', self)  # Загружаем дизайн
        self.setFixedSize(1100, 900)  # Resize blocked
        self.setWindowTitle('Adding recipe')
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.db = sqlite3.connect("recipies.sqlite")
        if self.db.cursor().execute(f"""SELECT id FROM Recipes""").fetchall():
            self.recipe = len(self.db.cursor().execute(f"""SELECT id FROM Recipes""").fetchall()[-1]) + 1
            self.db_tags = self.db.cursor().execute(f"""SELECT title FROM Tags""").fetchall()[0]
        else:
            self.recipe = 1
            self.db_tags = []
        self.im = ''
        self.source = ''
        self.tag_color = ''
        self.tags = []

        print('qwer', self.recipe)

        self.image_btn.clicked.connect(self.choose_image)
        self.source_btn.clicked.connect(self.choose_source)
        self.add_btn.clicked.connect(self.add_tag)
        self.add_btn_2.clicked.connect(self.choose_tag_color)
        self.commit_btn.clicked.connect(self.submit)
        # self.initUI()

    def choose_image(self):
        self.im, ok_pressed = QFileDialog.getOpenFileName(self, 'Choose a image', '')
        if self.im:
            ic = QIcon(self.im)
            self.image_btn.setIcon(ic)
            self.image_btn.setIconSize(QtCore.QSize(579, 321))
            self.image_btn.setStyleSheet(f'border-radius: 15px;'
                                         f'background-color: rgb{middle_color(self.im)};')
        # if not ok_pressed:
        #    self.image_btn.setIcon(QIcon('pictures/plus-lg 9.png'))

    def choose_source(self):
        self.source, ok_pressed = QInputDialog.getText(self, "Source", "Enter a source link")
        if ok_pressed and self.source:
            self.source_btn.setStyleSheet('background-color: rgb(142, 222, 198);'
                                          'font: 16pt "Leelawadee UI";'
                                          'border-radius: 15px;')

    def add_tag(self):
        tag_name, ok_pressed = QInputDialog.getText(self, "Tags", "Enter a tag name")
        self.tags.append(tag_name)
        # self.tags = self.db.cursor().execute(f"""SELECT title FROM Tags""").fetchall()[0]  To correcting window
        self.add_btn_2.setText(f'tags:  {"  ".join(self.tags)}')

    def choose_tag_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            h = color.name().lstrip('#')
            self.tag_color = tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
            print(self.tag_color)
            self.add_btn_2.setStyleSheet(f'font: 13pt "Leelawadee UI";'
                                         f'background-color: rgb{self.tag_color};'
                                         f'border-radius: 15px;'
                                         f'text-align: left;'
                                         f'padding-left: 20px;'
                                         f'padding-right: 20px;'
                                         f'color: rgb(44, 44, 44);')

    def submit(self):
        cost = self.cost_line.text().rstrip()
        if cost != 'Cost:':
            cost = cost[5:]
        if self.ingridients.toPlainText():
            print(self.ingridients.toPlainText(), type(self.ingridients.toPlainText()))
        query = f"""INSERT INTO Recipes (id, image, source, main_text, title, cost, tags_color) 
        VALUES ({self.recipe}, "{self.im}", "{self.source}", "{self.main_text.toPlainText()}", 
        "{self.title.text()}", "{cost}", "{self.tag_color}")"""
        self.db.cursor().execute(query)
        # self.db.commit()

        counter = 0
        for tag in self.tags:
            if tag not in self.db_tags:
                query1 = f"""INSERT INTO Tags (id, title) VALUES ({len(self.db_tags) + counter}, "{tag}")"""
                self.db.cursor().execute(query1)
                query1 = f"""INSERT INTO Recipes_Tags (resipesId, tagsId) VALUES 
                ({self.recipe}, {len(self.db_tags) + counter})"""
                self.db.cursor().execute(query1)
                counter += 1

        db_ingridients = self.db.cursor().execute(f"""SELECT id FROM Ingridients""").fetchall()[0]
        query2 = f"""INSERT INTO Ingridients (id, list) VALUES ({len(db_ingridients) + 1}, 
        "{self.ingridients.toPlainText()}")"""
        self.db.cursor().execute(query2)
        # self.db.commit()
        query2 = f"""INSERT INTO Recipes_Ingridients (recipesId, ingridientsId) 
        VALUES ("{self.recipe}", "{len(db_ingridients) + 1}")"""
        self.db.cursor().execute(query2)
        self.db.commit()
        print('commit')
        self.db.close()
        self.hide()
