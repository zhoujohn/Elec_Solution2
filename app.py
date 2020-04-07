import os,sys
sys.path.append('/home/gate001/wa/Elec_Solution')
PATH = os.environ
for key in PATH:
    print (key, PATH[key])

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
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'config.json'))
    with open(config_path, 'r') as f:
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

    loop_index = 0
    while not exit:
        time.sleep(5)
        manager.monitorProcs(devInfos)
        loop_index = loop_index + 1
        if loop_index > 60:
            loop_index = 0
            devInfos = refresh(manager, devInfos)


def refresh(manager, devInfos):
    devInfos_dynamic = discovery.discover()
    #if len(devInfos_dynamic) != len(devInfos):
    ###find difference
    for devi in devInfors_dynamic:
        is_new = 1
        for devi_o in devInfos:
            if devi_o.urn == devi.urn and devi_o.xaddr == devi_o.xaddr:
                is_new = 0
                break
        if is_new == 1:
            manager.addDevices(devi)
    return devInfos_dynamic



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        discovery.stop()
        manager.stop()
        exit = True
