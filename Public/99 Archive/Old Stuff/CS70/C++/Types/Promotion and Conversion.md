An `int` plus an `int` makes an `int`
+ Same is true with all other numeric types

# Promotion
Involves *different sizes* of the same type
##### Example:
+ Assuming a `long` is bigger than an `int`, what happens if we add an `int` and a `long`?
	+ The `int` gets widened to be a `long` before the addition occurs
		+ The final sum ends up being a `long`
	+ This widening is called a *promotion*
+ What if we had an `unsigned int` and `long`
	+ The `unsigned int` gets promoted for as long as it's smaller than a long
	+ This is because the range of an `unsigned int` is entirely within the range of a `long`

C++ performs promotions automatically
**Rules for Promotion:**
- The types must be of the same kind (integer to integer or floating point to floating point)
- The range of the type being promoted *to* must completely include the range of the type being promoted *from*
- Thus, **A promotion can never cause information to be lost**

##### Example: Promotion when Initializing new Variables
```
short weekDay = 3;
int yearStart = weekDay;
```
Here, `weekDay` gets promoted to an `int`

#### Explicit Promotions
```
signed char dollar = 36;
std::cout << "Printed as a character " << dollar << std::endl
          << "Printed as an integer  " << int(dollar) << std::endl;
```
prints
```
Printed as a character $
Printed as an integer  36
```
Here, `dollar` was promoted from a `char` to an `int`
Note that we use the same syntax for conversions
## Conversion
Any other kind of conversion between numeric types that's not a promotion

More specifically, if we move a numeric value between types it's a *conversion*.
##### Example:
```
double usPopulation = 336858333;
int thisWeeksGain   = 36538;
std::cout << "US population is now "
          << usPopulation + thisWeeksGain
          << std::endl;
```
Here, C++ choses to convert the sum to a `double`

**IMPORTANT: *Conversions can potentially lose information***
If we run
```
long worldPop = 7960583250;
std::cout << "World pop as long " << worldPop << std::endl
          << "----------> float " << float(worldPop) << std::endl
          << "-----------> long " << long(float(worldPop)) << std::endl;
```
it prints
```
World pop as long 7960583250
----------> float 7.96058e+09
-----------> long 7960583168
```
Which shows that we lost 82 people!

## Conversion Rules:
+ Promotions and Conversions usually happen automatically
	+ e.g. when we call a function that wants a different type from what we're providing
+ Changing any type of integer to a type of float is *always* a conversion
+ Changing to a smaller incarnation of the basic type is a conversion
	+ e.g. `int` $\to$ `short int` or `double` $\to$ `float`
+ Signed $\to$ unsigned is *always* a conversion
+ Unsigned $\to$ signed is *usually* a conversion 
	+ It's a promotion if the signed type is larger (rare)