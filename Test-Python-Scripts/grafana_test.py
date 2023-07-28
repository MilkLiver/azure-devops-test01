# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 15:54:45 2023

@author: user
"""

import sys,os
import logging

logger = logging.getLogger()
#logger.setLevel(logging.NOTSET)
logger.setLevel(logging.DEBUG)
#logger.setLevel(logging.INFO)

import json

GRAFANA_IP = "<IP>"
GRAFANA_PORT = <PORT>
GRAFANA_BEARER = '<TOKEN>'

GRAFANA_DASHBOARDS_SAVE_PATH = r"D:\test\temp01\grafana-test-gitops"

IGNORE_FOLDER_IS_EXISTS = True
#IGNORE_FOLDER_IS_EXISTS = False

def Grafana_get_folder():
    import http.client
    import ssl
    #conn = http.client.HTTPSConnection(GRAFANA_IP, GRAFANA_PORT, context = ssl._create_unverified_context())
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

def Grafana_get_all_dashboards():
    import http.client

    #conn = http.client.HTTPSConnection(GRAFANA_IP, GRAFANA_PORT, context = ssl._create_unverified_context())
    conn = http.client.HTTPConnection(GRAFANA_IP, GRAFANA_PORT)
    payload = ''
    headers = {
        'Authorization': 'Bearer ' + GRAFANA_BEARER
    }
    conn.request("GET", "/api/search?type=dash-db", payload, headers)
    res = conn.getresponse()
    data = res.read()
    #print(data.decode("utf-8"))
    return data.decode("utf-8")

def Grafana_get_dashboard_json(dashboard_uid):
    import http.client
    
    #conn = http.client.HTTPSConnection(GRAFANA_IP, GRAFANA_PORT, context = ssl._create_unverified_context())
    conn = http.client.HTTPConnection(GRAFANA_IP, GRAFANA_PORT)
    payload = ''
    headers = {
      'Authorization': 'Bearer ' + GRAFANA_BEARER
    }
    conn.request("GET", "/api/dashboards/uid/" + dashboard_uid, payload, headers)
    res = conn.getresponse()
    data = res.read()
    #print(data.decode("utf-8"))
    return data.decode("utf-8")

def get_and_create_grafana_dashboards_folder():
    
    foldersJsonStr = Grafana_get_folder()
    foldersJsonList = json.loads(foldersJsonStr)
    
    # get all folders data
    for folderJson in foldersJsonList:
        try:
            folderCreatePath = os.path.join(GRAFANA_DASHBOARDS_SAVE_PATH, str(folderJson["title"]))
            logger.info("-------------------------------------")
            logger.debug("folder Json: " + str(folderJson))
            logger.info("folder title: " + str(folderJson["title"]))
            logger.info("folder uid: " + str(folderJson["uid"]))
            logger.info("folder id: " + str(folderJson["id"]))
            
            # create folder
            logger.info("create folder " + folderCreatePath + " ...")
            os.makedirs(folderCreatePath, exist_ok=IGNORE_FOLDER_IS_EXISTS)
            logger.info("create folder " + folderCreatePath + " finish")
        
        
            folderJsonSavePath = os.path.join(folderCreatePath, "folder.json")
            # get and create folder json
            logger.info("save folder json " + folderJsonSavePath + " ...")
            with open(folderJsonSavePath, 'w+', encoding='UTF-8') as f:
                f.write(str(folderJson))
            logger.info("save folder json " + folderJsonSavePath + " finish")
        except FileNotFoundError:
            logger.info("The 'docs' directory does not exist")
        except Exception as e:
            logger.debug(e, stack_info=True, exc_info=True)
            logger.error(e)

    return 0

def download_grafana_dashboards():
    
    
    dashboardsInfoJsonStr = Grafana_get_all_dashboards()
    dashboardsInfoJsonList = json.loads(dashboardsInfoJsonStr)
    for dashboardInfoJson in dashboardsInfoJsonList:
        try:
            logger.info("-------------------------------------")
            logger.debug("dashboard Json: " + str(dashboardInfoJson))
            logger.info("dashboard folderTitle: " + str(dashboardInfoJson["folderTitle"]))
            logger.info("dashboard folderId: " + str(dashboardInfoJson["folderId"]))
            logger.info("dashboard folderUid: " + str(dashboardInfoJson["folderUid"]))
            logger.info("dashboard title: " + str(dashboardInfoJson["title"]))
            logger.info("dashboard uid: " + str(dashboardInfoJson["uid"]))
            logger.info("dashboard id: " + str(dashboardInfoJson["id"]))
            
            folderCreatePath = os.path.join(GRAFANA_DASHBOARDS_SAVE_PATH, str(dashboardInfoJson["folderTitle"]))
            dashboardSaveDirPath = os.path.join(folderCreatePath, "dashboards")

            # create dashboard folder
            if not os.path.exists(dashboardSaveDirPath):
                logger.info("create dashboard folder " + folderCreatePath + " ...")
                os.makedirs(dashboardSaveDirPath, exist_ok=IGNORE_FOLDER_IS_EXISTS)
                logger.info("create dashboard folder " + folderCreatePath + " finish")
            dashboardJsonSavePath = os.path.join(dashboardSaveDirPath, str(dashboardInfoJson["title"]))
            
            dashboardJsonStr = Grafana_get_dashboard_json(str(dashboardInfoJson["uid"]))
            
            logger.info("save dashboard json " + dashboardJsonSavePath + " ...")
            with open(dashboardJsonSavePath, 'w+', encoding='UTF-8') as f:
                f.write(str(dashboardJsonStr))
            logger.info("save folder json " + dashboardJsonSavePath + " finish")

        except FileNotFoundError:
            logger.info("The 'docs' directory does not exist")
        except Exception as e:
            logger.debug(e, stack_info=True, exc_info=True)
            logger.error(e)
        
    return 0

def backup_grafana_dashboards():
    get_and_create_grafana_dashboards_folder()
    download_grafana_dashboards()
    return 0
def main(argc, argv, envp):
    logger.info("hello")
    
    backup_grafana_dashboards()
    
    return 0



if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv, os.environ))
