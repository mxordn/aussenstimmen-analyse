from music21 import stream, figuredBass, voiceLeading, note, interval, converter, expressions
import copy

class KlauselAnalyser():
    def __init__(self, aStreamHandedOver, partNumber):
        self.ergebnis = []
        self.oberStimme = aStreamHandedOver.parts[0]
        if partNumber > len(aStreamHandedOver.parts):
            self.zweiteStimme = aStreamHandedOver.parts[1]
        else:
            self.zweiteStimme = aStreamHandedOver.parts[partNumber]
        self.aStream = stream.Score()
        self.aStream.insert(0, self.oberStimme)
        self.aStream.insert(0, self.zweiteStimme)
        self.originalStream = copy.deepcopy(self.aStream)
        self.wasEnding: bool = False


    def hasFermata(self, someNote):
        for ornament in someNote.expressions:
            if type(ornament) == expressions.Fermata:
                return True
        return False
    
    def isAnticipatio(self, cantus1, ultima, somePart):
        if cantus1.quarterLength <= 0.5 and cantus1.pitch == ultima.pitch:
            return True
        else:
            return False

    def getEndeCantus(self, somePart, ultima):
        try:
            cantus1 = somePart.flat.notes.getElementBeforeOffset(ultima.offset)
            #print(ultima, cantus1)
            if not self.isAnticipatio(cantus1, ultima, somePart):
                oInterval = interval.Interval(cantus1, ultima)
                return (cantus1, ultima, oInterval)
            else:
                cantus1 = somePart.flat.notes.getElementBeforeOffset(cantus1.offset)
                oInterval = interval.Interval(cantus1, ultima)
                return (cantus1, ultima, oInterval)
        except:
            print("blubb")
            return ("blubb")

    def getEndeSecondVoice(self, somePart, ultima):
        bass1 = somePart.flat.notes.getElementBeforeOffset(ultima.offset)
        bass2 = somePart.flat.notes.getElementAtOrBefore(ultima.offset)
        bassInterval = interval.Interval(bass1, bass2)
        return (bass1, bass2, bassInterval)

    def switchKlausel(self, melStep, lastInterval, bassStep):
        switchDict = {
            -7: self.jumpDown5,
            -6: self.jumpDownTritone,
            -5: self.jumpDown4,
            -4: self.jumpDownG3,
            -3: self.jumpDownK3,
            -2: self.stepDownG2,
            -1: self.stepDownK2,
            0: self.noStep,
            1: self.stepUpK2,
            2: self.stepUpG2,
            3: self.jumpUp3,
            4: self.jumpUp3,
            5: self.jumpUp4,
            6: self.jumpUpTritone,
            7: self.jumpUp5,
            8: self.noStep,
        }
        
        func = switchDict.get(melStep, self.NA)
        return func(lastInterval, bassStep)
    
    def NA(self, lastInterval, bassStep):
        return ["", "", "Error!"]
    
    def noStep(self, lastInterval, bassStep):
        if lastInterval.intervalClass == 0:
            if bassStep.semitones in [-3,-4]:
                return ["", "", "Klangumschichtung/keine Schlusswirkung"]
            elif bassStep.semitones in [3,4]:
                return ["", "", "Klanumschichtung/keine Schlusswirkung"]
            elif bassStep.intervalClass == 5:
                return ["AK", "BK dissceta", "Cadentia minor/Clausula dissecta acqu./desid."]
