#管道

class Pipeline(object):
    """实现管道封装，能够对item处理"""

    def process_item(self,item):
        '''
        处理item
        :param item:对象
        :return:
        '''
        print(item)