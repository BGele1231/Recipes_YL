import sys
import sqlite3

from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtGui import QIcon, QPixmap, QImage


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

        self.initUI()

    def initUI(self):
        res = self.db.cursor().execute("""SELECT id FROM Recipes""").fetchall()
        # print(res)
        if len(res) % (self.page * 3) == 0:
            self.recipe_one_hide()
            self.recipe_two_hide()
            self.recipe_three_hide()
        elif len(res) % (self.page * 3) == 1:
            self.recipe_two_hide()
            self.recipe_three_hide()
            self.recipe_fill_id = len(res) - len(res) % 3 + 1
            self.recipe_fill_one()
        elif len(res) % (self.page * 3) == 2:
            self.recipe_three_hide()
            self.recipe_fill_id = len(res) - len(res) % 3 + 1
            self.recipe_fill_two()
        else:
            self.recipe_fill_id = len(res)
            self.recipe_fill_three()

    def recipe_one_hide(self):
        self.border_recipe_one.hide()
        self.title_one.hide()
        self.text_one.hide()
        self.image_one.hide()

    def recipe_two_hide(self):
        self.border_recipe_two.hide()
        self.title_two.hide()
        self.text_two.hide()
        self.image_two.hide()

    def recipe_three_hide(self):
        self.border_recipe_three.hide()
        self.title_three.hide()
        self.text_three.hide()
        self.image_three.hide()

    def recipe_fill_one(self):
        res_recipe = self.db.cursor().execute(f"""SELECT image, title, main_text FROM Recipes
        WHERE id={self.recipe_fill_id}""").fetchall()
        print(self.recipe_fill_id, res_recipe[0][0])
        # self.image_one.setPixmap(*res_recipe[0][0])
        self.title_one.setText(res_recipe[0][1])
        self.text_one.setText(res_recipe[0][2])

    def recipe_fill_two(self):
        res_recipe = self.db.cursor().execute(f"""SELECT image, title, main_text FROM Recipes
        WHERE id={self.recipe_fill_id}""").fetchall()
        self.image_two.setPixmap(res_recipe[0][0])
        self.title_two.setText(res_recipe[0][1])
        self.text_two.setText(res_recipe[0][2])

    def recipe_fill_three(self):
        res_recipe = self.db.cursor().execute(f"""SELECT image, title, main_text FROM Recipes
        WHERE id={self.recipe_fill_id}""").fetchall()
        self.image_three.setPixmap(res_recipe[0][0])
        self.title_three.setText(res_recipe[0][1])
        self.text_three.setText(res_recipe[0][2])

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
    sys.exit(app.exec_())