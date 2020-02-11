# '''
# Linked List hash table key/value pair
# '''
class LinkedPair:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

class HashTable:
    '''
    A hash table with `capacity` buckets
    that accepts string keys
    '''
    def __init__(self, capacity):
        self.capacity = capacity  # Number of buckets in the hash table
        self.initial_capacity = capacity
        self.storage = [None] * capacity
        self.size = 0



    def _hash(self, key):
        '''
        Hash an arbitrary key and return an integer.

        You may replace the Python hash with DJB2 as a stretch goal.
        '''
        return hash(key)


    def _hash_djb2(self, key):
        '''
        Hash an arbitrary key using DJB2 hash

        OPTIONAL STRETCH: Research and implement DJB2
        '''
        hash_value = 5381
        for char in key:
            hash_value = ((hash_value << 5) + hash_value) + ord(char)
        return hash_value


    def _hash_mod(self, key):
        '''
        Take an arbitrary key and return a valid integer index
        within the storage capacity of the hash table.
        '''
        return self._hash_djb2(key) % self.capacity


    def insert(self, key, value):
        '''
        Store the value with the given key.

        Hash collisions should be handled with Linked List Chaining.
        '''
        index = self._hash_mod(key)
        node = self.storage[index]
        if node is None:
            self.storage[index] = LinkedPair(key, value)
            self.size += 1
        else:
            while node:
                if node.key == key:
                    node.value = value
                    return
                prev = node
                node = node.next
            prev.next = LinkedPair(key, value)
            self.size += 1
        
        if self.size / self.capacity > 0.7:
            self.resize()


    def remove(self, key):
        '''
        Remove the value stored with the given key.

        Print a warning if the key is not found.
        '''
        removed = False
        index = self._hash_mod(key)
        node = self.storage[index]
        prev = None
        while node:
            if node.key == key:
                if prev:
                    prev.next = node.next
                else:
                    self.storage[index] = node.next
                removed = True
                self.size -= 1
                break
            prev = node
            node = node.next
        if removed:
            if self.size / self.capacity < 0.2 and self.capacity > self.initial_capacity:
                self.resize(rate=0.5)
        else:
            print(f'Error: no entry for "{key}" was found.')


    def retrieve(self, key):
        '''
        Retrieve the value stored with the given key.

        Returns None if the key is not found.
        '''
        node = self.storage[self._hash_mod(key)]
        while node:
            if node.key == key:
                return node.value
            node = node.next
        return None


    def resize(self, rate=2):
        '''
        Double or halve the capacity of the
        hash table and rehash all key/value pairs.
        '''
        self.capacity = int(rate * self.capacity)
        self.size = 0
        old_storage = self.storage
        self.storage = [None] * self.capacity

        for node in old_storage:
            while node:
                self.insert(node.key, node.value)
                node = node.next


if __name__ == "__main__":
    ht = HashTable(2)

    ht.insert("line_1", "Tiny hash table")
    ht.insert("line_2", "Filled beyond capacity")
    ht.insert("line_3", "Linked list saves the day!")

    print("")

    # Test storing beyond capacity
    print(ht.retrieve("line_1"))
    print(ht.retrieve("line_2"))
    print(ht.retrieve("line_3"))

    # Test resizing
    old_capacity = len(ht.storage)
    ht.resize()
    new_capacity = len(ht.storage)

    print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    # Test if data intact after resizing
    print(ht.retrieve("line_1"))
    print(ht.retrieve("line_2"))
    print(ht.retrieve("line_3"))


    print("")
