## Make Changes to Variables with Functions:
We can use references to make changes to variables with functions
```
void spotTransplant(Cow donor, Cow recipient) {
    size_t donorSpots = donor.getNumSpots();
    size_t recipientSpots = recipient.getNumSpots();

    recipient.setNumSpots(donorSpots + recipientSpots);
    donor.setNumSpots(0);
}

int main() {
    Cow buttercup{1, 3}; // Cow(size_t numSpots, size_t age)
    Cow flopsy{2, 13};
    spotTransplant(flopsy, buttercup);

    cout << buttercup.getNumSpots() << " "
         << flopsy.getNumSpots();
}
```
Here, the output is "1 2" instead of "3 0" because when the function is called, a copy of the `Cow`s are made and used in `spotTransplant`'s stack frame. If we instead make the parameters references, then no copies would be made and we could modify the Cows that are passed in despite them being declared outside of the function's scope.
>`void spotTransplant(Cow& donor, Cow& recipient) {...}

## Multiple Return Values from One Function:
They can also be used to essentially get multiple return values from a function
```
void div(size_t a, size_t b, size_t& quo, size_t& rem)
{
    rem = a;
    quo = 0;
    while (rem >= b) {
        rem = rem - b;
        ++quo;
    }
}

int main() {
    size_t x = 24;
    size_t y = 7;
    size_t quotient;
    size_t remainder;
    div(x, y, quotient, remainder);
    cout << x << " " << y;
    cout << " " << quotient;
    cout << " " << remainder;
}
```
This prints "24 7 3 3". Here, `div` modified `quotient` and `remainder` (since references were used for them). We can then use continue to use these changed values throughout the program. Therefore, `div` essentially returned the quotient and remainder when evaluating `x / y` by modifying `quotient` and `remainder`.

## Prevent Unnecessary Copy Operations
Consider the following code with type `Elephant` which presumedly requires a lot of memory
```
bool isJuvenile(Elephant e) {
    return e.age() >= 5 && e.age() < 10;
}

int main() {
    Elephant nelly{"Nelly", 17, false, true};
    cout << isJuvenile(nelly) << endl;
}
```
This code is inefficient because we have two copies of the same elephant.

Instead,
> `bool isJuvenile(Elephant& e) {...}`

Creates a reference to the elephant, so we don't unnecessarily use memory