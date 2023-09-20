import QtQuick 2.15
import QtQuick.Controls 2.15
import "../components" as Components
import "../utilities" as Utilities

Item {
    // Components from parent
    property var dropDownListView

    property string boxLabel: "Label"

    // External properties to handle unique behavior
    property var filteredModel: undefined  // Placeholder for the filtered model
    property var otherTextInput: null
    property var otherDropdownListView: null

    Utilities.UtilityFunctions {
        id: utilityFunctions
    }
    function hideDropdown() {
        dropDownListView.visible = false;
    }

    Components.LabelledTextInput {
        id: textBoxArea
        readOnly: false
        boxLabel: "Location"
        popupComponent: dropDownListView
        utilityFunctions: utilityFunctions
    }

    Components.LocationPopup {
        id: dropDownListView
        textInput: textBoxArea.textInput
    }

 
}

