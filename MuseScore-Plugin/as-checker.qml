import QtQuick 2.1
import QtQuick.Dialogs 1.0
import QtQuick.Controls 1.0
import QtQuick.Layouts 1.0
import MuseScore 3.0
import FileIO 3.0

MuseScore {
    menuPath: "Plugins.Außenstimmen-Check"
    version: "1.0"
    description: qsTr("This plugin calls the Aussenstimmen App API in order to perform checks on your two voice setting e.g. for voiceleading and clauses.")
    requiresScore: true
    pluginType: "dialog"

    id:window
    width:  290; height: 150;
    onRun: {}

    FileIO {
        id: myFile
        onError: console.log(msg + "  Filename = " + myFileAbc.source)
        }

    FileIO {
        id: myXmlScore
        onError: console.log(msg)
        }
    
    ColumnLayout {
        id: column
        width: parent.width
        y: 10
        x: 10
        spacing: 10

        CheckBox {
            id:klauselnBox
            checked: true
            text: qsTr("Klauseln prüfen")
        }

            CheckBox {
                id:klauselnBoxAlle
                checked: false
                text: qsTr("Klauseln prüfen (alle Noten einschließen)")
            }
        
        CheckBox {
            id:intervalBox
            checked: true
            text: qsTr("Außenstimmensatz prüfen")
        }
    }

    RowLayout {
        id: buttonRow
        width: parent.width
        anchors {
            bottom: parent.bottom
            margins: 10
        }

        Button {
            id : buttonCheck
            isDefault: true
            anchors {
                  left: parent.left
                  margins: 10
            }
            text: qsTr("Check")
            onClicked: {
                var filePath = "/Users/moritzheffter/Downloads/test-file"
                console.log("filePath: " + filePath + " " + curScore)
                writeScore(curScore, filePath, "xml")
                
                myXmlScore.source = filePath + ".xml"
                var xmlText = myXmlScore.read()
                //console.log("thisScore: " + xmlText)
                var content = "content=" + encodeURIComponent(xmlText)
                if (klauselnBoxAlle.checked & klauselnBox.checked) {
                    var klauseln = "klauseln=alle" + encodeURIComponent(klauselnBox.checked)
                }
                if (klauselnBox.checked & !klauselnBoxAlle.checked) {
                    var klauseln = "klauseln=fermaten" + encodeURIComponent(klauselnBox.checked)
                }
                
                var aussenstimmen = "aussenstimmen=" + encodeURIComponent(intervalBox.checked)
                var form = content + "&"  + klauseln + "&" + aussenstimmen

                //console.log("content : " + content)

                var request = new XMLHttpRequest()
                request.onreadystatechange = function() {
                    if (request.readyState == XMLHttpRequest.DONE) {
                        var response = request.responseText
                        console.log("responseText : " + response)
                        myFile.source = filePath + "-new.xml"
                        myFile.write(response)
                        readScore(myFile.source)
                            Qt.quit()
                        }
                    }
                request.open("POST", "http://127.0.0.1:8100/aschecker/analyse", true)
                request.setRequestHeader("Content-Type", "application/x-www-form-urlencoded")
                request.send(form)
            }
        }

        Button {
            id : buttonCancel
            anchors {
                  right: parent.right
                  margins: 10
            }
            text: qsTr("Cancel")
            onClicked: {
                    console.log(klauselnBox.checked)
                    Qt.quit();
                }
            }
        }
    }
