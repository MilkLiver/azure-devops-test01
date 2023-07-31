# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 15:54:45 2023

@author: user
"""

import sys,os
import logging

logger = logging.getLogger()
#logger.setLevel(logging.NOTSET)
#logger.setLevel(logging.DEBUG)
logger.setLevel(logging.INFO)

import json

GRAFANA_IP = "<IP>"
GRAFANA_PORT = <PORT>
GRAFANA_BEARER = r'<TOKEN>'

GRAFANA_DASHBOARDS_SAVE_PATH = r"D:\test\temp01\grafana-test-gitops\all-dashboards"
GRAFANA_DASHBOARDS_LOAD_PATH = r"D:\test\temp01\grafana-test-gitops\all-dashboards"

IGNORE_FOLDER_IS_EXISTS = True
#IGNORE_FOLDER_IS_EXISTS = False

DELETE_CURRENT_ALL_GRAFANA_DASHBOARDS = True

# get grafana dashboard's folders list
def grafana_get_folder():
    import http.client
    import ssl
    try:
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
    except Exception as e:
        logger.debug(e, stack_info=True, exc_info=True)
        logger.error(e)
    return data.decode("utf-8")

# get all grafana dashboards list
def grafana_get_all_dashboards():
    import http.client
    try:
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
    except Exception as e:
        logger.debug(e, stack_info=True, exc_info=True)
        logger.error(e)
    return data.decode("utf-8")

# get specific dashboard json with dashboard uid
def grafana_get_dashboard_json(dashboard_uid):
    import http.client
    try:
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
    except Exception as e:
        logger.debug(e, stack_info=True, exc_info=True)
        logger.error(e)

    return data.decode("utf-8")

# create local folder which is used to save grafana dashboard json
def get_and_create_grafana_dashboards_folder():
    
    foldersJsonStr = grafana_get_folder()
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

# Get all grafana dashboard json
def download_grafana_dashboards():
    
    dashboardsInfoJsonStr = grafana_get_all_dashboards()
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
            
            dashboardJsonStr = grafana_get_dashboard_json(str(dashboardInfoJson["uid"]))
            
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

# backup grafana all dashboards to local
def backup_grafana_dashboards():
    get_and_create_grafana_dashboards_folder()
    download_grafana_dashboards()
    return 0

# create grafana dashboard
def create_grafana_dashboard(dashboardJsonDict):
    import http.client
    import json
    try:
        #conn = http.client.HTTPSConnection(GRAFANA_IP, GRAFANA_PORT, context = ssl._create_unverified_context())
        conn = http.client.HTTPConnection(GRAFANA_IP, GRAFANA_PORT)
        payload = json.dumps(dashboardJsonDict)

        logger.debug("dashboardJsonDictStr: " + str(dashboardJsonDict))
        logger.debug("payload: " + payload)
        headers = {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + GRAFANA_BEARER
        }
        conn.request("POST", "/api/dashboards/import", payload, headers)
        res = conn.getresponse()
        data = res.read()
        logger.info(data.decode("utf-8"))
    except Exception as e:
        logger.debug(e, stack_info=True, exc_info=True)
        logger.error(e)
    return data.decode("utf-8")

# create grafana dashboard
def create_grafana_all_dashboard_in_folder(dashboardLoadPathStr, folderGrafanaJsonDic):
    try:
        logger.info("dashboardLoadPathStr: " + dashboardLoadPathStr)
        dashboardList = [item for item in os.listdir(dashboardLoadPathStr) if os.path.isfile(os.path.join(dashboardLoadPathStr, item))]
        logger.debug("dashboardList: " + str(dashboardList))
        for dashboardName in dashboardList:
            logger.info("dashboardName: " + dashboardName)
            dashboardLoadPath = os.path.join(dashboardLoadPathStr, dashboardName)
            logger.info("dashboardLoadPath: " + dashboardLoadPath)
            
            with open(dashboardLoadPath, 'r', encoding='UTF-8') as f:
                dashboardJsonStr = str(f.read())
                #logger.debug("dashboardJsonStr: "+ dashboardJsonStr)
                dashboardJsonDict = json.loads(dashboardJsonStr)
                #logger.debug("dashboardJsonDict: " + str(dashboardJsonDict["meta"]))
            
            dashboardJsonDict["folderId"] = folderGrafanaJsonDic["id"]
            dashboardJsonDict["folderUid"] = folderGrafanaJsonDic["uid"]
            dashboardJsonDict["dashboard"]["id"] = None
            #dashboardJsonDict["dashboard"]["uid"] = folderGrafanaJsonDic["uid"]
            dashboardJsonDict["dashboard"]["uid"] = None
            dashboardJsonDict["meta"]["url"] = folderGrafanaJsonDic["url"]
            create_grafana_dashboard(dashboardJsonDict)
            
    except Exception as e:
        logger.debug(e, stack_info=True, exc_info=True)
        logger.error(e)
    return 0

# create grafana dashboard's folder
def create_grafana_dashboard_folder(folderJsonStr):
    import http.client
    import json
    try:
        #conn = http.client.HTTPSConnection(GRAFANA_IP, GRAFANA_PORT, context = ssl._create_unverified_context())
        conn = http.client.HTTPConnection(GRAFANA_IP, GRAFANA_PORT)
        payload = json.dumps(eval(folderJsonStr))

        logger.debug("folderJsonStr: " + folderJsonStr)
        logger.debug("payload: " + payload)
        headers = {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + GRAFANA_BEARER
        }
        conn.request("POST", "/api/folders", payload, headers)
        res = conn.getresponse()
        data = res.read()
        logger.info(data.decode("utf-8"))
    except Exception as e:
        logger.debug(e, stack_info=True, exc_info=True)
        logger.error(e)
    return data.decode("utf-8")

# create all grafana dashboards
def create_grafana_dashboards():
    try:
        dashboardFoldersList = [item for item in os.listdir(GRAFANA_DASHBOARDS_LOAD_PATH) if os.path.isdir(os.path.join(GRAFANA_DASHBOARDS_LOAD_PATH, item))]
        for dashboardFolder in dashboardFoldersList:
            logger.info("-------------------------------------")
            logger.info("dashboardFolder: " + dashboardFolder)
            
            # get grafana dashboard folder load path
            folderLoadPath = os.path.join(GRAFANA_DASHBOARDS_LOAD_PATH, dashboardFolder)
            logger.info("folderLoadPath: " + folderLoadPath)
            
            # get grafana dashboard folder json load path
            folderJsonLoadPath = os.path.join(folderLoadPath, "folder.json")
            logger.info("folderJsonLoadPath: " + folderJsonLoadPath)
            
            # read dashboard folder json and create dashboard folder and get folder return json data
            with open(folderJsonLoadPath, 'r', encoding='UTF-8') as f:
                folderCreateReturnJsonDic = json.loads(create_grafana_dashboard_folder(f.read()))
                logger.debug("folderCreateReturnJsonDic: " + str(folderCreateReturnJsonDic))
                logger.info("folder id: " + str(folderCreateReturnJsonDic["id"]))
                logger.info("folder title: " + str(folderCreateReturnJsonDic["title"]))
                logger.info("folder uid: " + str(folderCreateReturnJsonDic["uid"]))
                logger.info("folder url: " + str(folderCreateReturnJsonDic["url"]))
                
                dashboardsLoadPath = os.path.join(folderLoadPath, "dashboards")
                create_grafana_all_dashboard_in_folder(dashboardsLoadPath, folderCreateReturnJsonDic)
            
    except Exception as e:
        logger.debug(e, stack_info=True, exc_info=True)
        logger.error(e)
    return 0

def delete_all_grafana_dashboards():
    return 0

# restore all grafana dashboards from local grafana files
def restore_grafana_dashboards():
    try:
        logger.info("=====================================")
        if DELETE_CURRENT_ALL_GRAFANA_DASHBOARDS:
            delete_all_grafana_dashboards()
        create_grafana_dashboards()
        logger.info("=====================================")
    except Exception as e:
        logger.debug(e, stack_info=True, exc_info=True)
        logger.error(e)
    return 0

def main(argc, argv, envp):
    #backup_grafana_dashboards()
    restore_grafana_dashboards()
    return 0



if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv, os.environ))