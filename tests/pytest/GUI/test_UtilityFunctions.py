import pytest
import os
import time
from PyQt6 import QtCore
from PyQt6.QtCore import QUrl, QObject
from PyQt6.QtQml import QQmlApplicationEngine
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlComponent

@pytest.fixture(scope="session")
def app():
    return QGuiApplication([])

@pytest.fixture(scope="session")
def qml_engine(app):
    return QQmlApplicationEngine()

@pytest.fixture
def qml_context(qml_engine):
    context = qml_engine.rootContext()
    return context

class MockListModel(QtCore.QObject):
    def __init__(self):
        super().__init__()
        self.items = []
        self._visible = False  # initialize the private _visible attribute

    @QtCore.pyqtSlot()
    def clear(self):
        self.items.clear()

    @QtCore.pyqtSlot(QtCore.QVariant)
    def append(self, item):
        self.items.append(item)
        
    @property
    def visible(self) -> bool:
        return self._visible

    @visible.setter
    def visible(self, value: bool):
        self._visible = value



class TestUtilityFunctions:

    def test_updateModel(self, qml_engine, qml_context):
        qml_file = "/home/will_bulmer/PROJECTS/BudgetVoyager/input/GUI/UtilityFunctions.qml"
        qml_engine.load(QUrl.fromLocalFile(qml_file))

        # Check if the QML file has been loaded successfully
        root_objects = qml_engine.rootObjects()
        if not root_objects:
            raise ValueError(f"Failed to load QML file: {qml_file}")

        found_test_object = next((obj for obj in root_objects if obj.objectName() == "testObject"), None)
        if not found_test_object:
            raise ValueError("testObject not found in QML file.")
        
        input_text = "test"
        mock_model = MockListModel()
        other_textbox_value = "other_value"

        full_list = ["test1", "test2", "other_value"]
        qml_context.setContextProperty("fullList", full_list)

        if not hasattr(found_test_object, "updateModel"):
            raise AttributeError("Method updateModel doesn't exist on testObject.")

        found_test_object.updateModel(input_text, mock_model, other_textbox_value)
        
        assert len(mock_model.items) == 2
        assert mock_model.items[0].toVariant() == {"name": "test1"}
        assert mock_model.items[1].toVariant() == {"name": "test2"}

    def test_highlightText(self, qml_engine):
        qml_file = "/home/will_bulmer/PROJECTS/BudgetVoyager/input/GUI/UtilityFunctions.qml"
        qml_engine.load(QUrl.fromLocalFile(qml_file))
        
        root_objects = qml_engine.rootObjects()
        if not root_objects:
            raise ValueError(f"Failed to load QML file: {qml_file}")

        found_test_object = next((obj for obj in root_objects if obj.objectName() == "testObject"), None)

        if not found_test_object:
            raise ValueError("testObject not found in QML file.")
        
        if not hasattr(found_test_object, "highlightText"):
            raise AttributeError("Method highlightText doesn't exist on testObject.")

        result = found_test_object.highlightText("hello", "lo")
        print(result)
        assert '<span style=\'background-color: yellow\'>lo</span>' in result

    # TESTED OMITTED. TOO MUCH HASSLE TRYING TO GET QT OBJECT TO SYNC WITH PYTHON OBJECT
    def handleVisibilityFor(self, qml_engine):
        qml_file = "/home/will_bulmer/PROJECTS/BudgetVoyager/input/GUI/UtilityFunctions.qml"
        qml_engine.load(QUrl.fromLocalFile(qml_file))

        # Check if the QML file has been loaded successfully
        root_objects = qml_engine.rootObjects()
        if not root_objects:
            raise ValueError(f"Failed to load QML file: {qml_file}")

        found_test_object = next((obj for obj in root_objects if obj.objectName() == "testObject"), None)
        if not found_test_object:
            raise ValueError("testObject not found in QML file.")

        mock_text_input = QObject()
        mock_text_input.text = "test"

        mock_dropdown1 = MockListModel()
        mock_dropdown2 = MockListModel()
        print("Before:", mock_dropdown1.visible)

        found_test_object.handleVisibilityFor(mock_text_input, mock_dropdown1, mock_dropdown2)
        assert hasattr(mock_dropdown1, 'visible')
        assert mock_dropdown1.visible
        assert not mock_dropdown2.visible



