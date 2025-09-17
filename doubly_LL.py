from typing import Generic, TypeVar, Optional, Iterator, Iterable

T = TypeVar("T")

class DNode(Generic[T]):
    def __init__(self, value: T):
        self.value: T = value
        self.prev: Optional["DNode[T]"] = None
        self.next: Optional["DNode[T]"] = None

class DoublyLinkedList(Generic[T]):
    def __init__(self, iterable: Optional[Iterable[T]] = None):
        self.head: Optional[DNode[T]] = None
        self.tail: Optional[DNode[T]] = None
        self.length: int = 0
        if iterable:
            for x in iterable:
                self.append(x)

    @classmethod
    def from_iterable(cls, it: Iterable[T]) -> "DoublyLinkedList[T]":
        lst = cls()
        for x in it:
            lst.append(x)
        return lst

    def append(self, value: T) -> None:
        new_node = DNode(value)
        if self.head is None:               # empty list
            self.head = new_node
            self.tail = new_node
        else:
            assert self.tail is not None
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self.length += 1


    def pop(self) -> Optional[DNode[T]]:
        if self.head is None:               # no nodes
            return None
        assert self.tail is not None
        temp = self.tail
        if self.length == 1:                # one node
            self.head = None
            self.tail = None
        else:
            self.tail = temp.prev
            assert self.tail is not None
            self.tail.next = None
            temp.prev = None
        self.length -= 1
        return temp


    def prepend(self, value: T) -> None:
        new_node = DNode(value)
        if self.head is None:               # empty list
            self.head = new_node
            self.tail = new_node
        else:
            assert self.head is not None
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self.length += 1
    
    def pop_first(self) -> Optional[DNode[T]]:
        if self.head is None:
            return None
        temp = self.head
        if self.length == 1:
            self.head = None
            self.tail = None
        else:
            assert temp.next is not None
            self.head = temp.next
            self.head.prev = None
            temp.next = None
        self.length -= 1
        return temp

    def get(self, index: int) -> Optional[DNode[T]]:
        if index < 0 or index >= self.length:
            return None
        # Bidirectional traversal optimization
        if index < self.length // 2:
            temp = self.head
            for _ in range(index):
                assert temp is not None
                temp = temp.next
            return temp
        else:
            temp = self.tail
            for _ in range(self.length - 1, index, -1):
                assert temp is not None
                temp = temp.prev
            return temp
    
    def set_value(self, index: int, value: T) -> bool:
        node = self.get(index)
        if node is not None:
            node.value = value
            return True
        return False
        
    def insert(self, index: int, value: T) -> bool:
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

        new_node = DNode(value)
        nxt = prev.next

        # Link new_node between prev and nxt
        new_node.prev = prev
        new_node.next = nxt
        prev.next = new_node
        if nxt is not None:
            nxt.prev = new_node
        else:
            # inserting at tail 
            self.tail = new_node

        self.length += 1
        return True
    
    def remove(self, index: int) -> Optional[DNode[T]]:
        if index < 0 or index >= self.length:
            return None
        if index == 0:
            return self.pop_first()
        if index == self.length - 1:
            return self.pop()

        temp = self.get(index)
        if temp is None:
            return None

        assert temp.prev is not None
        assert temp.next is not None

        temp.prev.next = temp.next
        temp.next.prev = temp.prev

        temp.prev = None
        temp.next = None
        self.length -= 1
        return temp
    
    # helper methods

    def __len__(self) -> int: return self.length

    def __iter__(self) -> Iterator[T]:
        cur = self.head
        while cur:
            yield cur.value
            cur = cur.next

    def __repr__(self):
        return f"DoublyLinkedList([{', '.join(repr(x) for x in self)}])"

    def __getitem__(self, index: int) -> T:
        node = self.get(index)
        if node is None: raise IndexError("list index out of range")
        return node.value

    def __setitem__(self, index: int, value: T) -> None:
        if not self.set_value(index, value): raise IndexError("list index out of range")
