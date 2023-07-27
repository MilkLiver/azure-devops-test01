# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 15:54:45 2023

@author: user
"""

import sys,os
import logging

logger = logging.getLogger()
logger.setLevel(logging.NOTSET)
#logger.setLevel(logging.INFO)

import json

GRAFANA_IP = "127.0.0.1"
GRAFANA_PORT = 3000
GRAFANA_BEARER = 'xxxxxxxxxxxxxxxx'

def Grafana_get_folder():
    import http.client
    import ssl
    # conn = http.client.HTTPSConnection(GRAFANA_IP, 443,context = ssl._create_unverified_context())
    conn = http.client.HTTPConnection(GRAFANA_IP, GRAFANA_PORT)
    payload = ''
    headers = {
    'Authorization': 'Bearer ' + GRAFANA_BEARER
    }
    conn.request("GET", "/api/folders", payload, headers)
    res = conn.getresponse()
    data = res.read()
    #print(data.decode("utf-8"))
    return data.decode("utf-8")

def main(argc, argv, envp):
    logger.info("hello")
    
    foldersJsonStr = Grafana_get_folder()
    foldersJsonList = json.loads(foldersJsonStr)
    
    for folderDic in foldersJsonList:
        print(folderDic)
        print("uid: " + folderDic["uid"])
    
    return 0

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv, os.environ))