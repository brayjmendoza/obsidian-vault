Self-balancing trees demand that they are balanced. There are two main self-balancing trees: 2-3-4 Trees and Red-Black Trees
## 2-3-4 Tree
A 2-3-4 tree demands that it is balanced. To do so, it has 3 different node types
#### Node Types
**2-Node**:
+ A normal node like we would find in a BST
+ Stores a value (we'll call it *key*) and has two children (or none)
	+ Left subtrees holds values that are less than *key*
	+ Right subtree holds values that are greater than *key*

**3-Node:**
+ Expands on the 2-node by allowing for a second value to be stored in it (so we have values *key1* and *key2*)
+ Has three children
	- The left subtree holds values that are less than _key1_
	- The middle subtree holds values that are between _key1_ and _key2_
	- The right subtree holds values that are greater than _key2_

**4-Node**:
+ Expands on the 3-node by allowing for a third value to be stored in it (we'll call these values *key1*, *key2*, and *key3*)
+ Has four children
	+ The left subtree holds values that are less than _key1_
	- The next subtree holds values that are between _key1_ and _key2_
	- The third subtree holds values that are between _key2_ and _key3_
	- The right subtree holds values that are greater than _key3_

##### Diagram of Node Types
![[234TreeNodes.png]]

#### Insert
Similar to insert for a BST, but when we encounter a 2- or 3-node, we insert the value into that node (resulting in a 3- or 4-node respectively)
+ Note that the leftmost value in a node is the smallest, and the rightmost is the largest
+ Whenever we encounter a 4-node, we promote the middle value
	+ This middle value can be a parent for the other two values!
	+ This middle value joins the layer above (if there is one)

#### Time Complexity:
+ Lookup and insert
	+ Best case: $\Theta(1)$
	+ Worst Case: $\Theta(\log{n})$
	+ Overall: $O(\log{n})$
	+ For insertion, inserting the key takes constant time, so the time complexity of insert is the same as lookup

#### Converting 2-3-4 Trees to Binary Trees
+To implement 2-3-4 trees, we can "binarize" it in order to more easily operate with the different nodes
###### Converting 4-Nodes to Mini-Trees:
+ Anywhere we have a four-node in a 2–3–4 tree, we could draw an equivalent binary tree where the 4-node is broken up into three BST nodes
+ This is the same as when we promote 4-nodes during insertion

We could convert
![[Binarize4Node1.png]]
to
![[Binarize4Node2.png]]
+ Note that the edges between the nodes that were originally part of the 4-node are marked (bright red and thicker)
	+ We call these edges "super edges"
	+ Remembering which edges belong to the node allow us to easily convert back to the 2-3-4 tree

###### Converting 3-Nodes to Mini-Trees
Similar to the 4-node, but we have a choice of how we can break up the node.
We can go from this
![[3NodeBinarize1.png]]
to either![[3NodeBinarize2.png]]
+ Note again that we mark the super edges so we know how to reconstruct the original 2-3-4 tree

Though this "binarization" of the nodes makes it so the 2-3-4 tree in practice isn't perfectly balanced, it turns out that it's height is still $\Theta(\log{n})$, so we call it balanced.

## Red-Black Tree
A red-black tree is a binary representation of a 2-3-4 tree
+ Instead of coloring the super edges red, we can move this coloring to the nodes
	+ Red nodes represent nodes that are part of a 3- or 4- node
	+ Black nodes represent the "parent" node of the larger 2-, 3-, or 4-node

	+ Red nodes are those with a super edge pointing into it (the big red edges from the 2-3-4 tree diagrams above)
	+ Black nodes are those without a super edge pointing into it
#### Insert
Insertion involves traveling down the tree to a leaf (like a normal BST) and along the way:
+ Possibly performing a rotation
	+ Ensures that each 4-node always has the proper shape with two a red node on both sides
+ Possibly changing some node colors
	+ Correspond to promotions in the corresponding 2-3-4 tree
###### Example:
Consider the red-black tree with the black node 50 and red node 40 (This corresponds to a 2-3-4 tree that contains a singular 3-node)
+ Let's insert 30
	+ 30 goes in the left subtree of 40
	+ 40 becomes the new black node and 30 and 50 become red nodes 
![[RedBlackTreeInsert.png]]
We started with a 3-node containing 40 and 50 and ended up with a 4-node containing 30, 40, and 50.
+ Some nodes changed colors 
+ Edges were rewired (through a [[Public/99 Archive/Old Stuff/CS70/Trees/Terminology|tree rotation]])


#### Time Complexity
Same as 2-3-4 Trees
+ Lookup and insert
	+ Best case: $\Theta(1)$
	+ Worst Case: $\Theta(\log{n})$
	+ Overall: $O(\log{n})$

#### Rules
+ No adjacent red nodes
+ The root is always black
+ Every path from the root to a leaf goes through the same number of black nodes

## Additional Notes
+ Red-black trees are commonly used to implement C++'s `std::map` and `std::set`
+ [Completely Fair Scheduling](https://en.wikipedia.org/wiki/Completely_Fair_Scheduler)
+ 