#            Dieser Fall wird durch die Tonwiederholungsregel am Anfang abgegriffen.
            elif bassStep.intervalClass == 0:
                return ["", "", "Klangwiederholung/Klangumschichtung"]
        elif lastInterval.intervalClass == 5:
            if bassStep.intervalClass == 5:
                return ["AK", "BK", "Cadentia maior"]
            elif bassStep.intervalClass == 1:
                return ["AK", "SK", "Cadentia minima ascendens"]
        elif lastInterval.intervalClass in [3,4]:
            return ["", "", "keine Schlusswirkung"]

    
    def stepDownK2(self, lastInterval, bassStep):
        if lastInterval.intervalClass == 0:
            if bassStep.semitones == 2:
                return ["pTK", "pSK", "Mi-Kadenz, Cadentia minima ascendens"]
            elif bassStep.intervalClass in [3,4]:
                return ["pTK", "keine Klausel", "keine Schlusswirkung, selten"]
        elif lastInterval.intervalClass == 5:
            if bassStep.intervalClass == 5:
                return ["pTK", "pBK", "Mi-Kadenz, Cadentia minor"]
            elif bassStep.intervalClass in [1,2]:
                return ["pTK", "4-5", "Halbschluss"]
        elif lastInterval.intervalClass in [3,4]:
            if bassStep.intervalClass == 5:
                return ["SK dissecta", "BK dissecta", ["Cadentia minor/Clausula dissecta (acqu./desid.)", "Plagal-Schluss/Halbschluss"]]
            elif bassStep.semitones == 2 and lastInterval.intervalClass == 4:
                return ["1-7", "4-5", "Halbschluss"]
            elif bassStep.semitones == -1 and lastInterval.intervalClass == 4:
                if lastInterval.semitones % 12 in [8,9]:
                    return ["pAK", "pTK", ["Mi-Kadenz", "Cadentia minima"]]
                else:
                    return ["6-5", "1-7", "Halbschluss"]
            elif bassStep.semitones == -1 and lastInterval.intervalClass == 3:
                return ["3-2", "1-7", "Halbschluss"]
            elif bassStep.semitones == -2:
                return ["vAK/4-3", "TK/6-5", "keine Schlusswirkung"]
    
    def stepUpK2(self, lastInterval, bassStep):
        if lastInterval.intervalClass == 0:
            if bassStep.intervalClass == 2:
                return ["SK", "TK", "Cadentia minima"]
#            elif bassStep.intervalClass == 1:
#                return ["SK", "pTK", ["6-5 mit ü6", "Halbschluss"]]
            elif bassStep.intervalClass == 5:
                return ["SK", "BK", "Cadentia maior"]
            elif bassStep.intervalClass in [3,4]:
                return ["SK?", "keine Klausel", "keine Schlusswirkung"]
        elif lastInterval.intervalClass == 5:
            if bassStep.intervalClass == 2:
                return ["SK", "TK", ["Cadenza sffugita", "Renaissance-typische Kadenz, polyphone Herkunft"]]
            elif bassStep.intervalClass in [3,4]:
                return ["SK?", "keine Klausel", "keine Schlusswirkung"]
        elif lastInterval.intervalClass in [3,4]:
            if bassStep.semitones in [-5,7]:
                return ["SK", "pBK", "Cadentia minor"]
            elif bassStep.semitones in [5,-7]:
                return ["vTK", "BK", "Cadentia maior"]
            elif bassStep.semitones == 2:
                return ["SK", "5-6", "Trugschluss"]
            elif bassStep.semitones == 1 and lastInterval.intervalClass == 3:
                return ["vTK", "SK", "Cadentia minima ascendens"]
            elif bassStep.semitones == 1 and lastInterval.intervalClass == 4:
                return ["SK", "5-6", "Trugschluss"]
            elif bassStep.semitones == -2:
                return ["vTK", "TK", "Cadentia minima"]
            elif bassStep.intervalClass in [3,4]:
                return ["SK", "AK", ["altizans", "keine Schlusswirkung"]]
    
    def stepDownG2(self, lastInterval, bassStep):
        if lastInterval.intervalClass == 5:
            if bassStep.intervalClass == 5:
                return ["TK dissecta", "BK dissecta", ["Cadentia minor/Clausula dissecta (acqu./desid.)", "Plagal-Schluss/Halbschluss"]]
            elif bassStep.intervalClass in [3,4]:
                return ["TK", "keine Klausel", "Halbschluss"]
