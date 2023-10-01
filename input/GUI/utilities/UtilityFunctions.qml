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

    function handleVisibilityFor(textInput, locationPopup) {
        locationPopup.visible = (textInput && textInput.text.length > 0); // Checks if text present
    }
    function updateSearchBoxState() {
        if (fromBoxSelected && toBoxSelected && departureDateSelected) {
            searchBox.isSearchBoxEnabled = true;
        }
    }

    function transformDate(inputDate) {
        // Helper function to zero-pad numbers less than 10
        function zeroPad(num) {
            return (num < 10 ? "0" : "") + num;
        }

        // If inputDate is of MockDate type
        if (inputDate.hasOwnProperty("day") && inputDate.hasOwnProperty("month") && inputDate.hasOwnProperty("year")) {
            // Handle MockDate object
            var day = zeroPad(inputDate.day);
            var month = zeroPad(inputDate.month + 1); // +1 to adjust 0-indexed month
            var year = inputDate.year;
            return day + "." + month + "." + year;
        } 
        // Else, handle as a regular Date
        else {
            var months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
            var dateParts = inputDate.toString().split(" ");
            
            var day = zeroPad(parseInt(dateParts[2], 10));
            var month = zeroPad(months.indexOf(dateParts[1]) + 1);  // +1 since months array is 0-indexed
            var year = dateParts[4];
            
            return day + "." + month + "." + year;
        }
    }

    function extractTimeFromISOString(isoString) {
        try {
            var date = new Date(isoString);
            var hours = date.getHours();
            var minutes = date.getMinutes();

            // Pad single digit minutes or hours with a leading zero
            var formattedHours = hours.toString().padStart(2, '0');
            var formattedMinutes = minutes.toString().padStart(2, '0');

            return formattedHours + ":" + formattedMinutes;
        } catch (error) {
            console.error("Failed to extract time from ISO string:", error);
            return "";
        }
    }

  
}