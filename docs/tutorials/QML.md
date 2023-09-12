# A Dump of Info for QML

# 1. ListView

### Basic Usage
```qml
import QtQuick 2.15

ListView {
    width: 200; height: 400

    model: ListModel {
        ListElement { name: "Apple" }
        ListElement { name: "Banana" }
        ListElement { name: "Cherry" }
    }

    delegate: Text {
        text: model.name
    }
}
```

**model**: Describes the data that the ListView displays. It can be a ListModel, an array, or other types of models.
**delegate**: Describes how each item in the list looks. It can be any type of item, not just a Text.
**currentIndex**: The index of the current item. Can be used for tracking the selected item.
**orientation**: Specifies the scroll direction; can be Qt.Vertical (default) or Qt.Horizontal.
**spacing**: Defines the spacing between items in the list.

**onCurrentIndexChanged**: Triggered when the currentIndex changes.
**onCountChanged**: Triggered when the number of items in the model changes.

### Advanced Usage

```qml
ListView {
    width: 200; height: 400
    highlight: Rectangle { color: "lightblue"; radius: 5 }
    focus: true

    model: ["Apple", "Banana", "Cherry"]

    delegate: Text {
        text: modelData
        MouseArea {
            anchors.fill: parent
            onClicked: listView.currentIndex = index
        }
    }
}
```
Here, a **MouseArea** is used in the **delegate** so that items can be clicked to change the **currentIndex**, and a **Rectangle** is used as the **highlight**.