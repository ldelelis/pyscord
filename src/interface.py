import curses


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

    def __init__(self, ySize, xSize, delimiterChars=['|', '-']):
        BaseWindow.__init__(self, ySize, xSize, delimiterChars)
        self.__renderWindow()
        self.cursesRenderedWindow.scrollok(True)
        self.cursorStartY, self.cursorStartX = self.__setCursor()

    def __renderWindow(self):
        self.cursesRenderedWindow = curses.newwin(self.ySize, self.xSize)

        cursorY, cursorX = self.cursesRenderedWindow.getyx()

        self.cursesRenderedWindow.refresh()

    def __setCursor(self):
        cursorY, cursorX = self.cursesRenderedWindow.getyx()
        return cursorY + 1, cursorX + 1

    def _countLines(self, message):
        return message.clean_content.count("\n") + 1

    def _shouldScroll(self, scrollLines):
        if self.cursorYOffset + scrollLines + 2 >= self.ySize:
            return True
        else:
            return False

    def printMessage(self, message="", prevAuthor="", prevChannel=""):
        attachments = message.attachments and \
            '(message contains attachments)' or ''

        scrollLines = self._countLines(message)

        if self._shouldScroll(scrollLines):
            self.cursesRenderedWindow.scroll(scrollLines+1)
            self.cursorYOffset -= 2
            self.cursesRenderedWindow.refresh()

        if prevAuthor != message.author or prevChannel != message.channel.name:
                self.cursesRenderedWindow.addstr(
                    self.cursorStartY+self.cursorYOffset,
                    self.cursorStartX+1,
                    '[%s][%s] %s:\r' % (message.server, message.channel.name,
                                        message.author))

        self.cursesRenderedWindow.addstr(
            self.cursorStartY+self.cursorYOffset+1,
            self.cursorStartX+1,
            '    %s %s\r' % (message.clean_content, attachments))

        self.cursorYOffset += scrollLines + 1

        self.cursesRenderedWindow.refresh()


class RenderablePane(BaseWindow):
    def __init__(self, xSize=0, ySize=0, delimiterChars=['|', '-'],
                 orientation="left"):
        BaseWindow.__init__(self, xSize, ySize, delimiterChars, orientation)
