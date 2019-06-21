from context import logger
import requests
import json


VERSION = 1         # msg version
TYPE = 5            # msg type
SERIALIZATION = 0   # msg serialization string


class DataReporter(object):
    def __init__(self, url):
        logger.info("DataReporter init")
        self.__url = url

    def publish(self, topic, payload):
        if payload is not None:
            msg = json.dumps({'from':'ipcam','topic':topic,'qos':1,'encrypt':0,'payload':payload})
            logger.debug('mqtt message: %s' % msg)
            info = ""
            try:
                result = requests.post(self.__url, data=msg).json()
                status = result.get('status')
                info = "Message publishing %s: %s" % ('done' if status == 'ok' else 'failed', payload)
            except Exception as e:
                logger.warn('Exception in message publishing: %s' % e)
            finally:
                logger.debug(info)
        else:
            info = "No data to report."
            logger.warn(info)
