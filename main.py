from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from Controller.SqliteHelper import *
from Common.Threads import *
import os
import subprocess
import hashlib
from Register import *
from itertools import islice

def chunk(arr_range, arr_size):
    arr_range = iter(arr_range)
    return iter(lambda: tuple(islice(arr_range, arr_size)), ())

            
class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        # self.resize(700,  600)
        time_expiration = bullshit()
        self.setStyleSheet(
            """
            QPushButton {
                border-style: outset;
                border-radius: 0px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #cf7500;
                border-style: inset;
            }
            QPushButton:pressed {
                background-color: #ffa126;
                border-style: inset;
            }
            """
        )
        
        try:
            self.configs = read_js(path= PATH + "/config.json" )
        except:
            self.configs = {"number_thread" : 5,
                            "token_proxy" : ""}
        # set logo
        self.setWindowIcon(QtGui.QIcon(PATH + '/logo.ico'))
        self.setWindowTitle("Tool Auto Fifa v0.1")
        self.centralwidget = QtWidgets.QWidget(parent=self)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        
        self.groupBox = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.groupBox.setMinimumSize(QtCore.QSize(280, 200))
        self.groupBox.setMaximumSize(QtCore.QSize(280, 500))
        self.groupBox.setObjectName("groupBox")
        self.groupBox.setTitle("Cấu hình chung")
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        
        # Chọn luồng
        self.label = QtWidgets.QLabel(parent=self.groupBox)
        self.label.setObjectName("label")
        self.label.setText("Số luồng:")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)

        self.spinBox_numberthread = QtWidgets.QSpinBox(parent=self.groupBox)
        self.spinBox_numberthread.setMinimumSize(QtCore.QSize(0, 30))
        self.spinBox_numberthread.setObjectName("spinBox_numberthread")
        self.spinBox_numberthread.setProperty("value", self.configs['number_thread'])
        self.gridLayout_2.addWidget(self.spinBox_numberthread, 0, 1, 1, 1)
        
        self.label = QtWidgets.QLabel(parent=self.groupBox)
        self.label.setObjectName("label")
        self.label.setText("Nhập key proxy:")
        self.gridLayout_2.addWidget(self.label, 1, 0, 1, 1)
        
        self.plainTextEdit_proxy = QPlainTextEdit(parent=self.groupBox)
        self.plainTextEdit_proxy.setMinimumSize(QtCore.QSize(0, 100))
        self.plainTextEdit_proxy.setObjectName(f"plainTextEdit_proxy")
        self.plainTextEdit_proxy.insertPlainText(self.configs["token_proxy"])
        self.plainTextEdit_proxy.setPlaceholderText("Nhập key proxy tmproxy.com")
        self.gridLayout_2.addWidget(self.plainTextEdit_proxy, 1, 1, 1, 1)
            
        self.groupBox_2 = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.groupBox_2.setMinimumSize(QtCore.QSize(400, 100))
        self.groupBox_2.setTitle("Nhập tài khoản")
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout.addWidget(self.groupBox_2, 0, 1, 5, 1)
        
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        
        self.plainTextEdit_accs = QPlainTextEdit(parent=self.groupBox_2)
        self.plainTextEdit_accs.setMinimumSize(QtCore.QSize(0, 100))
        self.plainTextEdit_accs.setObjectName(f"plainTextEdit_accs")
        # self.plainTextEdit_accs.insertPlainText(self.configs["accs"])
        self.plainTextEdit_accs.setPlaceholderText("dangky2010ss|Trungtrau@123\nMinhMocc123dd|Trungtrau@123\nlongdz1022|Trunghoang@256")
        self.gridLayout_3.addWidget(self.plainTextEdit_accs, 0, 0, 1, 1)
        
        self.pushButton_import = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_import.setObjectName("pushButton_import")
        self.pushButton_import.setStyleSheet("background-color:yellow")
        self.pushButton_import.setText("Nhập tài khoản")
        self.gridLayout.addWidget(self.pushButton_import, 1, 0, 1, 1)
        
        self.pushButton_run = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_run.setObjectName("pushButton_run")
        self.pushButton_run.setStyleSheet("background-color:rgb(0, 170, 127)")
        self.pushButton_run.setText("Chạy")
        self.gridLayout.addWidget(self.pushButton_run, 2, 0, 1, 1)
        
        self.pushButton_stop = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_stop.setObjectName("pushButton_stop")
        self.pushButton_stop.setStyleSheet("background-color:red")
        self.pushButton_stop.setText("Dừng")
        self.gridLayout.addWidget(self.pushButton_stop, 3, 0, 1, 1)
        
        self.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        
        # Connect
        self.pushButton_import.clicked.connect(self.get_accs)
        self.pushButton_run.clicked.connect(self.run)
        self.pushButton_stop.clicked.connect(self.stop_thread)
        
        
        #Connect to database
        try:
            self.conn = create_connection(r".\database\database.db")
            self.load_data(query= "SELECT * FROM accs")
        except:
            pass
    
    def get_accs(self):

        conn = create_connection(PATH+ "/database/database.db")
        delete_table(conn=conn, table="accs")
        query = f"""CREATE TABLE IF NOT EXISTS accs (
                                    id integer PRIMARY KEY AUTOINCREMENT,
                                    account text NOT NULL,
                                    password text NOT NULL,
                                    status text
                                );"""
        create_table(conn=conn, query=query)
        index_device = 0
        list_accs = self.plainTextEdit_accs.toPlainText().split("\n")
        for acc in list_accs:
            acc = acc.split("|")
            insert_table(conn=conn, table='accs',
                        columns=['id', 'account', 'password', 'status'],
                        values=[index_device, acc[0], acc[1],  'unknow'],
                        realtime = False)
            index_device += 1
        conn.commit() 
        self.load_data(query= "SELECT * FROM accs")
    
    def run(self):
        self.save_config()
        error = 0
        self.number_threads = self.spinBox_numberthread.value()
        self.proxy_tokens = self.plainTextEdit_proxy.toPlainText()
        self.proxy_tokens = self.proxy_tokens.split("\n")
        index_selected = self.tableWidget.selectionModel().selectedIndexes()
        self.index_selected = list(set([row.row() for row in index_selected]))
        self.index_selected.sort()
        if len(self.index_selected) == 0:
            self.show_warning_messagebox("Hãy bôi đen các hàng cần chạy!")
            return False
        
        # Run multi threads
        if len(self.index_selected) < self.number_threads:
                self.number_threads = len(self.index_selected)
        
        self.sessions = list(chunk(arr_range=self.index_selected,
                                arr_size=self.number_threads))
        
        self.IDs = {}
        self.threads = {}
        
        for index_thread in range(self.number_threads):  
                                
            # Proxy
            try:
                    if len(self.proxy_tokens) < self.number_threads:
                            proxy_token = random.choice(self.proxy_tokens)
                    else :
                            proxy_token = self.proxy_tokens[index_thread]
                    
            except:
                    proxy_token = ''
            
            data_row = [self.tableWidget.item(self.sessions[0][index_thread], col).text() for col in range(self.tableWidget.columnCount())]
            self.IDs[data_row[0]] = self.sessions[0][index_thread]
            self.threads[f"{index_thread}, {0}"] = ThreadsFifa(
                                                                    data_row=data_row,
                                                                    proxy_token = proxy_token,
                                                                    thread_info = [index_thread, 0]
                                                                    )
            self.threads[f"{index_thread}, {0}"].start()
            self.threads[f"{index_thread}, {0}"].signal_data.connect(self.update_table)
            self.threads[f"{index_thread}, {0}"].off_thread.connect(self.on_finished)
            time.sleep(0.2)

    def on_finished(self, index_thread, session):

                try:
                        if len(self.proxy_tokens) < self.number_threads:
                                proxy_token = random.choice(self.proxy_tokens)
                        else :
                                proxy_token = self.proxy_tokens[index_thread]
                        
                except:
                        proxy_token = ''
                try:
                    
                    data_row = [self.tableWidget.item(self.sessions[session][index_thread], col).text() for col in range(self.tableWidget.columnCount())]
                    self.IDs[data_row[0]] = self.sessions[session][index_thread]
                    self.threads[f"{index_thread}, {session}"] = ThreadsFifa(
                                                                            data_row=data_row,
                                                                            proxy_token = proxy_token,
                                                                            thread_info = [index_thread, session]
                                                                            )
                    self.threads[f"{index_thread}, {session}"].start()
                    self.threads[f"{index_thread}, {session}"].signal_data.connect(self.update_table)
                    self.threads[f"{index_thread}, {session}"].off_thread.connect(self.on_finished)
                except:
                        pass

    def update_table(self, data):
        
        try:
                index_row  =  self.IDs[data[0]]
                print("Data :              ", data, index_row)
                self.tableWidget.setItem(index_row, 3, QTableWidgetItem(data[3]))
                        
                update_table(conn=self.conn,
                                table= "accs",
                                columns=["account", "password", "status"],
                                values= data[1:],
                                column_where= "id",
                                value_where= int(data[0]))
        except Exception as e:
                print(e)
        
    def stop_thread(self):
        
        self.threads_stop = {}
        for thread in self.threads: 
                        
                        self.threads_stop[thread] = ThreadsStop(thread=self.threads[thread])
                        self.threads_stop[thread].start()
    
    def save_config(self):

        config = {
                        
                        "number_thread": self.spinBox_numberthread.value(),
                        "token_proxy": self.plainTextEdit_proxy.toPlainText()
                        }
                
        write_js(data=config, path=PATH + "/config.json")
                
    def load_data(self, query):
        try:
            self.tableWidget.deleteLater()
        except:
            pass
        
        self.conn = create_connection(r".\database\database.db")
        columns_name = get_columns_name(self.conn, 'accs')
        columns_name = list(map(lambda x: x.replace('status', 'Trạng thái'), columns_name))
        columns_name = list(map(lambda x: x.replace('id', 'STT'), columns_name))
        columns_name = list(map(lambda x: x.replace('device_name', 'Tên thiết bị'), columns_name))
        self.tableWidget = QtWidgets.QTableWidget(parent=self.centralwidget)
        self.tableWidget.setMinimumSize(QtCore.QSize(600, 300))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setStyleSheet("background-color:rgb(85, 255, 127)rgb(255, 255, 255)")
        self.tableWidget.setColumnCount(len(columns_name))
        self.tableWidget.setHorizontalHeaderLabels(columns_name)
        self.tableWidget.setSelectionMode(QAbstractItemView.MultiSelection)
        # self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        
        delegate = ReadOnlyDelegate(self.tableWidget)
        self.tableWidget.setItemDelegateForColumn(0, delegate)
        self.tableWidget.setItemDelegateForColumn(1, delegate)
        self.tableWidget.setItemDelegateForColumn(3, delegate)
        self.tableWidget.setItemDelegateForColumn(4, delegate)
        
        self.tableWidget.horizontalHeader().setSectionResizeMode(len(columns_name)-1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeColumnToContents(2)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.gridLayout.addWidget(self.tableWidget, 8, 0, 1, 2)
        self.tableWidget.setRowCount(get_length(conn = self.conn, 
                                                query="SELECT count(*) FROM accs"))
        self.tableWidget.setSortingEnabled(True)
        self.horizontalHeader = self.tableWidget.horizontalHeader()
        self.horizontalHeader.sectionClicked.connect(self.on_view_horizontalHeader_sectionClicked)
        
        cur = self.conn.cursor()
        row_index = 0
        rows = cur.execute(query)
        for row in rows:
            item_ID = QTableWidgetItem()
            item_ID.setData(QtCore.Qt.EditRole, row[0])
            self.tableWidget.setItem(row_index, 0, item_ID) 
            for i in range(1, len(columns_name)):
                self.tableWidget.setItem(row_index, i, QtWidgets.QTableWidgetItem(row[i]))
            row_index+=1
        self.tableWidget.setColumnWidth(1, 100)
        self.tableWidget.setColumnWidth(2, 100)
        
    # Filter by horizontal Header
    def on_view_horizontalHeader_sectionClicked(self, logicalIndex):
        if logicalIndex == 0:
            pass
        else:
            self.logicalIndex   = logicalIndex

            valuesUnique = [self.tableWidget.item(row, self.logicalIndex).text() for row in range(self.tableWidget.rowCount()) if not self.tableWidget.isRowHidden(row)]

            # Mở cửa sổ con
            self.Menudialog = QDialog(parent=self)
            self.Menudialog.setWindowTitle('Chọn giá trị cần lọc')
            self.Menudialog.setMinimumSize(QtCore.QSize(400, 400))

            self.list_widget = QListWidget(parent=self)
            valuesUnique = sorted(list(set(valuesUnique)))
            valuesUnique.insert(0, "Tất cả")
            valuesUnique.insert(1, "Bỏ chọn tất cả")
            self.list_widget.addItems(valuesUnique)
            
            # create QScrollArea，put QListWidget in it
            scroll_area = QScrollArea(self.Menudialog)
            scroll_area.setWidgetResizable(True)
            scroll_area.setWidget(self.list_widget)

            self.list_widget.currentItemChanged.connect(self.on_list_item_clicked)
            layout = QVBoxLayout(self.Menudialog)
            layout.addWidget(scroll_area)

            headerPos = self.tableWidget.mapToGlobal(self.horizontalHeader.pos())
            posY = headerPos.y() + self.horizontalHeader.height()
            # posX = headerPos.x() + self.horizontalHeader.sectionPosition(self.logicalIndex)
            posX = headerPos.x() + self.horizontalHeader.sectionViewportPosition(self.logicalIndex)
            if posX > 1700:
                posX = 1620
            self.Menudialog.setGeometry(posX +100, posY, 200, 300)
            self.Menudialog.exec()
            
    def on_list_item_clicked(self):
        item = self.list_widget.currentItem()
        if item.text() == "Tất cả":
            query = f"SELECT * FROM devices"
            self.load_data(query=query)
            self.tableWidget.selectAll()
                                    
        elif item.text() == "Bỏ chọn tất cả":
            self.tableWidget.clearSelection()
            
        else:
            map_column_name = {"STT": "index_device", 
                                "Tên thiết bị": "device_name",
                                "Trạng thái": "status"}
            column_name = map_column_name[self.tableWidget.horizontalHeaderItem(self.logicalIndex).text()]   
            query = f"SELECT * FROM devices WHERE {column_name} == '{item.text()}'"
            self.tableWidget.clearSelection()
            self.load_data(query=query)
            self.tableWidget.selectAll()
        self.Menudialog.close()
    
    def show_warning_messagebox(self, mess):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
    
        # setting message for Message Box
        msg.setText(mess)
        
        # setting Message box window title
        msg.setWindowTitle("Lỗi")
        
        # declaring buttons on Message Box
        msg.setStandardButtons(QMessageBox.Ok)
        
        # start the app
        retval = msg.exec_()

    #  Utils 
    def get_index_by_column_name(self, label):
        for index_column in range(self.tableWidget.columnCount()):
            if self.tableWidget.horizontalHeaderItem(index_column).text() == label:
                return index_column
        return -1
    

class ReadOnlyDelegate(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        return
    
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main = Ui_MainWindow()
    main.show()
    sys.exit(app.exec())
