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

## Fehler von O im ersten Zug ausnutzen

X beginnt. Schon die erste Antwort von O kann einen **erzwungenen Sieg für X** ermöglichen: X kann dann auch gegen jede weitere, optimale Verteidigung gewinnen. Dazu muss X den richtigen Gewinnweg spielen; ein schlechter Folgezug kann den Vorteil wieder verschenken.

Die Feldnummern entsprechen dieser Anordnung:

| | | |
| --- | --- | --- |
| 1 | 2 | 3 |
| 4 | 5 | 6 |
| 7 | 8 | 9 |

**Ecken:** 1, 3, 7, 9. **Kanten:** 2, 4, 6, 8. **Mitte:** 5.

### Welche Antworten sind Fehler?

Die Tabelle zeigt je eine Eröffnung pro Stellungstyp. Alle anderen Eröffnungen ergeben sich durch Drehen oder Spiegeln des Bretts; dabei werden sämtliche Feldnummern entsprechend mitverändert.

| Erster Zug von X | O hält die Remischance mit | O ermöglicht einen erzwungenen Sieg mit |
| --- | --- | --- |
| Mitte: 5 | 1, 3, 7, 9 | 2, 4, 6, 8 |
| Ecke: 1 | 5 | 2, 3, 4, 6, 7, 8, 9 |
| Kante: 2 | 1, 3, 5, 8 | 4, 6, 7, 9 |

Eine sichere erste Antwort bedeutet, dass O bei anschließend richtigem Spiel ein Remis halten kann. X hat dann keinen erzwungenen Gewinn und braucht einen späteren Fehler von O. Auch später muss O auf Doppeldrohungen achten, nicht nur auf unmittelbar drohende Dreierreihen.

### Das Gewinnprinzip: eine Gabel vorbereiten

Eine **Gabel** ist ein Zug, der zwei verschiedene Gewinnfelder gleichzeitig erzeugt. O kann mit einem Zug nur eines davon besetzen; X gewinnt auf dem anderen. Vor der Gabel lässt sich O oft durch eine einfache Drohung zu einem bestimmten Abwehrzug zwingen.

Die folgenden Beispiele decken, zusammen mit ihren Drehungen und Spiegelungen, alle fehlerhaften ersten Antworten ab. Lies jede Zeile von links nach rechts: **X, O, X, O, X**. Die beiden letzten Felder sind danach die Gewinnmöglichkeiten für X.

| X eröffnet | O macht den Fehler | X droht | O muss blocken | X setzt die Gabel | X droht auf |
| --- | --- | --- | --- | --- | --- |
| 5 | 2 | 1 | 9 | 7 | 3 und 4 |
| 1 | 2 | 5 | 9 | 7 | 3 und 4 |
| 1 | 6 | 5 | 9 | 3 | 2 und 7 |
| 1 | 3 | 7 | 4 | 9 | 5 und 8 |
| 1 | 9 | 3 | 2 | 7 | 4 und 5 |
| 2 | 4 | 5 | 8 | 1 | 3 und 9 |
| 2 | 7 | 1 | 3 | 5 | 8 und 9 |

**Warum ist der Abwehrzug erzwungen?** Wenn O nicht auf dem Feld in „O muss blocken“ spielt, vollendet X dort schon im nächsten Zug eine Dreierreihe. Blockt O, setzt X die angegebene Gabel. In diesen Beispielen hat O dabei selbst keinen sofortigen Gewinnzug und kann die beiden Drohungen nicht mehr gleichzeitig abwehren.

**Eigene Drohungen von O beachten:** Eine Gabel nützt nichts, wenn O vorher selbst gewinnen kann. Nach **X1, O6, X5, O9** muss X auf **3** spielen: Das blockt Os Spalte 3–6–9 und erzeugt zugleich die Gabel auf 2 und 7. Ebenso blockt **X5** in der letzten Tabellenzeile die Diagonale 3–5–7 von O und droht gleichzeitig auf 8 und 9.

### Beispiel: X beginnt in der Mitte, O antwortet auf einer Kante

Nach **X5, O2** spielt X auf **1**. X droht nun über die Diagonale **1–5–9** auf Feld **9** zu gewinnen. O muss deshalb auf **9** antworten. X spielt anschließend auf **7** und droht gleichzeitig auf **3** (Diagonale 3–5–7) und auf **4** (Spalte 1–4–7). Egal, welches Feld O blockt: X gewinnt auf dem anderen.

Antwortet O auf **X5** dagegen mit einer **Ecke**, ist das kein Fehler. Das erklärt, warum die Mitteleröffnung gegen einen richtig antwortenden Gegner keinen Gewinn garantiert. Um frühe Fehler gezielt zu üben, wähle im Trainer **X** und **Früh: bei erster Gelegenheit**. Mit **Zug prüfen / Tipp** kannst du prüfen, welche Fortsetzungen den Gewinn bewahren.
