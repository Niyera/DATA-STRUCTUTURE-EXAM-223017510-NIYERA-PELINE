from dataclasses import dataclass
from typing import Optional, Any, List, Queue
from datetime import datetime
from collections import deque
from enum import Enum
from queue import Queue as ProcessingQueue

class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class EnergyReading:
    timestamp: datetime
    consumption: float  # in kWh
    device_id: str
    reading_type: str  # e.g., "peak", "off-peak"
    priority: Priority = Priority.MEDIUM

    def __lt__(self, other):
        return self.priority.value < other.priority.value

@dataclass
class ProcessingTask:
    reading: EnergyReading
    task_type: str
    status: str = "pending"
    processed_timestamp: Optional[datetime] = None

class EnergyProcessingQueue:
    def __init__(self):
        self.tasks = ProcessingQueue()
        self.processing_history = []
        
    def enqueue_task(self, reading: EnergyReading, task_type: str) -> None:
        """Add a new processing task to the queue."""
        task = ProcessingTask(reading, task_type)
        self.tasks.put(task)
        
    def process_next_task(self) -> Optional[ProcessingTask]:
        """Process the next task in the queue."""
        if self.tasks.empty():
            return None
            
        task = self.tasks.get()
        task.status = "processed"
        task.processed_timestamp = datetime.now()
        self.processing_history.append(task)
        return task
        
    def get_pending_tasks_count(self) -> int:
        """Get count of pending tasks."""
        return self.tasks.qsize()
        
    def get_processing_history(self) -> List[ProcessingTask]:
        """Get list of processed tasks."""
        return self.processing_history

class SelectionSortManager:
    @staticmethod
    def selection_sort_readings(readings: List[EnergyReading]) -> List[EnergyReading]:
        """Sort energy readings using selection sort based on priority."""
        n = len(readings)
        for i in range(n):
            max_idx = i
            for j in range(i + 1, n):
                if readings[j].priority.value > readings[max_idx].priority.value:
                    max_idx = j
            readings[i], readings[max_idx] = readings[max_idx], readings[i]
        return readings

class DoublyLinkedNode:
    def __init__(self, reading: EnergyReading):
        self.reading = reading
        self.next: Optional[DoublyLinkedNode] = None
        self.prev: Optional[DoublyLinkedNode] = None

class EnergyTreeNode:
    def __init__(self, name: str, parent_id: Optional[str] = None):
        self.node_id = name
        self.parent_id = parent_id
        self.name = name
        self.children: List[EnergyTreeNode] = []
        self.readings: List[EnergyReading] = []
        self.total_consumption = 0.0
        self.processing_queue = EnergyProcessingQueue()

    def add_child(self, child: 'EnergyTreeNode') -> None:
        self.children.append(child)

    def add_reading(self, reading: EnergyReading) -> None:
        self.readings.append(reading)
        self.total_consumption += reading.consumption
        # Queue reading for processing
        self.processing_queue.enqueue_task(reading, "consumption_analysis")

    def process_pending_readings(self) -> List[ProcessingTask]:
        """Process all pending readings in the queue."""
        processed_tasks = []
        while self.processing_queue.get_pending_tasks_count() > 0:
            task = self.processing_queue.process_next_task()
            if task:
                processed_tasks.append(task)
        return processed_tasks

class EnergyHierarchyTree:
    def __init__(self):
        self.root = EnergyTreeNode("Building")
        self.node_map = {"Building": self.root}

    def add_zone(self, zone_name: str, parent_name: str) -> bool:
        if parent_name not in self.node_map:
            return False
            
        parent_node = self.node_map[parent_name]
        new_node = EnergyTreeNode(zone_name, parent_name)
        parent_node.add_child(new_node)
        self.node_map[zone_name] = new_node
        return True

    def process_zone_readings(self, zone_name: str) -> List[ProcessingTask]:
        """Process readings for a specific zone."""
        if zone_name not in self.node_map:
            return []
        return self.node_map[zone_name].process_pending_readings()

class EnergyConsumptionList:
    def __init__(self):
        self.head: Optional[DoublyLinkedNode] = None
        self.tail: Optional[DoublyLinkedNode] = None
        self.size = 0
        self.processing_queue = EnergyProcessingQueue()

    def add_reading(self, reading: EnergyReading) -> None:
        new_node = DoublyLinkedNode(reading)
        
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        
        self.size += 1
        # Queue reading for processing
        self.processing_queue.enqueue_task(reading, "historical_analysis")

class CircularEnergyQueue:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.queue = [None] * capacity
        self.front = 0
        self.rear = -1
        self.size = 0
        self.processing_queue = EnergyProcessingQueue()

    def enqueue(self, reading: EnergyReading) -> bool:
        if self.is_full():
            return False
            
        self.rear = (self.rear + 1) % self.capacity
        self.queue[self.rear] = reading
        self.size += 1
        # Queue reading for processing
        self.processing_queue.enqueue_task(reading, "recent_analysis")
        return True

    def is_full(self) -> bool:
        return self.size == self.capacity

    def is_empty(self) -> bool:
        return self.size == 0

class EnergyTrackingSystem:
    def __init__(self, recent_readings_capacity: int = 24):
        self.hierarchy = EnergyHierarchyTree()
        self.history = EnergyConsumptionList()
        self.recent = CircularEnergyQueue(recent_readings_capacity)
        self.main_processing_queue = EnergyProcessingQueue()

    def add_reading(self, reading: EnergyReading, zone_name: str) -> bool:
        """Add a reading to all data structures and queue for processing."""
        if not self.hierarchy.add_reading_to_zone(zone_name, reading):
            return False

        self.history.add_reading(reading)
        self.recent.enqueue(reading)
        self.main_processing_queue.enqueue_task(reading, "system_analysis")
        return True

    def process_all_pending(self) -> dict:
        """Process all pending tasks across the system."""
        results = {
            'system': [],
            'zones': {},
        }
        
        # Process main system queue
        while self.main_processing_queue.get_pending_tasks_count() > 0:
            task = self.main_processing_queue.process_next_task()
            if task:
                results['system'].append(task)
        
        # Process zone-specific queues
        for zone_name in self.hierarchy.node_map:
            processed = self.hierarchy.process_zone_readings(zone_name)
            if processed:
                results['zones'][zone_name] = processed
        
        return results

# Example usage and testing
def main():
    # Initialize system
    system = EnergyTrackingSystem()
    
    # Set up building hierarchy
    system.hierarchy.add_zone("Floor 1", "Building")
    system.hierarchy.add_zone("Room 101", "Floor 1")
    
    # Create and add readings
    readings = [
        EnergyReading(
            timestamp=datetime.now(),
            consumption=2.5,
            device_id=f"device_{i}",
            reading_type="peak",
            priority=Priority.MEDIUM
        )
        for i in range(3)
    ]
    
    # Add readings to system
    for reading in readings:
        system.add_reading(reading, "Room 101")
    
    # Process all pending tasks
    processing_results = system.process_all_pending()
    
    # Print processing results
    print("\nProcessing Results:")
    print(f"System tasks processed: {len(processing_results['system'])}")
    for zone, tasks in processing_results['zones'].items():
        print(f"Zone '{zone}' tasks processed: {len(tasks)}")

if __name__ == "__main__":
    main()