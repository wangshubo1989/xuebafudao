#! /usr/bin/env python
# coding=utf-8
'''
 * 网易云信server API 接口 1.6
 * Class ServerAPI
 * @author  hzchensheng15@corp.netease.com
 * @date    2015-10-28  16:30
 * 
'''

import urllib2,urllib
import random,time,hashlib
import logging
import logging.config
from neteaseIM import workec
import json
import requests

class workecAPI():
    '''
     * 参数初始化
     * @param AppKey
     * @param AppSecret
    '''
    def __init__(self,appId,appSecret,corpId):
        self.appId = appId;               #开发者平台分配的AppKey
        self.appSecret = appSecret;         #开发者平台分配的AppSecret,可刷新
        self.corpId = corpId;

    def gettoken(self):
        url = "https://open.workec.com/auth/accesstoken"
        payload = dict({
            "appId"   : self.appId,
            "appSecret" : self.appSecret,
            })
        payload = json.dumps(payload)
        response = requests.request("POST", url, data=payload)
        return json.loads(response.text)

    def addcustomer(self,data,token):
        print data
        url = "https://open.workec.com/customer/create"

        payload = dict({
          "optUserId": 3796852,
          "followUserId": 3796852,
          "fieldNameMapping": [
            "f_name",
            "f_mobile",
            "81055023",
            "81054636",
            "81055075",
          ],
          "customFieldMapping": {
            "81055023": {
              "option_id": "",
              "type": "1"
            },
            "81054636": {
              "option_id": "",
              "type": "1"
            },
            "81055075": {
              "option_id": "",
              "type": "1"
            }
          },
          "fieldValueList": [
            [
                data["realname"],
                data["realmobile"],
                data["parentmoblie"],
                data["parentrelation"],
                data["realqq"]
            ]
          ]
        })
        payload = json.dumps(payload)
        headers = {
            'authorization': token,
            'corp-id': self.corpId,
            }
        print payload
        response = requests.request("POST", url, data=payload, headers=headers)
        print(response.text)
        return json.loads(response.text)

workecSrv = workecAPI(workec["appId"], workec["appSecret"], workec["corpId"])