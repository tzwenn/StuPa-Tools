# StuPa-Tools

Eine Sammlung von Werkzeugen zur Sitzungsvorbereitung des Studierendenparlaments der Universität Potsdam.

## Sitzungsmappen

Sitzungsmappen werden vor der Sitzung an der Verteiler geschickt ("intern") und auf die [Webseite](http://www.stupa.uni-potsdam.de/doku.php?id=protokolle) gestellt ("öffentlich"). Ein paar Menschen bekommen auf Anfrage toten Baum.

Der einzige Sinn und Zweck dieses Programms ist es ein schönes Inhaltsverzeichnis für das PDF zu generieren.

### Installation

Benötigt werden:

   * Python mit [PyYAML](https://pypi.python.org/pypi/PyYAML)
   * LaTeX mit `latexmk`
   * [Coherent PDF Command Line](http://community.coherentpdf.com) (Overkill. Zum Abschneiden der letzten Folie. Geht auch in Acrobat/Apple Preview/pdftk/…)

### Benutzung

Als Eingabe wird ein Ordner mit den zu beinhaltenden PDFs und eine YAML-Datei folgenden Formats benötigt:

```yaml
- Tagesordnung: 0_Deckblatt.pdf            # Datei einbinden unter diesem Lesezeichen
- Protokoll der letzten Sitzung: 2_Letztes_Protokoll.pdf
- Berichte:                                # Neue Sektion
  - Rechenschaftsbericht AStA: AStA.pdf    # Eine Untersektion mit PDF
  - Mietrechtsberatung: Jahresbericht Mietrechtsberatung.pdf
- Wahl des Lorem-Ipsum-Gremiums:
  - !intern H. Arendt: KandidaturA.pdf     # Kommt nicht in die öffentliche Mappe
  - !intern B. Brecht: KandidaturB.pdf
- "Zweite Lesung: Haushalt": 6_HH16-17.pdf # Für Doppelpunkte, etc. " nutzen

```

Die Sitzungsmappe wird dann erzeugt mit

```bash
$ sitzungsmappe.py inhalt.yaml --nummer 7 -o 20170131_Sitzungsmappe.pdf
$ sitzungsmappe.py inhalt.yaml --nummer 7 --public -o 20170131_Sitzungsmappe_webseite.pdf
```


### Was fehlt

Automatische Konvertierung von Markdown/EML/Excel-Bestandteilen. Die Tagesordnung könnte auch automatisch erzeugt werden.
