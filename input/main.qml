import QtQuick 2.15
import QtQuick.Controls 2.15

// Path might need setting every time?
// export QML2_IMPORT_PATH=/home/will_bulmer/.local/lib/python3.10/site-packages/PyQt6/Qt6/qml
// echo $QML2_IMPORT_PATH

// TODO: Validate JSON data before preceding. Need error handling and tests for all qml functionality. Introduce retry mechanisms.
// TODO: Take out all functionality into a separate qml file? Or header file?


ApplicationWindow {
    visible: true
    width: 500  // Adjusted width to better accommodate two boxes
    height: 500
    title: "Textbox with Dynamic Dropdown"
    color: "white"

    property var fullList : [""]

    Component.onCompleted: {
        target: jsonBackend
        Qt.callLater(function() {
            console.log("Attempting to open JSON file");
            jsonBackend.loadJSON("input/flixbus/bus_stops.json");
        });
    }

    Connections {
        target: jsonBackend

        function onJsonLoaded() {
            console.log("JSON data loaded successfully");
            
            try {
                var parsedData = JSON.parse(jsonBackend.jsonData);
                
                // Reset the fullList and filteredModels
                fullList = [];
                filteredModelLeft.clear();
                filteredModelRight.clear();
                
                for (var key in parsedData) {
                    fullList.push(parsedData[key].name);
                    filteredModelLeft.append({"name": parsedData[key].name});
                    filteredModelRight.append({"name": parsedData[key].name});
                }

                // Update both input models initially after loading the JSON
                updateModel("", filteredModelLeft, "");
                updateModel("", filteredModelRight, "");
            } catch (error) {
                console.error("Failed to parse JSON data:", error);
            }
        }

        function onJsonLoadError(errorMessage) {
            console.error("Failed to load JSON data:", errorMessage);
        }
    }

    function updateModel(inputText, modelToUpdate, otherTextboxValue) {
    modelToUpdate.clear();
    for (var i = 0; i < fullList.length; i++) {
        var itemName = fullList[i];
        if ((itemName.toLowerCase().startsWith(inputText.toLowerCase()) || inputText === "") 
            && itemName !== otherTextboxValue) {
            modelToUpdate.append({"name": itemName});
        }
    }
}

    function highlightText(fullText, searchText) {
        if (!fullText) return "";
        if (searchText === "") return fullText;
        var regExp = new RegExp("(" + searchText + ")", "ig");
        return fullText.replace(regExp, "<span style='background-color: yellow'>$1</span>");
    }

    function handleVisibilityFor(textInput, dropDownListView, otherDropDownListView) {
        dropDownListView.visible = (textInput.text.length > 0);
        otherDropDownListView.visible = false;
    }

    /*
    Component.onCompleted: {
        updateModel("", filteredModelLeft);
        updateModel("", filteredModelRight);
    }
    */

    Item {
        id: inputBoxesContainer
        height: 54
        width: parent.width
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: parent.top
        anchors.topMargin: 50

        // Include fromBox.qml (LEFT)
        Item {
            id: inputContainerLeft
            height: 54
            width: inputBoxesContainer.width * 0.5 // 50% of the parent's width
            anchors.left: parent.left

            ListView {
                id: dropDownListViewLeft
                width: parent.width
                y: parent.y + parent.height
                visible: textInputLeft.activeFocus
                anchors.horizontalCenter: parent.horizontalCenter
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
                            text: highlightText(model.name, textInputLeft.text)
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
                width: 50
                height: 20
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
                width: 204
                height: 34
                border.color: "black"
                border.width: 1
                color: "white"
                radius: 4
                anchors.bottom: parent.bottom

                Image {
                    id: locationIconLeft
                    source: "assets/location_picture.jpg"
                    width: 24
                    height: 24
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
                        updateModel(text, filteredModelLeft, textInputRight.text);
                        handleVisibilityFor(textInputLeft, dropDownListViewLeft, dropDownListViewRight);
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

        // The right input box ("To")
        Item {
            id: inputContainerRight
            height: parent.height
            width: inputBoxesContainer.width * 0.5 // 50% of the parent's width
            anchors.right: parent.right
            //anchors.left: inputContainerLeft.right
            //anchors.right: parent.right // Make this textbox flush to the right
            anchors.rightMargin: inputBoxesContainer.width * 0.094

            ListView {
                id: dropDownListViewRight
                width: parent.width
                y: parent.y + parent.height
                visible: textInputRight.activeFocus
                anchors.horizontalCenter: parent.horizontalCenter
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
                            text: highlightText(model.name, textInputRight.text)
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
                width: 50
                height: 20
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
                width: 204
                height: 34
                border.color: "black"
                border.width: 1
                color: "white"
                radius: 4
                anchors.bottom: parent.bottom

                Image {
                    id: locationIconRight
                    source: "assets/location_picture.jpg"
                    width: 24
                    height: 24
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
                        updateModel(text, filteredModelRight, textInputLeft.text);
                        handleVisibilityFor(textInputRight, dropDownListViewRight, dropDownListViewLeft);
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
    }
        

    Button {
        text: "Quit"
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 20
        onClicked: {
            Qt.quit()
        }
    }

    ListModel {
        id: filteredModelLeft
    }

    ListModel {
        id: filteredModelRight
    }
}





