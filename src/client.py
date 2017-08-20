import discord
import asyncio

from utils import loadConfig, setLogging
from interface import MainWindow
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
        loop.close()

    @asyncio.coroutine
    def closeSession(self):
        self.client.close()

    @client.event
    @asyncio.coroutine
    def on_ready():
        logger.info('Client connected.')

    @client.event
    @asyncio.coroutine
    def on_message(message):
        attachments = message.attachments and '(message contains attachments)' \
                      or ''
        print("[%s] %s says:\r" % (message.server, message.author))
        print('    %s %s\r' % (message.clean_content, attachments))


def mainLoop(stdscr):

    mainScreenObj = MainWindow()
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
