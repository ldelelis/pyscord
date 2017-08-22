import curses
from math import floor


class BaseWindow:

    def __init__(self, ySize=0, xSize=0, delimiterChars=""):
        self.xSize = xSize
        self.ySize = ySize
        self.delimiterChars = delimiterChars

    def __renderWindow(self):
        raise NotImplementedError

    def __setCursor(self):
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
        self.__renderWindow()

    def __renderWindow(self):
        self.cursesMainScreen = curses.initscr()
        self.cursesMainScreen.keypad(True)

    def getMaxAxis(self):
        maxY, maxX = self.cursesMainScreen.getmaxyx()
        return maxY, maxX


class RenderableWindow(BaseWindow):

    cursesRenderedWindow = None
    cursorYOffset = 0

    def __init__(self, ySize=0, xSize=0, delimiterChars=['|', '-']):
        BaseWindow.__init__(self, ySize, xSize, delimiterChars)
        self.xOffset = floor(xSize * 0.1)
        self.yOffset = floor(ySize * 0.05)
        self.__renderWindow()
        self.cursorStartY, self.cursorStartX = self.__setCursor()

    def __renderWindow(self):
        self.cursesRenderedWindow = curses.newwin(floor(self.ySize * 0.95),
                                                  floor(self.xSize * 0.75),
                                                  self.yOffset,
                                                  self.xOffset)
        self.cursesRenderedWindow.box()

        cursorY, cursorX = self.cursesRenderedWindow.getyx()

        self.cursesRenderedWindow.refresh()

    def __setCursor(self):
        cursorY, cursorX = self.cursesRenderedWindow.getyx()
        return cursorY + 1, cursorX + 1

    def printMessage(self, message="", prevAuthor=""):
        attachments = message.attachments and \
            '(message contains attachments)' or ''

        if prevAuthor != message.author:
            self.cursesRenderedWindow.addstr(
                self.cursorStartY+self.cursorYOffset,
                self.cursorStartX+1,
                '[%s] %s:\r' % (message.server, message.author))

        self.cursesRenderedWindow.addstr(
            self.cursorStartY+self.cursorYOffset+1,
            self.cursorStartX+1,
            '    %s %s\r' % (message.clean_content, attachments))

        self.cursesRenderedWindow.refresh()

        self.cursorYOffset += 2


class RenderablePane(BaseWindow):

    def __init__(self, xSize=0, ySize=0, delimiterChars=['|', '-'],
                 orientation="left"):
        BaseWindow.__init__(self, xSize, ySize, delimiterChars, orientation)
