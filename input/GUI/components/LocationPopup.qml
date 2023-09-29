import QtQuick 2.15
import QtQuick.Controls 2.15
import "." as InputDir

Popup {
    id: locationPopup
    property var filteredModelInternal
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
        model: filteredModelInternal
        clip: true
        boundsBehavior: Flickable.StopAtBounds
        //cacheBuffer: filteredModel.count * 30
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
                    property string clickedModelName: "" // Store the model name when the MouseArea is created

                    Component.onCompleted: {
                        clickedModelName = model.name;  // Store the model name when the MouseArea is created
                    }
                    onClicked: function(mouse) {
                        if (debouncing) return;
                        debouncing = true;
                        mouse.accepted = true;

                        // Must redeclarae variable since delegate can be created and destroyed
                        var textInput = locationPopup.textInput;
                        var otherTextInputChild = locationPopup.otherTextInputChild;
                        var updateModelFunction = utilityFunctions.updateModel;// Assigning function reference
                        var currentFilteredModel = filteredModelInternal;
                        var parentPopup = locationPopup; // Passing reference to locationPopup

                        textInput.text = clickedModelName;
                        textInput.selectionMadeBool = true;
                        parentPopup.locationSelectionMade(textInput.text); // Send signal
                        updateModelFunction(textInput.text, currentFilteredModel, otherTextInputChild ? otherTextInputChild.text : "");
                        parentPopup.close();
                    }
                }
            }
        }
    }
}