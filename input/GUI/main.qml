import QtQuick 2.15
import QtQuick.Controls 2.15
import "." as InputDir

// Path might need setting every time?
// export QML2_IMPORT_PATH=/home/will_bulmer/.local/lib/python3.10/site-packages/PyQt6/Qt6/qml
// echo $QML2_IMPORT_PATH

// TO DO: Need better control over popup visibilities. When any place not in the popup is clicked, it vanishes  
// Also need to ensure that if a selection was not made and the popup vanishes, that the text goes back to blank

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
    
    MouseArea {
        anchors.fill: parent
        propagateComposedEvents: true
        onClicked: function(mouse) {
            console.log("Global Mouse Space Clicked");
            
            // Only hide dropdowns if the click wasn't on them or their associated text inputs
            if (!fromInputComponent.dropDownListViewLeftAlias.containsMouse &&
                !fromInputComponent.textInputLeftAlias.containsMouse &&
                !toInputComponent.dropDownListViewRightAlias.containsMouse &&
                !toInputComponent.textInputRightAlias.containsMouse) {
                toInputComponent.dropDownListViewRightAlias.visible = false;
                fromInputComponent.dropDownListViewLeftAlias.visible = false;

                // Explicitly remove focus from both TextInputs
                fromInputComponent.textInputLeftAlias.focus = false;
                toInputComponent.textInputRightAlias.focus = false;
            }
            
            mouse.accepted = false;  // Let the click propagate further if needed.
        }
    }

    Item {
        id: allboxesContainer
        height: 54
        width: parent.width
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: parent.top
        anchors.topMargin: 50

        Item {
            id: inputBoxesContainer
            height: parent.height
            width: (2/3)*parent.width
            //anchors.left: parent.left
 
            // Include fromBox.qml (LEFT)
            FromInputBox {
                id: fromInputComponent
                boxLabel: "From"
                filteredModel: filteredModelLeft
                width: parent.width / 2
                height: parent.height
                anchors.left: parent.left
                
                // Exchanging variables between child modules
                textInputRight: toInputComponent.textInputRightAlias
                dropDownListViewRight : toInputComponent.dropDownListViewRightAlias
            }

            // The right input box ("To")
            ToInputBox {
                id: toInputComponent
                boxLabel: "To"
                filteredModel: filteredModelRight
                width: parent.width / 2
                height: parent.height
                anchors.left: fromInputComponent.right
                //anchors.leftMargin: parent.width * 0.109

                // Exchanging variables between child modules
                textInputLeft: fromInputComponent.textInputLeftAlias
                dropDownListViewLeft : fromInputComponent.dropDownListViewLeftAlias
            }
        }
        
        DepartureDateBox {
            id: departureDateComponent
            boxLabel: "Date"
            width: (1/3)*parent.width
            height: parent.height
            Component.onCompleted: {
                anchors.left = inputBoxesContainer.right
            }
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





