import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15 
import "../components" as Components
import "../utilities" as Utilities

Item {

    property string boxLabel

    Utilities.UtilityFunctions {
        id: utilityFunctions
    }
    function hideDropdown() {
        popupDate.visible = false;
    }
    // Model for the days of the month
    property var daysOfTheMonth: []
    Component.onCompleted: {
        for(var i = 1; i <= 31; i++) {
            daysOfTheMonth.push(i);
        }
    }

    // TEXTBOX AND TITLE
    Components.LabelledDateInput {
        id: textBoxArea
        popupComponent: departurePopup
        utilityFunctions: utilityFunctions
        boxLabelInner: boxLabel
        imageSource: "assets/calender_icon_transparent.png"
    }

    Components.DeparturePopup {
        id: departurePopup
        textInput: textBoxArea.textInput
        x: textBoxArea.x
        y: textBoxArea.y + textBoxArea.height
    }
}