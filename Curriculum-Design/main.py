import ctypes
import sys

if sys.platform == "win32":
    try:
        ctypes.OleDLL('shcore').SetProcessDpiAwareness(2)
    except AttributeError:
        pass
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except AttributeError:
        pass

from gui import ContactManagerApp

if __name__ == "__main__":
    app = ContactManagerApp()
    app.mainloop()
