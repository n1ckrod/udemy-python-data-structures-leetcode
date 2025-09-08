from typing import Generic, TypeVar, Optional

T = TypeVar("T")

class Node(Generic[T]):
    def __init__(self, value: T):
        self.value: T = value
        self.next: Optional["Node[T]"] = None

class LinkedList(Generic[T]):
    def __init__(self, value: T):
        new_node = Node(value)
        self.head: Optional[Node[T]] = new_node
        self.tail: Optional[Node[T]] = new_node
        self.length: int = 1

    def print_list(self) -> None:               # Print Function - (-> None) like void in C++
        temp = self.head
        while temp is not None:
            print(temp.value)
            temp = temp.next

    def append(self, value: T) -> None:         # Append Function
        new_node = Node(value)
        if self.head is None:                   # empty List
            self.head = new_node
            self.tail = new_node
        else:
            assert self.tail is not None
            self.tail.next = new_node           # attach the tail
            self.tail = new_node
        self.length += 1

    def pop(self) -> Optional[Node[T]]:         # pop function
        if self.head is None:                   # nodes
            return None
        curr = self.head
        pre = self.head
        while curr.next is not None:            # > 2 nodes
            pre = curr
            curr = curr.next
        self.tail = pre
        assert self.tail is not None
        self.tail.next = None
        self.length -= 1
        if self.length == 0:                    # 1 node
            self.head = None
            self.tail = None
        return curr
    
    def prepend(self, value: T) -> None:        # prepend function
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head = new_node
        self.length += 1

    def pop_first(self) -> Optional[Node[T]]:   #pop_first
        if self.head is None:
            return None
        temp = self.head
        self.head = self.head.next
        temp.next = None
        self.length -= 1
        if self.length == 0:
            self.tail = None
        return temp
    
    def get(self, index: int) -> Optional[Node[T]]:
        if index < 0 or index >= self.length:
            return None
        temp = self.head
        for _ in range(index):                  # no variable inside the function so _
            assert temp is not None
            temp = temp.next
        return temp
    
    def set_value(self, index: int, value: T) -> bool:
        node = self.get(index)
        if node is not None:
            node.value = value
            return True
        return False
    
    def insert(self, index: int, value: T) -> bool:  #insert function
        if index < 0 or index > self.length:
            return False
        if index == 0:
            self.prepend(value)
            return True
        if index == self.length:
            self.append(value)
            return True
        prev = self.get(index - 1)
        if prev is None:
            return False
        new_node = Node(value)
        new_node.next = prev.next
        prev.next = new_node
        self.length += 1
        return True
    
    def remove(self, index: int) -> Optional[Node[T]]:   #remove function
        if index < 0 or index >= self.length:
            return None
        if index == 0:
            return self.pop_first()
        if index == self.length - 1:
            return self.pop()
        prev = self.get(index - 1)
        if prev is None or prev.next is None:
            return None
        temp = prev.next
        prev.next = temp.next
        temp.next = None
        self.length -= 1
        return temp
    
    def reverse(self) -> None:                      #reverse function
        if self.length <= 1:
            return
        prev: Optional[Node[T]] = None
        curr = self.head
        self.tail = self.head
        while curr is not None:
            after = curr.next
            curr.next = prev
            prev = curr
            curr = after
        self.head = prev

    def __len__(self) -> int:
        return self.length
    
    def __iter__(self):
        temp = self.head
        while temp is not None:
            yield temp.value
            temp = temp.next

    def __repr__(self) -> str:
        values = [str(v) for v in self]
        return "LinkedList([" + ", ".join(values) + "])"