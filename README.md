# Tic-Tac-Toe Trainer

Ein kleines Trainingsprogramm mit grafischer Oberfläche. Du spielst X oder O und übst, Fehler des Gegners auszunutzen oder gegen einen perfekten Gegner ein Remis zu halten.

## Start

Benötigt Python 3 mit Tkinter. Unter Windows ist Tkinter normalerweise in der Python-Installation enthalten; unter Linux muss gegebenenfalls das Paket `python3-tk` installiert werden.

```bash
python -m pip install -r requirements.txt
python tic_tac_toe_training.py
```

Unter Linux heißt der Befehl häufig `python3 tic_tac_toe_training.py`. Für die formatierte README-Anzeige werden **Markdown** und **TkinterWeb** benötigt; `requirements.txt` enthält diese Pakete. Das Spiel selbst funktioniert auch ohne sie.

## Bedienung

Wähle oben, ob du **X** oder **O** spielst. X beginnt immer; wenn du O wählst, eröffnet der Computer. Klicke ein freies Feld für deinen Zug. **Neue Runde** startet neu, **Zug prüfen / Tipp** zeigt den spieltheoretischen Wert der Stellung und markiert gute Züge grün. Die Feldnummern laufen zeilenweise von 1 (oben links) bis 9 (unten rechts).

| Modus | Verhalten des Computers |
| --- | --- |
| Perfekter Gegner (kein Fehler) | Spielt durchgehend optimal. Bei fehlerfreiem Spiel entsteht ein Remis. |
| Früh: bei erster Gelegenheit | Lässt bei der ersten geeigneten Gelegenheit einen erzwungenen Gewinn für dich zu. |
| Später: kein Sofortgewinn | Wartet bis später und macht nur einen Fehler, der dir keinen sofortigen Gewinnzug gibt. |
| Späte Trainingsstellung laden | Beginnt direkt nach einem späteren Fehler des Computers. Finde den Gewinnweg. |

**README / Hilfe** öffnet diese Anleitung in einem eigenen, scrollbaren Lesefenster mit formatierten Überschriften, Fettdruck, Tabellen und Codeblöcken. Der Text lässt sich markieren und kopieren, aber nicht bearbeiten. Links öffnen sich im Standardbrowser. Ein erneuter Klick holt das offene Fenster nach vorne. Mit **Schließen** oder **Esc** schließt du es. Die Datei `README.md` muss neben `tic_tac_toe_training.py` liegen; die Anleitung ist auch offline verfügbar.

Das HTML wird bei jedem neuen Öffnen direkt aus der aktuellen README erzeugt und nur im Speicher gehalten. Es wird keine HTML-Datei gespeichert oder eingecheckt.

Nach seinem einmaligen Fehler verteidigt sich der Computer wieder optimal. In einer selbst gespielten Partie kann eine passende Fehlergelegenheit ausbleiben, insbesondere wenn du vorher selbst von der optimalen Linie abweichst. Gedrehte und gespiegelte Stellungen sind ebenfalls enthalten.
