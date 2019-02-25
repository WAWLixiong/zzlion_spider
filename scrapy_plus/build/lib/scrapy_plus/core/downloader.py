#下载器模块
import  requests
from scrapy_plus.http.response import Response

class Downloader(object):
    """下载器对象封装"""

    def get_response(self,request):
        '''
        接收resposne对象，发送请求，返回对应的response对象
        :param request:
        :return:response对象
        '''
        if request.method.upper() == 'GET':
            resp=requests.get(url=request.url,headers=request.headers,
                         params=request.params)
        elif request.method.upper() == 'POST':
            resp=requests.post(url=request.url,headers=request.headers,
                             params=request.params,data=request.data)
        else:
            raise Exception('不支持该请求方法<{}>'.format(request.method))

        return Response(url=resp.url,headers=resp.headers,body=resp.content,status_code=resp.status_code)

