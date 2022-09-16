# Aussenstimmen-Analyse

A service that checks a 2-voice musical setting for clauses, cadences, and standard voiceleading rules.

The flask service accepts musicxml files that are send e.g. by MuseScore. It is designed to serve as a headless backend for the MuseScore Plugin, but can be used by any other client.

The MuseScore Plugin sends a POST Request with a body x-www-formdata-urlencoded.

Options are:
- content: [musicxml string]
- kauseln: true|false
- aussenstimmen: alletrue|fermatentrue

"alletrue" checks for clauses at every step of the melody. "fermatentrue" only checks at fermatas.

The services can be installed as a docker container.
