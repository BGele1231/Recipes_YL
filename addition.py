import sys
import sqlite3
from PIL import Image
import os

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


def main_w_crop(name_im, recipe_id):
    print('pictures/recipes_images' + str(recipe_id) + '.' + name_im.split('.')[-1])
    im = Image.open(name_im)
    x, y = im.size
    if x < y:
        times = round(x / 340, 2)
        im2 = im.crop((0, y // 2 - round(times * 200) // 2,
                       x, y // 2 + round(200 * times) // 2))
    else:
        times = round(y / 200, 2)
        im2 = im.crop((x // 2 - round(times * 340) // 2, 0,
                       x // 2 + round(340 * times) // 2, y))
    im2.save('pictures/recipes_images/' + str(recipe_id) + '.' + name_im.split('.')[-1])
    return 'pictures/recipes_images/' + str(recipe_id) + '.' + name_im.split('.')[-1]


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

        self.image_btn.clicked.connect(self.choose_image)
        self.source_btn.clicked.connect(self.choose_source)
        self.add_btn.clicked.connect(self.add_tag)
        self.add_btn_2.clicked.connect(self.choose_tag_color)
        self.commit_btn.clicked.connect(self.submit)

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
        if not cost[-1].isdigit():
            cost += '₽'
        if self.ingridients.toPlainText():
            print(self.ingridients.toPlainText(), type(self.ingridients.toPlainText()))
        query = f"""INSERT INTO Recipes (id, image, source, main_text, title, cost, tags_color) 
        VALUES ({self.recipe}, "{self.im}", "{self.source}", "{self.main_text.toPlainText()}", 
        "{self.title.text()}", "{cost}", "{self.tag_color}")"""
        self.db.cursor().execute(query)

        counter = 1
        for tag in self.tags:
            if tag not in self.db_tags:
                query1 = f"""INSERT INTO Tags (id, title) VALUES ({len(self.db_tags) + counter}, "{tag}")"""
                self.db.cursor().execute(query1)
                query1 = f"""INSERT INTO Recipes_Tags (recipesId, tagsId) VALUES 
                ({self.recipe}, {len(self.db_tags) + counter})"""
                self.db.cursor().execute(query1)
                counter += 1

        if self.db.cursor().execute(f"""SELECT id FROM Ingridients""").fetchall():
            db_ingridients = self.db.cursor().execute(f"""SELECT id FROM Ingridients""").fetchall()[0]
        else:
            db_ingridients = []
        query2 = f"""INSERT INTO Ingridients (id, list) VALUES ({len(db_ingridients) + 1}, 
        "{self.ingridients.toPlainText()}")"""
        self.db.cursor().execute(query2)
        query2 = f"""INSERT INTO Recipes_Ingridients (recipesId, ingridientsId) 
        VALUES ("{self.recipe}", "{len(db_ingridients) + 1}")"""
        self.db.cursor().execute(query2)
        self.db.commit()
        print('commit')
        self.db.close()
        self.hide()


class ViewingWindow(QDialog):
    def __init__(self, recipe_id):
        super().__init__()
        uic.loadUi('viewing_window.ui', self)
        self.setFixedSize(1100, 900)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.recipe_id = recipe_id
        self.db = sqlite3.connect("recipies.sqlite")

        res_recipe = self.db.cursor().execute(f"""SELECT image, title, main_text, tags_color, cost, source FROM Recipes
                WHERE id={self.recipe_id}""").fetchall()
        self.source = res_recipe[0][5]
        self.setWindowTitle(res_recipe[0][1])
        self.title.setText(res_recipe[0][1])
        self.main_text.setText(res_recipe[0][2])
        self.cost_line.setText(res_recipe[0][4])

        ic = QIcon(res_recipe[0][0])
        self.image_btn.setIcon(ic)
        self.image_btn.setIconSize(QtCore.QSize(579, 321))
        self.image_btn.setStyleSheet(f'border-radius: 15px;'
                                     f'background-color: rgb{middle_color(res_recipe[0][0])};')
        self.ingridients.setText(self.db.cursor().execute(f"""SELECT list FROM Ingridients
                        WHERE id IN (SELECT ingridientsId FROM Recipes_Ingridients
                        WHERE recipesId={self.recipe_id})""").fetchall()[0][0])

        print(res_recipe[0][3], 'color')
        self.tags_btn.setStyleSheet(f'background-color: rgb{res_recipe[0][3]};'
                                    'border-radius: 15px;'
                                    'font: 12pt "Leelawadee UI";'
                                    'padding-left: 20px;'
                                    'padding-right: 20px;'
                                    'text-align: left;')

        res_recipe = self.db.cursor().execute(f"""SELECT title FROM Tags
                        WHERE id IN (SELECT tagsId FROM Recipes_Tags 
                        WHERE recipesId={self.recipe_id})""").fetchall()
        self.tags_btn.setText('tags:  ' + '  '.join([x[0] for x in res_recipe]))

        if not self.source:
            self.source_btn.hide()
        else:
            self.source_btn.show()
        self.source_btn.clicked.connect(self.go_to_source)
        self.edit_btn.clicked.connect(self.edit_window)

    def go_to_source(self):
        os.system(f"start \" \" {self.source}")

    def edit_window(self):
        pass