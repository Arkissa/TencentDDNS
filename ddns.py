import requests
import re
import os
import time
'''
self.ip => id of token
self.token => token
self.dnsUrl => update url of ip dns
self.domain => domain
self.subDomain => subDomain
self.recordId => id of record
self.info => get record info of ip
'''


class ddns:
    def __init__(self):
        self.request = requests.session()
        self.ipUrl = "http://pv.sohu.com/cityjson?ie=utf-8"
        self.id = ""
        self.token = ""
        self.dnsUrl = "https://dnsapi.cn/Record.Ddns"
        self.domain = ""
        self.subDomain = ""
        self.recordId = ""
        self.info = "https://dnsapi.cn/Record.Info"

    def getIp(self):
        response = self.request.get(self.ipUrl)
        content = response.text
        ip = re.findall(r"((\d+\.).(\d+\.)+(\d+))", content)
        return ip[0][0]

    def getRecord(self):
        newIp = self.getIp()
        data = {
            'login_token': f'{self.id},{self.token}',
            'format': 'json',
            "domain": f'{self.domain}',
            'record_id': f'{self.recordId}',
            "value": f'{newIp}',
        }
        response = self.request.post(
            self.info,
            data=data,
        )
        ip = re.findall(r"((\d+\.).(\d+\.)+(\d+))", response.text)
        return ip[0][0]

    def updateDns(self):
        ip = self.getIp()
        data = {
            'login_token': f'{self.id},{self.token}',
            'format': 'json',
            'domain': f'{self.domain}',
            'record_id': f'{self.recordId}',
            'record_line': '默认'.encode("utf-8"),
            'sub_domain': 'www',
            'value': f'{ip}'
        }
        response = self.request.post(
            self.dnsUrl,
            data=data,
        )
        response.encoding = response.apparent_encoding
        return response.json()


if __name__ == "__main__":
    ip = ddns()
    oldIp = ip.getRecord()
    newIp = ip.getIp()
    time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    if oldIp != newIp:
        update = ip.updateDns()
        print(f"Time of acquisition:{time}\nUpdate new ip:{newIp}")
        exit()
    print(f"Now ip:{oldIp}")
