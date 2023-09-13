#!/usr/bin/env python3
import os
import sys
import json
from PyQt6.QtCore import QUrl, QObject, pyqtSlot, pyqtSignal
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine
from PyQt6.QtCore import pyqtProperty

class JSONBackend(QObject):
    jsonLoaded = pyqtSignal(str) # Signal emitted when something happens to a Qobject. Emits a string.
    jsonLoadError = pyqtSignal(str)
    
    def __init__(self):
        super(JSONBackend, self).__init__() # Inits a QObject with parent parameter.
        self._jsonData = ""

    # When pyqtProperty changes, jsonLoaded signal emitted
    @pyqtProperty(str, notify=jsonLoaded)
    def jsonData(self):
        return self._jsonData

    # Slots are special methods in QT. Can be connect to any signal.
    @pyqtSlot(str)
    def loadJSON(self, filepath):
        retries = 0
        MAX_RETRIES = 3
        while retries < MAX_RETRIES:
            try:
                absolute_filepath = os.path.abspath(filepath)
                if not os.path.exists(absolute_filepath):
                    self.jsonLoadError.emit("File does not exist")
                    return
                with open(absolute_filepath, 'r') as file:
                    data = json.load(file)
                    self._jsonData = json.dumps(data)
                    self.jsonLoaded.emit(self._jsonData)
                    return
            except Exception as e:
                retries += 1
                self.jsonLoadError.emit(str(e))
                print(f"Attempt {retries} - Error loading JSON: {e}", flush = True)
        print("Failed to load JSON after all retries", flush = True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GUI_PATH = os.path.join(BASE_DIR,'main.qml')
#GUI_PATH = os.path.join(BASE_DIR,'Main.qml')

#JSON_PATH = os.path.join(BASE_DIR, 'flixbus/bus_stops.json')

def main():
    app = QGuiApplication(sys.argv)    
    engine = QQmlApplicationEngine() # Tool to load QML files
    
    # Must expose jsonBackend before loading GUI
    jsonBackend = JSONBackend()
    #jsonBackend.loadJSON(JSON_PATH)
    engine.rootContext().setContextProperty("jsonBackend", jsonBackend) # Expose the Python object to QML
    engine.load(QUrl(GUI_PATH))
    
    if not engine.rootObjects():
        sys.exit(-1) # Check objects have been loaded.

    sys.exit(app.exec())

if __name__ == '__main__':
    main()
