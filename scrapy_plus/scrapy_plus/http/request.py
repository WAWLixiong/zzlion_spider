# request对象

class Request(object):
    """完成request对象的封装"""

    def __init__(self, url,callback='parse',meta=None,method='GET', headers=None,
                 params=None, data=None,filter=True):
        '''
        :param url:请求url
        :param method:请求方法GET，POST
        :param headers:请求头
        :param params:请求参数
        :param data:请求体
        '''
        self.url = url
        self.method = method
        self.headers = headers
        self.params = params
        self.data = data
        self.callback=callback #添加解析函数
        self.meta=meta #添加一些需要传递的数据
        self.filter=filter #默认去重