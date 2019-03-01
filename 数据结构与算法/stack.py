#实现栈

class Stack(object):
    def __init__(self):
        self.item=[]

    def push(self,data):
        '''添加一个新的元素到栈顶'''
        self.item.append(data)

    def pop(self):
        '''弹出栈顶元素'''
        self.item.pop()

    def peek(self):
        '''返回栈顶元素值'''
        return self.item[len(self.item)-1]

    def is_empty(self):
        return len(self.item)==0

    def size(self):
        return len(self.item)

if __name__ == '__main__':
    stack=Stack()
    stack.push('name')
    stack.push('age')
    stack.push('18')
    print(stack.size())
    print(stack.peek())
    print(stack.pop())
    
