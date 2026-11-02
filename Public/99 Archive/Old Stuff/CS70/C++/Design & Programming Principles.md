The creator of C++, Bjarne Stroustrup, wanted a language that was fast and could give him a lot of control
+ He needed this because he wanted to write code that would analyze the performance of the UNIX operating system

Stroustrup also wanted C++ to be an extension of C to ensure that he had a community of programmers who would be interested in using his language
+ Consequently, all valid C programs work in C++
+ C++ programs should be just as fast and use as little memory as equivalent C programs
+ Any additional features from C++ wouldn't affect a C program's efficiency

# Zero-Overhead Principle
What you don't use, you don't pay for (in time or space). Also, what you do use, you couldn't *hand code* any better
+ No feature should be added to C++ which would make existing code (not using the feature) larger/slower
+ No feature should be added where the compiler would generate code that's not as good as the programmer could make without using the feature

**Consequences:** C++ won't throw an error or tell you if you do something that could break something
+ If you break the rules, it results in *undefined behavior*
+ It's possible code that breaks the rules runs fine
+ Compilers or other tools may give warnings


# "Power to the People" Principle
C++ gives programmers a high level of control and trust

# The Principle of Ownership
This is the programming principle that anything on the heap has a single owner that's responsible for its lifetime (creation and destruction)
+ Helps prevent memory leaks and dangling pointers