import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15 
import "../components" as Components
import "../utilities" as Utilities

Item {
    signal dateSelectionMadePropagator(date dateClicked)

    property string boxLabel

    Utilities.UtilityFunctions {
        id: utilityFunctions
    }
    function hideDropdown() {
        popupDate.visible = false;
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
        onDateSelectionMade: function(dateClicked) {
            dateSelectionMadePropagator(dateClicked);
        }
    }
}