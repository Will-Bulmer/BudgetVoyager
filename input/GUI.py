#!/usr/bin/env python3
import os
import sys
import json
from PyQt6.QtCore import QUrl, QObject, pyqtSlot, pyqtSignal
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine
from PyQt6.QtCore import pyqtProperty

# Signals: Allows asynchronous workflow in case of large JSONs.
# self.jsonLoaded.emit(self._jsonData) -> Anything connected to this signal can recieve data and react to it.
class JSONBackend(QObject):
    jsonLoaded = pyqtSignal(str) # Signal emitted when something happens to a Qobject. Emits a string.

    def __init__(self):
        super(JSONBackend, self).__init__() # Inits a QObject with parent parameter.
        self._jsonData = ""

    # When pyqtProperty changes, jsonLoaded signal emitted
    @pyqtProperty(str, notify=jsonLoaded)
    def jsonData(self):
        return self._jsonData

    # Slots are special methods in QT. Can be connect to any signal.
    # Primary use is to be notified when a signal is emitted. Loose coupling.
    @pyqtSlot(str)
    def loadJSON(self, filepath):
        # Get the absolute path to the JSON file
        absolute_filepath = os.path.abspath(filepath)

        try:
            with open(absolute_filepath, 'r') as file:
                data = json.load(file)
                self._jsonData = json.dumps(data)
                self.jsonLoaded.emit(self._jsonData) # Emit the signal with jsonData
        except Exception as e:
            print(f"Error loading JSON: {e}")


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GUI_PATH = os.path.join(BASE_DIR,'main.qml')

def main():
    app = QGuiApplication(sys.argv)

    # Tool to load QML files
    engine = QQmlApplicationEngine()
    engine.load(QUrl(GUI_PATH))

    jsonBackend = JSONBackend()
    engine.rootContext().setContextProperty("jsonBackend", jsonBackend) # Expose the Python object to QML

    if not engine.rootObjects():
        sys.exit(-1) # Check objects have been loaded.

    sys.exit(app.exec())

if __name__ == '__main__':
    main()
