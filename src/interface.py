import curses
from math import floor


class BaseWindow:

    def __init__(self, ySize=0, xSize=0, delimiterChars=""):
        self.xSize = xSize
        self.ySize = ySize
        self.delimiterChars = delimiterChars

    def renderWindow(self):
        raise NotImplementedError


class MainWindow(BaseWindow):

    """
    delimiterChars is currently unusable because doing so would require
    a huge, very ugly dict remapping of every possible character to its
    curses binding integer. Or investigating a better method,
    which I'm not going to do since it's 3 AM.
    """

    cursesMainScreen = None

    def __init__(self, ySize=0, xSize=0, delimiterChars=['|', '-']):
        BaseWindow.__init__(self, ySize, xSize, delimiterChars)

    def renderWindow(self):
        self.cursesMainScreen = curses.initscr()
        self.cursesMainScreen.keypad(True)

    def getMaxAxis(self):
        maxY, maxX = self.cursesMainScreen.getmaxyx()
        return maxY, maxX


class RenderableWindow(BaseWindow):

    cursesRenderedWindow = None

    def __init__(self, ySize=0, xSize=0, delimiterChars=['|', '-']):
        BaseWindow.__init__(self, ySize, xSize, delimiterChars)
        self._renderWindow()

    def _renderWindow(self):
        self.cursesRenderedWindow = curses.newwin(floor(self.ySize * 0.95),
                                                  floor(self.xSize * 0.9),
                                                  floor(self.xSize * 0.01),
                                                  floor(self.ySize * 0.12))
        self.cursesRenderedWindow.box()
        cursorY, cursorX = self.cursesRenderedWindow.getyx()
        self.cursesRenderedWindow.move(cursorY+1, cursorX+1)
        self.cursesRenderedWindow.refresh()

    """
    TODO: Define a printMessage method to set the cursor to a certain pos
    and print without going off borders
    """


class RenderablePane(BaseWindow):

    def __init__(self, xSize=0, ySize=0, delimiterChars=['|', '-'],
                 orientation="left"):
        BaseWindow.__init__(self, xSize, ySize, delimiterChars, orientation)
