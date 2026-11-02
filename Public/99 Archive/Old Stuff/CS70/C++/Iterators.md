An iterator is **an object that represents the location of one item in a collection of items** (such as a list)
+ The iterator can be moved around to visit and access all items in the collection

### Abstract Definition
All iterators (no matter what programming language) need to support the following operations:
+ BEGIN(_data_): initializes an iterator to some starting point in _data_
+ NEXT(_iter_): move the iterator forward through the data structure
+ FETCH(_iter_): access the piece of data the iterator is currently referring to
+ IS-DONE(_iter_): determine whether the iterator has reached its end point

### Concrete Example: C++
For C++, an iterator is any type that supports the following loop:
```
for (auto i = start_point; i != past_the_end_point; ++i) {
    ... *i ...
}
```
+ Pointers are a kind of iterator (used as iterators for arrays)
+ Not all iterators are pointers and refer to an array of elements (think linked lists and trees)

So
+ Iterators need to be initialized to some starting point
	+ `begin()` provides this value
+ `++` moves the iterator forward through the data structure
+ `*` accesses the element the iterator is currently referring to
+ `!=` is used to see if we've run off the end and should stop
	+ Needs a "past-the-end" value to compare against (provided by `end()`)
+ Iterators also typically support `==` and `->`

### Read-only Iterators
Say we want to iterate on a list that is read only.
+ We can't use a `const` iterator (e.g. `const std::list<double>::iterator`)
	+ We can't change a `const` iterator! (we won't be able to do pointer math to change what value the iterator is referencing)

**C++ Solution:** provide an almost identical class that returns a `const` reference when using `*`
+ `std::list<double>::iterator` is an iterator that lets you write the data (and read it, too).
- `std::list<double>::const_iterator` is an iterator that only lets you read the data.
	- `auto` is able to determine which of these to use!

### Iterator Functionality (C++)
+ `begin` - returns an iterator to the first item
+ `end` - returns an iterator "one past" the last item
+ It must be the case that
	+ If `i` is an iterator to the last item in `c`, then `++i == c.end()`
	- A container `c` is empty if and only if `c.begin() == c.end()`
- `*iter` - returns a reference to the item at the iterator's location
- `++iter` - advances the iterator to the next location.
- `iter != otherIter` - returns true if the two iterators are not at the same location

### Iterator Rules
You *must* follow the following iterator rules in C++ or else you will get undefined behavior:
- Don't use `*` on a past-the-end iterator
- Don't use `++` on a past-the-end iterator (you can't move “beyond past-the-end”)
- Don't use `--` on an iterator at the beginning (no such thing as a before-the-beginning iterator)
- Don't compare iterators that have different origins
	- If you have two lists, you aren't allowed to compare iterators between those lists, only iterators within _the same_ list
- Don't do anything to an iterator that isn't valid other than destroy it or assign a new value to it.

### Iterator Validity
An iterator is **invalid** when we can no longer use them (i.e. doing so would break iterator rules)
+ If a container is destroyed, all of its iterators cease to be valid.
+ We can pass an iterator into the `erase` function to remove an item from the list.
	- When `erase` returns,  the passed iterator no longer refers to accessible data
		- This passed-in iterator is no longer valid
		- Any other iterators pointing to that location can also no longer give access to that item, so all of them are now invalid, too
	- **Bonus note:** In the C++ standard library, `erase` typically _returns an iterator_; specifically, an iterator to the item that _would have been next_ before `erase` was called. 
		- `iter = l.erase(iter);` erases an item, and sets `iter` to the next item so that it's still valid

For array-backed lists
 + Resizing invalidates all iterators referring to the list because resizing could cause all the data to be relocated to a new array (that the iterator doesn't refer to)
+ Adding or removing something from the list invalidates iterators for the same reason as above
+ **Note:** For linked lists, insertions don't affect validity because the underlying nodes are unaffected