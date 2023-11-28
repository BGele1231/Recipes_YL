from addition import AddWindow, middle_color
import sys
import sqlite3
import math

from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5 import QtCore

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_window.ui', self)  # Загружаем дизайн
        self.setFixedSize(1400, 900)  # Resize blocked
        self.setWindowTitle('Recipes')

        self.db = sqlite3.connect("recipies.sqlite")

        self.recipe_id = 1
        self.recipe_fill_id = 1
        self.page = 1
        self.all_pages = [x[0] for x in self.db.cursor().execute("""SELECT id FROM Recipes""").fetchall()]
        self.pages = self.all_pages[:3]

        self.page_box.setMaximum(math.ceil(len(self.all_pages) / 3))
        self.left_page_btn.clicked.connect(self.left_page)
        self.right_page_btn.clicked.connect(self.right_page)
        self.search_btn.clicked.connect(self.searching)
        self.plu_lg.pressed.connect(self.new_recipe)
        self.initUI()

    def initUI(self):
        self.all_pages = [x[0] for x in self.db.cursor().execute("""SELECT id FROM Recipes""").fetchall()]
        self.pages = self.all_pages[:3]
        print('ui', self.pages)
        if len(self.pages) % (self.page * 3) == 0:
            self.recipe_one_hide()
            self.recipe_two_hide()
            self.recipe_three_hide()
        elif len(self.pages) % (self.page * 3) == 1:
            self.recipe_two_hide()
            self.recipe_three_hide()
            self.recipe_one_show()
            self.recipe_fill_id = len(self.pages) - len(self.pages) % 3 + 1
            self.recipe_fill_one()
        elif len(self.pages) % (self.page * 3) == 2:
            self.recipe_three_hide()
            self.recipe_one_show()
            self.recipe_two_show()
            self.recipe_fill_id = len(self.pages) - len(self.pages) % 3
            self.recipe_fill_one()
            self.recipe_fill_id = len(self.pages) - len(self.pages) % 3 + 1
            self.recipe_fill_two()
        else:
            self.recipe_one_show()
            self.recipe_two_show()
            self.recipe_three_show()
            self.recipe_fill_id = len(self.pages) - 2
            self.recipe_fill_one()
            self.recipe_fill_id = len(self.pages) - 1
            self.recipe_fill_two()
            self.recipe_fill_id = len(self.pages)
            self.recipe_fill_three()

    def recipe_one_hide(self):
        self.border_recipe_one.hide()
        self.title_one.hide()
        self.text_one.hide()
        self.image_one.hide()
        self.tags_line_one.hide()

    def recipe_two_hide(self):
        self.border_recipe_two.hide()
        self.title_two.hide()
        self.text_two.hide()
        self.image_two.hide()
        self.tags_line_two.hide()

    def recipe_three_hide(self):
        self.border_recipe_three.hide()
        self.title_three.hide()
        self.text_three.hide()
        self.image_three.hide()
        self.tags_line_three.hide()

    def recipe_one_show(self):
        self.border_recipe_one.show()
        self.title_one.show()
        self.text_one.show()
        self.image_one.show()
        self.tags_line_one.show()

    def recipe_two_show(self):
        self.border_recipe_two.show()
        self.title_two.show()
        self.text_two.show()
        self.image_two.show()
        self.tags_line_two.show()

    def recipe_three_show(self):
        self.border_recipe_three.show()
        self.title_three.show()
        self.text_three.show()
        self.image_three.show()
        self.tags_line_three.show()

    def recipe_fill_one(self):
        print(self.recipe_fill_id)
        res_recipe = self.db.cursor().execute(f"""SELECT image, title, main_text, tags_color FROM Recipes
        WHERE id={self.recipe_fill_id + 1}""").fetchall()
        print(res_recipe)
        self.image_one.setStyleSheet(f'border-radius: 15px;'
                                     # f'background-color: rgb{middle_color(res_recipe[0][0])};'
                                     f'border-image: url({res_recipe[0][0]})')
        self.image_one.adjustSize()
        # self.image_one.setPixmap(QPixmap(res_recipe[0][0]).scaled(340, 201))

        self.title_one.setText(res_recipe[0][1])
        # self.text_one.setText(res_recipe[0][2])
        # print(res_recipe[0][-1])
        self.tags_line_one.setStyleSheet(f'background-color: rgb({res_recipe[0][-1]});'
                                         'border-radius: 15px;'
                                         'font: 12pt "Leelawadee UI";'
                                         'padding-left: 20px;'
                                         'padding-right: 20px;')

        res_recipe = self.db.cursor().execute(f"""SELECT title FROM Tags
                WHERE id IN (SELECT tagsId FROM Recipes_Tags 
                WHERE resipesId={self.recipe_fill_id + 1})""").fetchall()
        self.tags_line_one.setText('tags:  ' + '  '.join([x[0] for x in res_recipe]))
        # self.recipe_fill_id += 1

    def recipe_fill_two(self):
        print(self.recipe_fill_id)
        res_recipe = self.db.cursor().execute(f"""SELECT image, title, main_text, tags_color FROM Recipes
        WHERE id={self.recipe_fill_id + 1}""").fetchall()
        print(res_recipe)
        self.image_two.setStyleSheet(f'border-radius: 15px;'
                                     f'border-image: url({res_recipe[0][0]})')
        self.image_two.adjustSize()
        # self.image_two.setPixmap(QPixmap(res_recipe[0][0]).scaled(340, 201))
        self.title_two.setText(res_recipe[0][1])
        # self.text_two.setText(res_recipe[0][2])

        self.tags_line_one.setStyleSheet(f'background-color: rgb({res_recipe[0][-1]});'
                                         'border-radius: 15px;'
                                         'font: 12pt "Leelawadee UI";'
                                         'padding-left: 20px;'
                                         'padding-right: 20px;')

        res_recipe = self.db.cursor().execute(f"""SELECT title FROM Tags
                        WHERE id IN (SELECT tagsId FROM Recipes_Tags 
                        WHERE resipesId={self.recipe_fill_id + 1})""").fetchall()
        self.tags_line_two.setText('tags:  ' + '  '.join([x[0] for x in res_recipe]))

    def recipe_fill_three(self):
        res_recipe = self.db.cursor().execute(f"""SELECT image, title, main_text, tags_color FROM Recipes
        WHERE id={self.recipe_fill_id + 1}""").fetchall()
        self.image_three.setPixmap(QPixmap(res_recipe[0][0]).scaled(340, 201))
        self.title_three.setText(res_recipe[0][1])
        # self.text_three.setText(res_recipe[0][2])

        res_recipe = self.db.cursor().execute(f"""SELECT title FROM Tags
                        WHERE id IN (SELECT tagsId FROM Recipes_Tags 
                        WHERE resipesId={self.recipe_fill_id})""").fetchall()
        self.tags_line_three.setText('tags:  ' + '  '.join([x[0] for x in res_recipe]))

    def searching(self):
        query = self.search_line.text()
        # print(query)
        self.pages = self.db.cursor().execute(f"""SELECT id FROM Recipes
        WHERE title LIKE '%{query}%'""").fetchall()
        if self.pages:
            self.pages = self.pages[0]
        print(self.pages)
        self.initUI()

    def left_page(self):
        if self.page != 1:
            self.page -= 1
            self.pages = self.all_pages[3 * self.page - 1:]
            self.initUI()

    def right_page(self):
        if math.ceil(len(self.pages) / 3) != self.page:
            self.page += 1
            self.pages = self.all_pages[3 * self.page - 1:]
            self.initUI()

    def new_recipe(self):
        self.dialog = AddWindow()
        self.dialog.show()
        self.initUI()

    def mousePressEvent(self, event):
        if 125 < event.x() < 495 and 235 < event.y() < 756:
            self.recipe_id = None
            self.recipe()

    def recipe(self):
        print('2')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
