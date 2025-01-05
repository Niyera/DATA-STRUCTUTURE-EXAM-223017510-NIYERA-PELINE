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

# Example usage for the residential energy consumption tracker
# Doubly Linked List usage to track data logs
data_logs = DoublyLinkedList()
data_logs.append({"date": "2025-01-01", "consumption": 30})
data_logs.append({"date": "2025-01-02", "consumption": 25})
data_logs.append({"date": "2025-01-03", "consumption": 28})
data_logs.display()

# Circular Queue usage to track live sensor data
live_data = CircularQueue(5)
live_data.enqueue(35)
live_data.enqueue(40)
live_data.enqueue(45)
live_data.display()

live_data.dequeue()
live_data.display()