import QtQuick 2.15
import QtQuick.Controls 2.15
import "." as InputDir

Popup {
    id: locationPopup
    closePolicy: Popup.NoAutoClose
    signal locationSelectionMade(string locationName)
    property var textInput
    property var otherTextInputChild
    width: 1.2 * parent.width
    height: Math.min(8, filteredModel.count + 1) * 30
    y: parent.y + parent.height

    padding: 0  // Remove default padding
    background: Rectangle { color: "transparent" }  // Set transparent background



    ListView {
        id: dropDownListView
        visible: true
        anchors.fill: parent
        model: filteredModel
        clip: true
        boundsBehavior: Flickable.StopAtBounds
        cacheBuffer: 30*50 // 50 selections 
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
                    cursorShape: Qt.PointingHandCursor
                    property bool debouncing: false
                    onClicked: function(mouse) {
                        if (debouncing) return;
                        debouncing = true;
                        mouse.accepted = true; // Stop propagation to prevent pareent handler interference
                        textInput.text = model.name;
                        console.log(model.name)
                        textInput.selectionMadeBool = true;
                        locationSelectionMade(textInput.text);
                        utilityFunctions.updateModel(textInput.text, filteredModel, otherTextInputChild ? otherTextInputChild.text : "");
                        locationPopup.close(); // Close the popup when an item is clicked
                    }
                }
            }
        }
    }
}