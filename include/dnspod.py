#!/usr/bin/env python
# coding:utf-8
import httplib,json
import socket
import re
import pycurl
import StringIO
import urllib
class dnspod:
    def __init__(self,loginEmail,loginPassword,apiUrl = 'https://dnsapi.cn/Info.Version',format = 'json',lang = 'cn',**kw ):
        self.param = {'login_email' : loginEmail,'login_password' : loginPassword,'lang' : lang,'format':format}
        self.param.update(kw)
        self.apiUrl = apiUrl

    def apiPost(self):
        url=self.apiUrl
        ch = pycurl.Curl()
        ch.setopt(pycurl.VERBOSE,1)
        ch.setopt(pycurl.FOLLOWLOCATION, 1)
        ch.setopt(pycurl.MAXREDIRS, 5)
        ch.fp = StringIO.StringIO()
        #ch.setopt(pycurl.AUTOREFERER,1)
        ch.setopt(pycurl.CONNECTTIMEOUT, 60)
        ch.setopt(pycurl.TIMEOUT, 300)
        #ch.setopt(pycurl.PROXY,proxy)
        ch.setopt(pycurl.HTTPPROXYTUNNEL,1)
        ch.setopt(pycurl.USERAGENT, "crud dns/1.0(kevin8096@live.com)")
        ch.setopt(ch.POSTFIELDS,  urllib.urlencode(self.param))
        ch.setopt(pycurl.URL, url)
        ch.setopt(ch.WRITEFUNCTION,ch.fp.write)
        ch.perform()
        return ch.fp.getvalue()



