
#单向循环链表

class Node(object):
    def __init__(self,data):
        self.data=data
        self.next_link=None

class CycleLinkList(object):
    def __init__(self):
        self.__header=None

    def is_empty(self):
        return self.__header == None

    def len(self):
        cur=self.__header
        if self.is_empty():
            return 0
        else:
            count=1
            while cur.next_link != self.__header:
                count+=1
                cur=cur.next_link
            return count

    def travel(self):
        cur = self.__header
        if self.is_empty():
            return
        while cur.next_link != self.__header:
            print(cur.data,end=' ')
            cur=cur.next_link
        print(cur.data)
        print('')


    def add(self,data):
        node=Node(data)
        if self.is_empty():
            self.__header=node
            node.next_link=node
        else:
            cur=self.__header
            while cur.next_link != self.__header:
                cur=cur.next_link
            node.next_link=self.__header
            self.__header=node
            cur.next_link = node

    def append(self,data):
        node = Node(data)
        if self.is_empty() == None:
            self.__header=node
            node.next_link=node
        else:
            cur=self.__header
            while cur.next_link != self.__header:
                cur=cur.next_link
            cur.next_link=node
            self.__header=node
            node.next_link=self.__header

    def insert(self,index,data):
        node=Node(data)
        if index <=0:
            self.add(data)
        elif index >=self.len():
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
        if self.is_empty():
            return
        elif cur.data==data and self.len()==1:
            self.__header=None
        else:
            while cur.next_link != self.__header:
                if cur.data==data:
                    if cur == self.__header:
                        self.__header=cur.next_link
                        rear=self.__header
                        while rear.next_link != self.__header:
                            rear=rear.next_link
                        self.__header=cur.next_link
                        rear.next_link=cur.next_link
                    else:
                        pre.next_link=cur.next_link
                    return
                else:
                    pre=cur
                    cur=cur.next_link
            if cur.data==data:
                pre.next_link=self.__header

    def find(self,data):
        cur=self.__header
        while cur != None:
            if cur.data==data:
                return True
            else:
                cur=cur.next_link
        return False

if __name__ == '__main__':
    ssl=CycleLinkList()
    ssl.add(10)
    ssl.add(11)
    ssl.add(10)
    ssl.append(500)
    ssl.insert(5,22)
    ssl.remove(10)
    # ssl.remove(22)
    # ssl.remove(22)

    # print(ssl.find(999))
    ssl.travel()
    print(ssl.len())
    print(ssl.is_empty())


