import QtQuick 2.15
import QtQuick.Controls 2.15
import "." as InputDir

ListView {
    property var textInput

    id: dropDownListView
    width: 1.2 * parent.width
    y: parent.y + parent.height
    visible: textInput.activeFocus
    anchors.left: parent.left
    model: filteredModel
    height: Math.min(8, filteredModel.count + 1) * 30
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
        width: dropDownListView.width
        height: 30
        Rectangle {
            width: parent.width
            height: 30
            color: mouseArea.containsMouse ? "#d0d0d0" : "white"
            Text {
                anchors.left: parent.left
                anchors.leftMargin: parent.width * 0.10
                anchors.verticalCenter: parent.verticalCenter
                text: utilityFunctions.highlightText(model.name, textInput.text)
                color: "black"
                textFormat: Text.RichText
            }
            MouseArea {
                id: mouseArea
                anchors.fill: parent
                hoverEnabled: true
                onClicked: {
                    textInput.text = model.name;
                    textInput.selectionMade = true;
                    dropDownListView.visible = false;
                }
            }
        }
    }
}