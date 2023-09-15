import pytest
import os
import time
from PyQt6 import QtCore, QtQml, QtGui
from PyQt6.QtCore import QUrl, QObject, pyqtProperty, pyqtSignal

@pytest.fixture(scope="session")
def app():
    return QtGui.QGuiApplication([])

@pytest.fixture(scope="session")
def qml_engine(app):
    return QtQml.QQmlApplicationEngine()

@pytest.fixture
def qml_context(qml_engine):
    return qml_engine.rootContext()

@pytest.fixture
def load_qml_file(qml_engine):
    def _loader(file_path):
        qml_engine.load(QUrl.fromLocalFile(file_path))
        root_objects = qml_engine.rootObjects()
        assert root_objects, f"Failed to load QML file: {file_path}"
        return root_objects
    return _loader

class MockTextInput(QtCore.QObject):
    textChanged = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._text = ''

    def _get_text(self):
        return self._text

    def _set_text(self, value):
        if self._text != value:
            self._text = value
            self.textChanged.emit(self._text)

    text = pyqtProperty(str, _get_text, _set_text, notify=textChanged)


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
            
    # Getter for the visible property
    def _get_visible(self):
        return self._visible
    # Setter for the visible property
    def _set_visible(self, value):
        self._visible = value

    visible = pyqtProperty(bool, _get_visible, _set_visible)

class TestUtilityFunctions:

    QML_FILE_PATH = "/home/will_bulmer/PROJECTS/BudgetVoyager/input/GUI/UtilityFunctions.qml"

    def get_test_object(self, root_objects):
        found_test_object = next((obj for obj in root_objects if obj.objectName() == "testObject"), None)
        assert found_test_object, "testObject not found in QML file."
        return found_test_object

    def test_updateModel(self, qml_engine, qml_context, load_qml_file):
        root_objects = load_qml_file(self.QML_FILE_PATH)
        test_object = self.get_test_object(root_objects)
        
        # Setup
        input_text = "test"
        mock_model = MockListModel()
        other_textbox_value = "other_value"
        full_list = ["test1", "test2", "other_value"]
        qml_context.setContextProperty("fullList", full_list)
        assert hasattr(test_object, "updateModel")

        # Action
        test_object.updateModel(input_text, mock_model, other_textbox_value)
        
        # Assertions
        assert len(mock_model.items) == 2
        assert mock_model.items[0].toVariant() == {"name": "test1"}
        assert mock_model.items[1].toVariant() == {"name": "test2"}

    def test_highlightText(self, qml_engine, load_qml_file):
        root_objects = load_qml_file(self.QML_FILE_PATH)
        test_object = self.get_test_object(root_objects)
        
        assert hasattr(test_object, "highlightText")
        result = test_object.highlightText("hello", "lo")
        assert '<span style=\'background-color: yellow\'>lo</span>' in result

    def test_handleVisibilityFor(self, qml_engine, load_qml_file):
        root_objects = load_qml_file(self.QML_FILE_PATH)
        test_object = self.get_test_object(root_objects)

        mock_text_input = MockTextInput()
        mock_text_input.text = "test"
        qml_engine.rootContext().setContextProperty("textInput", mock_text_input)

        mock_dropdown1 = MockListModel()
        mock_dropdown2 = MockListModel()

        test_object.handleVisibilityFor(mock_text_input, mock_dropdown1, mock_dropdown2)
        assert hasattr(mock_dropdown1, 'visible')
        assert mock_dropdown1.visible
        assert not mock_dropdown2.visible



