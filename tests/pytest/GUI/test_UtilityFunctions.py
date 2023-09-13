import pytest
import os
import time
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

class MockListModel:
    def __init__(self):
        self.items = []
        self.visible = False

    def clear(self):
        self.items = []

    def append(self, item):
        self.items.append(item)

def updateModel(qml_engine, qml_context):
    qml_file = "path_to_your_qml_file.qml"
    qml_engine.load(QUrl.fromLocalFile(qml_file))

    test_object = qml_engine.rootObjects()[0].findChild(QObject, "testObject")

    input_text = "test"
    mock_model = MockListModel()
    other_textbox_value = "other_value"

    full_list = ["test1", "test2", "other_value"]
    qml_context.setContextProperty("fullList", full_list)

    test_object.updateModel(input_text, mock_model, other_textbox_value)

    assert len(mock_model.items) == 1
    assert mock_model.items[0] == {"name": "test1"}

def test_highlightText(qml_engine):
    # Path to the QML file
    qml_file = "/home/will_bulmer/PROJECTS/BudgetVoyager/input/GUI/UtilityFunctions.qml"
    
    # Load the QML file into the engine
    qml_engine.load(QUrl.fromLocalFile(qml_file))
    
    # Check if the QML file has been loaded successfully
    if not qml_engine.rootObjects():
        raise ValueError(f"Failed to load QML file: {qml_file}")
    
    # Introduce a short delay just in case there's a delay in object creation
    #time.sleep(1)
    
    # Find the testObject from root objects
    found_test_object = None
    for root_object in qml_engine.rootObjects():
        if root_object.objectName() == "testObject":
            found_test_object = root_object
            break

    # If the test object isn't found, let's create it explicitly
    if not found_test_object:
        component = QQmlComponent(qml_engine, QUrl.fromLocalFile(qml_file))
        if component.isError():
            for error in component.errors():
                print(error.toString())
            raise ValueError("Component has errors.")
    
        obj = component.create()
        if obj.objectName() == "testObject":
            found_test_object = obj

    # Verify the result
    if found_test_object:
        if hasattr(found_test_object, "highlightText"):
            result = found_test_object.highlightText("hello", "lo")
            print(result)
            # Here you can also add assertions to check if the result is as expected
            # e.g., assert '<span style='background-color: yellow'>lo</span>' in result
        else:
            raise AttributeError("Found testObject but the method highlightText doesn't exist on it.")
    else:
        raise ValueError("testObject not found in QML file.")


def handleVisibilityFor(qml_engine):
    qml_file = "path_to_your_qml_file.qml"
    qml_engine.load(QUrl.fromLocalFile(qml_file))

    test_object = qml_engine.rootObjects()[0].findChild(QObject, "testObject")

    mock_text_input = QObject()
    mock_text_input.text = "test"

    mock_dropdown1 = MockListModel()
    mock_dropdown2 = MockListModel()

    test_object.handleVisibilityFor(mock_text_input, mock_dropdown1, mock_dropdown2)

    assert mock_dropdown1.visible == True
    assert mock_dropdown2.visible == False

