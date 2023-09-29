import QtQuick 2.15
import QtQuick.Controls 2.15
   
Rectangle {
    gradient: Gradient {
        GradientStop { position: 0.0; color: "dodgerblue" }
        GradientStop { position: 1.0; color: "skyblue" }
    }

    Text {
        id: bannerText
        anchors.centerIn: parent
        text: "Budget Voyager"
        font.pixelSize: 30 // Adjust the font size to your preference
        font.family: "Arial Black"
        color: "white"
        font.bold: true
    }

    Canvas {
        id: underline
        width: bannerText.width
        height: 10 // Adjust the maximum thickness of the underline
        anchors.top: bannerText.bottom
        anchors.topMargin: -5
        anchors.horizontalCenter: bannerText.horizontalCenter

        onPaint: {
            var ctx = getContext("2d");
            ctx.globalAlpha = 0.3
            ctx.beginPath();
            ctx.moveTo(0, 0); // Start at the top-left corner
            ctx.lineTo(width, 0); // Go to the top-right corner
            ctx.lineTo(0, height); // Go to the bottom-left corner
            ctx.closePath(); // Close the path
            ctx.fillStyle = "white";
            ctx.fill();
        }
    }
}