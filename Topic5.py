class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

    def remove(self, data):
        current = self.head
        while current:
            if current.data == data:
                if current.prev:
                    current.prev.next = current.next
                else:
                    self.head = current.next

                if current.next:
                    current.next.prev = current.prev
                else:
                    self.tail = current.prev
                return True
            current = current.next
        return False

    def display(self):
        current = self.head
        while current:
            print(current.data, end=' <-> ' if current.next else '\n')
            current = current.next

class CircularQueue:
    def __init__(self, size):
        self.size = size
        self.queue = [None] * size
        self.front = -1
        self.rear = -1

    def enqueue(self, data):
        if (self.rear + 1) % self.size == self.front:
            print("Queue is full")
            return False

        if self.front == -1:
            self.front = 0

        self.rear = (self.rear + 1) % self.size
        self.queue[self.rear] = data
        return True

    def dequeue(self):
        if self.front == -1:
            print("Queue is empty")
            return None

        data = self.queue[self.front]
        if self.front == self.rear:
            self.front = self.rear = -1
        else:
            self.front = (self.front + 1) % self.size
        return data

    def display(self):
        if self.front == -1:
            print("Queue is empty")
            return

        idx = self.front
        while True:
            print(self.queue[idx], end=' <- ' if (idx != self.rear) else '\n')
            if idx == self.rear:
                break
            idx = (idx + 1) % self.size

class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, data):
        self.items.append(data)

    def dequeue(self):
        if self.is_empty():
            print("Queue is empty")
            return None
        return self.items.pop(0)

    def is_empty(self):
        return len(self.items) == 0

    def display(self):
        print(" <- ".join(map(str, self.items)))

class TreeNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

class BinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, data):
        if not self.root:
            self.root = TreeNode(data)
        else:
            self._insert_recursive(self.root, data)

    def _insert_recursive(self, node, data):
        if data < node.data:
            if node.left is None:
                node.left = TreeNode(data)
            else:
                self._insert_recursive(node.left, data)
        else:
            if node.right is None:
                node.right = TreeNode(data)
            else:
                self._insert_recursive(node.right, data)

    def inorder_traversal(self):
        def _inorder(node):
            if node:
                _inorder(node.left)
                print(node.data, end=' ')
                _inorder(node.right)
        _inorder(self.root)
        print()

# Combined Example Usage

# 1. Doubly Linked List for dynamically tracking daily logs
data_logs = DoublyLinkedList()
data_logs.append({"date": "2025-01-01", "consumption": 30})
data_logs.append({"date": "2025-01-02", "consumption": 25})
data_logs.append({"date": "2025-01-03", "consumption": 28})
data_logs.append({"date": "2025-01-04", "consumption": 32})
print("Doubly Linked List (Daily Logs):")
data_logs.display()
data_logs.remove({"date": "2025-01-02", "consumption": 25})
print("After Removing a Log:")
data_logs.display()

# 2. Circular Queue for live sensor data
live_data = CircularQueue(5)
live_data.enqueue(35)
live_data.enqueue(40)
live_data.enqueue(45)
print("\nCircular Queue (Live Sensor Data):")
live_data.display()
live_data.dequeue()
print("After Dequeue:")
live_data.display()

# 3. Standard Queue for task processing
processing_queue = Queue()
processing_queue.enqueue("Analyze January data")
processing_queue.enqueue("Generate consumption report")
processing_queue.enqueue("Notify user about high usage")
print("\nStandard Queue (Task Processing):")
processing_queue.display()
processing_queue.dequeue()
print("After Dequeue:")
processing_queue.display()

# 4. Binary Tree for order management
order_tree = BinaryTree()
order_tree.insert("Order A: 50 units")
order_tree.insert("Order B: 30 units")
order_tree.insert("Order C: 70 units")
order_tree.insert("Order D: 20 units")
order_tree.insert("Order E: 40 units")
print("\nBinary Tree (Orders Inorder Traversal):")
order_tree.inorder_traversal()
