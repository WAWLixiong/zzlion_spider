#response对象
from lxml import etree
import json
import re

class Response(object):
    """response对象的封装"""
    def __init__(self,url,headers,body,status_code,meta={}):
        '''
        :param url:响应url
        :param headers:响应头
        :param body:响应体
        :param status_code:状态码
        '''
        self.url=url
        self.headers=headers
        self.body=body
        self.status_code=status_code
        self.meta=meta

    def xpath(self,rule):
        html=etree.HTML(self.body)
        return html.xpath(rule)

    @property
    def json(self):
        return json.loads(self.body.decode())

    def re_findall(self,rule,data=None):
        if data is None:
            data=self.body
        return re.findall(rule,data)





