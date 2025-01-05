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

    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

    def from_list(self, data_list):
        self.head = self.tail = None
        for data in data_list:
            self.append(data)

    def selection_sort(self, key=None):
        current = self.head
        while current:
            smallest = current
            check = current.next
            while check:
                if key:
                    if key(check.data) < key(smallest.data):
                        smallest = check
                else:
                    if check.data < smallest.data:
                        smallest = check
                check = check.next
            if smallest != current:
                current.data, smallest.data = smallest.data, current.data
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
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

    def display(self, level=0):
        print("  " * level + str(self.data))
        for child in self.children:
            child.display(level + 1)

class HierarchicalTree:
    def __init__(self, root_data):
        self.root = TreeNode(root_data)

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

# Sort the doubly linked list by consumption
print("\nDoubly Linked List After Sorting by Consumption:")
data_logs.selection_sort(key=lambda x: x["consumption"])
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

# 4. Hierarchical Tree for representing residential energy consumption hierarchy
hierarchy_tree = HierarchicalTree("Residential Energy Consumption")
daily_usage = TreeNode("Daily Usage")
daily_usage.add_child(TreeNode("2025-01-01: 30 kWh"))
daily_usage.add_child(TreeNode("2025-01-02: 25 kWh"))
daily_usage.add_child(TreeNode("2025-01-03: 28 kWh"))
hierarchy_tree.root.add_child(daily_usage)

monthly_usage = TreeNode("Monthly Usage")
monthly_usage.add_child(TreeNode("January: 850 kWh"))
monthly_usage.add_child(TreeNode("February: 780 kWh"))
hierarchy_tree.root.add_child(monthly_usage)

print("\nHierarchical Tree (Energy Consumption):")
hierarchy_tree.root.display()