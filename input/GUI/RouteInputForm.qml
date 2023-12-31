import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import "components" as Components
import "views" as Views
import "utilities" as Utilities
import "." as InputDir


Flow {
    property bool fromBoxSelected: false
    property bool toBoxSelected: false
    property bool departureDateSelected: false
    property string fromLocationName: ""
    property string toLocationName: ""
    property string departureDateString: ""
    property date departureDateObject: new Date()

    id: boxesContainer
 
    flow: Flow.LeftToRight
    spacing: 15 // Opt for constant space?

    readonly property real thresholdWidth: 800
    readonly property real boxLagTolerance: 1 // Smallest value we can get away with to compensate for Flow lag

    readonly property real boxBaseWidth: (boxesContainer.width - (2*spacing)) / 4
    readonly property bool isNarrow: boxesContainer.width < thresholdWidth
    Utilities.UtilityFunctions {
    id: utilityFunctions
    }
    // Wrap two boxes in so that they may have no spacing
    Rectangle {
        id: locationBoxesContainer
        height: parent.height
        width: boxesContainer.isNarrow ? boxesContainer.width : 2 * boxesContainer.boxBaseWidth

        onWidthChanged: {
            fromBox.width = locationBoxesContainer.width / 2
            toBox.width = locationBoxesContainer.width / 2
        }

        Views.LocationInput {
            id: fromBox
            boxLabel: "From"
            filteredModel: filteredModelLeft
            otherTextInput: toBox.textInput
            otherLocationPopup: toBox.locationPopup
            height: parent.height
            anchors.left: parent.left
            // Connect to the signal
            Component.onCompleted: {
                mainWindow.globalClick.connect(hidePopup);
            }
            onLocationSelectionMadePropagator: function(locationName) {
                boxesContainer.fromBoxSelected = true;
                boxesContainer.fromLocationName = locationName;
                console.log("Location Selected: ", locationName);
                utilityFunctions.updateSearchBoxState();
            }
        }

        Views.LocationInput {
            id: toBox
            boxLabel: "To"
            filteredModel: filteredModelRight
            otherTextInput: fromBox.textInput
            otherLocationPopup: fromBox.locationPopup
            height: parent.height
            anchors.left: fromBox.right
            onLocationSelectionMadePropagator: function(locationName) {
                    boxesContainer.toBoxSelected = true;
                    boxesContainer.toLocationName = locationName;
                    console.log("Location Selected: ", locationName);
                    utilityFunctions.updateSearchBoxState();
                }
            // Connect to the signal
            Component.onCompleted: {
                mainWindow.globalClick.connect(hidePopup);
            }
        }
    }

    Views.DepartureDateInput {
        id: departureDateComponent
        boxLabel: "Departure"
        height: parent.height
        width: boxesContainer.isNarrow ? (2 * boxesContainer.boxBaseWidth + (boxesContainer.spacing / 2)) : boxesContainer.boxBaseWidth
        onDateSelectionMadePropagator: function(dateClicked) {
            boxesContainer.departureDateSelected = true;
            boxesContainer.departureDateObject = dateClicked
            boxesContainer.departureDateString = utilityFunctions.transformDate(boxesContainer.departureDateObject);
            console.log("Date Selected:", boxesContainer.departureDateString);
            utilityFunctions.updateSearchBoxState();
        }
    }

    // Wrap Search box so we may use anchor to the bottom
    Rectangle {
        width: searchBox.width
        height: boxesContainer.height

        Components.SearchBox {
            id: searchBox
            isSearchBoxEnabled: fromBoxSelected && toBoxSelected && departureDateSelected
            width: boxesContainer.isNarrow ? (2 * boxesContainer.boxBaseWidth + (boxesContainer.spacing / 2) - boxesContainer.boxLagTolerance) : boxesContainer.boxBaseWidth - (boxesContainer.boxLagTolerance)
            boxLabel: "Search"
            height: parent.height / 2
            anchors.bottom: parent.bottom
            fromLocationName: boxesContainer.fromLocationName
            toLocationName: boxesContainer.toLocationName
            departureDateString: boxesContainer.departureDateString
            onSearchClicked: {
                searchBox.isSearchBoxEnabled = false;
            }
        }
    }
}