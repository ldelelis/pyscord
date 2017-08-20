import curses


class BaseWindow:

    def __init__(self, xSize=0, ySize=0, delimiterChars=""):
        self.xSize = xSize
        self.ySize = ySize
        self.delimiterChars = delimiterChars

    def _startWindow(self):
        raise NotImplementedError


class MainWindow(BaseWindow):

    """
    delimiterChars is currently unusable because doing so would require
    a huge, very ugly dict remapping of every possible character to its
    curses binding integer. Or investigating a better method,
    which I'm not going to do since it's 3 AM.
    """

    def __init__(self, xSize=0, ySize=0, delimiterChars=['-', '|']):
        BaseWindow.__init__(self, xSize, ySize, delimiterChars)
        self.cursesMainScreen = self._startWindow()

    def _startWindow(self):
        self.cursesMainScreen = curses.initscr()
        self.cursesMainScreen.keypad(True)
        self.cursesMainScreen.box()


class BasePane(BaseWindow):
    pass


class MainPane(BasePane):
    pass
