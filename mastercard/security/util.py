import time
from random import randint


def getTimestamp():
    """
    Returns the UTC timestamp (seconds passed since epoch)
    """
    return str(int(time.time()))

def getNonce(length = 16):
    """
    Returns a random string of length=@length
    """
    characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    charlen    = len(characters)
    return "".join([characters[randint(0,charlen-1)] for i in range(0,length)])
