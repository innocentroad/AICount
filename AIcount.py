import sys
import configparser
import os
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QMenu, QAction
from PyQt5.QtGui import QFont, QColor, QPainter, QPen, QIcon
from PyQt5.QtCore import Qt
import keyboard

class CounterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.count = 1
        self.reset_number = 2
        self.reset_number_2 = 3
        self.change_hotkey = "Shift"
        self.count_hotkey = "Ctrl"
        self.current_reset_number = 3
        self.display_additional_text = True
        self.prefix_text = "AI"
        self.small_font_color = 'snow'  # デフォルトの小さなテキストのフォントカラー
        self.x_offset = -70  # デフォルトのオフセット
        self.y_offset = 30  # デフォルトのオフセット
        self.outline_color = 'black'  # デフォルトのアウトラインの色
        self.initUI()
        self.load_settings()

        keyboard.on_press_key(self.count_hotkey, self.increment_count)
        keyboard.on_press_key(self.change_hotkey, self.change_settings)

    def initUI(self):
        self.setWindowTitle("Counter App")
        self.setGeometry(100, 100, 300, 200)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setStyleSheet("background-color: rgba(0, 0, 0, 0);")

        self.label = QLabel("AI 1", self)
        self.label.setGeometry(50, 50, 200, 100)
        self.label.setAlignment(Qt.AlignCenter)

        font = QFont("Meiryo")
        font.setPointSize(24)
        font.setStyleStrategy(QFont.PreferAntialias)
        self.label.setFont(font)
        self.label.setStyleSheet("color: Snow;")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.setFont(self.label.font())

        painter.setPen(self.outline_pen)

        rect = self.label.geometry()
        text_width = painter.fontMetrics().width(self.label.text())
        text_height = painter.fontMetrics().height()

        for dx in [-2, 0, 2]:
            for dy in [-2, 0, 2]:
                painter.drawText(rect.translated(dx, dy), Qt.AlignCenter, self.label.text())

        if self.display_additional_text:
            additional_text = ""
            if self.current_reset_number == self.reset_number:
                additional_text = "1"
            elif self.current_reset_number == self.reset_number_2:
                additional_text = "2"
            
            font = QFont("Meiryo")
            font.setPointSize(9)
            painter.setFont(font)
            additional_text_width = painter.fontMetrics().width(additional_text)
            additional_text_height = painter.fontMetrics().height()
            
            outline_pen = QPen(self.outline_pen.color())
            outline_pen.setWidth(4)
            painter.setPen(outline_pen)

            # 文字の描画位置を調整する
            x_offset = rect.width() - additional_text_width - text_width + self.x_offset
            y_offset = self.y_offset
            
            painter.drawText(rect.adjusted(x_offset, y_offset, 0, 0), Qt.AlignLeft, additional_text)

            painter.setPen(QColor(self.small_font_color))
            painter.drawText(rect.adjusted(x_offset, y_offset, 0, 0), Qt.AlignLeft, additional_text)

    def load_settings(self):
        config = configparser.ConfigParser()
        config.read('config.ini')

        self.reset_number = int(config['Settings']['reset_number'])
        self.reset_number_2 = int(config['Settings']['reset_number_2'])
        self.change_hotkey = config['Settings']['change_hotkey']
        self.count_hotkey = config['Settings']['count_hotkey']
        self.current_reset_number = self.reset_number

        self.display_additional_text = config.getboolean('Settings', 'display_additional_text', fallback=True)
  
        self.prefix_text = config['Settings'].get('prefix_text', 'AI')
        self.small_font_color = config['Settings'].get('small_font_color', 'Red')
        outline_color = config['Settings'].get('outline_color', 'black')
        self.outline_pen = QPen(QColor(outline_color))
        self.outline_pen.setWidth(4)

        self.font_color = config['Settings'].get('font_color', 'Snow')
        self.switch_font_color = config['Settings'].get('switch_font_color', 'Red')

        self.x_offset = int(config['Settings'].get('x_offset', -70))  # xオフセットを読み込む
        self.y_offset = int(config['Settings'].get('y_offset', 30))  # yオフセットを読み込む
        
        self.label.setText(f"{self.prefix_text} {self.count}")
        self.label.setStyleSheet(f"color: {self.font_color};")


    def increment_count(self, event):
        self.count += 1
        if self.count > self.current_reset_number:
            self.count = 1
        self.label.setText(f"{self.prefix_text} {self.count}")
        self.update()

    def change_settings(self, event):
        current_style_sheet = self.label.styleSheet()
        if self.current_reset_number == self.reset_number:
            self.current_reset_number = self.reset_number_2
            self.label.setStyleSheet(f"color: {self.switch_font_color}; background-color: rgba(0, 0, 0, 0);")
        else:
            self.current_reset_number = self.reset_number
            self.label.setStyleSheet(f"color: {self.font_color}; background-color: rgba(0, 0, 0, 0);")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = event.globalPos() - self.pos()
        elif event.button() == Qt.RightButton:
            self.contextMenuEvent(event)

    def mouseMoveEvent(self, event):
        self.move(event.globalPos() - self.offset)

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        exit_action = QAction("終了", self)
        exit_action.triggered.connect(QApplication.instance().quit)
        menu.addAction(exit_action)
        menu.setStyleSheet("QMenu { color: white; background-color: rgba(50, 50, 50, 150); }" 
                           "QMenu::item:selected { background-color: rgba(100, 100, 100, 150); }")
        menu.addSeparator()
        cancel_action = QAction("戻る", self)
        cancel_action.triggered.connect(menu.close)
        menu.addAction(cancel_action)
        menu.exec_(self.mapToGlobal(event.pos()))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    counter_app = CounterApp()
    counter_app.show()

    # アイコンを読み込む
    if getattr(sys, 'frozen', False):
        icon_path = os.path.join(sys._MEIPASS, "AIcount128.ico") # 実行中のスクリプトがexeファイルにパッケージ化された場合
    else:
        icon_path = "AIcount128.ico" # 通常のPythonスクリプトの場合
    app.setWindowIcon(QIcon(icon_path))
    sys.exit(app.exec_())
