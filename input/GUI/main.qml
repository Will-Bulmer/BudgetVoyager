import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import "utilities" as Utilities
import "components" as Components

// Path might need setting every time?
// export QML2_IMPORT_PATH=/home/will_bulmer/.local/lib/python3.10/site-packages/PyQt6/Qt6/qml
// echo $QML2_IMPORT_PATH

// TO DO: Need better control over popup visibilities. When any place not in the popup is clicked, it vanishes  
// Also need to ensure that if a selection was not made and the popup vanishes, that the text goes back to blank

ApplicationWindow {
    id: mainWindow
    visible: true
    width: 1080  // Adjusted width to better accommodate two boxes
    height: 800
    //visibility: Window.Maximized
    title: "Budget Voyager"
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
                routeInputFormLoader.sourceComponent = routeInputFormComponent; // Load input fields only once model is populated. Need loader due to asynchronous loading.
                buttonLoader.sourceComponent = buttonComponent;

            } catch (error) {
                console.error("Failed to parse JSON data:", error);
            }
        }

        function onJsonLoadError(errorMessage) {
            console.error("Failed to load JSON data:", errorMessage);
        }
    }

    // Connect the Python signal to a QML function
    Connections {
        target: functionalityBackend
        function onJourneyDataReady(data) {
            try {
                var jsonData = JSON.parse(data); // Parse the JSON string

                // Process jsonData and update the UI as needed
                journeyModel.clear(); // Clear the previous data if any

                for (var i = 0; i < jsonData.length; i++) {
                    journeyModel.append({ "data": jsonData[i].toString() });
                }
            } catch (error) {
                console.error("Failed to parse JSON data:", error);
            }
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

    Components.TitleBanner{
        id: titleBanner
        width: parent.width
        anchors.top: parent.top
        height: 80 // Adjust the height to your preference
    }
    // Loader to load the RouteInputForm once the models are populated
    Loader {
        id: routeInputFormLoader
        height: 76
        width: (8/10)*parent.width
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: titleBanner.bottom
        anchors.topMargin: 30
        anchors.leftMargin: parent.width * (1/10)
        anchors.rightMargin: parent.width * (1/10)
    }
    
    Component {
        id: routeInputFormComponent
        RouteInputForm {
        }
    }
    
    Rectangle {
        id: separatorLine
        width: parent.width
        height: 2 // Set the thickness of the line
        color: "black" // Set the color of the line
        anchors.topMargin: 30
        anchors.top: routeInputFormLoader.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        opacity: 0.3
    }

    Loader {
        id: buttonLoader
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 20
    }

    ListView {
        model: journeyModel
        anchors.top: separatorLine.bottom
        anchors.topMargin: 30
        width: parent.width
        delegate: Text {
            width: parent.width
            //text: model.data.toString() // Convert the data to a string
            text: model.data
        }
    }

    Component {
        id: buttonComponent
        Button {
            text: "Quit"
            onClicked: {
                Qt.quit()
            }
        }
    }


    ListModel {
        id: filteredModelLeft
    }

    ListModel {
        id: filteredModelRight
    }

    ListModel {
        id: journeyModel
    }
}





