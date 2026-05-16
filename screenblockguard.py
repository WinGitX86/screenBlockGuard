#!/usr/bin/env python3
# ScreenBlockGuard GUI
# Author: WinGitX86
# License: GNU GPLv3
import sys
import json
from pathlib import Path
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QListWidget, QPushButton, QLabel,
                             QListWidgetItem, QMessageBox)

CONFIG_DIR = Path("/etc/screenblockguard")
CONFIG_FILE = CONFIG_DIR / "trustlist.json"

def load_conf():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_conf(data):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ScreenBlockGuard - 截屏管控面板 | 作者:WinGitX86 | GPLv3")
        self.setGeometry(100,100,620,420)
        self.init_ui()
        self.refresh_list()

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        layout.addWidget(QLabel("信任区(禁止截屏) ←→ 不信任区(允许截屏)"))
        h_layout = QHBoxLayout()

        self.trust_list = QListWidget()
        self.trust_list.setToolTip("非预装程序默认在此，禁止截屏")
        h_layout.addWidget(self.trust_list)

        btn_layout = QVBoxLayout()
        self.move_untrust = QPushButton("→ 移至允许截屏")
        self.move_trust = QPushButton("← 移至禁止截屏")
        self.refresh_btn = QPushButton("刷新列表")
        btn_layout.addWidget(self.move_untrust)
        btn_layout.addWidget(self.move_trust)
        btn_layout.addWidget(self.refresh_btn)
        h_layout.addLayout(btn_layout)

        self.untrust_list = QListWidget()
        self.untrust_list.setToolTip("预装程序/手动允许截屏的程序")
        h_layout.addWidget(self.untrust_list)

        layout.addLayout(h_layout)

        self.move_untrust.clicked.connect(self.to_untrust)
        self.move_trust.clicked.connect(self.to_trust)
        self.refresh_btn.clicked.connect(self.refresh_list)

    def refresh_list(self):
        conf = load_conf()
        self.trust_list.clear()
        self.untrust_list.clear()
        for app in conf["trust"]:
            self.trust_list.addItem(QListWidgetItem(app))
        for app in conf["untrust"]:
            self.untrust_list.addItem(QListWidgetItem(app))

    def to_untrust(self):
        item = self.trust_list.currentItem()
        if not item:
            return
        app = item.text()
        conf = load_conf()
        conf["trust"].remove(app)
        conf["untrust"].append(app)
        save_conf(conf)
        self.refresh_list()
        QMessageBox.information(self, "成功", f"{app} 已允许截屏")

    def to_trust(self):
        item = self.untrust_list.currentItem()
        if not item:
            return
        app = item.text()
        conf = load_conf()
        conf["untrust"].remove(app)
        conf["trust"].append(app)
        save_conf(conf)
        self.refresh_list()
        QMessageBox.information(self, "成功", f"{app} 已禁止截屏")

def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
 