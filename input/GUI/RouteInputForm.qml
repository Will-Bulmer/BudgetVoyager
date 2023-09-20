import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import "components" as Components
import "views" as Views
import "." as InputDir

Flow {
    // Components at higher level
    property var dropDownListView
    id: boxesContainer
    height: 54
    width: (8/10)*parent.width
    anchors.horizontalCenter: parent.horizontalCenter
    anchors.top: parent.top
    anchors.topMargin: 50
    anchors.leftMargin: parent.width * (1/10)
    anchors.rightMargin: parent.width * (1/10)
    flow: Flow.LeftToRight
    //spacing: boxesContainer.width * (1/30)
    spacing: 15 // Opt for constant space?

    readonly property real thresholdWidth: 500
    readonly property real boxLagTolerance: 1 // Smallest value we can get away with to compensate for Flow lag

    readonly property real boxBaseWidth: (boxesContainer.width - (2*spacing)) / 4
    readonly property bool isNarrow: boxesContainer.width < thresholdWidth

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
            otherDropdownListView: toBox.dropDownListView
            height: parent.height
            anchors.left: parent.left
            
            // Connect to the signal
            Component.onCompleted: {
                mainWindow.globalClick.connect(hideDropdown);
            }
        }

        Views.LocationInput {
            id: toBox
            boxLabel: "To"
            filteredModel: filteredModelRight
            otherTextInput: fromBox.textInput
            otherDropdownListView: fromBox.dropDownListView
            height: parent.height
            anchors.left: fromBox.right

            // Connect to the signal
            Component.onCompleted: {
                mainWindow.globalClick.connect(hideDropdown);
            }
        }
    }

    Views.DepartureDateInput {
        id: departureDateComponent
        boxLabel: "Departure"
        height: parent.height
        width: boxesContainer.isNarrow ? (2 * boxesContainer.boxBaseWidth + (boxesContainer.spacing / 2)) : boxesContainer.boxBaseWidth
    }

    // Wrap Search box so we may use anchor to the bottom
    Rectangle {
        width: searchBox.width
        height: boxesContainer.height

        Components.SearchBox {
            id: searchBox
            width: boxesContainer.isNarrow ? (2 * boxesContainer.boxBaseWidth + (boxesContainer.spacing / 2) - boxesContainer.boxLagTolerance) : boxesContainer.boxBaseWidth - (boxesContainer.boxLagTolerance)
            boxLabel: "Search"
            height: parent.height / 2
            anchors.bottom: parent.bottom
        }
    }
}