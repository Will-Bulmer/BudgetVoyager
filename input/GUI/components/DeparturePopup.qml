import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15 
import "." as InputDir

// POPUP    
Rectangle {
    property var textInput

    id: popupDate
    y: parent.y + parent.height
    visible: false
    width: parent.width
    color: "white"
    border.color: "black"
    border.width: 5
    anchors.left: parent.left

    ColumnLayout {
        anchors.fill: parent // Ensure ColumnLayout takes the full width and height of popupDate
        spacing: 5

        // Month Header
        Rectangle {
            Layout.fillWidth: true
            width: parent.width
            height: 30
            color: "#e0e0e0"
            Label {
                text: "September 2023"
                anchors.centerIn: parent
                color: "black"
                font.bold: true
            }
        }

        // Days of the week header
        RowLayout {
            Layout.fillWidth: true
            height: 30
            Repeater {
                model: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
                delegate: Label {
                    width: parent.width / 7
                    height: 30
                    text: modelData
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    color: "grey"
                    font.bold: true
                    Layout.alignment: Qt.AlignCenter
                }
            }
        }

        // Days of the month in GridView
        GridView {
            Layout.fillWidth: true
            height: 250
            cellWidth: width / 7
            cellHeight: 40
            model: daysOfTheMonth

            delegate: Rectangle {
                width: gridView.cellWidth
                height: gridView.cellHeight
                color: "white"
                border.color: "lightgray"
                Text {
                    anchors.centerIn: parent
                    text: modelData
                    color: "black"
                }

                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        // Handle day click
                        console.log("Clicked day:", modelData);
                    }
                }
            }
        }
    }
}