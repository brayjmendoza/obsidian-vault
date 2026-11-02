A **destructor** defines what happens to an instance of a class when it is destroyed.
+ The destructor is automatically called whenever an object goes into destruction phase

For a `Cow`, the destructor would look like:
> `~Cow();`

If we want the compiler to make it:
>`~Cow() = default;`
+ This synthesized destructor will destroy each member variable

Technically, you could use `delete`. However, this is a very bad idea. All classes *need* to have a destructor since everything will need to be destroyed at some point!

**When you have stuff on the heap**, the destructor is where you would `delete` everything so that there aren't any memory leaks
+ The synthesized destructor only destroys and deallocates member variables, so anything allocated on the heap from the class will be leaked if not properly `delete`d