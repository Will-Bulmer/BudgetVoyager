import QtQuick 2.15
import QtQuick.Controls 2.15

Item {
    id: root
    property string boxLabel: "Label"
    property bool isSearchBoxEnabled: true // Add this property to enable/disable the search box

    Rectangle {
        id: searchBox
        width: parent.width
        height: parent.height
        border.color: "#FFA500"
        border.width: 1
        color: "#FFA500" // Yellowy orange color
        radius: 4
        opacity: root.isSearchBoxEnabled ? 1 : 0.5 // Set opacity based on isSearchBoxEnabled

        Text {
            text: "Search"
            anchors.centerIn: parent
            color: "black"
        }

        MouseArea {
            anchors.fill: parent
            enabled: root.isSearchBoxEnabled // Set MouseArea enabled/disabled based on isSearchBoxEnabled
            cursorShape: root.isSearchBoxEnabled ? Qt.PointingHandCursor : Qt.ArrowCursor
            onClicked: {
                console.log("Search Box Clicked!")
                var tripDetails = functionalityBackend.getJourneyDetails(fromLocationName, toLocationName, departureDate.toString());
            }
        }
    }
}

