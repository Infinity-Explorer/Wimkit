import sys
import platform
import os
import multiprocessing
import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel, QMessageBox,
                            QFrame, QSizePolicy)
from PyQt6.QtCore import Qt, QUrl, QTimer
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtGui import QPalette, QColor
import re
import threading
from PyQt6.QtCore import QTranslator, QLocale, QLibraryInfo

class MainUI(QMainWindow):

    if os.path.exists("./settings/settings.txt") != True:
        with open("settings.txt", "w",encoding="utf-8") as f:
            f.write("{'compression': 'middle', 'verify_backup': True, 'confirm_overwrite': True, 'create_directories': True, 'theme': 'light', 'language': 'en_us'}")
    
    def readSettingsInfoFromTXT(objFunc:str):             
        with open("./settings/settings.txt", "r",encoding="utf-8") as f:
            settingsInfo = f.readlines()
            settingsInfo = str(settingsInfo)
            print(type(settingsInfo))
            print(settingsInfo)
            matchObject = re.search(r"'theme':\s*'([^']+)'", settingsInfo)
            if objFunc == "theme":
                print(matchObject.group(1))
                return matchObject.group(1)
            if objFunc == "compressLevel":
                matchObject = re.search(r"'compression':\s*'([^']+)'", settingsInfo)
                print(matchObject.group(1))
                return matchObject.group(1)
            if objFunc == "language":
                matchObject = re.search(r"'language':\s*'([^']+)'", settingsInfo)
                print(matchObject.group(1))
                return matchObject.group(1)
        
            
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wimkit")
        self.setGeometry(100, 100, 600, 400)
        
        # Initialize language files
        translator = QTranslator()
        language = MainUI.readSettingsInfoFromTXT("language")
        if not translator.load(f"./resources/translations/mainUI.py/{language}.qm"):
            print("Failed to load translation file")
            sys.exit(1)
        else:
            app.installTranslator(translator)

        QApplication.instance().installTranslator(translator)
        # Create main window widget
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        
        if MainUI.readSettingsInfoFromTXT("theme") == "dark":
            self.palette = QPalette()
            self.palette.setColor(QPalette.ColorRole.Window, QColor(30,30,30))
            self.palette.setColor(QPalette.ColorRole.WindowText, QColor(220,220,220))
            self.palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
            self.palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
            self.palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
            self.setPalette(self.palette)
            QApplication.setPalette(self.palette)

        # Create main layout
        self.main_layout = QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)
        
        # Welcome label
        self.welcome_label = QLabel(self.tr("Welcome to Wimkit tool, select an option to continue"))
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.welcome_label.setStyleSheet("font-size: 20px;")
        self.main_layout.addWidget(self.welcome_label)
        
        # Create button area
        self.button_layout = QHBoxLayout()
        self.main_layout.addLayout(self.button_layout)
        
        # Backup button
        self.backup_button = QPushButton(self.tr("➡  Backup My Files"))
        self.backup_button.clicked.connect(self.backup_files)
        self.button_layout.addWidget(self.backup_button)
        self.backup_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 14px;")
        self.backup_button.setFixedSize(300, 50)
        self.backup_button.setToolTip(self.tr("Click to backup my files"))
        
        # Restore button
        self.restore_button = QPushButton(self.tr("➡   Restore My Files"))
        self.restore_button.clicked.connect(self.restore_files)
        self.button_layout.addWidget(self.restore_button)
        self.restore_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 14px;")
        self.restore_button.setFixedSize(300, 50)
        self.restore_button.setToolTip(self.tr("Click to restore my files"))
        
        # Settings button
        self.settings_button = QPushButton("⚙")
        self.settings_button.clicked.connect(self.open_settings)
        self.settings_button.setFixedSize(38, 30)
        self.main_layout.addWidget(self.settings_button, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        
        # Create separator
        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.Shape.HLine)
        self.separator.setFrameShadow(QFrame.Shadow.Sunken)
        self.main_layout.addWidget(self.separator)
        
        # Create center area
        self.center_frame = QFrame()
        self.center_layout = QVBoxLayout()
        self.center_frame.setLayout(self.center_layout)
        self.center_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.center_frame.setStyleSheet("background-color: white; border: 1px solid #ccc;")
        self.main_layout.addWidget(self.center_frame, stretch=1)
        
        # Add system information
        self.system_info_label = QLabel()
        self.system_info_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.center_layout.addWidget(self.system_info_label)
        self.update_system_info()
        
        # Add timer to update system information
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_system_info)
        self.timer.start(5000)  # Update every 5 seconds
        
        # Bottom help area
        self.help_layout = QHBoxLayout()
        self.main_layout.addLayout(self.help_layout)
        
        self.help_label = QLabel(self.tr("Encountered a problem?"))
        self.help_layout.addWidget(self.help_label)
        
        self.help_button = QPushButton(self.tr("Click Here"))
        self.help_button.clicked.connect(self.open_help)
        self.help_layout.addWidget(self.help_button)
        
    def update_system_info(self):
        # Get system information
        system = platform.system()
        release = platform.release()
        version = platform.version()
        processor = platform.processor()
        
        # Get CPU core count
        cpu_count = multiprocessing.cpu_count()
        
        # Get memory information (simplified version)
        try:
            import psutil
            memory = psutil.virtual_memory()
            memory_total = round(memory.total / (1024 ** 3), 2)  # GB
            memory_used = round(memory.used / (1024 ** 3), 2)  # GB
            memory_percent = memory.percent
            memory_available = True
        except ImportError:
            memory_total = self.tr("Unknown")
            memory_used = self.tr("Unknown")
            memory_percent = self.tr("Unknown")
            memory_available = False
        
        # Get current time
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Build information text
        info_text = self.tr(f"""
        <b>System Information</b><br>
        Operating System: {system} {release}<br>
        Processor: {processor}<br>
        CPU Cores: {cpu_count}<br>
        Current Time: {current_time}<br><br>
        
        <b>Memory Information</b><br>
        """)
        
        if memory_available:
            info_text += self.tr(f"""
        Total Memory: {memory_total} GB<br>
        Used Memory: {memory_used} GB<br>
        Memory Usage: {memory_percent}%
        """)
        else:
            info_text += self.tr("(psutil library needs to be installed for detailed information)")
        
        self.system_info_label.setText(info_text)
        
    def backup_files(self):
        try:
            if not os.path.exists("./backupUI.exe"):
                threadBackup = threading.Thread(target=os.system, args=("python ./backupUI.py",))
                threadBackup.start()
            else:
                threadBackupWithoutPy = threading.Thread(target=os.system, args=("start ./backupUI.exe",))
                threadBackupWithoutPy.start()
        except Exception as e:
            QMessageBox.critical(self, self.tr("Error", "Backup program not found, please check if the backup program is in the current directory"))
            
    def restore_files(self):
        try:
            if not os.path.exists("./restoreUI.exe"):
                threadRestore = threading.Thread(target=os.system, args=("python restoreUI.py",))
                threadRestore.start()
            else:
                threadRestoreWithoutPy = threading.Thread(target=os.system, args=("start ./restoreUI.exe",))
                threadRestoreWithoutPy.start()
        except Exception as e:
            QMessageBox.critical(self, self.tr("Error", "Restore program not found, please check if the restore program is in the current directory"))
            
    def open_settings(self):
        try:
            if not os.path.exists("./settingsUI.exe"):
                threadSettings = threading.Thread(target=os.system, args=("python settingsUI.py",))
                threadSettings.start()
            else:
                threadSettingsWithoutPy = threading.Thread(target=os.system, args=("start ./settingsUI.exe",))
                threadSettingsWithoutPy.start()
        except Exception as e:
            QMessageBox.critical(self, self.tr("Error", "Settings program not found, please check if the settings program is in the current directory"))
            
    def open_help(self):
        try:
            QDesktopServices.openUrl(QUrl("https://github.com/Infinity-Explorer/DiskBackupAndRestore-ToolBox"))
        except Exception as e:
            QMessageBox.critical(self, self.tr("Error", "Unable to open webpage, please check your network connection"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainUI()
    window.show()
    sys.exit(app.exec())
