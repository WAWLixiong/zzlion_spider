class Node(object):
    def __init__(self,data):
        self.data=data
        self.next_link=None

class SingelLinkList(object):
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
        node=Node(data)
        if self.is_empty():
            self.__header=node
        else:
            node.next_link=self.__header
            self.__header=node

    def append(self,data):
        node = Node(data)
        if self.is_empty() == None:
            self.__header=node
        else:
            cur=self.__header
            while cur.next_link != None:
                cur=cur.next_link
            cur.next_link=node

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
            cur.next_link=node


    def remove(self,data):
        '''删除全部的data'''
        cur=self.__header
        pre=None
        while cur != None:
            if cur.data==data:
                if cur == self.__header:
                    self.__header=cur.next_link
                else:
                    pre.next_link=cur.next_link
                    return
            pre=cur
            cur=cur.next_link

    def find(self,data):
        cur=self.__header
        if self.__header == None:
            return False
        else:
            while cur.next_link != self.__header:
                if cur.data==data:
                    return True
                else:
                    cur=cur.next_link
            if cur.data==data:
                return True
            return False

if __name__ == '__main__':
    ssl=SingelLinkList()
    ssl.add(10)
    ssl.add(11)
    ssl.add(99)
    ssl.add(11)
    ssl.append(100)
    ssl.remove(11)
    print(ssl.find(999))
    ssl.travel()
    print(ssl.len())
    print(ssl.is_empty())