#            elif bassStep.intervalClass in [1,2]:
#                return ["TK", "4-5", "Halbschluss"]
        elif lastInterval.intervalClass == 0:
            if bassStep.intervalClass == 5:
                return ["TK", "BK", "Cadentia maior"]
            elif bassStep.intervalClass == 1:
                return ["TK", "SK", "Cadentia minima ascendens"]
            elif bassStep.intervalClass == 2:
                return ["TK/6-5", "4-5", "Halbschluss"]
        elif lastInterval.intervalClass in [3,4]:
            if bassStep.semitones in [1,2] and lastInterval.semitones % 12 in [3,4]:
                return ["TK/5-4", "2-3/5-6", "keine Schlusswirkung"]
            elif bassStep.semitones in [1,2] and lastInterval.semitones % 12 in [8,9]:
                return ["TK", "5-6", "Trugschluss"]
            elif bassStep.semitones in [-3,-4]:
                return ["TK", "AK", ["altizans", "keine Schlusswirkung"]]
            elif bassStep.semitones == -1 and lastInterval.semitones % 12 in [8,9]:
                return ["TK dissecta", "SK dissecta", ["Cadentia minor/Clausula dissecta (acqu./desid.)", "Plagal-Schluss/Halbschluss"]]
            elif bassStep.semitones == -1 and lastInterval.semitones % 12 in [3,4]:
                return ["", "", "keine Schlusswirkung"]
            elif bassStep.semitones == -2:
                return ["vAK/4-3", "TK", "Cadentia minor descendens"]
                        #TK/6-5,  (2-1/6-5)keine Schlusswirkung

    def stepUpG2(self, lastInterval, bassStep):
        if lastInterval.intervalClass == 5:
            if bassStep.intervalClass == 1:
                return ["AK/4-5", "pTK", "Mi-Kadenz, Cadentia minima"]
            elif bassStep.intervalClass == 2:
                return ["AK/4-5", "TK/6-5", "Cadentia minima, Halbschluss"]
            elif bassStep.intervalClass == 5:
                return ["pSK", "pBK", ["Mi-Kadenz", "Cadentia minor"]]
        elif lastInterval.intervalClass == 0:
            if bassStep.intervalClass == 1:
                return ["pSK", "pTK", "Mi-Kadenz, Cadentia minima"]
            elif bassStep.intervalClass == 2:
                return ["kein Leitton", "TK", "keine Schlusswirkung"]
        elif lastInterval.intervalClass in [3,4]:
            if bassStep.semitones in [5, -7]:
                return ["vTK", "BK", "Cadentia maior"]
            elif bassStep.semitones in [-5, 7]:
                return ["pAK", "pBK", "Mi-Kadenz, Cadentia minor"]
            elif bassStep.semitones == -2:
                return ["vTK", "TK", "Cadentia minima"]
            elif bassStep.semitones == 1:
                return ["vTK", "SK", "Cadentia minima ascendens"]
    
    def jumpDownK3(self, lastInterval, bassStep):
        if lastInterval.intervalClass in [3,4]:
            if bassStep.intervalClass == 5:
                return ["vAK", "BK", "Cadentia maior"]
            elif bassStep.intervalClass == 1:
                return ["vAK", "SK", "Cadentia minima ascendens"]
            elif bassStep.intervalClass == 2:
                return ["", "4-5", "Halbschluss"]
            elif bassStep.intervalClass == 0:
                return ["", "", "Klangumschichtung"]
        elif lastInterval.intervalClass == 5:
            if bassStep.semitones == 2:
                return ["AK", "4-5/5-6", "Halb-/Trugschluss"]
            elif bassStep.semitones in [-1,-2]:
                return ["AK", "6-5", "Halbschluss"]
            elif bassStep.intervalClass == 5:
                return ["4-2", "2-5", "Halbschluss"]
        elif lastInterval.intervalClass == 0:
            if bassStep.intervalClass == 0:
                return ["", "", "keine Schlusswirkung"]
            elif bassStep.intervalClass in [3,4]:
                return ["", "", "keine Schlusswirkung"]
            elif bassStep.intervalClass == 5:
                return ["", "", "keine Schlusswirkung"]
            
    def jumpDownG3(self, lastInterval, bassStep):
        if lastInterval.intervalClass in [3,4]:
            if bassStep.intervalClass == 5:
                return ["vAK", "BK", "Cadentia maior"]
            elif bassStep.intervalClass == 1:
                return ["vAK", "SK", "Cadentia minima ascendens"]
            elif bassStep.intervalClass == 2:
                return ["8-6", "3-4", "keine Schlusswirkung"]
            elif bassStep.intervalClass == 0:
                return ["", "", "Klangumschichtung"]
        elif lastInterval.intervalClass == 5:
            if bassStep.semitones == 1:
                return ["AK", "5-6", "Trugschluss"]
            elif bassStep.semitones == -2:
                return ["abspringende SK", "TK", "Cadentia minima (selten)"]
            elif bassStep.intervalClass == 5:
                return["abspringende SK", "BK", "Cadentia maior"]
        elif lastInterval.intervalClass == 0:
            if bassStep.intervalClass == 0:
                return ["", "", "Klangumschichtung"]
            elif bassStep.intervalClass in [3,4]:
                return ["", "", "keine Schlusswirkung"]

    
    
    def jumpUp3(self, lastInterval, bassStep):
        if lastInterval.intervalClass == 0:
            if bassStep.intervalClass == 0:
                return ["", "", "Klangumschichtung"]
            elif bassStep.intervalClass in [3,4]:
                return ["", "", "keine Schlusswirkung"]
            elif bassStep.intervalClass in [1,2]:
                return ["vSK", "TK", "Cadentia minima"]
            elif bassStep.intervalClass == 5:
                return ["6-8", "BK dissecta", ["Cadentia minor/Clausula dissecta (acqu./desid.)", "Plagal-Schluss/Halbschluss"]]
        elif lastInterval.intervalClass == 5:
            if bassStep.intervalClass in [3,4]:
                return ["", "", "keine Schlusswirkung"]
            elif bassStep.intervalClass == 0:
                return ["", "", "Klangumschichtung"]
        elif lastInterval.intervalClass in [3,4]:
            if bassStep.intervalClass == 0:
                return ["", "", "Klangumschichtung"]
            elif bassStep.intervalClass in [1,2]:
                return ["", "8-7", "keine Schlusswirkung"]
            elif bassStep.intervalClass == 5:
                return ["vAK", "pBK", "Cadentia minor"]
        else:
            return ["", "", "ungewöhnliches Ende"]
    
    def jumpDown4(self, lastInterval, bassStep):
        if lastInterval.intervalClass == 0:
            if bassStep.intervalClass in [3,4]:
                return ["", "3-5", "Halbschluss"]
            elif bassStep.intervalClass == 1:
                return ["Stimmkreuzung", "pTK", "Mi-Kadenz, Cadentia minima"]
            elif bassStep.intervalClass == 2:
                return ["", "4-5", "Halbschluss"]
        elif lastInterval.intervalClass == 5:
            if bassStep.semitones == 0:
                return ["", "", "Klangumschichtung"]
        elif lastInterval.semitones % 12 in [3,4]:
            pass
        elif lastInterval.semitones % 12 in [8,9]:
            pass
    
    def jumpUp4(self, lastInterval, bassStep):
        if lastInterval.intervalClass in [3,4]:
            if bassStep.intervalClass in [1,2]:
                if bassStep.direction == 1:
                    return ["BK", "5-6", "Trugschluss"]
                elif bassStep.direction == -1:
                    return ["BK", "4-3", "keine Schlusswirkung"]
            elif bassStep.intervalClass in [3,4]:
                return ["BK", "AK", "keine Schlusswirkung"]
            elif bassStep.intervalClass == 5:
                return ["", "", "keine Schlusswirkung"]
        elif lastInterval.semitones % 12 in [8,9]:
            if bassStep.intervalClass in [3,4]:
                return ["", "6-4", "keine Schlusswirkung"]
        elif lastInterval.intervalClass == 0:
            if bassStep.semitones == 1:
                return ["BK", "SK", "Cadentia minima ascendens"]
            elif bassStep.semitones == 2:
                return ["", "4-5", "Halbschluss"]
            elif bassStep.intervalClass in [3,4]:
                return ["", "", "keine Schlusswirkung"]
        elif lastInterval.intervalClass == 5:
            if bassStep.semitones == 1:
                return ["BK", "SK", "Cadentia minima ascendens"]
            elif bassStep.semitones == 2:
                return ["", "4-5", "Halbschluss"]
    
    def jumpUpTritone(self, lastInterval, bassStep):
        if lastInterval.intervalClass == 5:
            if bassStep.intervalClass == 1:
                return ["abspringende pTK", "pTK/6-5", "Halbschluss"]
        elif lastInterval.intervalClass == 4:
            if bassStep.semitones == -1:
                return ["abspringende pSK", "pTK/6-5", "Halbschluss"]
        else:
            return ["", "", "Tritonus"]
    
    def jumpDownTritone(self, lastInterval, bassStep):
        if lastInterval.intervalClass == 5:
            if bassStep.intervalClass == 2:
                return ["abspringende pTK", "pSK/4-5", "Halbschluss"]
            elif bassStep.semitones == -1:
                return ["abspringende pTK", "pTK/6-5", "Halbschluss"]
        else:
            return ["", "", "Tritonus"]
    
    def jumpDown5(self, lastInterval, bassStep):
        if lastInterval.intervalClass == 0:
            if bassStep.intervalClass == 1:
                return ["BK", "SK", "Cadentia minima ascendens"]
            elif bassStep.intervalClass == 2:
                return ["", "4-5", "Halbschluss"]
            elif bassStep.intervalClass == 5:
                return ["BK", "BK", "Cadentia maior, nur in vollstimmigen Sätzen"]
            elif bassStep.intervalClass in [0,3,4]:
                return ["", "", "keine Schlusswirkung"]
        elif lastInterval.intervalClass == 5:
            if bassStep.semitones == 1:
                return ["abspringende TK", "SK", "Cadentia minor ascendens"]
            elif bassStep.semitones == 2:
                return ["", "4-5", "Halbschluss"]
            elif bassStep.semitones == -2:
                return ["abspringende TK", "TK", "Cadentia minima"]
            elif bassStep.intervalClass == 5:
                return ["abspringende TK", "BK", "Cadentia maior, nur in vollstimmigen Sätzen"]
        elif lastInterval.intervalClass in [3,4]:
            if bassStep.intervalClass in [1,2]:
                return ["BK", "5-6", "Trugschluss"]
            elif bassStep.intervalClass == 5 and lastInterval.intervalClass == 4:
                return ["abspringende SK", "BK", "Cadentia maior (selten)"]
            elif bassStep.intervalClass == 5 and lastInterval.intervalClass == 3:
                return ["", "", "keine Schlusswirkung"]
        else:
            return ["", "", "unbestimmbar"]
    
    def jumpUp5(self, lastInterval, bassStep):
        if lastInterval.intervalClass == 0:
            if bassStep.semitones == -1:
                return ["abspringende pAK", "6-5", "Halbschluss"]
            elif bassStep.semitones == -2:
                return ["abspringende AK", "6-5", "Halbschluss"]
            elif bassStep.semitones == 2:
                return ["", "4-5", "Halbschluss"]
        elif lastInterval.intervalClass == 5:
            if bassStep.intervalClass == 0:
                return ["", "", "keine Schlusswirkung"]
