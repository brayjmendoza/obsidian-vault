## General Rules
+ Tests must only use the public interface
	+ You should be able to write your tests before implementing the thing you are testing
	+ All you need to know are what each function/operator promises to do
	+ Tests should work for different implementations (not just your own)
	+ Testing functions also don't have access to the private interface
+ Tests *must not* break the rules
	+ We can't have undefined behavior!
		+ **Do not** test for undefined behavior
+ Tests must not making extra assumptions
	+ Can't test things specific to your implementation and aren't specified in the interface

+ If you don't follow these rules, it is highly likely that that your tests will fail for other correct implementations

## Practical Advice
+ Keep tests limited and focused
	+ Goal is to figure out what and *where* code is wrong
	+ **Rule of thumb:** try to arrange your tests so that each one tests a very limited set of new operations/cases, otherwise making use of things that have already been tested
+ Try to find ways to break your code and test them
	+ Edge cases
	+ Coverage
		+ Do different cases trigger different behavior (e.g. if statements)
	+ Catch bugs
	+ Imagine bugs other people may face