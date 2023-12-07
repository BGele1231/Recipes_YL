from addition import AddWindow, ViewingWindow, main_w_crop
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

        self.line_pages.setText('1')
        self.left_page_btn.clicked.connect(self.left_page)
        self.right_page_btn.clicked.connect(self.right_page)
        self.search_btn.clicked.connect(self.searching)
        self.plu_lg.pressed.connect(self.new_recipe)
        self.initUI()

    def initUI(self):
        # self.all_pages = [x[0] for x in self.db.cursor().execute("""SELECT id FROM Recipes""").fetchall()]
        self.pages = self.all_pages[(self.page - 1) * 3:self.page * 3]
        print('ui', self.pages, self.all_pages, len(self.all_pages) - len(self.pages) % 3)
        if len(self.pages) % (self.page * 3) == 0:
            self.recipe_one_hide()
            self.recipe_two_hide()
            self.recipe_three_hide()
        elif len(self.pages) % (self.page * 3) == 1:
            self.recipe_two_hide()
            self.recipe_three_hide()
            self.recipe_one_show()
            self.recipe_fill_id = self.pages[0]
            self.recipe_fill_one()
        elif len(self.pages) % (self.page * 3) == 2:
            self.recipe_three_hide()
            self.recipe_one_show()
            self.recipe_two_show()
            self.recipe_fill_id = self.pages[0]
            self.recipe_fill_one()
            self.recipe_fill_id = self.pages[1]
            self.recipe_fill_two()
        else:
            self.recipe_one_show()
            self.recipe_two_show()
            self.recipe_three_show()
            self.recipe_fill_id = self.pages[0]
            self.recipe_fill_one()
            self.recipe_fill_id = self.pages[1]
            self.recipe_fill_two()
            self.recipe_fill_id = self.pages[2]
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
        WHERE id={self.recipe_fill_id}""").fetchall()
        self.image_one.setStyleSheet(f'border-radius: 15px;'
                                     # f'background-color: rgb{middle_color(res_recipe[0][0])};'
                                     f'border-image: url({main_w_crop(res_recipe[0][0], self.recipe_fill_id)})')
        # self.image_one.adjustSize()
        # self.image_one.setPixmap(QPixmap(res_recipe[0][0]).scaled(340, 201))

        self.title_one.setText(res_recipe[0][1])
        self.text_one.setText(self.db.cursor().execute(f"""SELECT list FROM Ingridients
                WHERE id IN (SELECT ingridientsId FROM Recipes_Ingridients
                WHERE recipesId={self.recipe_fill_id})""").fetchall()[0][0])
        self.tags_line_one.setStyleSheet(f'background-color: rgb{res_recipe[0][-1]};'
                                         'border-radius: 15px;'
                                         'font: 12pt "Leelawadee UI";'
                                         'padding-left: 20px;'
                                         'padding-right: 20px;')

        res_recipe = self.db.cursor().execute(f"""SELECT title FROM Tags
                WHERE id IN (SELECT tagsId FROM Recipes_Tags 
                WHERE recipesId={self.recipe_fill_id})""").fetchall()
        if res_recipe:
            self.tags_line_one.show()
            self.tags_line_one.setText('tags:  ' + '  '.join([x[0] for x in res_recipe]))
        else:
            self.tags_line_one.hide()

    def recipe_fill_two(self):
        res_recipe = self.db.cursor().execute(f"""SELECT image, title, main_text, tags_color FROM Recipes
        WHERE id={self.recipe_fill_id}""").fetchall()
        self.image_two.setStyleSheet(f'border-radius: 15px;'
                                     f'border-image: url({main_w_crop(res_recipe[0][0], self.recipe_fill_id)})')
        # self.image_two.adjustSize()
        # self.image_two.setPixmap(QPixmap(res_recipe[0][0]).scaled(340, 201))
        self.title_two.setText(res_recipe[0][1])
        self.text_two.setText(self.db.cursor().execute(f"""SELECT list FROM Ingridients
                WHERE id IN (SELECT ingridientsId FROM Recipes_Ingridients
                WHERE recipesId={self.recipe_fill_id})""").fetchall()[0][0])

        self.tags_line_two.setStyleSheet(f'background-color: rgb{res_recipe[0][-1]};'
                                         'border-radius: 15px;'
                                         'font: 12pt "Leelawadee UI";'
                                         'padding-left: 20px;'
                                         'padding-right: 20px;')

        res_recipe = self.db.cursor().execute(f"""SELECT title FROM Tags
                        WHERE id IN (SELECT tagsId FROM Recipes_Tags 
                        WHERE recipesId={self.recipe_fill_id})""").fetchall()
        if res_recipe:
            self.tags_line_two.show()
            self.tags_line_two.setText('tags:  ' + '  '.join([x[0] for x in res_recipe]))
        else:
            self.tags_line_two.hide()

    def recipe_fill_three(self):
        res_recipe = self.db.cursor().execute(f"""SELECT image, title, main_text, tags_color FROM Recipes
                WHERE id={self.recipe_fill_id}""").fetchall()
        self.image_three.setStyleSheet(f'border-radius: 15px;'
                                     f'border-image: url({main_w_crop(res_recipe[0][0], self.recipe_fill_id)})')
        self.title_three.setText(res_recipe[0][1])
        self.text_three.setText(self.db.cursor().execute(f"""SELECT list FROM Ingridients
                        WHERE id IN (SELECT ingridientsId FROM Recipes_Ingridients
                        WHERE recipesId={self.recipe_fill_id})""").fetchall()[0][0])

        self.tags_line_three.setStyleSheet(f'background-color: rgb{res_recipe[0][-1]};'
                                         'border-radius: 15px;'
                                         'font: 12pt "Leelawadee UI";'
                                         'padding-left: 20px;'
                                         'padding-right: 20px;')

        res_recipe = self.db.cursor().execute(f"""SELECT title FROM Tags
                                WHERE id IN (SELECT tagsId FROM Recipes_Tags 
                                WHERE recipesId={self.recipe_fill_id})""").fetchall()
        if res_recipe:
            self.tags_line_three.show()
            self.tags_line_three.setText('tags:  ' + '  '.join([x[0] for x in res_recipe]))
        else:
            self.tags_line_three.hide()

    def searching(self):
        query = self.search_line.text()
        print(query.capitalize(), 'query')
        if query:
            self.all_pages = self.db.cursor().execute(f"""SELECT id FROM Recipes
            WHERE title LIKE '%{query.lower()}%'""").fetchall()
            if self.all_pages:
                self.all_pages = [x[0] for x in self.all_pages]
        else:
            self.all_pages = [x[0] for x in self.db.cursor().execute("""SELECT id FROM Recipes""").fetchall()]
        print(self.all_pages, 'searching pages')
        self.initUI()

    def left_page(self):
        if self.page != 1:
            self.page -= 1
            self.pages = self.all_pages[3 * self.page - 1:]
            self.line_pages.setText(self.page)
            self.initUI()

    def right_page(self):
        if math.ceil(len(self.pages) / 3) != self.page:
            self.page += 1
            self.pages = self.all_pages[3 * self.page - 1:]
            self.line_pages.setText(self.page)
            self.initUI()

    def new_recipe(self):
        self.dialog = AddWindow()
        self.dialog.show()
        self.initUI()

    def mousePressEvent(self, event):
        if 125 < event.x() < 495 and 235 < event.y() < 756:
            print(1)
            self.recipe_first()
        if 529 < event.x() < 899 and 235 < event.y() < 756:
            print(2)
            self.recipe_second()
        if 925 < event.x() < 1295 and 235 < event.y() < 756:
            print(3)
            self.recipe_third()

    def recipe_first(self):
        self.viewing = ViewingWindow(self.pages[0])
        self.viewing.show()

    def recipe_second(self):
        self.viewing = ViewingWindow(self.pages[1])
        self.viewing.show()

    def recipe_third(self):
        self.viewing = ViewingWindow(self.pages[2])
        self.viewing.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