#            elif bassStep.intervalClass == 2:
#                return ["", "4-5", "Halbschluss"]
        elif lastInterval.intervalClass in [3,4]:
            if bassStep.intervalClass == 5:
                return ["", "", "keine Schlusswirkung"]
            elif bassStep.intervalClass == 0:
                return ["", "", "keine Schlusswirkung"]
            elif bassStep.intervalClass in [1, 2]:
                return ["", "", "keine Schlusswirkung"]
        else:
            return ["", "", "unbestimmbar"]
    
    def klauselBestimmen(self, vlq, iO, iU):
        liste = []
        lastInterval = interval.Interval(vlq.v1n2, vlq.v2n2)
        pUinterval = interval.Interval(vlq.v1n1, vlq.v2n1)
        #Schlussklang konsonant?
        if not lastInterval.isConsonant():
            return ["", "", "Dissonanter Schlussklang"]
        if not pUinterval.isConsonant():
            #Kleine Septe auf der PU.
            if pUinterval.simpleName == "m7":
                if lastInterval.intervalClass in [3,4] and iO.semitones in [-1,-2]:
                    return ["4-3", "BK", "D7 Schluss"]
                elif lastInterval.intervalClass == 5 and iO.semitones in [-1, -2] and iU.semitones == 1:
                    return ["6-5", "7-1", "Cadentia minima ascendens"]
                else:
                    return ["", "", "unbestimmbar"]
            #Verminderter PU Klang, der zur Quintlage auf der Ultima geht
            elif pUinterval.simpleName == "d7":
                if lastInterval.intervalClass == 5 and iO.semitones == -1 and iU.semitones == 1:
                    return ["6-5", "SK", "Cadentia minima ascendens mit verminderter PU"]
                else:
                    return ["", "", "unbestimmbar"]
            #PU hat Tritonus-Klang
            elif pUinterval.intervalClass == 6:
                if lastInterval.intervalClass == 0:
                    bassLeap = interval.Interval(vlq.v2n1, vlq.v2n2)
                    if bassLeap.semitones in [-5,7]:
                        return ["7-1", "BK dissecta", "Cadentia minor/Clausula dissecta acquiescens"]
                elif lastInterval.intervalClass in [3,4]:
                    bassStep = interval.Interval(vlq.v2n1, vlq.v2n2)
                    if bassStep.semitones == 1:
                        return ["4-3", "7-1", ["Cadentia minima ascendens", "Wenn 7, dann 4"]]
                    elif bassStep.semitones == -1:
                        return ["7-1", "4-3", "Wenn 4, dann 7"]
            #Große Septe auf Der PU.
            elif pUinterval.simpleName == "M7":
                bassLeap = interval.Interval(vlq.v2n1, vlq.v2n2)
                if bassLeap.semitones == 2:
                    return ["3-2", "4-5", "Halbschluss"]
            else:
                return ["", "", "Dissonante Penultima"]
        #Die Letzten beiden Intervalle sind gleich. Z.B. Nachsilben/Tonverdopplungen am Ende der Choralzeile.
        #In diesem Fall wird nach den Intervallen eine Position weiter vorne (WV) geschaut.
        elif pUinterval.simpleName == lastInterval.simpleName and vlq.v1n1.pitch == vlq.v1n2.pitch:
            self.initSingleAnalysis(vlq.v1n1)
        #Normalfall
        else:
            liste = self.switchKlausel(iO.semitones, lastInterval, iU)
            return liste
        return liste

    def initSingleAnalysis(self, ultima):
        oEnde = self.getEndeCantus(self.aStream.parts[0], ultima)
        uEnde = self.getEndeSecondVoice(self.aStream.parts[1], ultima)
        #print(oEnde, uEnde)
        try:
            vLquartet = voiceLeading.VoiceLeadingQuartet(oEnde[0], oEnde[1], uEnde[0], uEnde[1])
            theResult = self.klauselBestimmen(vLquartet, oEnde[2], uEnde[2])
            if len(theResult) > 0:
                self.ergebnis.append(theResult)
                self.annotate(theResult, oEnde, uEnde)
        except:
            self.ergebnis.append(["", "", "Kein Schlussintervall vorhanden oder nicht analysierbar."])

    def analyse(self, analyseAll=False):
        for each in self.aStream.parts[0].recurse().notes:
            if self.hasFermata(each):
                print("Fermaten: ", each.pitch)
                self.initSingleAnalysis(each)
                self.wasEnding = True
            elif not self.hasFermata(each) and analyseAll == True:
                print("Andere: ", each.offset)
                if not self.wasEnding:
                    self.initSingleAnalysis(each)
                self.wasEnding = False



    def annotate(self, theResult, oEnde, uEnde):
        oN2 = oEnde[1]
        oN2.addLyric(theResult[0])
        uN2 = uEnde[1]
        uN2.addLyric(theResult[1])
    
    def getListofKlauseln(self):
        return self.ergebnis
    
    def getAnnotatedStream(self):
        return self.aStream
    
    def getOriginalStream(self):
        return self.originalStream
