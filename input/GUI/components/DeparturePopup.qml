import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15 

Popup {
    id : departurePopup
    signal dateSelectionMade(date dateClicked)

    closePolicy: Popup.NoAutoClose

    property var textInput
    property date currentDate: new Date()
    property real cellWidth: 40
    property real cellHeight: 30
    y: parent.y + parent.height
    width: cellWidth * 7
    height: 240 // Adjust as needed

    padding: 0
    background: Rectangle { color: "transparent" }

    onCurrentDateChanged: {
        updateDaysModel();
    }

    function updateDaysModel() {
        daysOfTheMonth.clear();
        let firstDay = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1).getDay();
        let daysInMonth = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 0).getDate();

        // Adjust firstDay to match the model starting with Monday
        firstDay = (firstDay === 0) ? 6 : firstDay - 1;

        // Add placeholders for the days before the first day
        for (let i = 0; i < firstDay; i++) {
            daysOfTheMonth.append({"day": 0, "isPlaceholder": true});
        }

        // Add the actual days of the month
        for (let i = 1; i <= daysInMonth; i++) {
            daysOfTheMonth.append({"day": i, "isPlaceholder": false});
        }
    }

    Rectangle {
        id: popupDate
        anchors.fill: parent

        ColumnLayout {
            anchors.fill: parent
            spacing: 0

            // Month Header
            Rectangle {
                Layout.fillWidth: true
                height: departurePopup.cellHeight
                color: "#e0e0e0"

                // Left arrow
                Item {
                    id: leftContainer
                    width: leftArrow.width
                    height: leftArrow.height
                    anchors.left: parent.left
                    anchors.leftMargin: 10 // adjust as needed
                    anchors.verticalCenter: parent.verticalCenter

                    Rectangle {
                        id: leftArrow
                        width: 20 
                        height: 20
                        color: "transparent"

                        Text {
                            text: "<"
                            font.bold: true
                            anchors.centerIn: parent
                        }

                        MouseArea {
                            anchors.fill: parent
                            cursorShape: Qt.PointingHandCursor
                            onClicked: {
                                departurePopup.currentDate = new Date(currentDate.getFullYear(), currentDate.getMonth() - 1, 1);
                            }
                        }
                    }
                }

                Label {
                    text: Qt.formatDate(departurePopup.currentDate, "MMMM yyyy")
                    color: "black"
                    font.bold: true
                    anchors.centerIn: parent
                }

                // Right arrow
                Item {
                    id: rightContainer
                    width: rightArrow.width
                    height: rightArrow.height
                    anchors.right: parent.right
                    anchors.rightMargin: 10 // adjust as needed
                    anchors.verticalCenter: parent.verticalCenter

                    Rectangle {
                        id: rightArrow
                        width: 20
                        height: 20 
                        color: "transparent"

                        Text {
                            text: ">"
                            font.bold: true
                            anchors.centerIn: parent
                        }

                        MouseArea {
                            anchors.fill: parent
                            cursorShape: Qt.PointingHandCursor
                            onClicked: {
                                departurePopup.currentDate = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 1);
                            }
                        }
                    }
                }
            }

            // Days of the week header
            GridView {
                id: weekHeader
                boundsBehavior: Flickable.StopAtBounds
                Layout.fillWidth: true
                height: departurePopup.cellHeight
                cellWidth: parent.width / 7
                cellHeight: departurePopup.cellHeight
                model: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
                
                delegate: Item {
                    width: cellWidth
                    height: cellHeight
                    
                    Rectangle {
                        width: parent.width
                        height: parent.height
                        anchors.centerIn: parent
                        color: "transparent" // Since you might not need a background color for this
                        
                        Text {
                            anchors.centerIn: parent
                            text: modelData
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                            color: "black"
                            font.bold: true
                        }
                    }
                }
            }

            // Days of the month 
            GridView {
                id: gridView
                boundsBehavior: Flickable.StopAtBounds
                Layout.fillWidth: true
                Layout.fillHeight: true
                cellWidth: parent.width / 7
                cellHeight: departurePopup.cellHeight
                model: ListModel {
                    id: daysOfTheMonth
                    // Add code here to populate the model with the days of the current month
                    Component.onCompleted: departurePopup.updateDaysModel();
                }
                
                delegate: Item {
                    width: cellWidth
                    height: cellHeight
                    
                    Rectangle {
                        id: dayRect
                        width: parent.width
                        height: parent.height
                        anchors.centerIn: parent
                        color: "white"
                        
                        Text {
                            anchors.centerIn: parent
                            text: model.isPlaceholder ? "" : model.day
                            color: (model.isPlaceholder || (new Date(currentDate.getFullYear(), currentDate.getMonth(), model.day) < new Date())) ? "lightgray" : "black"
                        }
                        
                        MouseArea {
                            id: mouseArea
                            anchors.fill: parent
                            // Check if the date is before the current date or if it's a placeholder
                            enabled: !model.isPlaceholder && !(new Date(currentDate.getFullYear(), currentDate.getMonth(), model.day) < new Date())
                            // Set the cursor shape depending on the enabled property
                            cursorShape: enabled ? Qt.PointingHandCursor : Qt.ForbiddenCursor
                            hoverEnabled: true 
                            onClicked: {
                                if (enabled) {
                                    let clickedDate = new Date(currentDate.getFullYear(), currentDate.getMonth(), model.day);
                                    textInput.text = Qt.formatDate(clickedDate, "ddd, dd MMM");
                                    dateSelectionMade(clickedDate);
                                    departurePopup.close();
                                }
                            }
                            onEntered: {
                                dayRect.color = enabled ? "#d0d0d0" : "white"; // change color on mouse enter only if enabled
                            }
                            onExited: {
                                dayRect.color = "white"; // revert to default color on mouse exit
                            }
                        }
                    }
                }
            }
        }
    }
}
