import QtQuick 2.15
import QtQuick.Controls 2.15
//import "./UtilityFunctions.qml" as UF
import "." as InputDir

Item {
    InputDir.UtilityFunctions {
    id: utilityFunctions
    }
    property string boxLabel: "From"
    property var filteredModel: undefined  // Placeholder for the filtered model

    // Giving Variables to the ToInputBox.qml
    property alias textInputLeftAlias: textInputLeft
    property alias dropDownListViewLeftAlias : dropDownListViewLeft

    // Getting Variables from the ToInputBox.qml
    property var textInputRight
    property var dropDownListViewRight

    id: inputContainerLeft
    height: parent.height

    ListView {
        id: dropDownListViewLeft
        width: 1.5*parent.width // Done the math. This will not go off the side of the app.
        y: parent.y + parent.height
        visible: textInputLeft.activeFocus
        anchors.left: parent.left

        model: filteredModelLeft
        height: Math.min(8, filteredModelLeft.count+1) * 30
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
                text: "Available Cities"
                anchors.centerIn: parent
                color: "black"
                font.bold: true
            }
        }
        delegate: Item {
            width: dropDownListViewLeft.width
            height: 30
            Rectangle {
                width: parent.width
                height: 30
                color: mouseArea.containsMouse ? "#d0d0d0" : "white"
                Text {
                    anchors.left: parent.left
                    anchors.leftMargin: parent.width * 0.10
                    anchors.verticalCenter: parent.verticalCenter
                    text: utilityFunctions.highlightText(model.name, textInputLeft.text)
                    color: "black"
                    textFormat: Text.RichText
                }
                MouseArea {
                    id: mouseArea
                    anchors.fill: parent
                    hoverEnabled: true
                onClicked: {
                    textInputLeft.text = model.name;
                    textInputLeft.selectionMade = true;
                    dropDownListViewLeft.visible = false;
                    }
                }
            }
        }
    }
    Rectangle {
        width: parent.width / 5
        height: parent.height / 2
        color: "white"
        anchors.top: parent.top
        anchors.left: textInputWrapperLeft.left
        Label {
            text: "From"
            color: "grey"
            anchors.centerIn: parent
        }
    }
    Rectangle {
        id: textInputWrapperLeft
        width: parent.width
        height: parent.height / 2
        border.color: "black"
        border.width: 1
        color: "white"
        radius: 4
        anchors.bottom: parent.bottom

        Image {
            id: locationIconLeft
            source: "assets/location_picture.jpg"
            width: 24
            height: parent.height * 0.8
            anchors.verticalCenter: parent.verticalCenter
            anchors.left: parent.left
            anchors.leftMargin: 5
        }

        TextInput {
            id: textInputLeft

            property bool selectionMade: false  // Add this property
            property string previousSelection: ""  // New property
            property bool italicizeLeft: false  // New property to control italic styling
            font.italic: italicizeLeft  // Bind the font italic property to the 'italicize' property

            width: parent.width - 4
            height: parent.height - 4
            anchors.centerIn: parent
            verticalAlignment: TextInput.AlignVCenter
            leftPadding: locationIconLeft.width + 10
            onTextChanged: {
                utilityFunctions.updateModel(text, filteredModelLeft, textInputRight.text);
                utilityFunctions.handleVisibilityFor(textInputLeft, dropDownListViewLeft, dropDownListViewRight);
            }

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
