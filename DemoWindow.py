from PySide6.QtWidgets import QWidget, QPushButton, QListWidget, QApplication, QListWidgetItem, QInputDialog
import Demo
import Map


def do_map():
    Map.get_map()


class Comp490DemoWindow(QWidget):
    def __init__(self, data_to_show, sheet):
        super().__init__()
        self.win = QWidget()
        self.sheet = sheet
        self.data = data_to_show
        self.list_control = None
        self.setup_window()

    def setup_window(self):
        self.setWindowTitle("GUI: Demo Data")
        self.setGeometry(300, 100, 400, 200)
        quit_button = QPushButton("Quit Now", self)
        quit_button.clicked.connect(QApplication.instance().quit)
        quit_button.resize(quit_button.sizeHint())
        quit_button.move(280, 150)
        data_visual = QPushButton("Visualize Data", self)
        data_visual.move(30, 30)
        data_visual.clicked.connect(self.do_visualize_data)
        comp490_demo_button = QPushButton("Update Data", self)
        comp490_demo_button.move(280, 30)
        comp490_demo_button.clicked.connect(self.do_update_data)
        self.setStyleSheet("background-color: rgb(15, 15, 15); color: green;")
        self.show()

    def put_data_in_list(self):
        display_list = QListWidget(self.win)
        self.win.list_control = display_list
        display_list.resize(600, 500)
        display_list.move(0, 100)
        order = QPushButton("Change Order", self.win)
        order.move(280, 70)
        order.clicked.connect(self.order_list)
        for item in self.data:
            display_text = f"{item['id']}\t\t{item['school.name']}"
            list_item = QListWidgetItem(display_text, listview=self.win.list_control)
        order.show()
        display_list.show()

    def order_list(self):
        display_list = QListWidget(self.win)
        self.win.list_control = display_list
        display_list.resize(600, 500)
        display_list.move(0, 100)
        self.data.reverse()
        for item in self.data:
            display_text = f"{item['id']}\t\t{item['school.name']}"
            list_item = QListWidgetItem(display_text, listview=self.win.list_control)
        display_list.show()

    def do_visualize_data(self):
        self.win.setWindowTitle("Visualize Data")
        self.win.setGeometry(500, 300, 600, 600)
        self.win.setStyleSheet("background-color: rgb(15, 15, 15); color: green;")
        button = QPushButton("Show Data in Text", self.win)
        button.move(280, 30)
        button.clicked.connect(self.put_data_in_list)
        map_button = QPushButton("Show Data in Map", self.win)
        map_button.move(30, 30)
        map_button.clicked.connect(do_map)
        self.win.show()

    def do_update_data(self):
        text, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter text:')
        if ok:
            self.sheet = Demo.setup_xl(text)

