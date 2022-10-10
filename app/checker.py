from flask import (
    Blueprint
)

from music21 import converter, musicxml
from flask import request
from .asChecker import AsChecker
from .klauseln import KlauselAnalyser

bp = Blueprint('as', __name__, url_prefix='/as')

@bp.route('/analyse', methods=('GET', 'POST'))
def analyse():
    if request.method == "POST":
        xml = request.form.get("content")
        
        #get options from request
        paramCheck = lambda requestParam: True if (requestParam == 'true') else False

        klauseln = request.form.get("klauseln")
        aussenstimmen = paramCheck(request.form.get("aussenstimmen"))
        bewegungsCheck = paramCheck(request.form.get("bewegung"))
        parallelenCheck = paramCheck(request.form.get("parallelen"))
        melodieCheck = paramCheck(request.form.get("melodie"))
        print(klauseln, aussenstimmen, parallelenCheck, bewegungsCheck, melodieCheck)
        
        #set given top voice and bass voice, if possible otherwise use fallback
        customVoices: bool = False
        try:
            sopr = int(request.form.get("topVoice")) - 1
            bass = int(request.form.get("bassVoice")) - 1
            # avoid negativ sopr or zero bass values, that may result in having only one part in th escore
            if sopr <= -1:
                sopr = 0
            if bass <= 0:
                bass = 1
            customVoices = True
        except:
            sopr = 0
            bass = 1
            customVoices = False
        
        #load xml
        #print("xml Value: ", xml, customVoices)
        if xml != "":
            s = converter.parse(xml, format="xml")
        else:
            return "Nothing to be done"
  
        #remove unneeded parts in score, if neccessary
        if customVoices:
            try:
                for i in range(len(s.parts)):
                    if i != sopr and i != bass:
                        s.remove(s.parts[i])
                outStream = s
            except:
                outStream = s
        else:
            outStream = s

        
        if klauseln == "alletrue":
            kA = KlauselAnalyser(outStream, 1)
            kA.analyse(analyseAll=True) #
            outStream = kA.getAnnotatedStream()
        
        if klauseln == "fermatentrue":
            kA = KlauselAnalyser(outStream, 1)
            kA.analyse(analyseAll=False) #
            outStream = kA.getAnnotatedStream()


        if  True in [aussenstimmen, bewegungsCheck, parallelenCheck, melodieCheck]:
            #print(len(outStream.parts))
            asc = AsChecker(outStream, 1)
            asc.asPruefen(consDiss=aussenstimmen, motion=bewegungsCheck, parallels=parallelenCheck, melody=melodieCheck)
            outStream = asc.getAnnotatedStream()

        out = musicxml.m21ToXml.GeneralObjectExporter(outStream).parse().decode('utf-8')
        return out
    else:
        return "Das ist der Analyser :)"