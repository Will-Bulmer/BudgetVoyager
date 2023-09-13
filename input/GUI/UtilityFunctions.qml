import QtQuick 2.15

QtObject {
    objectName: "testObject" // Only named for testing purposes.
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
}