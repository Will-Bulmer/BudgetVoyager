import QtQuick 2.15
import QtQuick.Controls 2.15

// Path might need setting every time?
// export QML2_IMPORT_PATH=/home/will_bulmer/.local/lib/python3.10/site-packages/PyQt6/Qt6/qml
// echo $QML2_IMPORT_PATH

// TODO: Validate JSON data before preceding. Need error handling and tests for all qml functionality. Introduce retry mechanisms.
// TODO: Take out all functionality into a separate qml file? Or header file?


ApplicationWindow {
    visible: true
    width: 500  // Adjusted width to better accommodate two boxes
    height: 500
    title: "Textbox with Dynamic Dropdown"
    color: "white"

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
                updateModel("", filteredModelLeft, "");
                updateModel("", filteredModelRight, "");
            } catch (error) {
                console.error("Failed to parse JSON data:", error);
            }
        }

        function onJsonLoadError(errorMessage) {
            console.error("Failed to load JSON data:", errorMessage);
        }
    }

    function updateModel(inputText, modelToUpdate, otherTextboxValue) {
    modelToUpdate.clear();
    for (var i = 0; i < fullList.length; i++) {
        var itemName = fullList[i];
        if ((itemName.toLowerCase().startsWith(inputText.toLowerCase()) || inputText === "") 
            && itemName !== otherTextboxValue) {
            modelToUpdate.append({"name": itemName});
        }
    }
}

    function highlightText(fullText, searchText) {
        if (!fullText) return "";
        if (searchText === "") return fullText;
        var regExp = new RegExp("(" + searchText + ")", "ig");
        return fullText.replace(regExp, "<span style='background-color: yellow'>$1</span>");
    }

    function handleVisibilityFor(textInput, dropDownListView, otherDropDownListView) {
        dropDownListView.visible = (textInput.text.length > 0);
        otherDropDownListView.visible = false;
    }

    /*
    Component.onCompleted: {
        updateModel("", filteredModelLeft);
        updateModel("", filteredModelRight);
    }
    */

    Item {
        id: inputBoxesContainer
        height: 54
        width: parent.width
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: parent.top
        anchors.topMargin: 50

        // Include fromBox.qml (LEFT)
        FromInputBox {
            boxLabel: "From"
            filteredModel: filteredModelLeft
            anchors.left: parent.left
            // ... any other properties or configurations specific to this instance ...
        }
        // The right input box ("To")
        ToInputBox {
            boxLabel: "To"
            filteredModel: filteredModelRight
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





