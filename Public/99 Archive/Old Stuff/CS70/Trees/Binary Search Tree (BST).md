A binary tree such that
+ For any node, the key in that node is
    - Greater than all keys in the left subtree under that node
    - Less than all keys in the right subtree under that node

+ BST's can encode *maps* by storing both keys and its associated value in the node
+ BST's can encode *sets* by treating stored items as keys along with associated membership to avoid inserting duplicates

#### Lookup (exists)
Essentially binary search
+ If the node has the element we want, we're done
+ If the element is less than the item at the node, look in the left subtree
+ If the element is greater than the item at the node, look in the right subtree

+ Overall time complexity: $O(n)$ (more info below in the Time Complexity section)
#### Insert
***Pseudocode* (with recursion):**
BST-INSERT(_treenode_, _x_)**:**
    **if** there isn't a _treenode_ (i.e., this subtree is empty):    // base case
        replace empty subtree with new tree node containing _x_ as its value (and empty subtrees)
    **else if** _x_ < _treenode.value_**:**
        BST-INSERT(_treenode.leftSubtree_, _x_)        // recurse on smaller case (left subtree)
    **else:**    // _x_ >= _treenode.value_
        BST-INSERT(_treenode.rightSubtree_, _x_)     // recurse on smaller case (right subtree)

+ Overall time complexity is $O(n)$, same as lookup but with some additional operations that take $\Theta(1)$ time
#### Delete
There are three cases, when a node has:

**No Children:**
+ Simplest case, just remove the node

**One Child:**
+ Remove the node and move its child up to the deleted node's place

**Two Children:**
+ Once removing the node, we need to find a new parent that can correctly be a parent of to both of the removed node's children
	+ This node is always the rightmost left descendant (we could also use the leftmost right descendent)
		+ Both of these are the previous/next item if we were to sort all of the elements in the tree
		+ This node gets moved to the position the parent node was in

+ Overall time complexity is $O(n)$, same as lookup but with some additional operations that take $\Theta(1)$ time

#### Iterating over a BST
+ In-order traversal
	+ Traverse the BST in order from lowest value to highest value
	+ This is depth-first search

**Pseudocode:**
PRINT-IN-ORDER(_treenode_)
    **if** there is a _treenode_ (i.e., this subtree is not empty)
        PRINT-IN-ORDER(_treenode.leftSubtree_)   // Print the left subtree in order
        PRINT(_treenode_._key_)                               // Print the key in the root
        Print-In-Order(_treenode_._rightSubtree_)    // Print the right subtree in order
     // else, do nothing (base case)
#### Time Complexity
* **Perfectly balanced tree** - for any node, the left and right subtrees have exactly the same height
	* The shortest possible tree
	* Has height $\Theta(\log{n})$ (would take $\Theta(\log{n})$ operations to figure out the height)
	* Has lookup $O(\log{n})$
		* Best Case: $O(1)$
		* Worst Case: $O(\log{n})$
	* Has insert $O(\log{n})$
	* Has delete $O(\log{n})$
* **Stick** - All nodes are on the same subtree (e.g. all of the children are on the right and none are on the left)
	* The tallest possible tree
	* Essentially just a linked list
	* Has height $\Theta(n)$
	* Has lookup $O(n)$
		* Best Case: $O(1)$
		* Worst Case: $O(n)$
	* Has insert $O(n)$
	* Has delete $O(n)$
#### Example Tree
![[BSTExample.png]]

