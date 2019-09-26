import os
import logging
import logging.config


logger = None
_logs_path = '/tmp/ipcam'
_logger_conf_file = 'logger.conf'
_logger_name = 'root'


def init_logger():
    global logger
    if not os.path.exists(_logs_path):
        os.mkdir(_logs_path)
    logger_conf_path = os.path.abspath(os.path.join(os.path.dirname(__file__), _logger_conf_file))
    logging.config.fileConfig(logger_conf_path)
    logger = logging.getLogger(_logger_name)


init_logger()

_ctx = None


def setContext(ctx):
    global _ctx
    logger.info("=========Context set=========")
    _ctx = ctx


def getContext():
    global _ctx
    return _ctx


class Context(object):
    def __init__(self, conf, reporter):
        self.conf = conf
        self.reporter = reporter
