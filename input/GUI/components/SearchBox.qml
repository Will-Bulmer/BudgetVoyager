import QtQuick 2.15
import QtQuick.Controls 2.15

Item {
    property string boxLabel: "Label"

    Rectangle {
        width: parent.width
        height: parent.height
        border.color: "#FFA500"  
        border.width: 1
        color: "#FFA500"  // Yellowy orange color
        radius: 4

        Text {
            text: "Search"
            anchors.centerIn: parent
            color: "black"
        }
    }
}
