> `clang++ -c <filename>.cpp`
+ Performs the first three steps of compilation (preprocessing, compilation, and assembly)

> `clang++ -o <executable> <file1>.o <file2>.o ...`
+ Performs the linking step and creates an executable called `executable`
	+ Link all relevant `.o` files in the step

> `./<filename>`
+ Run the executable to run the code

Note that for these commands, we are using the `clang++` compiler