from tkinter import Tk, Canvas
from settings.appsettings import SCREEN_SIZE


class App(Tk):

    def useConfig(self):
        self.geometry(SCREEN_SIZE)

    def __init__(self, screenName: str | None = None, baseName: str | None = None, className: str = "Tk", useTk: bool = True, sync: bool = False, use: str | None = None):
        super().__init__(screenName, baseName, className, useTk, sync, use)
        self.useConfig()
        