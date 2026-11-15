# tkmacOS

tkmacOS is a fork of [tkmacosx](https://github.com/Saadmairaj/tkmacosx), originally created by **Saad Mairaj**. The original project is licensed under the Apache License, Version 2.0. This fork retains the upstream license and copyright notices; see [LICENSE](LICENSE) and [NOTICE](NOTICE).

## Why this fork exists

The upstream project is no longer actively maintained, and its custom buttons stopped responding to mouse clicks under Python 3.15. The failure came from Tkinter's changed cleanup of Tcl callbacks when event bindings are removed. tkmacOS maintains the widgets and fixes that event-dispatch incompatibility.

## What changed

- The installable distribution and import package are renamed from `tkmacosx` to `tkmacos`. This is a breaking import change: use `from tkmacos import Button`.
- Button, CircleButton, and Radiobutton defer cleanup of temporary release bindings until Tk finishes dispatching the current event. This keeps the callback available under Python 3.15.
- Package metadata is read directly from the source during builds, so building the package does not import Tkinter. Tkinter is still required to use the widgets.
- Regression coverage was added for normal clicks, disabled widgets, and releases outside the widget.

## Installation

```bash
python -m pip install tkmacos
```

tkmacOS requires Python 3, Tkinter, and the `colour` package. Tkinter must be available in the Python distribution used to run the application.

## Quick start

```python
import tkinter as tk
from tkmacos import Button

root = tk.Tk()
Button(root, text="Click me", command=lambda: print("Clicked")).pack()
root.mainloop()
```

For the full set of widget options, see the examples and API documentation in this repository.

## License and attribution

tkmacOS contains code derived from tkmacosx by Saad Mairaj. The original work and this fork are distributed under the [Apache License 2.0](LICENSE). Existing upstream copyright and license notices are retained. Fork modifications are identified in source files and summarized in [NOTICE](NOTICE).
