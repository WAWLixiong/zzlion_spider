import requests
import base64
from urllib.parse import urlencode
from lxml import etree

def ocr( ):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    baidu_url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token='
    access_token = '24.6e0783b52b0c2a1b7ed9f77ca32db969.2592000.1554299806.282335-15334177'
    url=baidu_url+access_token
    f=open('3.png','rb')
    img = base64.b64encode(f.read())
    f.close()
    data = {'image': img}
    data=urlencode(data)

    resp=requests.post(url,headers=headers,data=data).json()
    print(resp)

if __name__ == '__main__':
    a=ocr()
