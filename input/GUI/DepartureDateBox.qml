import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15 // Necessary for the RowLayout
//import "./UtilityFunctions.qml" as UF
import "." as InputDir

Item {
    InputDir.UtilityFunctions {
    id: utilityFunctions
    }
    property string boxLabel: "Date"
    id: inputContainerDate
    height: parent.height

    // Model for the days of the month
    property var daysOfTheMonth: []
    Component.onCompleted: {
        for(var i = 1; i <= 31; i++) {
            daysOfTheMonth.push(i);
        }
    }

    // POPUP    
    Rectangle {
        id: popupDate
        y: textInputWrapperDate.y + textInputWrapperDate.height
        visible: false
        width: parent.width
        color: "white"
        border.color: "black"
        border.width: 5
        anchors.right: textInputWrapperDate.right

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
    // TITLE
    Rectangle {
        width: parent.width / 3
        height: parent.height/2
        color: "white"
        anchors.top: parent.top
        anchors.left: textInputWrapperDate.left
        Label {
            text: "Departure"
            color: "grey"
            anchors.centerIn: parent
        }
    }
    // TEXTBOX
    Rectangle {
        id: textInputWrapperDate
        width: parent.width
        height: parent.height / 2
        border.color: "black"
        border.width: 1
        color: "white"
        radius: 4
        anchors.bottom: parent.bottom

        Image {
            id: locationIconDate
            source: "assets/location_picture.jpg"
            width: 24
            height: parent.height*0.8
            anchors.verticalCenter: parent.verticalCenter
            anchors.left: parent.left
            anchors.leftMargin: 5
        }

        TextInput {
            id: textInputDate
            property bool selectionMade: false  // Add this property
            property string previousSelection: ""  // New property

            width: parent.width - 4
            height: parent.height - 4
            anchors.centerIn: parent
            verticalAlignment: TextInput.AlignVCenter
            leftPadding: locationIconDate.width + 10

            readOnly: true

            MouseArea {
                anchors.fill: parent
                onClicked: {
                    popupDate.visible = true;
                }
            }

            onActiveFocusChanged: {
                if (!activeFocus) {
                    popupDate.visible = false;
                    if (!selectionMade) {
                        text = "";
                    }
                }
            }

            Connections {
                target: popupDate
                function onVisibleChanged() {
                if (!popupDate.visible) {
                    textInputDate.selectionMade = false;
                    }
                }
            }
        }
    }
}


