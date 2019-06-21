import discover
import device
import time
import context
from context import logger
import reporter
import json

def main():
    # __init()
    print("start...")
    with open('./config.json', 'r') as f:
        conf = json.load(f)
        logger.info(conf)

    
    # discovery.run()
    dataReporter = reporter.DataReporter(conf['reportUrl'])
    ctx = context.Context(conf, dataReporter)
    context.setContext(ctx)

    global discovery
    discovery = discover.Discover('test')
    devInfos = discovery.discover()
    global manager
    manager = device.DeviceManager()
    manager.addDevices(devInfos)
    global exit
    exit = False
    while not exit:
        time.sleep(2)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        discovery.stop()
        manager.stop()
        exit = True
