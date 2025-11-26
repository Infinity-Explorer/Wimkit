import sys
import json
import os
from PyQt6.QtWidgets import (QApplication, QDialog, QVBoxLayout, QHBoxLayout,
                           QLabel, QComboBox, QCheckBox, QPushButton,
                           QGroupBox, QSpinBox, QFileDialog, QMessageBox,
                           QListWidget, QStackedWidget, QWidget)
from PyQt6.QtCore import Qt, QSettings
from PyQt6.QtGui import QFont

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings_file = "settings.txt"
        self.settings = self.load_settings()
        self.init_ui()
        
    def load_settings(self):
        default_settings = {
            "language": "en_US",
            "compression": "middle",
            "verify_backup": True,
            "confirm_overwrite": True,
            "create_directories": True,
            "theme": "light",
            "backup_path": "",
            "max_backup_versions": 5,
            "auto_backup": False,
            "auto_backup_interval": 24,  # hours
            "restore_path": "",
            "verify_restore": True
        }
        
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, "r", encoding="utf-8") as f:
                    loaded_settings = json.load(f)
                    default_settings.update(loaded_settings)
            except:
                pass
                
        return default_settings

    def save_settings(self):
        self.settings["language"] = self.language_combo.currentData()  # 使用currentData()获取值
        self.settings["theme"] = self.theme_combo.currentData()  # 使用currentData()获取值
        with open(self.settings_file, "w", encoding="utf-8") as f:
            json.dump(self.settings, f, indent=4)

    def init_ui(self):
        self.setWindowTitle("Settings")
        self.setMinimumSize(600, 400)
        
        # 主布局
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)
        
        # 左侧菜单列表
        self.menu_list = QListWidget()
        self.menu_list.addItems([
            "Language Settings",
            "Backup Settings",
            "Restore Settings"
        ])
        self.menu_list.setMaximumWidth(200)
        self.menu_list.currentRowChanged.connect(self.switch_page)
        main_layout.addWidget(self.menu_list)
        
        # 右侧设置页面
        self.pages = QStackedWidget()
        main_layout.addWidget(self.pages)
        
        # 创建设置页面
        self.create_language_page()
        self.create_backup_page()
        self.create_restore_page()
        
        # 底部按钮
        buttons_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_and_close)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        buttons_layout.addStretch()
        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(cancel_button)
        
        main_layout.addLayout(buttons_layout)
        
    def create_language_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        page.setLayout(layout)
        
        # 语言设置组
        lang_group = QGroupBox("Language Settings")
        lang_layout = QVBoxLayout()
        lang_group.setLayout(lang_layout)
        
        # 语言选择下拉框
        self.language_combo = QComboBox()
        self.language_combo.addItem("English", "en_US")
        self.language_combo.addItem("简体中文", "zh_CN")
        
        # 设置当前语言
        current_lang = self.settings.get("language", "en_US")
        for i in range(self.language_combo.count()):
            if self.language_combo.itemData(i) == current_lang:
                self.language_combo.setCurrentIndex(i)
                break
                
        lang_layout.addWidget(QLabel("Select Language:"))
        lang_layout.addWidget(self.language_combo)
        
        # 主题设置
        self.theme_combo = QComboBox()
        self.theme_combo.addItem("Light Theme", "light")
        self.theme_combo.addItem("Dark Theme", "dark")
        
        # 设置当前主题
        current_theme = self.settings.get("theme", "light")
        for i in range(self.theme_combo.count()):
            if self.theme_combo.itemData(i) == current_theme:
                self.theme_combo.setCurrentIndex(i)
                break
                
        lang_layout.addWidget(QLabel("Select Theme:"))
        lang_layout.addWidget(self.theme_combo)
        
        layout.addWidget(lang_group)
        layout.addStretch()
        
        self.pages.addWidget(page)

    def create_backup_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        page.setLayout(layout)
        
        # 备份设置组
        backup_group = QGroupBox("Backup Settings")
        backup_layout = QVBoxLayout()
        backup_group.setLayout(backup_layout)
        
        # 压缩级别
        compression_layout = QHBoxLayout()
        compression_layout.addWidget(QLabel("Compression Level:"))
        self.compression_combo = QComboBox()
        self.compression_combo.addItems([
             "none","fast","middle","maximum"
        ])
        
        current_compression = self.settings.get("compression", "middle")
        for i in range(self.compression_combo.count()):
            if self.compression_combo.itemData(i) == current_compression:
                self.compression_combo.setCurrentIndex(i)
                break
                
        compression_layout.addWidget(self.compression_combo)
        backup_layout.addLayout(compression_layout)
        
        # 备份选项
        self.verify_backup = QCheckBox("Verify backup after creation")
        self.verify_backup.setChecked(self.settings.get("verify_backup", True))
        backup_layout.addWidget(self.verify_backup)
        
        self.confirm_overwrite = QCheckBox("Confirm before overwriting existing backups")
        self.confirm_overwrite.setChecked(self.settings.get("confirm_overwrite", True))
        backup_layout.addWidget(self.confirm_overwrite)
        
        self.create_directories = QCheckBox("Create missing directories automatically")
        self.create_directories.setChecked(self.settings.get("create_directories", True))
        backup_layout.addWidget(self.create_directories)
        
        # 备份路径
        path_layout = QHBoxLayout()
        path_layout.addWidget(QLabel("Default Backup Path:"))
        self.backup_path_edit = QLabel(self.settings.get("backup_path", "Not Set"))
        self.backup_path_edit.setStyleSheet("QLabel { background-color: white; border: 1px solid gray; padding: 5px; }")
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browse_backup_path)
        path_layout.addWidget(self.backup_path_edit, 1)
        path_layout.addWidget(browse_button)
        backup_layout.addLayout(path_layout)
        
        # 自动备份设置
        self.auto_backup = QCheckBox("Enable automatic backup")
        self.auto_backup.setChecked(self.settings.get("auto_backup", False))
        backup_layout.addWidget(self.auto_backup)
        
        interval_layout = QHBoxLayout()
        interval_layout.addWidget(QLabel("Backup Interval (hours):"))
        self.backup_interval = QSpinBox()
        self.backup_interval.setRange(1, 168)  # 1 hour to 1 week
        self.backup_interval.setValue(self.settings.get("auto_backup_interval", 24))
        interval_layout.addWidget(self.backup_interval)
        interval_layout.addStretch()
        backup_layout.addLayout(interval_layout)
        
        layout.addWidget(backup_group)
        layout.addStretch()
        
        self.pages.addWidget(page)

    def create_restore_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        page.setLayout(layout)
        
        # 恢复设置组
        restore_group = QGroupBox("Restore Settings")
        restore_layout = QVBoxLayout()
        restore_group.setLayout(restore_layout)
        
        # 验证恢复
        self.verify_restore = QCheckBox("Verify backup before restore")
        self.verify_restore.setChecked(self.settings.get("verify_restore", True))
        restore_layout.addWidget(self.verify_restore)
        
        # 恢复路径
        path_layout = QHBoxLayout()
        path_layout.addWidget(QLabel("Default Restore Path:"))
        self.restore_path_edit = QLabel(self.settings.get("restore_path", "Not Set"))
        self.restore_path_edit.setStyleSheet("QLabel { background-color: white; border: 1px solid gray; padding: 5px; }")
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browse_restore_path)
        path_layout.addWidget(self.restore_path_edit, 1)
        path_layout.addWidget(browse_button)
        restore_layout.addLayout(path_layout)
        
        layout.addWidget(restore_group)
        layout.addStretch()
        
        self.pages.addWidget(page)

    def switch_page(self, index):
        self.pages.setCurrentIndex(index)

    def browse_backup_path(self):
        path = QFileDialog.getExistingDirectory(self, "Select Backup Directory")
        if path:
            self.backup_path_edit.setText(path)

    def browse_restore_path(self):
        path = QFileDialog.getExistingDirectory(self, "Select Restore Directory")
        if path:
            self.restore_path_edit.setText(path)

    def save_and_close(self):
        # 保存语言设置
        self.settings["language"] = self.language_combo.currentData()
        self.settings["theme"] = self.theme_combo.currentData()
        
        # 保存备份设置
        self.settings["compression"] = self.compression_combo.currentData()
        self.settings["verify_backup"] = self.verify_backup.isChecked()
        self.settings["confirm_overwrite"] = self.confirm_overwrite.isChecked()
        self.settings["create_directories"] = self.create_directories.isChecked()
        self.settings["backup_path"] = self.backup_path_edit.text()
        self.settings["auto_backup"] = self.auto_backup.isChecked()
        self.settings["auto_backup_interval"] = self.backup_interval.value()
        
        # 保存恢复设置
        self.settings["verify_restore"] = self.verify_restore.isChecked()
        self.settings["restore_path"] = self.restore_path_edit.text()
        
        # 保存到文件
        self.save_settings()
        
        QMessageBox.information(self, "Settings", "Settings have been saved successfully!")
        self.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = SettingsDialog()
    dialog.show()
    sys.exit(app.exec())
