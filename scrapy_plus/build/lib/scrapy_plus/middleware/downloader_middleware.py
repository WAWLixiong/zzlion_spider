#下载中间件

class DownloaderMiddleware(object):
    '''封装下载中间件'''
    def process_request(self,request):
        # print('请求经过下载中间件')
        return request

    def process_response(self,response):
        # print('响应经过下载中间件')
        return response