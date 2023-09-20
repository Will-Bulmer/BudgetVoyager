import QtQuick 2.15
import QtQuick.Controls 2.15

MouseArea {
    property alias textInput: textInput

    id: hoverArea
    anchors.fill: parent
    hoverEnabled: true

    property string boxLabel: "Label"
    property bool readOnly: false
    property var popupComponent: null
    property var utilityFunctions: null
    property var filteredModelInternal
    property var otherTextInput: null
    property var otherDropdownListView: null

    onClicked: {
        textInput.forceActiveFocus();
    }

    onContainsMouseChanged: {
        if (containsMouse) {
            textInputWrapper.color = "#d0d0d0"; // hover color
        } else {
            textInputWrapper.color = "white"; // default color
        }
    }

    FocusScope {
        id: focusArea
        anchors.fill: parent

        Rectangle {
            width: parent.width
            height: parent.height / 2
            color: "white"
            anchors.top: parent.top
            anchors.left: parent.left

            Label {
                text: boxLabel
                color: "grey"
                anchors.left: parent.left
                anchors.bottom: parent.bottom
            }
        }

        Rectangle {
            id: textInputWrapper
            width: parent.width
            height: parent.height / 2
            border.color: "black"
            border.width: 1
            color: hoverArea.containsMouse ? "#d0d0d0" : "white"
            radius: 4
            anchors.bottom: parent.bottom

            Image {
                id: locationIcon
                source: "assets/location_picture.jpg"
                width: 24
                height: parent.height * 0.8
                anchors.verticalCenter: parent.verticalCenter
                anchors.left: parent.left
                anchors.leftMargin: 5
            }

            TextInput {
                id: textInput
                property bool selectionMade: false
                property bool italicize: false
                property string previousSelection: ""
                font.italic: italicize
                width: parent.width - 4
                height: parent.height - 4
                anchors.centerIn: parent
                verticalAlignment: TextInput.AlignVCenter
                leftPadding: locationIcon.width + 10
                readOnly: readOnly

                onTextChanged: {
                    if (utilityFunctions) {
                        utilityFunctions.updateModel(text, filteredModel, otherTextInput ? otherTextInput.text : "");
                        utilityFunctions.handleVisibilityFor(textInput, popupComponent);
                    }
                }

                onActiveFocusChanged: {
                    if (activeFocus) {
                        if (popupComponent) {
                            popupComponent.open()
                        }
                    } else {
                        if (popupComponent) {
                            popupComponent.close()
                        }
                    }
                    if (!activeFocus && !selectionMade) {
                        text = "";
                    }
                    if (activeFocus && text === "") {
                        selectionMade = false;
                    }
                }
            }
        }
    }
}

