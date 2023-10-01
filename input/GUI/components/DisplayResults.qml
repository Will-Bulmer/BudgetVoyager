import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Item {
    id: displayResultsRoot
    property alias model: journeyListView.model
    width: parent.width
    height: 60

    // Background Rectangle for ListView
    Rectangle {
        anchors.fill: parent
        color: "lightgray"

        ListView {
            id: journeyListView
            anchors.fill: parent
            model: journeyModel

            delegate: Rectangle {
                anchors.fill: parent
                border.color: "black"
                border.width: 1
                color: "white"  // Background color for each delegate item

                RowLayout {
                    anchors.fill: parent
                    anchors.margins: 10
                    spacing: 20

                    // Provider (flixbus)
                    Column {
                        Layout.preferredWidth: displayResultsRoot.width * 0.2 // Adjust width as needed
                        Text {
                            text: model.provider
                            font.bold: true
                            anchors.verticalCenter: parent.verticalCenter
                        }
                    }

                    // Departure time and city
                    Column {
                        Text {
                            text: model.departureTime
                            font.bold: true
                        }
                        Text { text: model.departureCity }
                    }

                    // Arrival time and city
                    Column {
                        Text {
                            text: model.arrivalTime
                            font.bold: true
                        }
                        Text { text: model.arrivalCity }
                    }

                    // Price and seats left
                    Column {
                        Text {
                            text: model.price + " GDP"
                            font.bold: true
                        }
                        Text { text: model.seatsLeft + " seats left" }
                    }
                }
            }
        }
    }
}
