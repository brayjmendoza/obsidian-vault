![[TreeComparisons.png]]
![[TreeComparisons2.png]]
Other things to think about:
+ **Memory overhead**: Red–black trees need to store extra information in each node (color). Splay trees don't.
- **Time overhead**: Red–black trees only rotate some nodes on the path and only for insertion. Splay trees rotate all the way to root during both insertion and lookup.
- **Complicatedness**: Red–black trees have a reputation for being complicated to implement. Splay trees are considerably simpler.
- **Locality**: Red–black trees do _poorly_ when there is temporal locality. Splay trees do _best_ when there is temporal locality.