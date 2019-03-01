class Node(object):
    def __init__(self,data):
        self.data=data
        self.next_link=None
        self.pre_link=None

class DoubleLinkList(object):
    def __init__(self):
        self.__header=None

    def is_empty(self):
        return self.__header == None

    def len(self):
        cur=self.__header
        count=0
        while cur != None:
            count+=1
            cur=cur.next_link
        return count

    def travel(self):
        cur = self.__header
        while cur != None:
            print(cur.data,end=' ')
            cur=cur.next_link
        print('')

    def add(self,data):
        '''头部添加'''
        node=Node(data)
        if self.is_empty():
            self.__header=node
        else:
            node.next_link=self.__header
            self.__header.pre_link=node
            self.__header=node

    def append(self,data):
        node = Node(data)
        cur=self.__header
        while cur.next_link != None:
            cur=cur.next_link
        cur.next_link=node
        node.pre_link=cur

    def insert(self,index,data):
        node=Node(data)
        if index <=0:
            self.add(data)
        elif index >self.len():
            self.append(data)
        else:
            cur=self.__header
            count=0
            while count <index-1:
                count+=1
                cur=cur.next_link
            node.next_link=cur.next_link
            cur.next_link.pre_link=node
            node.pre_link=cur
            cur.next_link=node

    def remove(self,data):
        '''删除全部的data'''
        cur=self.__header
        while cur != None:
            if cur.data==data:
                if cur == self.__header:
                    if cur.next_link:
                        self.__header=cur.next_link
                        cur.next_link.pre_link=None
                    else:
                        self.__header=None
                else:
                    if cur.next_link == None:
                        cur.pre_link.next_link=None
                    else:
                        cur.pre_link.next_link=cur.next_link
                        cur.next_link.pre_link=cur.pre_link
                    return
            cur=cur.next_link

    def find(self,data):
        cur=self.__header
        while cur != None:
            if cur.data==data:
                return True
            else:
                cur=cur.next_link
        return False

if __name__ == '__main__':
    ssl=DoubleLinkList()
    ssl.add(10)
    ssl.add(11)
    ssl.add(99)
    ssl.add(11)
    ssl.append(100)
    ssl.append(200)
    ssl.insert(2,22)
    ssl.insert(3,44)
    ssl.remove(200)
    ssl.travel()
    print(ssl.find(999))
    print(ssl.len())
    print(ssl.is_empty())


