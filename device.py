import os
import time
import datetime
from onvif import ONVIFCamera
import urllib.parse as url
from multiprocessing import Process
import context
import cv2
from camdetect import read_anno_config, entry_detect, release_detect, save_image_from_diff



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
    
    def addDevice(self, info):
        dev = Device(info)
        self.__devices[info.urn] = dev
        dev.run()
    
    def monitorProcs(self, deviceInfos):
        for info in deviceInfos:
            dev = self.__devices[info.urn]
            if dev.isAlive() is False:
                proc = dev.restart()

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
            self.__proc.terminate()
            if self.__rtsp is not None:
                self.__rtsp.release()
            print('Device %s stopped...', self.__urn)
    
    def restart(self):
        if self.__rtsp is not None:
            self.__rtsp.release()
        self.__proc = Process(target=self.__deviceProc, args=())
        #time.sleep(1)
        self.__proc.start()
    
    def isAlive(self):
        if self.__proc.is_alive():
            return True
        else:
            return False

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
        local_urn = self.__urn[-12:]

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

        detect_last_valid = {}
        
        no_frame_index = 0
        # capture and detect
        while self.__rtsp.isOpened():
            print('%s capture startinging...' % ip)
            #start = time.time()
            #print('start: %d' % start)
            ret, frame = self.__rtsp.read()
            
            ### Notice: no frame continues for 90 senconds, system will restart this process and reopen the camera to get stream
            if not ret:
                time.sleep(3)
                no_frame_index += 1
                if no_frame_index > 30: ## 90 seconds
                    no_frame_index = 0
                    self.__rtsp.release()
                    time.sleep(1)
                    break
                continue
            no_frame_index = 0
            #print('capture: %d' % time.time())
            # img = cv2.cvtColor(numpy.asarray(frame),cv2.COLOR_RGB2BGR)
            #print('convert: %d' % time.time())
            #tmp = self.__urn.split('-')
            #name = tmp[-1] + '.jpg'
            #cv2.imwrite(name, frame)

            detect_result = entry_detect(frame, num, matrix)
            #print(detect_result)
            if detect_result == detect_result1 and detect_result == detect_result2 and detect_result == detect_result3 and detect_result == detect_result4:
                print('***%s capture end.\n' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                print(detect_result)
                reporter.publish('cam_test', detect_result)
                # verify the difference between present result and previous result
                if detect_result != detect_last_valid and len(detect_last_valid) != 0:
                    # find the different ones
                    for ele in detect_result:
                        v1 = detect_result[ele]
                        v2 = detect_last_valid[ele]
                        if v2 != v1:
                            # check r,g,y difference
                            if v2&0x03 != v1&0x03:
                                save_image_from_diff(frame, matrix, ele, 0, local_urn, '_R', str(v1&0x03), str(v2&0x03))
                            if v2&0x0c != v1&0x0c:
                                save_image_from_diff(frame, matrix, ele, 1, local_urn, '_G', str(v1&0x0c), str(v2&0x0c))
                            if v2&0x30 != v1&0x30:
                                save_image_from_diff(frame, matrix, ele, 2, local_urn, '_Y', str(v1&0x30), str(v2&0x30))
                            if v2&0xc0 != v1&0xc0:
                                save_image_from_diff(frame, matrix, ele, 3, local_urn, '_H', str(v1&0xc0), str(v2&0xc0))
                        #print (v,v1)
                detect_last_valid = detect_result
            detect_result4 = detect_result3
            detect_result3 = detect_result2
            detect_result2 = detect_result1
            detect_result1 = detect_result

            time.sleep(3)

        
