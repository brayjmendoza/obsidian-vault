---
type: concept
created: 2026-11-23
updated: 2026-11-24
aliases:
  - Interface Testing
  - Writing Tests
  - Unit Testing
fields:
  - computer-science
confidence: 3
last_reviewed: 2026-11-23
sources:
  - "[[Data Structures & Program Development (HMC CS70)]]"
---
**Black-box testing** checks code only through its public interface, against what that interface promises, without depending on how the code is implemented.

The code under test is a box whose inside can't be seen, so its tests follow three rules:

1. **Use only the public interface.** A test calls the functions and operators the interface provides, and nothing private. All a test needs to know is what each of them promises to do, so the tests can be written before the code they test.
2. **Never break the language's rules.** A test must not cause [[Undefined Behavior|undefined behavior]] (e.g., calling a function with an argument its interface forbids), so it never tests what such code does: its result means nothing.
3. **Make no extra assumptions.** A test checks only what the interface specifies, not details that happen to hold in one implementation (e.g., the order a set returns its items in, when the interface doesn't promise one).

A test that follows these rules works for every correct implementation, not just the one its author wrote. A test that breaks them is likely to fail on some other implementation that is correct.

Beyond those rules, a test suite should help find *where* code is wrong, not just *that* it's wrong. So each test should be limited and focused: it tests a small set of new operations or cases, and otherwise uses only operations that earlier tests have already checked. Then the first failing test points to the operation at fault. Good tests also go looking for bugs: edge cases (e.g., an empty container, or one element), every case that triggers different behavior (e.g., each branch of an `if`), and mistakes other people would plausibly make.

More generally, the opposite approach is **white-box testing**, which uses knowledge of the implementation to choose tests (e.g., one test per branch in the code, measured as **code coverage**). A test of one small unit of code, such as a class or function, is a **unit test**, and writing the tests before the implementation is the core of test-driven development. As Edsger Dijkstra noted in 1970, testing can show that bugs are present, but never that they're absent.

# Examples

## Testing a Stack

A test for a stack checks what any stack promises: the last item pushed is the first popped (an example not from the source).

```c++
void testPushThenPop() {
    Stack s;
    s.push(1);
    s.push(2);
    assert(s.top() == 2);   // the last item pushed is on top
    s.pop();
    assert(s.top() == 1);
    s.pop();
    assert(s.empty());
}
```

It uses only `push`, `pop`, `top`, and `empty`, so it passes for a stack built on an array and one built on a linked list alike. It never calls `top` on an empty stack, which many stack interfaces forbid. A test that instead checked a private member, such as the size of the array underneath, would fail for the linked-list stack, though that stack is correct.

# Connections

- [[Undefined Behavior]]: tests must avoid it, since its outcome isn't defined
- [[Abstraction]]: an interface hides an implementation, and a black-box test respects what it hides
- [[Abstract Data Type]]: the interface a black-box test is written against
- [[Stack (Abstract Data Type)]]: the interface the example's tests are written against

# Sources

- [[Data Structures & Program Development (HMC CS70)]]

# Maps

![[Map.base#Maps]]
