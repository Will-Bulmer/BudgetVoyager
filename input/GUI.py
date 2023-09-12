#!/usr/bin/env python3
import os
import sys
import json
from PyQt6.QtCore import QUrl, QObject, pyqtSlot, pyqtSignal
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine

class JSONBackend(QObject):
    jsonLoaded = pyqtSignal(str)

    @pyqtSlot(str)
    def loadJSON(self, filepath):
        with open(filepath, 'r') as file:
            data = json.load(file)
            self.jsonLoaded.emit(json.dumps(data))


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GUI_PATH = os.path.join(BASE_DIR,'main.qml')

def main():
    app = QGuiApplication(sys.argv)

    engine = QQmlApplicationEngine()
    engine.load(QUrl(GUI_PATH))

    # Create an instance of our JSON Backend
    jsonBackend = JSONBackend()
    # Expose the Python object to QML
    engine.rootContext().setContextProperty("jsonBackend", jsonBackend)

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())

if __name__ == '__main__':
    main()
