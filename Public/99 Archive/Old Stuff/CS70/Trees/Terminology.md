+ **Node** - An element in a tree
+ **Edge** - A connection between two nodes
	+ Let's say that edge($A$,$B$) goes from node $A$ to node $B$.
+ **Parent/Child** -  In an edge($A$,$B$), $A$ is the parent (where the edge originates) and $B$ is the child (where the edge leads)
+ **Root** - The "top-most" node in a tree
	+ The node with no parent
+ **Leaf** - A node with no children
+ **Subtree** - A node in a tree and the tree rooted at that node 
	+ The node's children and their children etc.
+ **Height** - Length of the longest path from the root to a leaf
	+ A tree with one node has height 0
	+ An empty tree has height –1
+ **Binary Tree** 
	+ A tree in which every node has at most two children, a left child and a right child
	- The children are _ordered_. For a tree with only one child, it matters whether the child is on the left or the right
	- It can be defined recursively as either being an _empty_ tree, or a _node_ with left and right subtrees as children (either of which can be empty)
+ **Balanced Binary Tree**
	+ A tree where each node is balanced, which means that the heights of its left and right subtrees are similar

### Tree Rotations
Tree rotations rearrange a tree in a specific way. There are two main nodes involved:
+ The root of the tree (or subtree)
+ The node that will become the new root (one of the original root's children)
+ Both of these nodes have subtrees we also need to pay attention to

Rotations preserve the following properties of BSTs:
+ The old root becomes the child on the correct side of the new root.
- The subtree that lies “between” the old root and the new root remains “between” them.
- The subtrees all the way to the left and all the way to the right stay where they are

Rotations take constant time
##### Visual Diagram
![[TreeRotations.png]]