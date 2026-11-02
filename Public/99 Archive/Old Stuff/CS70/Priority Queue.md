- Every item is inserted with an **ordered key** (e.g. a priority)
	- **Ordered keys** can be compared using `<` (most commonly numbers)
    - We can decide whether higher or lower values are more important.
- Main operations:
    - INSERT — Add a new item with a given key.
    - GET-MIN — Return the item with smallest key (equal keys come out in arbitrary order).
    - POP-MIN — Remove the item with the smallest key.
    - CHANGE-PRIORITY — changes the priority of an item already in the priority queue (and adjusts accordingly)
	    - $O(\log{n})$ complexity

#### Example
```c++
PriorityQueue pq;
pq.insert("First", 5); // Item, key
pq.insert("Second", 3);
pq.insert("Third", 10);

for (size_t i = 0; i < 3; ++i) {
    cout << pq.getMin() << " ";
    pq.popMin();
}
```
This outputs `Second First Third`

###  Example Applications
+ Shortest path problem
+ Huffman codes