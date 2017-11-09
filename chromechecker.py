#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from xml.dom.minidom import parseString
from base64 import b64decode
from urllib import request

info = {
    "Stable": {
        "x86": "-multi-chrome",
        "x64": "x64-stable-multi-chrome",
        "appid": "{8A69D345-D564-463C-AFF1-A69D9E530F96}"
    },
    "Beta": {
        "x86": "1.1-beta",
        "x64": "x64-beta-multi-chrome",
        "appid": "{8A69D345-D564-463C-AFF1-A69D9E530F96}"
    },
    "Dev": {
        "x86": "2.0-dev",
        "x64": "x64-dev-multi-chrome",
        "appid": "{8A69D345-D564-463C-AFF1-A69D9E530F96}"
    },
    "Canary": {
        "x86": "",
        "x64": "x64-canary",
        "appid": "{4EA16AC7-FD5A-47C3-875B-DBF4A2008C20}"
    }
}

update_url = 'https://tools.google.com/service/update2'

for ver in info:
    for arch in ['x64','x86']:
        print('='*20)
        print(ver, arch)
        payload = """<?xml version='1.0' encoding='UTF-8'?>
            <request protocol='3.0' version='1.3.23.9' ismachine='0'
                     installsource='ondemandcheckforupdate' dedup='cr'
                     sessionid='{3597644B-2952-4F92-AE55-D315F45F80A5}'
                     requestid='{CD7523AD-A40D-49F4-AEEF-8C114B804658}'>
            <hw sse='1' sse2='1' sse3='1' ssse3='1' sse41='1' sse42='1' avx='1'/>
            <os platform='win' version='6.3' arch='"""+arch+"""'/>
            <app appid='"""+info[ver]['appid']+"""' ap='"""+info[ver][arch]+"""' brand='GGLS'>
                <updatecheck/>
            </app>
            </request>
        """

        requ = request.Request(url=update_url, data=payload.encode())
        resp = request.urlopen(requ).read().decode('utf-8')
        DOMTree = parseString(resp)

        for action in DOMTree.getElementsByTagName('action'):
            if action.getAttribute('run') != '': # kind weird
                name = action.getAttribute('run')
            if action.getAttribute('Version') != '':
                print('version:', action.getAttribute('Version'))

        for url in DOMTree.getElementsByTagName('url'):
            if url.getAttribute('codebase').startswith('https'):
                print(url.getAttribute('codebase')+name)

        for package in DOMTree.getElementsByTagName('package'):
            print('size: %.2fMB' %(int(package.getAttribute('size'))/1024/1024))
            print('sha1:', b64decode(package.getAttribute('hash').encode()).hex())
            print('sha256:', package.getAttribute('hash_sha256'))
