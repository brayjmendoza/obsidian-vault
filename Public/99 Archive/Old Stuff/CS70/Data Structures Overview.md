## Linear Data Structures 
Each of these are supported by array-backed lists or linked lists

- Stack
    - First-in, last-out.
    - Like (ideal) plane boarding: the first people to board are at the back, and therefore are also the last to leave.
- Queue
    - First-in, first-out.
    - Like a bank: first customer in line gets served first.
- Steque
    - Add to either end, take only from the front.
    - Like the milk refrigerator at the grocery store. Employees put milk in from the back. At the front, customers can take milk, and put it back if they change their minds.
- Deque
    - Add to and remove from either end.
    - Like a freight train: you can attach/detach cars on either end, but not in the middle.
- List
    - Stores items in a linear order. Allows access/insertion/removal at any position.
    - Like a… list of things.

## Associative Containers
Each of these are supported by BSTs or hash tables

- Set
    - Stores unique keys, not necessarily in any order.
    - Supports insert/lookup/remove of any key.
- Map
    - Associates unique keys with values (not necessarily unique).
    - Supports looking up the value associated with a key, and inserting/removing key/value pairs.
    - (Example: Python dictionary)
- Multiset
    - Pretty much like a set, but allows duplicate keys.
- Multimap
    - Pretty much like a map, but allows duplicate keys, each with their own value.