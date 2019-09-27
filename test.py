import os
import discover
import numpy
import cv2
from onvif import ONVIFCamera
import urllib.parse as url
from camdetect import read_anno_config, entry_detect, release_detect
import time

def main():
    # __init()
    print("start...")
    global discovery
    discovery = discover.Discover('test')
    devInfos = discovery.discover()
    for info in devInfos:
        res = url.urlparse(info.xaddr)
        #print(res)
        tmp = res[1].split(':')
        ip = tmp[0]
        if len(tmp) > 1:
            port = tmp[1]
        else:
            port = 80

        # get camera instance
        cam = ONVIFCamera(ip, port, '', '')
        # create media service
        media_service = cam.create_media_service()
        token = '000'

        # set video configuration
        configurations_list = media_service.GetVideoEncoderConfigurations()
        video_encoder_configuration = configurations_list[0]
        options = media_service.GetVideoEncoderConfigurationOptions({'ProfileToken': token})
        video_encoder_configuration.Encoding = 'H264'
        video_encoder_configuration.Resolution = options.H264.ResolutionsAvailable[1]
        for resolution in options.H264.ResolutionsAvailable:
            #print (resolution)
            if resolution["Width"] == 2592 and resolution["Height"] == 1944:
                video_encoder_configuration.Resolution = resolution
                print (resolution)
        #video_encoder_configuration.Resolution.width = 2592
        #video_encoder_configuration.Resolution.height = 1944
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
            'ProfileToken': '000'
        }
        res = media_service.GetStreamUri(streamSetup)
        #time.sleep(5)
        #rtspclt = rtsp.Client(rtsp_server_uri=res.Uri)
        #content = rtspclt.read()
        #img = cv2.cvtColor(numpy.asarray(content), cv2.COLOR_RGB2BGR)
        cam = cv2.VideoCapture(res.Uri)
        result, img = cam.read()
        num, matrix = read_anno_config(os.path.abspath(os.path.join(os.path.dirname(__file__),'config/' + info.urn[-12:] + '.json')))
        if not result:
            continue
            #if img is not None:
        print (img.shape[0],img.shape[1])
        detect_result = entry_detect(img, num, matrix)
        print ("+++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print (detect_result)
        print ("+++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        #tmp = info.urn.split('-')
        #name = './capture/' + tmp[-1] + '.jpg'
        #cv2.imwrite(name, img)


if __name__ == '__main__':
        main()
