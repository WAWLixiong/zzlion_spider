#调度器

#利用six模块实现py2和py3的兼容
from six.moves.queue import Queue
from ..utils.log import logger

class Scheduler(object):
    """
    实现调度器的封装
    存储request对象
    对request对象去重
    """
    def __init__(self):
        self.queue=Queue()#使用该队列存储request请求

    def add_request(self,request):
        '''
        添加request对象到queue队列
        :param request:对象
        :return:
        '''
        #self._filter_request(request)
        self.queue.put(request)

    def get_request(self):
        '''
        从queue中取出request对象
        :return:request对象
        '''
        try:
            request=self.queue.get(False) #False 不等待，直接取，没Value会报错
            logger.info(request.url)
        except:
            request= None
        return request


    def _filter_request(self,request):
        '''
        实现对request对象的去重
        :param request:对象
        :return:bool
        '''
        pass

