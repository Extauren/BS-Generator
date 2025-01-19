import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs
import QtCore
// import "components"
import bs_generator 1.0

Window {
    width: 600
    height: 400
    visible: true
    title: "BS Generator"

    function checkArgument(structure, bsType) {
        if (structure == "") {
            dialog.text = "Structure name is missing"
            dialog.open()
            return
        }
        if (fileDialog.selectedFile == "") {
            dialog.text = "File path is missing"
            dialog.open()
            return
        }
        else {
            pyConsole.generate_bs(structure, false, fileDialog.selectedFile)
            dialog.open()
        }
    }

    Console {
        id: pyConsole
    }

    ColumnLayout {
        spacing: 50
        anchors.horizontalCenter: parent.horizontalCenter

        Rectangle {}

        Text {
            id: text
            text: "BS Generator"
            Layout.alignment: Qt.AlignHCenter
        }

        TextField {
            id: textField
            placeholderText: qsTr("Structure name")
            Layout.alignment: Qt.AlignHCenter
            // background: Rectangle {
            //     implicitWidth: 150
            //     implicitHeight: 30
            //     opacity: enabled ? 1 : 0.3
            //     border.width: 1.5
            //     radius: 10
            // }
        }
        
        ButtonGroup {
            id: bsType
            buttons: column.children
            onClicked: console.log("clicked:", button.text)
        }
        
        Row {
            id: column
            Layout.alignment: Qt.AlignHCenter
            RadioButton {
                checked: true
                text: qsTr("SEP")
            }
            RadioButton {
                text: qsTr("BSA AIR")
            }
            RadioButton {
                text: qsTr("SAS")
            }
        }

        ColumnLayout {
            Layout.alignment: Qt.AlignHCenter
            CheckBox {
                checked: false
                text: qsTr("Generate Docx")
            }
        }

        Button {
            text: qsTr("Choose location")
            onClicked: fileDialog.open()
            Layout.alignment: Qt.AlignHCenter
            // background: Rectangle {
                // implicitWidth: 150
                // implicitHeight: 40
                // opacity: enabled ? 1 : 0.3
                // border.color: control.down ? "#17a81a" : "#21be2b"
                // border.width: 1.5
                // radius: 15
            // }
        }

        FileDialog {
            id: fileDialog
            fileMode: FileDialog.SaveFile
            currentFolder: StandardPaths.standardLocations(StandardPaths.PicturesLocation)[0]
        }

        // ProgressBar{}

        Button {
            onClicked: checkArgument(textField.text, bsType.text)
            // contentItem: Text {
            //     text: "GENERATE"
            //     // font: 10
            //     // opacity: enabled ? 1.0 : 0.3
            //     // color: control.down ? "#17a81a" : "#21be2b"
            //     horizontalAlignment: Text.AlignHCenter
            //     verticalAlignment: Text.AlignVCenter
            //     elide: Text.ElideRight
            // }
            // background: Rectangle {
            //     implicitWidth: 110
            //     implicitHeight: 40
            //     opacity: enabled ? 1 : 0.3
            //     border.width: 1.5
            //     radius: 15
            // }
            Layout.alignment: Qt.AlignHCenter
        }

        MessageDialog {
            id: dialog
            buttons: MessageDialog.Ok
            text: "The BS was generate sucessfully"
        }
    }
}