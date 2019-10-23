import discover
import numpy
import cv2
from onvif import ONVIFCamera
import urllib.parse as url
import datetime
import os


def main():
    # __init()
    print("start...")
    global discovery
    discovery = discover.Discover('test')
    devInfos = discovery.discover()
    for info in devInfos:
        res = url.urlparse(info.xaddr)
        print(res)
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
        video_encoder_configuration.Encoding = 'H265'
        video_encoder_configuration.Resolution = options.H264.ResolutionsAvailable[1]
        for resolution in options.H264.ResolutionsAvailable:
            print (resolution)
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
            'ProfileToken': '000'
        }
        res = media_service.GetStreamUri(streamSetup)
        #rtspclt = rtsp.Client(rtsp_server_uri=res.Uri)
        #content = rtspclt.read()
        #img = cv2.cvtColor(numpy.asarray(content), cv2.COLOR_RGB2BGR)
        tmp = info.urn.split('-')
        isExists=os.path.exists('./capture/'+tmp[-1])
        if not isExists:
            os.mkdir('./capture/' + tmp[-1])

        amount = 5
        while amount:
            cam = cv2.VideoCapture(res.Uri)
            result, img = cam.read()
            #name = './capture/' + tmp[-1] + '/' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '.jpg'
            name = './capture/' + tmp[-1] + '/' + tmp[-1] + str(50-amount) + '.jpg'
            #name = './capture/' + tmp[-1] + '/' + str(datetime.datetime.now()) + '.jpg'
            cv2.imwrite(name, img)
            amount -= 1
            print (name, amount)

if __name__ == '__main__':
        main()
