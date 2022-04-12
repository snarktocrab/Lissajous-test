# -*- coding: utf-8 -*-
import sys
import os
import PyQt5.QtWidgets as qt
from PyQt5 import uic, QtGui
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
import json
import locale

from lissajousgen import LissajousGenerator, lissajous_figure


# Настройки фигуры по умолчанию
default_settings = {
    "freq_x": 2,
    "freq_y": 3,
    "color": "midnightblue",
    "width": 2,
    "resolution": 200,
    "phase_shift": 0
}


# Цвета для matplotlib
with open("mpl.json", mode="r", encoding="utf-8") as f:
    mpl_color_dict = json.load(f)


class LissajousWindow(qt.QMainWindow):
    def __init__(self):
        super(LissajousWindow, self).__init__()

        # Загружаем интерфейс из файла
        uic.loadUi("main_window_dynamic.ui", self)

        # Ставим версию и иконку
        with open("version.txt", "r") as f:
            version = f.readline()
        self.setWindowTitle("Генератор фигур Лиссажу. Версия {}. CC BY-SA 4.0 Ivanov".format(
            version
        ))
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        icon = QtGui.QIcon()
        icon.addFile(scriptDir + os.path.sep + "icons" + os.path.sep + "icon_32.bmp")
        icon.addFile(scriptDir + os.path.sep + "icons" + os.path.sep + "icon_64.bmp")
        icon.addFile(scriptDir + os.path.sep + "icons" + os.path.sep + "icon_128.bmp")
        #self.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep + "icon_64.bmp"))
        self.setWindowIcon(icon)

        # Создаём холст matplotlib
        self._fig = plt.figure(figsize=(4, 3), dpi=72)
        # Добавляем на холст matplotlib область для построения графиков.
        # В общем случае таких областей на холсте может быть несколько
        # Аргументы add_subplot() в данном случае:
        # ширина сетки, высота сетки, номер графика в сетке
        self._ax = self._fig.add_subplot(1, 1, 1)

        # Создаём qt-виджет холста для встраивания холста
        # matplotlib fig в окно Qt.
        self._fc = FigureCanvas(self._fig)
        # Связываем созданный холст c окном
        #self._fc.setParent(self.widget)
        self.centralwidget.layout().addWidget(self._fc)
        
        # Настраиваем размер и положение холста
        self._fc.setMinimumSize(400, 300)

        # Первичное построение фигуры
        self.plot_lissajous_figure()

        #self.resize(700, 300)
        self.plot_button.clicked.connect(self.plot_button_click_handler)
        self.save_button.clicked.connect(self.save_button_click_handler)

    def plot_button_click_handler(self):
        """
        Обработчик нажатия на кнопку применения настроек
        """
        # Получаем данные из текстовых полей
        settings = {}
        color = self.color_combobox.currentText()
        settings["freq_x"] = float(self.freq_x_lineedit.text())
        settings["freq_y"] = float(self.freq_y_lineedit.text())
        settings["color"] = mpl_color_dict[color]
        settings["width"] = int(self.width_combobox.currentText())
        settings["resolution"] = int(self.resolution_lineedit.text())
        settings["phase_shift"] = float(self.phase_shift_lineedit.text())

        # Перестраиваем график
        self.plot_lissajous_figure(settings)

    def plot_lissajous_figure(self, settings=default_settings):
        """
        Обновление фигуры
        """
        # Удаляем устаревшие данные с графика
        for line in self._ax.lines:
            line.remove()

        # Генерируем сигнал для построения
        self.generator = LissajousGenerator(resolution=settings["resolution"])
        figure = lissajous_figure([0, 1, 2, 3], [0, 2, 1, 3])
        figure = self.generator.generate_figure(settings["freq_x"],
                                                settings["freq_y"],
                                                settings["phase_shift"])

        # Строим график
        self._ax.plot(figure.x_arr, figure.y_arr,
                      color=settings["color"], linewidth=settings["width"])

        plt.axis("off")

        # Нужно, чтобы все элементы не выходили за пределы холста
        plt.tight_layout()

        # Обновляем холст в окне
        self._fc.draw()

    def save_button_click_handler(self):
        """
        Обработчик нажатия на кнопку сохранения настроек
        """
        file_path, _ = qt.QFileDialog.getSaveFileName(self, "Сохранение изображения", "C:\\",
                                                            "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")

        if file_path == "":
            return
        
        error_message = f"Файл {file_path} создан успешно."
        try:
            plt.savefig(file_path)
        except PermissionError:
            error_message = f"Невозможно создать файл {file_path}: в доступе отказано."
            print(error_message)
        except Exception as e:
            error_message = f"Непредусмотренная ошибка: {str(e)}"
            print(e)
        finally:
            msg = qt.QMessageBox()
            msg.setText(error_message)
            msg.exec()
            print(error_message)
        #raise NotImplementedError("Тут всего одной строчки не хватает.")


if __name__ == "__main__":
    # Инициализируем приложение Qt
    app = qt.QApplication(sys.argv)
    ##app.setAttribute(QtCore.qt.AA_EnableHighDpiScaling)

    # Создаём и настраиваем главное окно
    main_window = LissajousWindow()

    # Показываем окно
    main_window.show()

    # Запуск приложения
    # На этой строке выполнение основной программы блокируется
    # до тех пор, пока пользователь не закроет окно.
    # Вся дальнейшая работа должна вестись либо в отдельных потоках,
    # либо в обработчиках событиt Qt.
    #app.exec_()
    sys.exit(app.exec_())
