**Randomized trees** keep themselves balanced by _randomly_ selecting where along the path the new node should end up
+ At each point there's a chance we will insert at that location and it'll become the new root of the subtree and a chance that we will instead insert further down the tree
+ Simulates the process of shuffling keys by moving the randomness to insert
	+ This allows us to create a randomized BST without knowing all of the keys we are going to insert ahead of time

## Insertion
For a tree with $N$ nodes, the probability we insert a new key at the current node we're at is $\dfrac{1}{N+1}$
+ If we inserted, then the key we're inserting becomes the new root of the subtree
+ At this point we have $N+1$ total nodes (existing $N$ nodes and the node we're inserting)
	+ To simulate shuffling the keys, we can think that there is a $\dfrac{1}{N+1}$ chance that we inserted this value first for a normal BST
	+ $\dfrac{N}{N-1}$ chance that there value was NOT inserted first

#### Moving to Root
To insert a node and have it become a new root, we
+ Insert the node as a leaf as usual, then
+ Use tree rotations to move the node up to the root

## Complexity
+ Lookup/insert/remove: $O(n)$
	+ Best case: $\Theta(1)$
	+ Worst case: $\Theta(n)$
	+ But the worst case is extremely unlikely!
	+ We use expected time instead as it's not as misleading

+ Expected lookup time: $O(\log{n})$
+ Expected average depth: $\Theta(\log{n})$
	+ Same as average depth for a perfectly balanced tree

## Motivation
Consider a tree with 31 nodes. Now think about all the different possible ways the keys in this tree could have been inserted (which result in different possible tree shapes). Assuming a uniform probability distribution for key insertion, it is
+ Vastly unlikely that we'd get a stick
+ Vastly unlikely that we'd get a perfectly balanced tree
+ Likely that we will get a tree that is balanced *enough*
+ Average height is 8.174
	+ Perfect height is 4, so not too far off!
+ Standard deviation for height is 1.302

The order that we insert keys can influence the way the tree turns out. If the keys are not uniformly random, then it may be more likely we get something like a stick. So, by moving the randomization to insertion, we are effectively shuffling the keys we will insert into the tree before knowing what they are! Thus, we can expect randomized BST's to be balanced *enough* as it's vastly unlikely that we will get a very unbalanced tree.
+ The chance a randomized BST with 𝑛 nodes will be a stick is $\dfrac{2𝑛−1}{𝑛!}$
	+ It's much more likely a tree would turn out to be perfectly balanced