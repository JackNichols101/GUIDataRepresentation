from PyQt5.QtWidgets import qApp
from PySide2.QtGui import QFont, QColor
from PySide2.QtWebEngineWidgets import QWebEngineView
from PySide2.QtWidgets import QListWidget, QListWidgetItem, QInputDialog, \
    QDesktopWidget, QAction, QMenu, QMainWindow
import Demo


class Comp490DemoWindow(QMainWindow):
    def __init__(self, data_set, html):
        super().__init__()
        self.data_set = data_set
        self.list_control = None
        self.create_ui()
        self.html = html

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def create_ui(self):
        exit_app = QAction('&Exit', self)
        exit_app.setShortcut('Ctrl+Q')
        exit_app.setStatusTip('Exit application')
        exit_app.triggered.connect(qApp.quit)
        update_file = QAction('Update', self)
        update_file.setShortcut('Ctrl+u')
        update_file.setStatusTip('Enter new file to update data')
        update_file.triggered.connect(self.do_update_data)
        a_num_grads = QAction('Ascending Number Of College Grads', self)
        a_num_grads.triggered.connect(self.ascending_grads)
        d_num_grads = QAction('Descending Number Of College Grads', self)
        d_num_grads.triggered.connect(self.descending_grads)
        a_salary = QAction('Ascending Lower 25 percent Salary', self)
        a_salary.triggered.connect(self.ascending_salary)
        d_salary = QAction('Descending Lower 25 percent Salary', self)
        d_salary.triggered.connect(self.descending_salary)
        graph = QAction('Choropleth Map', self)
        graph.triggered.connect(self.do_map_method_one)
        graph_two = QAction('Choropleth Map', self)
        graph_two.triggered.connect(self.do_map_method_two)
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('&File')
        file_menu.addAction(exit_app)
        file_menu.addAction(update_file)
        self.statusBar()
        submenu = QMenu('College Grads vs Total Employment', self)
        submenu2 = QMenu('Cohort Declining Balance vs Annual Salary', self)
        submenu.addAction(a_num_grads)
        submenu.addAction(d_num_grads)
        submenu.addAction(graph)
        submenu2.addAction(a_salary)
        submenu2.addAction(d_salary)
        submenu2.addAction(graph_two)
        menu_bar.addMenu(submenu)
        menu_bar.addMenu(submenu2)
        self.resize(640, 500)
        self.center()
        self.setWindowTitle('Data GUI')
        self.show()

    def do_update_data(self):
        en = QInputDialog(self)
        en.resize(600, 120)
        text, ok = en.getText(self, 'Please Wait', 'Enter new file:')
        if ok:
            print(text)
            connection, cursor = Demo.open_db('college_data.db')
            self.data_set, self.html = Demo.update_file(text, cursor)

    def do_map_method_one(self):
        plot_widget = QWebEngineView(self)
        plot_widget.setHtml(self.html[0])
        plot_widget.move(0, 20)
        plot_widget.setMinimumSize(640, 480)
        plot_widget.show()

    def do_map_method_two(self):
        plot_widget = QWebEngineView(self)
        plot_widget.setHtml(self.html[1])
        plot_widget.move(0, 20)
        plot_widget.setMinimumSize(640, 480)
        plot_widget.show()

    def ascending_grads(self):
        color = 0
        display_list = QListWidget(self)
        self.list_control = display_list
        display_list.move(0, 21)
        display_list.setFont(QFont('Courier', 10))
        display_list.setMinimumSize(640, 479)
        self.data_set = sorted(self.data_set, key=lambda l: l[1])
        headers = ["State", "College Graduates", "Total Employment"]
        display_text = f"{headers[0].ljust(25)}{headers[1].ljust(25)}{headers[2]}"
        list_item = QListWidgetItem(display_text, listview=self.list_control)
        for item in self.data_set:
            color = color + 1
            display_text = f"{item[0].ljust(25)}{str(item[1]).ljust(25)}{item[2]}"
            list_item = QListWidgetItem(display_text, listview=self.list_control)
            list_item.setForeground(QColor(255 - 4*color, 4*color, 0))
            list_item.setBackground(QColor(0, 0, 0))
        display_list.show()

    def ascending_salary(self):
        color = 0
        display_list = QListWidget(self)
        self.list_control = display_list
        display_list.move(0, 21)
        display_list.setFont(QFont('Courier', 10))
        display_list.setMinimumSize(640, 479)
        self.data_set = sorted(self.data_set, key=lambda l: l[3])
        headers = ["State", "Lower 25% Salary", "Declining Balance %"]
        display_text = f"{headers[0].ljust(25)}{headers[1].ljust(25)}{headers[2]}"
        list_item = QListWidgetItem(display_text, listview=self.list_control)
        for item in self.data_set:
            color = color + 1
            display_text = f"{item[0].ljust(25)}{str(item[3]).ljust(25)}{item[4]}"
            list_item = QListWidgetItem(display_text, listview=self.list_control)
            list_item.setForeground(QColor(255 - 4*color, 4*color, 0))
            list_item.setBackground(QColor(0, 0, 0))
        display_list.show()

    def descending_salary(self):
        color = 0
        display_list = QListWidget(self)
        self.list_control = display_list
        display_list.move(0, 21)
        display_list.setFont(QFont('Courier', 10))
        display_list.setMinimumSize(640, 479)
        self.data_set = sorted(self.data_set, key=lambda l: l[3], reverse=True)
        headers = ["State", "Lower 25% Salary", "Declining Balance %"]
        display_text = f"{headers[0].ljust(25)}{headers[1].ljust(25)}{headers[2]}"
        list_item = QListWidgetItem(display_text, listview=self.list_control)
        for item in self.data_set:
            color = color + 1
            display_text = f"{item[0].ljust(25)}{str(item[3]).ljust(25)}{item[4]}"
            list_item = QListWidgetItem(display_text, listview=self.list_control)
            list_item.setForeground(QColor(4*color, 255 - 4*color, 0))
            list_item.setBackground(QColor(0, 0, 0))
        display_list.show()

    def descending_grads(self):
        color = 0
        display_list = QListWidget(self)
        self.list_control = display_list
        display_list.move(0, 21)
        display_list.setFont(QFont('Courier', 10))
        display_list.setMinimumSize(640, 479)
        self.data_set = sorted(self.data_set, key=lambda l: l[1], reverse=True)
        headers = ["State", "College Graduates", "Total Employment"]
        display_text = f"{headers[0].ljust(25)}{headers[1].ljust(25)}{headers[2]}"
        list_item = QListWidgetItem(display_text, listview=self.list_control)
        for item in self.data_set:
            color = color + 1
            display_text = f"{item[0].ljust(25)}{str(item[1]).ljust(25)}{item[2]}"
            list_item = QListWidgetItem(display_text, listview=self.list_control)
            list_item.setForeground(QColor(4*color, 255 - 4*color, 0))
            list_item.setBackground(QColor(0, 0, 0))
        display_list.show()