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

    Connections {
        target: functionalityBackend

        function onJourneyDataReady(journeyListString) {
            handleJourneyData(journeyListString);
        }
    }


    function handleJourneyData(journeyListString) {
        function capitalizeFirstLetter(string) {
            return string.charAt(0).toUpperCase() + string.slice(1);
        }
        try {
            var parsedJourneyList = JSON.parse(journeyListString);
            //console.log(parsedJourneyList)
            journeyModel.clear();
            
            for (var i = 0; i < parsedJourneyList.length; i++) {
                var journey = parsedJourneyList[i];
                //console.log(journey)
                journeyModel.append({
                    "departureCity": journey[0],
                    "departureTime": utilityFunctions.extractTimeFromISOString(journey[1]),
                    "arrivalCity": journey[2],
                    "arrivalTime": utilityFunctions.extractTimeFromISOString(journey[3]),
                    "price": journey[4],
                    "seatsLeft": journey[5],
                    "provider": capitalizeFirstLetter(journey[6])
                });
            }
        } catch (error) {
            console.error("Failed to process the journey data:", error);
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
        id: separatorLineTop
        width: parent.width
        height: 2 // Set the thickness of the line
        color: "black" // Set the color of the line
        anchors.topMargin: 30
        anchors.top: routeInputFormLoader.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        opacity: 0.3
    }


    Components.DisplayResults {
        id: displayResults
        anchors.top: separatorLineTop.bottom
        //anchors.topMargin: 15
        width: parent.width - 60 // account for margins
        anchors.bottomMargin: 15
        anchors.bottom: buttonLoader.top  // This ensures it fills up the space until the white strip
        anchors.leftMargin: 30  // Left margin
        anchors.rightMargin: 30  // Right margin
        anchors.horizontalCenter: parent.horizontalCenter  // Centering the delegate horizontally   
        Rectangle {
            color: "lightgray"
            anchors.fill: parent
            z: -1
        }
    }

    Loader {
        id: buttonLoader
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 20
    }
    Component {
        id: buttonComponent
        Rectangle {
            id: bottomStrip
            anchors.bottom: parent.bottom
            anchors.left: parent.left
            anchors.right: parent.right
            height: 30
            color: "white"

            Button {
                id: quitButton
                text: "Quit"
                anchors.centerIn: parent
                onClicked: {
                    Qt.quit()
                }
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





