import QtQuick 2.15
import QtQuick.Controls 2.15
//import "./UtilityFunctions.qml" as UF
import "." as InputDir




Item {
    InputDir.UtilityFunctions {
    id: utilityFunctions
    }
    property string boxLabel: "Date"
    id: inputContainerDate
    height: parent.height

    ListView {
        id: dropDownListViewDate
        width: 1.5*parent.width // Done the math. This will not go off the side of the app.
        y: parent.y + parent.height
        visible: textInputDate.activeFocus
        anchors.left: parent.left

        model: ["Mon", "Tues"]
        height: 30*7
        clip: true
        ScrollBar.vertical: ScrollBar {}

        Rectangle {
            color: "transparent"
            border.color: "lightgray"
            border.width: 1
            radius: 4
            anchors.fill: parent
        }
        header: Rectangle {
            width: parent.width
            height: 30
            color: "#e0e0e0"
            Label {
                text: "Current Month Page"
                anchors.centerIn: parent
                color: "black"
                font.bold: true
            }
        }
        // Each item within the ListView
        delegate: Item {
            width: dropDownListViewDate.width
            height: 30
            Rectangle {
                width: parent.width
                height: 30
                color: mouseArea.containsMouse ? "#d0d0d0" : "white"
                Text {
                    anchors.left: parent.left
                    anchors.leftMargin: parent.width * 0.10
                    anchors.verticalCenter: parent.verticalCenter
                    text: model.name
                    color: "black"
                    textFormat: Text.RichText
                }
                MouseArea {
                    id: mouseArea
                    anchors.fill: parent
                    hoverEnabled: true
                onClicked: {
                    textInputDate.text = model.name;
                    textInputDate.selectionMade = true;
                    dropDownListViewDate.visible = false;
                    }
                }
            }
        }
    }
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

            property bool selectionMade: false 
            property string previousSelection: "" 
            property bool italicizeLeft: false 
            font.italic: italicizeLeft 


            width: parent.width - 4
            height: parent.height - 4
            anchors.centerIn: parent
            verticalAlignment: TextInput.AlignVCenter
            leftPadding: locationIconDate.width + 10

            onActiveFocusChanged: {
                if (!activeFocus && !selectionMade) {
                    text = "";
                }
                if (activeFocus && text === "") {
                    selectionMade = false;  // Reset the flag when the box is focused again
                }
            }
        }
    }
}


