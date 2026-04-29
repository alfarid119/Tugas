#implementasi stack dengan linhked list

#membuat kelas node
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class stack:
    def __init__(self):
        self.top = None
        self.size = 0

    def is_empty(self):
        if self.top is None:
            return True
        else:
            return False

    def push(self, data):
        new_node = Node(data)
        new_node.next = self.top
        self.top = new_node
        self.size += 1
        
    def pop(self):
        if self.top is None:
            return "Stack is empty"
        else:
            popped_data = self.top.data
            self.size -= 1
            self.top = self.top.next
            return popped_data

    def peek(self):
        if self.top is None:
            return "Stack is empty"
        else:
            return self.top.data

    def display(self):
        current = self.top
        while current:
            print(current.data)
            current = current.next

myStack = stack()
myStack.is_empty() # True
myStack.push(10)
myStack.push(20)
myStack.push(30)
myStack.display() # 30, 20, 10
print("Top element:", myStack.peek())
print(myStack.pop()) # 30
print(myStack.peek())
print(myStack.is_empty())
