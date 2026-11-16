# Untersuchung: `tkmacosx`-Buttons unter Python 3.15

## Kurzfassung

Die Ursache liegt nicht in Tcl/Tk 9.1. Beide getesteten Interpreter verwenden:

```text
Python 3.14.10: Tcl/Tk 9.1
Python 3.15.2:  Tcl/Tk 9.1
```

Der Unterschied liegt in der Python-Standardbibliothek `tkinter`. Python 3.15
ändert `tkinter.Misc._unbind()`: Beim Entfernen eines Bindings werden nun auch
die zugehörigen registrierten Tcl-Kommandos gelöscht. `tkmacosx` 1.0.5 entfernt
Bindings jedoch dynamisch und erwartet das frühere Verhalten.

Das führt dazu, dass der `command`-Callback eines `tkmacosx.Button` vor seiner
Ausführung gelöscht wird. Die Anwendung bleibt sichtbar und läuft weiter, aber
Button-Klicks haben keine Wirkung.

Der bestehende Workaround in `handpicked.py` bleibt absichtlich unverändert.

## Relevanter Ablauf in `tkmacosx`

In `tkmacosx/utils/__init__.py:94-111` erledigt `_bind()` zwei Dinge:

1. Es hängt eigene Bind-Tags wie `button_press.<widget>` und
   `button_command.<widget>` an die Widget-Bind-Tags an.
2. Ohne `func` ruft es `unbind_class()` auf, um das Binding zu entfernen.

Beim Erzeugen des Buttons werden die permanenten Press-/Release-Handler
registriert (`basewidgets/button_base.py:1103-1113`).

Beim Drücken registriert `_on_press()` zusätzlich den temporären
`button_command`-Handler (`basewidgets/button_base.py:881-925`). Dieser soll
beim Loslassen den eigentlichen `command` ausführen.

Beim Loslassen ruft `_on_release()` zunächst `_bind()` ohne `func` für
`button_command` auf (`basewidgets/button_base.py:927-937`).

## Der inkompatible Unterschied

`tkinter.Misc._unbind()` in Python 3.14:

```python
if funcid is None:
    self.tk.call(*what, '')
```

`tkinter.Misc._unbind()` in Python 3.15:

```python
if funcid is None:
    self._delete_bind_commands(*what)
    self.tk.call(*what, '')
```

`_delete_bind_commands()` analysiert das Tcl-Binding-Skript, extrahiert die
registrierte Callback-ID und ruft `deletecommand()` auf. Damit wird nicht nur
das Binding entfernt, sondern auch der Python-Callback aus dem Tcl-Interpreter
gelöscht.

Das ist für den dynamischen Ablauf von `tkmacosx` problematisch: Der
`button_command`-Callback wird während der Release-Verarbeitung entfernt,
bevor er ausgeführt werden kann. Es erscheint dabei keine Anwendungsausnahme,
weil der Tcl-Binding-Code lediglich keinen noch gültigen Callback mehr
ausführt.

## Reproduktion

Die folgenden Tests wurden mit `tkmacosx==1.0.5` und Python 3.15.2
ausgeführt. Tcl/Tk war jeweils 9.1.

### Normales `tkmacosx.Button`

```python
import tkinter as tk
from tkmacosx import Button

root = tk.Tk()
button = Button(root, text="Test", command=lambda: print("CLICK"))
button.pack()
root.mainloop()
```

Der Button wird angezeigt, aber `CLICK` wird beim Mausklick nicht ausgegeben.

### Kontrolltest mit altem `_unbind()`-Verhalten

Wird in Python 3.15 vor dem Import von `tkmacosx` das Python-3.14-Verhalten
von `Misc._unbind()` wiederhergestellt, funktioniert derselbe Button wieder.
Der entscheidende Kontrolllauf ergab:

```text
Python 3.15.2 + tkmacosx 1.0.5 + aktuelles _unbind():  kein command-Aufruf
Python 3.15.2 + tkmacosx 1.0.5 + altes _unbind():      CMD
```

Das grenzt den Fehler auf die Interaktion zwischen `tkmacosx`' dynamischem
Binding-Management und `tkinter.Misc._unbind()` ein. Es ist kein allgemeiner
Fehler der Tk-Button-Ereignisse: Ein Standard-`tkinter.Button` löst unter
Python 3.15 dieselben Press-/Release-Ereignisse korrekt aus.

## Ansatzpunkte für einen späteren Fork

Für einen Fork von `tkmacosx` sollte insbesondere geprüft werden:

1. Dynamische Bindings mit Callback-ID gezielt entfernen, statt
   `unbind_class(classname, sequence)` ohne Callback-ID aufzurufen.
2. Callback-IDs und Bind-Skripte pro Binding selbst verwalten, damit die
   Python-3.15-Bereinigung nicht versehentlich den noch benötigten Callback
   löscht.
3. Die Release-Reihenfolge überprüfen: Der eigentliche `command`-Callback
   muss ausgeführt werden, bevor der temporäre Release-Handler entfernt wird.
4. Tests gegen mindestens Python 3.14 und 3.15 mit Tcl/Tk 9.1 ausführen.

Eine mögliche Reparatur sollte im Fork getestet werden; diese Dokumentation
nimmt bewusst keine Änderung an der installierten Library vor.
