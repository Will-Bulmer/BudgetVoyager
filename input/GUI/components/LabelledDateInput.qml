import QtQuick 2.15
import QtQuick.Controls 2.15

MouseArea {
    property alias textInput: textInput

 
    
    id: hoverArea
    anchors.fill: parent
    hoverEnabled: true

    property string boxLabelInner
    property bool readOnly: false
    property var popupComponent: null
    property var utilityFunctions: null
    property var imageSource: null

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
                text: boxLabelInner
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
                source: imageSource
                width: 15
                height: parent.height * 0.6
                anchors.verticalCenter: parent.verticalCenter
                anchors.left: parent.left
                anchors.leftMargin: 5
                opacity: 0.7  // Set to desired value between 0 and 1
            }

            TextField {
                id: textInput
                property bool selectionMade: false
                width: parent.width - 4
                height: parent.height - 4
                anchors.centerIn: parent
                verticalAlignment: TextInput.AlignVCenter
                leftPadding: locationIcon.width + 10
                readOnly: true
                placeholderTextColor: "gray" // style the placeholder as you wish

                onActiveFocusChanged: {
                    if (activeFocus) {
                        if (popupComponent) {
                            popupComponent.open();
                        }

                    } else {
                        if (popupComponent) {
                            popupComponent.close();
                        }
                    }
                }
            }
        }
    }
}

