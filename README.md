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

## Gabeln nach einer richtigen Antwort von O vorbereiten

Auch wenn O im ersten Zug richtig antwortet, kannst du auf spätere Gabelmöglichkeiten spielen. Dein Ziel ist dann, die eigene Remischance zu bewahren und einen späteren Fehler auszunutzen. Die Vorbereitung allein erzwingt noch keinen Sieg: Spielt O weiterhin richtig, bleibt ein Remis möglich.

### Kanteneröffnung: nach X2 mit X4 oder X6 fortsetzen

Mit X auf zwei benachbarten Kanten lassen sich Gabeln vorbereiten. Welche der beiden Fortsetzungen sicher ist, hängt jedoch von Os erster Antwort ab:

| Zugfolge bis zur ersten Antwort | Fortsetzung, die die Remischance bewahrt | Gefährliche Fortsetzung |
| --- | --- | --- |
| X2, O1 | X4 | X6 ermöglicht einen erzwungenen Sieg für O. |
| X2, O3 | X6 | X4 ermöglicht einen erzwungenen Sieg für O. |
| X2, O5 | X4 oder X6 | Keine der beiden verliert bei optimaler Fortsetzung. |
| X2, O8 | X4 oder X6 | Keine der beiden verliert bei optimaler Fortsetzung. |

**Eine mögliche Falle:** Nach **X2, O5, X4** ist **O8** ein Fehler. Mit **X1** erzeugst du eine Gabel: Du drohst auf **3** über die Reihe 1–2–3 und auf **7** über die Spalte 1–4–7. O kann nur eine der beiden Drohungen blocken.

**Die Gegenfalle von O:** Nach **X2, O1, X6** kann O mit **O7** den Sieg erzwingen. O droht zunächst auf **4** über die Spalte 1–4–7. Du musst mit **X4** blocken. Anschließend spielt O auf **5**: Das blockt deine Reihe 4–5–6 und erzeugt gleichzeitig eine Gabel auf **3** (Diagonale 3–5–7) und **9** (Diagonale 1–5–9). Du kannst nur eine davon abwehren. Nach **X2, O3, X4** gilt die gespiegelte Gegenfalle.

### Eckeneröffnung: nach X1, O5 mit X6 fortsetzen

Die Folge **X1, O5, X6** bewahrt deine Remischance und bereitet eine mögliche Gabel vor. Antwortet O anschließend mit **4 oder 7**, spielst du **X3**. Du drohst dann gleichzeitig auf **2** über die Reihe 1–2–3 und auf **9** über die Spalte 3–6–9. O hat in beiden Fällen keinen eigenen sofortigen Gewinnzug und kann die Gabel nicht mehr abwehren.

O kann diese Falle vermeiden: Mit **2, 3, 8 oder 9** als zweitem O-Zug bleibt bei optimalem Spiel ein Remis möglich. Diese Antworten sind also keine entscheidenden Fehler.

**Merksatz:** Bereite eine Gabel vor, ohne selbst einen erzwungenen Verlust zuzulassen. Prüfe dabei auch die Drohungen von O. Im Trainer zeigt **Zug prüfen / Tipp**, ob deine Stellung weiterhin remis ist oder nach einem Fehler des Gegners einen erzwungenen Gewinn enthält.

## Als O einen Fehler im zweiten Zug von X ausnutzen

Gemeint ist der **zweite eigene Zug von X**, also der dritte Zug der Partie: **X, O, X**. Voraussetzung ist, dass du als O zunächst die Remischance bewahrt hast. Ein entscheidender Fehler von X ermöglicht dir dann einen erzwungenen Sieg, auch wenn X sich anschließend optimal verteidigt.

### Wann kann X schon im zweiten Zug entscheidend falsch spielen?

| X eröffnet | Deine erste Antwort als O | Zweite X-Züge, die O einen erzwungenen Sieg ermöglichen |
| --- | --- | --- |
| 5 | 1 (stellvertretend für jede Ecke) | Keine. |
| 1 | 5 | Keine. |
| 2 | 1 | 3, 6, 8 |
| 2 | 3 | 1, 4, 8 |
| 2 | 5 | 8 |
| 2 | 8 | Keine. |

Alle anderen Eröffnungen ergeben sich durch Drehen oder Spiegeln. Nach einer Mittel- oder Eckeneröffnung von X und deiner richtigen Antwort bleibt mit jedem legalen zweiten X-Zug bei optimalem Spiel ein Remis möglich. Du brauchst dort einen späteren Fehler. Auch nach **X2, O8** kann X im zweiten Zug noch keinen entscheidenden Fehler machen.

### Vier Gewinnmuster für O

Nach einer Kanteneröffnung gibt es vier Grundfälle. Jede Zeile wird von links nach rechts gespielt: **X, O, X, O, X, O**. Dein zweiter O-Zug erzeugt zunächst eine einfache Drohung. X muss sie blocken; dein dritter O-Zug setzt dann eine Gabel.

| X eröffnet | O antwortet | X macht den Fehler | O droht | X muss blocken | O setzt die Gabel | O droht auf |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | 1 | 3 | 4 | 7 | 5 | 6 und 9 |
| 2 | 1 | 6 | 7 | 4 | 5 | 3 und 9 |
| 2 | 1 | 8 | 5 | 9 | 7 | 3 und 4 |
| 2 | 5 | 8 | 1 | 9 | 7 | 3 und 4 |

Blockt X deine erste Drohung nicht, gewinnst du sofort auf dem Feld in „X muss blocken“. Blockt X, erzeugst du die angegebene Gabel. X kann nur eines deiner beiden Gewinnfelder besetzen; du gewinnst auf dem anderen. Die Gabelzüge lassen X in diesen Beispielen keinen eigenen sofortigen Gewinn.

**Beispiel mit gleichzeitiger Abwehr:** Nach **X2, O1, X3** spielst du **O4** und drohst auf **7** über die Spalte 1–4–7. Nach dem erzwungenen **X7** spielst du **O5**. Damit blockst du zugleich die Diagonale 3–5–7 von X und drohst selbst auf **6** über die Reihe 4–5–6 sowie auf **9** über die Diagonale 1–5–9.

**Gegenüberliegende Kanten ausnutzen:** Nach **X2, O5, X8** haben die beiden X-Steine keine gemeinsame freie Dreierreihe mehr, weil du die Mitte besetzt hältst. Mit **O1** drohst du auf **9**. Nach **X9** setzt du **O7**, blockst damit zugleich die Reihe 7–8–9 von X und erzeugst deine Gabel auf **3** und **4**. In dieser Ausgangsstellung ist O1 eine konkrete Gewinnfortsetzung; auch die anderen freien Felder ermöglichen bei richtigem Weiterspielen einen erzwungenen Sieg.

Zum Üben wähle im Trainer **O** und **Früh: bei erster Gelegenheit**. X beginnt und macht höchstens einen entscheidenden Fehler; die passende Gelegenheit muss nicht bereits in seinem zweiten Zug auftreten. **Zug prüfen / Tipp** zeigt dir, ob O einen Gewinn erzwingen kann und welche Züge ihn bewahren.
