class Node(object):
    def __init__(self,data):
        self.data=data
        self.lchild=None
        self.rchild=None


class Tree(object):
    def __init__(self):
        self.root=None

    def add(self,data):
        node=Node(data)
        if self.root==None:
            self.root=node
        else:
            queue=[]
            queue.append(self.root)
            while queue:
                q=queue.pop(0)
                if  q.lchild is None:
                    q.lchild=node
                    return
                elif q.rchild is None:
                    q.rchild=node
                    return
                else:
                    queue.append(q.lchild)
                    queue.append(q.rchild)

    def travel(self):
        if self.root == None:
            print('')
            return
        else:
            queue=[]
            queue.append(self.root)
            while queue:
                q=queue.pop(0)
                print(q.data,end=' ')
                if q.lchild:
                    queue.append(q.lchild)
                if q.rchild:
                    queue.append(q.rchild)
            print('')


if __name__ == '__main__':
    tree=Tree()
    for i in range(10):
        tree.add(i)

    tree.travel()


