import QtQuick 2.15
import QtQuick.Controls 2.15
import "../components" as Components
import "../utilities" as Utilities

Item {
    // Components from parent
    property var locationPopup
    property var filteredModel
    property string boxLabel

    // External properties to handle unique behavior
    property var otherTextInput: null
    property var otherLocationPopup: null

    Utilities.UtilityFunctions {
        id: utilityFunctions
    }
    function hidePopup() {
        locationPopup.close();
    }

    Components.LabelledTextInput {
        id: textBoxArea
        readOnly: false
        boxLabelInner: boxLabel
        popupComponent: locationPopup
        utilityFunctions: utilityFunctions
        filteredModelInternal: filteredModel
        imageSource: "assets/location_picture_transparent.webp"
    }

    Components.LocationPopup {
        id: locationPopup
        textInput: textBoxArea.textInput
        x: textBoxArea.x
        y: textBoxArea.y + textBoxArea.height
    } 
    
 
}

