A splay tree is a binary search tree that does well when there is high temporal locality.
+ Check out this [splay tree visualizer](https://www.cs.usfca.edu/~galles/visualization/SplayTree.html)

### Insertion and Lookup
+ Splay trees first insert new keys as is typical for a BST
+ After insertion, a series of tree rotations are made so that the key that was just inserted becomes the root
	+ These rotations are known as the *splay operation*
+ If we lookup a value in the tree, that value then becomes the new root with splay operations

+ The big idea is that whenever a node is inserted _or_ is successfully found during a lookup, the splay operation moves that node to the root
	+ We expect recent nodes to be looked up again soon
	+ Allows splay trees to take advantage of temporal locality
		+ Looking up recently inserted or  found keys will take near best-case time!

### Splay Operations
For every insert/lookup, the inserted/found node is rotated up to the top
+ Splay trees also make use of *double rotations*
	+ When the node is the left child of a left child or the right child of a right child
	+ Allows for quicker movement up to the top
	+ This is critical for the amortized complexity guarantee of splay trees
#### Double Rotation Diagram
![[DoubleRotations.png]]
+ `Insert-at-root` makes use of single rotations to move the node up to the root
	+ Used in [[Randomized BST||randomized BSTs]]
+ The `splay operation` shows the double rotation

### Complexity
Insert and Lookup
+ $O(\log{n})$ [[Amortized Time||amortized time]]
+ For $n$ inserts, starting from an empty tree, it's $O(n\log{n})$
