#! /usr/bin/env python
# coding=utf-8
'''
 * 腾讯 workec API 接口 1.6
 * Class ServerAPI
 * @author  janreyho@gmail.com
 * @date    2016-8-28  16:30
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
        url = "https://open.workec.com/customer/create"

        payload = dict({
          "optUserId": 3796852,
          "followUserId": 3796852,
          "fieldNameMapping": [
            "f_name",
            "f_mobile",
            "f_qq",
            "81055023",
            "81054636"
          ],
          "customFieldMapping": {
            "81055023": {
              "option_id": "",
              "type": "1"
            },
            "81054636": {
              "option_id": "",
              "type": "1"
            }
          },
          "fieldValueList": [
            [
                data["realname"],
                data["realmobile"],
                data["realqq"],
                data["parentmoblie"],
                data["parentrelation"],
            ]
          ]
        })
        payload = json.dumps(payload)
        headers = {
            'authorization': token,
            'corp-id': self.corpId,
            }
        response = requests.request("POST", url, data=payload, headers=headers)
        return json.loads(response.text)

workecSrv = workecAPI(workec["appId"], workec["appSecret"], workec["corpId"])
