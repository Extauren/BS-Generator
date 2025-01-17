import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "components"

Window {
    width: 300
    height: 200
    visible: true
    title: "BS Generator"

    readonly property list<string> texts: ["Hallo Welt", "Hei maailma",
                                           "Hola Mundo", "Привет мир"]

    function setText() {
        var i = Math.round(Math.random() * 3)
        text.text = texts[i]
    }

    ColumnLayout {
        anchors.fill:  parent

        Text {
            id: text
            text: "BS Generator"
            Layout.alignment: Qt.AlignHCenter
        }

        TextField {
            placeholderText: qsTr("Nom de la structure")
            Layout.alignment: Qt.AlignHCenter
        }
        
        ButtonGroup {
            buttons: column.children
            onClicked: console.log("clicked:", button.text)
        }
        
        Row {
            id: column
            Layout.alignment: Qt.AlignHCenter

            RadioButton {
                checked: true
                text: qsTr("BS")
            }

            RadioButton {
                text: qsTr("BSA AIR")
            }
        }

        ProgressBar{}

        Button {
            onClicked: setText()

            contentItem: Text {
                text: "GENERATE BS"
                // font: 10
                // opacity: enabled ? 1.0 : 0.3
                // color: control.down ? "#17a81a" : "#21be2b"
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                elide: Text.ElideRight
            }

            background: Rectangle {
                implicitWidth: 150
                implicitHeight: 40
                opacity: enabled ? 1 : 0.3
                border.color: control.down ? "#17a81a" : "#21be2b"
                border.width: 1.5
                radius: 15
            }
            Layout.alignment: Qt.AlignHCenter
        }
    }
}