import discord
import asyncio
import sys

from utils import loadConfig, setLogging
from interface import MainWindow, RenderableWindow
from curses import wrapper


class DiscClient:

    client = discord.Client()

    def __init__(self, clientToken):
        self.clientToken = clientToken

    def runClient(self):
        connectLoop = asyncio.get_event_loop()
        connectLoop.run_until_complete(self.client.start(self.clientToken,
                                                         bot=False))
        connectLoop.close()

    async def getLogs(self, channel, limit):
        await self.client.logs_from(channel, limit)

    @client.event
    async def on_ready():
        logger.info('Client connected.')

    @client.event
    async def on_message(message):
        async for loggedMessage in mainClient.client.logs_from(
                message.channel, 1, before=message):
            prevAuthor = loggedMessage.author
            prevChannel = loggedMessage.channel.name

        chatWindowObj.printMessage(message, prevAuthor, prevChannel)


def mainLoop(stdscr):
    mainScreenObj = MainWindow()
    maxY, maxX = mainScreenObj.getMaxAxis()

    global chatWindowObj
    chatWindowObj = RenderableWindow(maxY, maxX)

    global mainClient
    mainClient = DiscClient(configs['token'])
    try:
        mainClient.runClient()
    except KeyboardInterrupt:
        sys.exit(1)


if __name__ == "__main__":
    global logger
    logger = setLogging()

    configs = loadConfig()

    wrapper(mainLoop)
