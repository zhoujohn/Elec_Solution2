import Queue

MSG_TYPE_DEVICE_DISCOVERED = 'device_discovered'

class MessageQueue(object):
    def __init__(self):
        self.__q = Queue.Queue(maxsize=0)

    def putMsg(self, msg):
        self.__q.put(msg, block=True)

    def getMsg(self):
        return self.__q.get(block=True)


class Msg(object):
    """docstring for Msg"""
    def __init__(self, msgType, data):
        self.__type = msgType
        self.__data = data
        

    def getData(self):
        return self.__data


    def getType(self):
        return self.__type