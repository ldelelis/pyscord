import discord
import asyncio

from utils import loadConfig, setLogging
from interface import MainWindow, RenderableWindow
from curses import wrapper
from signal import getsignal, SIGINT


class DiscClient:

    clientToken = None
    client = discord.Client()

    def __init__(self, clientToken):
        self.clientToken = clientToken

    def runClient(self):
        connectLoop = asyncio.get_event_loop()
        connectLoop.run_until_complete(self.client.start(self.clientToken,
                                                         bot=False))
        connectLoop.close()

    @asyncio.coroutine
    def closeSession(self):
        self.client.close()

    @client.event
    @asyncio.coroutine
    def on_ready():
        logger.info('Client connected.')

    @client.event
    @asyncio.coroutine
    def on_message(message, prevAuthor=None):
        attachments = message.attachments and \
                      '(message contains attachments)' or ''

        if prevAuthor != message.author:
            print("[%s] %s says:\r" % (message.server, message.author))

        print('    %s %s\r' % (message.clean_content, attachments))

        prevAuthor = message.author  # TODO: fix, doesn't work

        """
        TODO: implement line checking to avoid scrolling
        """


def mainLoop(stdscr):

    mainScreenObj = MainWindow()
    mainScreenObj.renderWindow()
    maxY, maxX = mainScreenObj.getMaxAxis()

    chatWindowObj = RenderableWindow(maxY, maxX)

    global logger
    logger = setLogging()
    configs = loadConfig()

    mainClient = DiscClient(configs['token'])
    mainClient.runClient()

    while True:
        if getsignal(SIGINT):
            mainClient.closeSession()


if __name__ == "__main__":
    wrapper(mainLoop)
