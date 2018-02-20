import curses


class BaseWindow:
    xSize = None
    ySize = None
    position = None

    def __renderWindow(self):
        raise NotImplementedError

    def __setCursor(self):
        raise NotImplementedError


class MainWindow(BaseWindow):
    cursesMainScreen = None

    def __init__(self, ySize=0, xSize=0):
        self.ySize = ySize
        self.xSize = xSize
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

    def __init__(self, ySize, xSize):
        self.ySize = ySize
        self.xSize = xSize
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
        return message.clean_content.count("\n")

    def _shouldScroll(self, scrollLines):
        if self.cursorYOffset + scrollLines + 2 >= self.ySize:
            return True
        else:
            return False

    def printMessage(self, message, prevAuthor="", prevChannel=""):
        attachments = message.attachments and \
            '(message contains attachments)' or ''

        scrollLines = self._countLines(message)

        if self._shouldScroll(scrollLines):
            self.cursesRenderedWindow.scroll(scrollLines+2)
            self.cursorYOffset -= scrollLines + 2
            self.cursesRenderedWindow.refresh()

        if prevAuthor != message.author or prevChannel != message.channel.name:
                self.cursesRenderedWindow.addstr(
                    self.cursorStartY+self.cursorYOffset,
                    self.cursorStartX+1,
                    '[%s][%s] %s:\r' % (message.server, message.channel.name,
                                        message.author))
                self.cursorYOffset += 1

        self.cursesRenderedWindow.addstr(
            self.cursorStartY+self.cursorYOffset,
            self.cursorStartX+1,
            "\t%s %s\r" % (message.clean_content, attachments))

        self.cursorYOffset += scrollLines + 1

        self.cursesRenderedWindow.refresh()


class RenderablePane(BaseWindow):
    def __init__(self, size=10, position="left"):
        self.position = position
        self.size = size
        self.__renderWindow()

        def setPosition(self):
            maxY, maxX = self.getMaxAxis()
            if self.position in ("left", "right"):
                self.ySize = maxY
                self.xSize = self.size
            elif self.position in ("top", "bottom"):
                self.ySize = self.size
                self.xSize = maxX
            pass

        def __renderWindow(self):
            pass
