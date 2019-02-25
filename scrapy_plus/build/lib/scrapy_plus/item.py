#item对象

class Item(object):
    """item对象封装"""
    def __init__(self,data):
        self.__data=data

    @property
    def data(self):
        return self.__data

if __name__ == '__main__':
    data={'name':'zzlion'}
    item=Item(data)
    # item.data=10
    print(item.data)
