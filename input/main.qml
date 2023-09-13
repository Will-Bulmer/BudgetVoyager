import QtQuick 2.15
import QtQuick.Controls 2.15
import "." as InputDir

// Path might need setting every time?
// export QML2_IMPORT_PATH=/home/will_bulmer/.local/lib/python3.10/site-packages/PyQt6/Qt6/qml
// echo $QML2_IMPORT_PATH


ApplicationWindow {
    visible: true
    width: 500  // Adjusted width to better accommodate two boxes
    height: 500
    title: "Textbox with Dynamic Dropdown"
    color: "white"
    InputDir.UtilityFunctions {
    id: utilityFunctions
    }
    property var fullList : [""]

    Component.onCompleted: {
        target: jsonBackend
        Qt.callLater(function() {
            console.log("Attempting to open JSON file");
            jsonBackend.loadJSON("input/flixbus/bus_stops.json");
        });
    }

    Connections {
        target: jsonBackend

        function onJsonLoaded() {
            console.log("JSON data loaded successfully");
            
            try {
                var parsedData = JSON.parse(jsonBackend.jsonData);
                
                // Reset the fullList and filteredModels
                fullList = [];
                filteredModelLeft.clear();
                filteredModelRight.clear();
                
                for (var key in parsedData) {
                    fullList.push(parsedData[key].name);
                    filteredModelLeft.append({"name": parsedData[key].name});
                    filteredModelRight.append({"name": parsedData[key].name});
                }

                // Update both input models initially after loading the JSON
                utilityFunctions.updateModel("", filteredModelLeft, "");
                utilityFunctions.updateModel("", filteredModelRight, "");
            } catch (error) {
                console.error("Failed to parse JSON data:", error);
            }
        }

        function onJsonLoadError(errorMessage) {
            console.error("Failed to load JSON data:", errorMessage);
        }
    }

    Item {
        id: inputBoxesContainer
        height: 54
        width: parent.width
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: parent.top
        anchors.topMargin: 50

        // Include fromBox.qml (LEFT)
        FromInputBox {
            id: fromInputComponent
            boxLabel: "From"
            filteredModel: filteredModelLeft
            
            // Exchanging variables between child modules
            textInputRight: toInputComponent.textInputRightAlias
            dropDownListViewRight : toInputComponent.dropDownListViewRightAlias
            anchors.left: parent.left
            // ... any other properties or configurations specific to this instance ...
        }
        // The right input box ("To")
        ToInputBox {
            id: toInputComponent
            boxLabel: "To"
            filteredModel: filteredModelRight
            // Exchanging variables between child modules
            textInputLeft: fromInputComponent.textInputLeftAlias
            dropDownListViewLeft : fromInputComponent.dropDownListViewLeftAlias

            anchors.right: parent.right
            // ... any other properties or configurations specific to this instance ...
        }

    }
        

    Button {
        text: "Quit"
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 20
        onClicked: {
            Qt.quit()
        }
    }

    ListModel {
        id: filteredModelLeft
    }

    ListModel {
        id: filteredModelRight
    }
}





