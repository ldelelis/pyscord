import signal
import discord
import json
import asyncio
import logging

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
        pass

    @client.event
    @asyncio.coroutine
    def on_message(message):
        print("on %s %s says:" % (message.server, message.author))
        print('    %s' % message.content)


def loadConfig():
    with open('../config.json') as configFile:
        return json.load(configFile)

def setLogging():
    logger = logging.getLogger('cliscord')
    logger.setLevel(logging.ERROR)
    handler = logging.FileHandler(filename="cliscord.log", encoding="utf-8",
                                  mode="w")
    handler.setFormatter(logging.Formatter(
        '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))


configs = loadConfig()

mainClient = DiscClient(configs['token'])
mainClient.runClient()


while True:
    if signal.getsignal(signal.SIGINT):
        mainClient.closeSession()
