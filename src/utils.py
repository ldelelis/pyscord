import logging
import json


def loadConfig():
    with open('../config.json') as configFile:
        return json.load(configFile)


def setLogging():
    logger = logging.getLogger('pyscord')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename="pyscord.log", encoding="utf-8",
                                  mode="w")
    handler.setFormatter(logging.Formatter(
        '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)
    return logger
