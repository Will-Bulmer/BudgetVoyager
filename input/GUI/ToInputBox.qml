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

    // Giving Variables to the FromInputBox.qml
    property alias textInputRightAlias: textInputRight
    property alias dropDownListViewRightAlias : dropDownListViewRight

    // Getting Variables from the FromInputBox.qml
    property var textInputLeft
    property var dropDownListViewLeft

    
    id: inputContainerRight
    height: parent.height

    ListView {
        id: dropDownListViewRight
        width: 1.5*parent.width
        y: parent.y + parent.height
        visible: textInputRight.activeFocus
        anchors.left: parent.left

        model: filteredModelRight
        height: Math.min(8, filteredModelRight.count+1) * 30
        clip: true
        ScrollBar.vertical: ScrollBar {}
        
        // ... [The contents of the ListView for the "To" box is identical to the "From" box]
        // You can consider creating a reusable Component for this to avoid redundancy

        // The rest of the content is the same as the left ListView
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
            width: dropDownListViewRight.width
            height: 30
            Rectangle {
                width: parent.width
                height: 30
                color: mouseArea.containsMouse ? "#d0d0d0" : "white"
                Text {
                    anchors.left: parent.left
                    anchors.leftMargin: parent.width * 0.10
                    anchors.verticalCenter: parent.verticalCenter
                    text: utilityFunctions.highlightText(model.name, textInputRight.text)
                    color: "black"
                    textFormat: Text.RichText
                }
                MouseArea {
                    id: mouseArea
                    anchors.fill: parent
                    hoverEnabled: true
                    onClicked: {
                        textInputRight.text = model.name;
                        textInputRight.selectionMade = true;
                        dropDownListViewRight.visible = false;
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
        anchors.left: textInputWrapperRight.left
        Label {
            text: "To"
            color: "grey"
            anchors.centerIn: parent
        }
    }

    Rectangle {
        id: textInputWrapperRight
        width: parent.width
        height: parent.height / 2
        border.color: "black"
        border.width: 1
        color: "white"
        radius: 4
        anchors.bottom: parent.bottom

        Image {
            id: locationIconRight
            source: "assets/location_picture.jpg"
            width: 24
            height: parent.height * 0.8
            anchors.verticalCenter: parent.verticalCenter
            anchors.left: parent.left
            anchors.leftMargin: 5
        }

        TextInput {
            id: textInputRight

            property bool selectionMade: false  // Add this property
            property bool italicizeRight: false  // New property to control italic styling
            property string previousSelection: ""  // New property

            font.italic: italicizeRight  // Bind the font italic property to the 'italicize' property

            width: parent.width - 4
            height: parent.height - 4
            anchors.centerIn: parent
            verticalAlignment: TextInput.AlignVCenter
            leftPadding: locationIconRight.width + 10
            onTextChanged: {
                utilityFunctions.updateModel(text, filteredModelRight, textInputLeft.text);
                utilityFunctions.handleVisibilityFor(textInputRight, dropDownListViewRight, dropDownListViewLeft);
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