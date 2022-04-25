import math

class HeapNode:
    def __init__(self, key, value):
        self.key : float = key
        self.val : int = value
        self.marked : bool = False
        self.degree : int = 0
        self.parent : HeapNode = None
        self.child : HeapNode = None
        self.left : HeapNode = None
        self.right : HeapNode = None

# References: https://github.com/danielborowski/fibonacci-heap-python/blob/master/fib-heap.py#L36 for implementation, https://en.wikipedia.org/wiki/Fibonacci_heap & https://www.cs.princeton.edu/~wayne/cs423/fibonacci/FibonacciHeapAlgorithm.html for theory
class Heap:
    head : HeapNode = None
    min_node : HeapNode = None
    n : int = 0
    
    def iterate(self, head : HeapNode):
        """Returns an iterator for the circular linked list held in head"""
        node = head
        end = head

        ended = False

        while True:
            if node == end and ended is True:
                break
            elif node == end:
                ended = True
            yield node
            node = node.right

    def get_min(self) -> HeapNode:
        """Returns a reference to the node with the minimum key"""
        return self.min_node

    def extract_min(self) -> HeapNode:
        """Removes and returns a reference to the node with the minimum key"""
        z = self.min_node
        if z is not None:
            if z.child is not None:
                children = [x for x in self.iterate(z.child)]
                for i in range(len(children)):
                    self.merge_with_root_list(children[i])
                    children[i].parent = None
            self.remove_from_root_list(z)

            if z == z.right:
                self.min_node = self.head = None
            else:
                self.min_node = z.right
                self.consolidate()
            self.n -= 1
        return z


    def add_with_priority(self, key : float, value : int) -> HeapNode:
        """Inserts a new node into the tree and returns a reference to it"""
        new_node = HeapNode(key, value)
        new_node.left = new_node.right = new_node
        self.merge_with_root_list(new_node)
        
        if self.min_node is None or new_node.key < self.min_node.key:
            self.min_node = new_node
        
        self.n += 1
        return new_node

    def decrease_key(self, x : HeapNode, k : float):
        """Decreases the key/priority of a given node x to equal k"""
        if k > x.key:
            return None
        x.key = k
        y = x.parent
        if y is not None and x.key < y.key:
            self.cut(x, y)
            self.cascading_cut(y)
        if x.key < self.min_node.key:
            self.min_node = x

    def cut(self, x : HeapNode, y : HeapNode):
        """Cuts a child node x out from its level and hoists it up to the root or top level"""
        self.remove_from_child_list(y, x)
        y.degree -= 1
        self.merge_with_root_list(x)
        x.parent = None
        x.mark = False

    def cascading_cut(self, y : HeapNode):
        """Hoists the entire tree leading down to y to the root level recursively"""
        z = y.parent
        if z is not None:
            if y.mark is False:
                y.mark = True
            else:
                self.cut(y, z)
                self.cascading_cut(z)

    def consolidate(self):
        """Combines root nodes of equal degrees"""
        A = [None] * int(math.log(self.n) * 2)
        nodes = [w for w in self.iterate(self.head)]
        for w in range(0, len(nodes)):
            x = nodes[w]
            d = x.degree
            while A[d] != None:
                y = A[d]
                if x.key > y.key:
                    temp = x
                    x, y = y, temp
                self.heap_link(y, x)
                A[d] = None
                d += 1
            A[d] = x

        # Find new min node
        for i in range(0, len(A)):
            if A[i] is not None:
                if A[i].key < self.min_node.key:
                    self.min_node = A[i]

    def heap_link(self, y : HeapNode, x : HeapNode):
        """Links two nodes in the root list"""
        self.remove_from_root_list(y)
        y.left = y.right = y
        self.merge_with_child_list(x, y)
        x.degree += 1
        y.parent = x
        y.mark = False

    # merge a node with the doubly linked root list
    def merge_with_root_list(self, node : HeapNode):
        """Merges node node with the root list"""
        if self.head is None:
            self.head = node
        else:
            node.right = self.head.right
            node.left = self.head
            self.head.right.left = node
            self.head.right = node

    def merge_with_child_list(self, parent, node):
        """Merges node node with the child list of parent"""
        if parent.child is None:
            parent.child = node
        else:
            node.right = parent.child.right
            node.left = parent.child
            parent.child.right.left = node
            parent.child.right = node

    def remove_from_root_list(self, node):
        """Removes a node node from the root list"""
        if node == self.head:
            self.head = node.right
        node.left.right = node.right
        node.right.left = node.left

    def remove_from_child_list(self, parent, node):
        """Removes the node node from the child list of parent"""
        if parent.child == parent.child.right:
            parent.child = None
        elif parent.child == node:
            parent.child = node.right
            node.right.parent = parent
        node.left.right = node.right
        node.right.left = node.left