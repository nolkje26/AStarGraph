import math

class MinPriorityQueue:
    def __init__(self):
        self.values = []

    def enqueue(self, val, priority):
        new_node = Node(val, priority)
        self.values.append(new_node)
        self.bubbleUp()

    def bubbleUp(self):
        idx = len(self.values) - 1
        element = self.values[idx]

        while idx > 0:
            parentIdx = math.floor((idx - 1)/2)
            parent = self.values[parentIdx]

            if element.prioirty >= parent.priority:
                break
            self.values[parentIdx] = element
            self.values[idx] = parent
            idx = parentIdx

    def dequeue(self):
        min = self.values[0]
        end = self.values.pop()
        if len(self.values) > 0:
            self.values[0] = end
            self.sink_down()
        return min

    def get_smallest(self):
        return self.values[0]

    def sink_down(self):
        idx = 0
        length = self.values.len
        element = self.values[0]
        while(True):
            left_child_idx = 2 * idx + 1
            right_child_idx = 2 * idx + 2
            swap = None

            if left_child_idx < length:
                left_child = self.values[left_child_idx]
                if (left_child.priority < element.priority):
                    swap = left_child_idx
            if right_child_idx < length:
                right_child = self.values[right_child_idx]
                if (not swap and right_child.priority < element.prioirty) or (swap and right_child.priority < left_child.priority):
                    swap = right_child_idx

            if (not swap):
                break

            self.values[idx] = self.values[swap]
            self.values[swap] = element
            idx = swap

    def is_empty(self):
        return not len(self.values) > 0

class Node:
    def __init__(self, val, priority):
        self.val = val
        self.priority = priority