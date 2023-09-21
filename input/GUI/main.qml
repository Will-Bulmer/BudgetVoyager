import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import "utilities" as Utilities

// Path might need setting every time?
// export QML2_IMPORT_PATH=/home/will_bulmer/.local/lib/python3.10/site-packages/PyQt6/Qt6/qml
// echo $QML2_IMPORT_PATH

// TO DO: Need better control over popup visibilities. When any place not in the popup is clicked, it vanishes  
// Also need to ensure that if a selection was not made and the popup vanishes, that the text goes back to blank

ApplicationWindow {
    id: mainWindow
    visible: true
    width: 1080  // Adjusted width to better accommodate two boxes
    height: 1080
    //visibility: Window.Maximized
    title: "Textbox with Dynamic Dropdown"
    color: "white"
    Utilities.UtilityFunctions {
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
    // Focus Sink
    Item {
        id: focusSink
        focus: true  // Ensure this item can receive focus
        anchors.fill: parent
    }
    // Global MouseArea
    signal globalClick()
    MouseArea {
        anchors.fill: parent
        propagateComposedEvents: true
        onClicked: function(mouse) {
            //console.log("Global Mouse Space Clicked");
            globalClick(); // Emit the signal here  
            mouse.accepted = false;  // Let the click propagate further if needed.
            focusSink.forceActiveFocus();
        }
    }
    RouteInputForm {}
        
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





