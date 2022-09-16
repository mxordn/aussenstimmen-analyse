from music21 import stream, interval, expressions, voiceLeading

class AsChecker():
    def __init__(self, s, partNumber):
        self.s1 = s
        self.md = self.s1.metadata
        self.p1 = self.s1.parts[0]
        if partNumber > len(self.s1.parts):
            self.bass = self.s1.parts[1]
        else:
            self.bass = self.s1.parts[partNumber]

    def hasFermata(self, someNote):
        for ornament in someNote.expressions:
            if type(ornament) == expressions.Fermata:
                return True
        return False

    #Hier werden alle anderen Progressionen gecheckt.
    def asPruefen(self, motion=False, relations=True, melody=True, parallels=True):
        for each in self.p1.flat.recurse().notesAndRests:
            if each.isRest:
                pass
            else:
                try:
                    eachBass = self.bass.flat.getElementAtOrBefore(each.offset)
                    eachBefore = self.p1.flat.getElementBeforeOffset(each.offset)
                    eachBassBefore = self.bass.flat.getElementBeforeOffset(each.offset)
                    klauselCheck = voiceLeading.VoiceLeadingQuartet(eachBefore, each, eachBassBefore, eachBass)
                    actualInterval = interval.Interval(eachBass, each)
                    bassProgression = interval.Interval(eachBassBefore, eachBass)


                    #Mehrere Bassnoten zur Melodie
                    aSlice = self.bass.flat.allPlayingWhileSounding(each)
                    for changedNote in aSlice.flat.notesAndRests:
                        if changedNote.isNote:
                            innerInterval = interval.Interval(changedNote, each)
                            if innerInterval.isConsonant():
                                changedNote.style.color = "green"
                            else:
                                changedNote.style.color = "red"
                    if motion:
                        if klauselCheck.contraryMotion():
                            klauselCheck.v1n2.style.color = "green"
                            klauselCheck.v2n2.style.color = "green"
                        elif klauselCheck.parallelMotion():
                            klauselCheck.v1n2.style.color = "blue"
                            klauselCheck.v2n2.style.color = "blue"
                        elif klauselCheck.similarMotion():
                            klauselCheck.v1n2.style.color = "blue"
                            klauselCheck.v2n2.style.color = "blue"
                        elif klauselCheck.noMotion():
                            klauselCheck.v1n2.style.color = "orange"
                            klauselCheck.v2n2.style.color = "orange"
                        elif klauselCheck.obliqueMotion():
                            klauselCheck.v1n2.style.color = "orange"
                            klauselCheck.v2n2.style.color = "orange"

                    if parallels:
                        #Quint- und Oktavparallelen checken
                        if klauselCheck.parallelFifth():
                            klauselCheck.v1n1.style.color = "red"
                            klauselCheck.v1n2.style.color = "red"
                            klauselCheck.v2n1.style.color = "red"
                            klauselCheck.v2n2.style.color = "red"
                            klauselCheck.v1n1.addLyric("Quintparallele")
                        elif klauselCheck.parallelOctave():
                            klauselCheck.v1n1.style.color = "red"
                            klauselCheck.v1n2.style.color = "red"
                            klauselCheck.v2n1.style.color = "red"
                            klauselCheck.v2n2.style.color = "red"
                            klauselCheck.v1n1.addLyric("Oktavparallele")
                        

                    if relations:
                        #wenn eachBass eine Pause ist, muss nichts gecheckt werden.
                        if eachBass.isNote:
                            if actualInterval.isConsonant() == False:
                                #if not actualInterval.name == "":
                                each.style.color = "red"
                                eachBass.style.color = "red"
                                if klauselCheck.isProperResolution():
                                    #print('Dissonanz mit guter Ausflösung')
                                    each.addLyric('Diss. \n aufgelöst')
                                else:
                                    each.addLyric("Dissonanz")

                    if melody:
                        #Check der Bassprogression auf falsche oder zu grosse Intervalle
                        if bassProgression.intervalClass == 6:
                            eachBass.style.color = "violet"
                            eachBass.addLyric("fieser Sprung")
                        elif bassProgression.direction == 1:
                            if bassProgression.semitones > 8 and bassProgression.semitones != 12:
                                eachBass.style.color = "violet"
                                eachBass.addLyric("fieser Sprung")
                        elif bassProgression.direction == -1:
                            if bassProgression.semitones < -7 and bassProgression.semitones != -12:
                                eachBass.style.color = "violet"
                                eachBass.addLyric("fieser Sprung")
                except:
                    print("except", each, each.offset)
                    try:
                        if eachBass.isNote:
                            actualInterval = interval.Interval(eachBass, each)
                            if actualInterval.isConsonant():
                                each.style.color = "green"
                                eachBass.style.color = "green"
                            else:
                                each.style.color = "red"
                                eachBass.style.color = "red"
                    except:
                        print('Seltsamer Fall', each, each.offset)

    def getAnnotatedStream(self):
        analyseDatei = stream.Stream()
        analyseDatei.append(self.p1)
        analyseDatei.append(self.bass)
        return analyseDatei
