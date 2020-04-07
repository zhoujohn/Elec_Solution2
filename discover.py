from multiprocessing import Process
import device
import socket
import xml.etree.ElementTree as ET
import time


class Discover(object):
    """docstring for Discover"""
    def __init__(self, arg):
        self.arg = arg
        self.__proc = Process(target=self.__discoverProc, args=())

    def run(self):
        print("[Discover] running...")
        self.__proc.start()

    def stop(self):
        if self.__proc.is_alive():
            self.__proc.join()
            print("[Discover] stopped.")

    def discover(self):
        deviceInfos = []
        probe = '''
            <?xml version="1.0" encoding="UTF-8"?>
            <s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope" xmlns:a="http://schemas.xmlsoap.org/ws/2004/08/addressing">
                <s:Header>
                    <a:Action s:mustUnderstand="1">http://schemas.xmlsoap.org/ws/2005/04/discovery/Probe</a:Action>
                    <a:MessageID>uuid:db7131fe-e3b4-416f-8ed3-432320bc723c</a:MessageID>
                    <a:ReplyTo>
                        <a:Address>http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous</a:Address>
                    </a:ReplyTo>
                    <a:To s:mustUnderstand="1">urn:schemas-xmlsoap-org:ws:2005:04:discovery</a:To>
                </s:Header>
                <s:Body>
                    <Probe xmlns="http://schemas.xmlsoap.org/ws/2005/04/discovery">
                        <d:Types xmlns:d="http://schemas.xmlsoap.org/ws/2005/04/discovery" xmlns:dp0="http://www.onvif.org/ver10/network/wsdl">dp0:NetworkVideoTransmitter</d:Types>
                    </Probe>
                </s:Body>
            </s:Envelope>
        '''

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(25)
        s.sendto(probe.encode('UTF-8'), ('239.255.255.250', 3702))
        timeout = time.time() + 35
        while time.time() < timeout:
            try:
                buf = s.recv(4096)
                print(buf)
                ns = {
                    'SOAP-ENV': 'http://www.w3.org/2003/05/soap-envelope',
                    'wsa': 'http://schemas.xmlsoap.org/ws/2004/08/addressing',
                    'd': 'http://schemas.xmlsoap.org/ws/2005/04/discovery'
                }
                root = ET.fromstring(buf)
                match = root.find('SOAP-ENV:Body', ns).find('d:ProbeMatches', ns).find('d:ProbeMatch', ns)
                print("match:", match)
                urn = match.find('wsa:EndpointReference', ns).find('wsa:Address', ns).text
                print("urn:", urn)
                xaddr = match.find('d:XAddrs', ns).text
                print("xaddr:", xaddr)
                deviceInfos.append(device.DeviceInfo(urn, xaddr))
            except Exception as e:
                print(e)
                break
            finally:
                pass

        return deviceInfos

    def __discoverProc(self):
        while True:
            devices = self.discover()
            print(devices)
            time.sleep(15)
        pass
