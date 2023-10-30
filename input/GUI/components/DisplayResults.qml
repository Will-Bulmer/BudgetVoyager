import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Item {
    id: displayResultsRoot
    property alias model: journeyListView.model
    width: parent.width

    ListView {
        id: journeyListView
        visible: true
        anchors.fill: parent
        model: journeyModel
        clip: true
        boundsBehavior: Flickable.StopAtBounds
        ScrollBar.vertical: ScrollBar {}

        delegate: Rectangle {
            color: "white"
            width: journeyListView.width - 4
            height: 50
            anchors.horizontalCenter: parent.horizontalCenter

            RowLayout {
                id: contentRow
                anchors.fill: parent
                //anchors.margins: 10
                spacing: 2

                Column {
                    //Layout.preferredWidth: displayResultsRoot.width * 0.1
                    Layout.preferredWidth: 85
                    Layout.alignment: Qt.AlignLeft
                    height: parent.height

                    Rectangle {
                        anchors.fill: parent
                        color: model.provider === "Flixbus" ? "#00BB5D" : "blue"
                        visible: true

                        Text {
                            anchors.centerIn: parent
                            text: model.provider
                            font.bold: true
                            color: "white"  // Set the text color to white for better contrast against the green or blue background
                        }
                    }
                }

                // Departure time and city
                Column {
                    Layout.fillWidth: true
                    Layout.preferredWidth: (displayResultsRoot.width - (displayResultsRoot.width * 0.15) + 85) * 0.5
                    Layout.leftMargin: 20  // Adding right
                    Text {
                        text: model.departureTime
                        font.bold: true
                    }
                    Text { text: model.departureCity }
                }

                // Arrival time and city
                Column {
                    Layout.fillWidth: true
                    Layout.preferredWidth: (displayResultsRoot.width - (displayResultsRoot.width * 0.15) * 2) * 0.5
                    Text {
                        text: model.arrivalTime
                        font.bold: true
                    }
                    Text { text: model.arrivalCity }
                }

                // Vertical line
                Rectangle {
                    Layout.preferredWidth: 2
                    color: "#E0E0E0"  // Very light grey
                    height: parent.height
                    Layout.rightMargin: 10  // Adding right
                }

                // Price and seats left
                Column {
                    Layout.preferredWidth: displayResultsRoot.width * 0.15
                    Layout.alignment: Qt.AlignRight
                    Text {
                        text: model.price + " GBP"
                        font.bold: true
                    }
                    Text { text: model.seatsLeft + " seats left" }
                }
            }
        }
    }
}
