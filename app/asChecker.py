from music21 import stream, interval, expressions, voiceLeading

class AsChecker():
    def __init__(self, s, partNumber):
        self.s1: stream.Stream = s
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
    def asPruefen(self, consDiss=True, motion=False, melody=True, parallels=True):
        sc = self.s1.chordify()

        for i in sc.flat.notesAndRests.recurse():

            v1n2 = self.s1.parts[0].flat.notesAndRests.getElementAtOrBefore(i.offset)
            v2n2 = self.s1.parts[1].flat.notesAndRests.getElementAtOrBefore(i.offset)

            try:
                vlq = voiceLeading.VoiceLeadingQuartet(v1n1, v1n2, v2n1, v2n2)
            except:
                vlq = None
                print('Not Working!')

            try:
                if consDiss:
                    if i.isConsonant():
                        if self.s1.parts[0].flat.notesAndRests.getElementAtOrBefore(i.offset).style.color == None:
                            self.s1.parts[0].flat.notesAndRests.getElementAtOrBefore(i.offset).style.color = 'violet'
                        if self.s1.parts[1].flat.notesAndRests.getElementAtOrBefore(i.offset).style.color == None:
                            self.s1.parts[1].flat.notesAndRests.getElementAtOrBefore(i.offset).style.color = 'violet'

                    else:
                        if self.s1.parts[0].flat.notesAndRests.getElementAtOrBefore(i.offset).style.color == None:
                            self.s1.parts[0].flat.notesAndRests.getElementAtOrBefore(i.offset).style.color = 'red'
                        if self.s1.parts[1].flat.notesAndRests.getElementAtOrBefore(i.offset).style.color == None:
                            self.s1.parts[1].flat.notesAndRests.getElementAtOrBefore(i.offset).style.color = 'red'
            except:
                print('Error in normal check (e.g. Chords)', i, i.offset)
            
            if vlq:
                if motion:
                        self._motus((vlq.contraryMotion()), vlq, 'green', allowedColors=['violet', None])
                        self._motus((vlq.parallelMotion() or vlq.similarMotion()), vlq, 'blue', allowedColors=['violet', None])
                        self._motus((vlq.obliqueMotion()), vlq, 'orange', allowedColors=['violet', None])

                if parallels:
                    #Quint- und Oktavparallelen checken
                    if vlq.parallelFifth():
                        vlq.v1n1.style.color = "red"
                        vlq.v1n2.style.color = "red"
                        vlq.v2n1.style.color = "red"
                        vlq.v2n2.style.color = "red"
                        vlq.v1n1.addLyric("Quintparallele")
                    elif vlq.parallelOctave():
                        vlq.v1n1.style.color = "red"
                        vlq.v1n2.style.color = "red"
                        vlq.v2n1.style.color = "red"
                        vlq.v2n2.style.color = "red"
                        vlq.v1n1.addLyric("Oktavparallele")
                    if melody:
                        #Check der Bassprogression auf falsche oder zu grosse Intervalle
                        topProgression = interval.Interval(vlq.v1n1, vlq.v1n2)
                        bassProgression = interval.Interval(vlq.v2n1, vlq.v2n2)
                        if bassProgression.intervalClass == 6:
                            vlq.v2n1.style.color = "violet"
                            vlq.v2n1.addLyric("fieser Sprung")
                        if topProgression.intervalClass == 6:
                            vlq.v1n1.style.color = "violet"
                            vlq.v1n1.addLyric("fieser Sprung")
                        elif topProgression.direction == 1:
                            if topProgression.semitones > 8 and bassProgression.semitones != 12:
                                vlq.v1n1.style.color = "violet"
                                vlq.v1n1.addLyric("fieser Sprung")
                        elif bassProgression.direction == 1:
                            if bassProgression.semitones > 8 and bassProgression.semitones != 12:
                                vlq.v2n1.style.color = "violet"
                                vlq.v2n1.addLyric("fieser Sprung")
                        elif bassProgression.direction == -1:
                            if bassProgression.semitones < -7 and bassProgression.semitones != -12:
                                vlq.v2n1.style.color = "violet"
                                vlq.v2n1.addLyric("fieser Sprung")
                        elif topProgression.direction == -1:
                            if topProgression.semitones < -7 and bassProgression.semitones != -12:
                                vlq.v1n1.style.color = "violet"
                                vlq.v1n1.addLyric("fieser Sprung")
            #except:
            #    print('Except:', i, i.offset)

            v1n1 = v1n2
            v2n1 = v2n2

    def _motus(self, motus, vlq, color, allowedColors=[None]):
        if motus:
            if vlq.v1n2.style.color in allowedColors:
                vlq.v1n2.style.color = color
                #pass
            if vlq.v2n2.style.color in allowedColors:
                vlq.v2n2.style.color = color

    def _markMelody(predicates, vlq, color, annotation):
        topProgression = interval.Interval(vlq.v1n1, vlq.v1n2)
        bassProgression = interval.Interval(vlq.v2n1, vlq.v2n2)
        for predicate in predicates:
            if predicate:
                pass

    
    def getAnnotatedStream(self):
        analyseDatei = stream.Stream()
        analyseDatei.append(self.p1)
        analyseDatei.append(self.bass)
        return analyseDatei