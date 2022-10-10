import QtQuick 2.9

import QtQuick.Dialogs 1.0
import QtQuick.Controls 1.2
import QtQuick.Layouts 1.0
import Qt.labs.settings 1.0
import QtQuick.Window 2.0  

import MuseScore 3.0
import FileIO 3.0

MuseScore {
      menuPath: "Plugins.As-Checker"
      description: "Annotation of Two-part-settings within a score."
      requiresScore: true
      version: "1.0"
      
      pluginType: "dialog"
      id: root
      width: content.width
      height: 600
      Layout.minimumWidth: 400
      Layout.minimumHeight: 580
      onRun: {
            console.log("Hallo")
            directorySelectDialog.folder = ((Qt.platform.os == "windows")? "file:///" : "file://");
            //Qt.quit()
            console.log(exportDir, dirIsSet)
       }
      
      FileIO {
            id: xmlFile
            onError: console.log(msg + "  Filename = " + xmlFile.source)
      }
      FileIO {
            id: helperFile
            onError: console.log(msg + "  Filename = " + helperFile.source)
      }
      
      property string exportDir: ""
      property string tempDir: ""
      property bool dirIsSet: false

      
             
      ColumnLayout {
          width: parent.width
          height: parent.height / 8
          id: titlesection
          Text {
                  id: title
                  Layout.leftMargin: 10
                  text: "<h2>Aussenstimmen Analyse</h2>"
            }
            Text {
                  id: desc
                  anchors.top: title.bottom
                  text: "This Plugin checks the outer voice setting for clauses <br> and counterpoint movements.</p>"
                  Layout.leftMargin: 10

            }
      }

      Rectangle {
            id: contentFrame
            anchors.top: titlesection.bottom
            //anchors.centerIn: root
            border {width: 2
                        color: "grey" }
            width: content.width
            height: content.height
            color: "#9acd32"
            ColumnLayout {
                  id: content
                  Layout.margins: 10

                  Text {
                        id: instr1
                        text: "<p>1) Please specify the two staves that should be compared and <br> select the annotations that you want.</p>"
                        Layout.leftMargin: 10
                        Layout.topMargin: 20
                  }
                  RowLayout {
                        id: stavesRow
                        anchors.top: instr1.bottom
                        TextField {
                              id: firstStaff
                              text: "1"
                              placeholderText: qsTr("staff number")
                              maximumLength: 2
                              focus: true
                              validator: IntValidator {bottom: 1; top: 31;}
                              Layout.leftMargin: 10
                              Layout.bottomMargin: 10
                        }

                        TextField {
                              id: secondStaff
                              text: "2"
                              placeholderText: qsTr("staff number")
                              maximumLength: 2
                              focus: true
                              validator: IntValidator {bottom: 1; top: 31;}
                              Layout.leftMargin: 10
                              Layout.bottomMargin: 10
                        }
                  }
                  
                  ColumnLayout {
                        anchors.top: secondStaff.bottom
                        Layout.leftMargin: 10
                        Text {
                              id: checkBoxes
                              anchors.top: parent.top
                              text: "<h3>Select elements to check for</h3>"
                        }
                        Text {
                              id: counterpoint
                              anchors.top: checkboxes.bottom
                              text: "<h4>2-part counterpoint</h4>"
                        }
                        CheckBox {
                              id: intervalBox
                              anchors.top: counterpoint.bottom
                              checked: true
                              text: qsTr("consonances and dissonances")
                        }
                        CheckBox {
                              id: parallelBox
                              checked: true
                              text: qsTr("parallels (parallel octaves and fifths)")
                        }
                        CheckBox {
                              id: motionBox
                              checked: true
                              text: qsTr("motions (parallel/contrary/oblique motion)")
                        }
                        CheckBox {
                              id: melodyBox
                              checked: true
                              text: qsTr("untypical melodic jumps")
                        }
                        Text {
                              id: clauses
                              anchors.top: checkboxes.bottom
                              text: "<h4>Clauses</h4>"
                        }
                        CheckBox {
                              id: klauselnBox
                              anchors.top: clauses.bottom
                              checked: true
                              text: qsTr("Klauseln/clauses")
                        }
                        CheckBox {
                              id:klauselnBoxAlle
                              Layout.leftMargin: 20
                              checked: false
                              text: qsTr("Klauseln prüfen (alle Noten einschließen)")
                        }
                  }
                  Text {
                        id: instr2
                        text: "2) Select a location where the annotated file should be saved:"
                        Layout.margins: 10
                  }
                  
                  RowLayout {
                        Button {
                              id: selectDirectory
                              Layout.margins: 10
                              text: qsTranslate("Dialog", "Choose path…")
                              onClicked: {
                                    directorySelectDialog.open();
                              }
                        }
                        Label {
                              id: exportDirectory
                              Layout.margins: 10
                              text: "<No location selected>"
                        }
                  }

                  FileDialog {
                        id: directorySelectDialog
                        title: qsTranslate("MS::PathListDialog", "Choose a directory")
                        selectFolder: true
                        visible: false
                        onAccepted: {
                              exportDir = this.folder.toString() + "/" + curScore.scoreName + "-annotated.musicxml";
                              tempDir = this.folder.toString() + "/" + curScore.scoreName + "-helper.musicxml";

                              xmlFile.source = exportDir.replace("file://", "/");
                              helperFile.source = tempDir.replace("file://", "/");
                              dirIsSet = true                        
                              var substrings = exportDir.split("/");
                              console.log(substrings, substrings[substrings.length - 1])
                              exportDirectory.text = "Save to: " + "…/" + substrings[substrings.length - 2] + "/" + substrings[substrings.length - 1]
                        }
                        Component.onCompleted: visible = false
                  }
            }
      }

      RowLayout {
            id: actions
            anchors.top: contentFrame.bottom
            width: contentFrame.width
            
            Button {
                  id: analyseButton
                  text: "Analysieren!"
                  Layout.margins: 10
                  onClicked: {
                        //var filePath = "/Users/moritzheffter/Downloads/temp-file.musicxml"
                        //xmlFile.source = exportDirectory.text.replace("file://", "/")
                        console.log("Schreiben: " + helperFile.source)
                        if (dirIsSet & exportDir != "") {
                              writeScore(curScore, helperFile.source, "musicxml")
                              console.log("Lesen")
                              readScore(helperFile.source)
                              console.log(filePath);
                              Qt.quit()      
                        }
                        else { console.log("Please select a directory.") }
                        
                        console.log("filePath: " + filePath + " " + curScore)
                        var xmlText = helperFile.read()
                        //console.log("thisScore: " + xmlText)
                        var content = "content=" + encodeURIComponent(xmlText)
                        if (klauselnBoxAlle.checked & klauselnBox.checked) {
                              var klauseln = "klauseln=alletrue" //+ encodeURIComponent(klauselnBox.checked)
                        }
                        if (klauselnBox.checked & !klauselnBoxAlle.checked) {
                              var klauseln = "klauseln=fermatentrue"// + encodeURIComponent(klauselnBox.checked)
                        }
                        if (parallelBox.checked) {
                              var parallelen = "parallelen=true" //+ encodeURIComponent(klauselnBox.checked)
                        }
                        if (motionBox.checked) {
                              var bewegung = "bewegung=true"
                        }
                        if (melodyBox.checked) {
                              var melodie = "melodie=true" //+ encodeURIComponent(klauselnBox.checked)
                        }
                        var topVoice = "topVoice=" + encodeURIComponent(firstStaff.text)
                        var bassVoice = "bassVoice=" + encodeURIComponent(secondStaff.text)
                        var aussenstimmen = "aussenstimmen=true"
                        // + encodeURIComponent(intervalBox.checked)
                        var form = content + "&"  + klauseln + "&" + aussenstimmen + "&" + parallelen + "&" + melodie + "&" + bewegung + "&" + topVoice + "&" + bassVoice;
                        //console.log("content : " + content)

                        var request = new XMLHttpRequest()
                        
                        request.open("POST", "http://satzlehre-online.de:8101/as/analyse", true)
                        request.setRequestHeader("Content-Type", "application/x-www-form-urlencoded")
                        request.send(form)

                        request.onreadystatechange = function() {
                        if (request.readyState == XMLHttpRequest.DONE) {
                              var response = request.responseText
                              console.log("responseText : " + response)
                              //xmlFile.source = filePath + "-new.xml"
                              helperFile.write(response)
                              //xmlFile.write(response)
                              //readScore(xmlFile.source)
                              readScore(helperFile.source)
                              //helperFile.source = ""
                              
                              Qt.quit()
                              }
                        }
                  }
            }

      Button {
            text: "Close and quit"
            Layout.rightMargin: 10
            anchors.right: parent.right
            onClicked: { Qt.quit() }
            }
      }
}