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
        aussenstimmen = request.form.get("aussenstimmen")
        klauseln = request.form.get("klauseln")
        #for el in request.form:
        #    print(el)
        #print(klauseln)
        
        s = converter.parse(xml, format="xml")
        outStream = s
        
        if klauseln == "alletrue":
            kA = KlauselAnalyser(outStream, 1)
            kA.analyse(analyseAll=True) #
            outStream = kA.getAnnotatedStream()
        
        if klauseln == "fermatentrue":
            kA = KlauselAnalyser(outStream, 1)
            kA.analyse(analyseAll=False) #
            outStream = kA.getAnnotatedStream()


        if aussenstimmen == "true":
            asc = AsChecker(outStream, 1)
            asc.asPruefen(motion=True)
            outStream = asc.getAnnotatedStream()

        out = musicxml.m21ToXml.GeneralObjectExporter(outStream).parse().decode('utf-8')
        return out
    else:
        return "Das ist der Analyser :)"