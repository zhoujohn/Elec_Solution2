import discover
import numpy
import cv2
import rtsp
from onvif import ONVIFCamera
import urllib.parse as url


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
        video_encoder_configuration.Encoding = 'H264'
        video_encoder_configuration.Resolution = options.H264.ResolutionsAvailable[0]
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
        rtspclt = rtsp.Client(rtsp_server_uri=res.Uri)
        content = rtspclt.read()
        img = cv2.cvtColor(numpy.asarray(content), cv2.COLOR_RGB2BGR)
        tmp = info.urn.split('-')
        name = './capture/' + tmp[-1] + '.jpg'
        cv2.imwrite(name, img)


if __name__ == '__main__':
        main()
