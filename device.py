import os
import time
from onvif import ONVIFCamera
import urllib.parse as url
from multiprocessing import Process
import context
import cv2
from camdetect import read_anno_config, entry_detect, release_detect



class DeviceManager(object):
    """docstring for DeviceManager"""
    def __init__(self):
        self.__devices = {}


    def addDevices(self, deviceInfos):
        #print('[DeviceManager]addDevices()', deviceInfos)
        for info in deviceInfos:
            dev = Device(info)
            self.__devices[info.urn] = dev
            dev.run()

    def stop(self):
        for k, v in self.__devices.items():
            v.stop()
        release_detect()

class DeviceInfo(object):
    """docstring for DeviceInfo"""
    def __init__(self, urn, xaddr):
        self.urn = urn
        self.xaddr = xaddr


class Device(object):
    """docstring for Device"""

    def __init__(self, info):
        self.__urn = info.urn
        self.__xaddr = info.xaddr
        self.__proc = Process(target=self.__deviceProc, args=())
        self.__rtsp = None
        self.__cam = None

    def run(self):
        print('Device %s running...', self.__urn)
        self.__proc.start()

    def stop(self):
        if self.__proc.is_alive():
            self.__proc.stop()
            if self.__rtsp is not None:
                self.__rtsp.close()
            print('Device %s stopped...', self.__urn)

    def __deviceProc(self):
        res = url.urlparse(self.__xaddr)
        #print(res)
        tmp = res[1].split(':')
        ip = tmp[0]
        if len(tmp) > 1:
            port = tmp[1]
        else:
            port = 80

        num, matrix = read_anno_config(os.path.abspath(os.path.join(os.path.dirname(__file__), 'config/' + self.__urn[-12:] + '.json')))

        retry = 5

        while retry:
            # get camera instance
            cam = ONVIFCamera(ip, port, '', '')
            # create media service
            media_service = cam.create_media_service()
            token = '000'
            # set video configuration
            configurations_list = media_service.GetVideoEncoderConfigurations()
            video_encoder_configuration = configurations_list[0]
            options = media_service.GetVideoEncoderConfigurationOptions({'ProfileToken':token})
            video_encoder_configuration.Encoding = 'H265'
            video_encoder_configuration.Resolution = options.H264.ResolutionsAvailable[1]
            for resolution in options.H264.ResolutionsAvailable:
                if resolution["Width"] == 2592 and resolution["Height"] == 1944:
                    video_encoder_configuration.Resolution = resolution
            request = media_service.create_type('SetVideoEncoderConfiguration')
            request.Configuration = video_encoder_configuration
            request.ForcePersistence = True
            media_service.SetVideoEncoderConfiguration(request)

            # get video stream
            streamSetup = {
                'StreamSetup': {
                    'Stream': 'RTP-Unicast',
                    'Transport': {
                        'Protocol': 'TCP'
                    }
                },
                'ProfileToken': token
            }
            res = media_service.GetStreamUri(streamSetup)
            self.__rtsp = cv2.VideoCapture(res.Uri)

            reporter = context.getContext().reporter
            time.sleep(1)
            retry = retry - 1
            if self.__rtsp.isOpened():
                print('--------------YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY camera opened')
                break

        
        detect_result1 = {}
        detect_result2 = {}
        detect_result3 = {}
        detect_result4 = {}
        # capture and detect
        while self.__rtsp.isOpened():
            print('%s capture startinging...' % ip)
            #start = time.time()
            #print('start: %d' % start)
            ret, frame = self.__rtsp.read()
            if not ret:
                time.sleep(3)
                continue
            #print('capture: %d' % time.time())
            # img = cv2.cvtColor(numpy.asarray(frame),cv2.COLOR_RGB2BGR)
            #print('convert: %d' % time.time())
            #tmp = self.__urn.split('-')
            #name = tmp[-1] + '.jpg'
            #cv2.imwrite(name, frame)

            detect_result = entry_detect(frame, num, matrix)
            print(detect_result)
            if detect_result == detect_result1 and detect_result == detect_result2 and detect_result == detect_result3 and detect_result == detect_result4:
                print('*****************XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX%s capture end %d. duration:%d' % (ip, time.time(), time.time())) # - start))
                reporter.publish('cam_test', detect_result)
            detect_result4 = detect_result3
            detect_result3 = detect_result2
            detect_result2 = detect_result1
            detect_result1 = detect_result
            
            time.sleep(3)

        
