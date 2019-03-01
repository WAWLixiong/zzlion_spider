#队列实现
#双端队列

class Queue(object):

    def __init__(self):
        self.item=[]

    def enqueue(self,data):
        self.item.insert(0,data)

    def hdequeue(self):
        self.item.pop(0)

    def tenqueue(self,data):
        self.item.append(data)

    def dequeue(self):
        return self.item.pop()

    def is_empty(self):
        return self.item == []

    def size(self):
        return len(self.item)
