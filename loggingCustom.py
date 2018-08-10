import logging


LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"


def log():
    logging.basicConfig(filename='RedisClient.log', level=logging.DEBUG,
               format=LOG_FORMAT, datefmt=DATE_FORMAT)
    return logging
