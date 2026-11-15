---
type: concept
created: 2026-11-15
updated: 2026-11-15
aliases:
  - Covariance
  - Contravariance
  - Variance
  - Function Subtyping
fields:
  - computer-science
confidence: 2
last_reviewed: 2026-11-15
sources:
  - "[[Programming Languages (HMC CS131)]]"
---
A compound type is **covariant** in a part when the subtyping of that part carries over in the same direction, and **contravariant** when it carries over reversed.

Pairs and lists are covariant: if `int` ⊑ `double`, then `[int]` ⊑ `[double]`, and a pair is a subtype of another pair when each component is (see [[Subtyping]]). Function types are the interesting case. A function type $t_1 \to t_2$ is a subtype of $t_3 \to t_4$ when:

- **The result is covariant:** $t_2 \sqsubseteq t_4$. The function may return something more specific than promised.
- **The argument is contravariant:** $t_3 \sqsubseteq t_1$. The function must accept everything the caller might pass, so it may accept something more general, never less.

$$
\frac{t_3 \sqsubseteq t_1 \qquad t_2 \sqsubseteq t_4}{t_1 \to t_2 \;\sqsubseteq\; t_3 \to t_4}
$$

The substitutability test explains it. Picture a factory between a farm and a shop, where a function is "turn what the farm sends into what the shop sells," and ask whether a received factory can replace the expected one:

| Expected | Received | Works? | Why |
|---|---|---|---|
| `apple → dessert` | `apple → pie` | Yes | Pie is a dessert |
| `apple → dessert` | `fruit → dessert` | Yes | It takes any fruit, so apples are fine |
| `apple → dessert` | `fruit → pie` | Yes | Both of the above |
| `fruit → dessert` | `apple → pie` | No | The farm may send fruit that isn't apples |
| `fruit → pie` | `fruit → dessert` | No | Not every dessert is a pie |

More generally, variance is everywhere that subtyping meets generics. Java's arrays are covariant, which is unsound for writing: storing a `double` into an array that's really an `int[]` fails at run time. Java's generics are invariant by default, with wildcards (`? extends`, `? super`) to choose a direction, and C# and Kotlin mark it with `out` and `in`. A mutable container has to be **invariant**, since reading from it wants covariance and writing to it wants contravariance.

# Example

The rule applied, with `apple` ⊑ `fruit` and `pie` ⊑ `dessert`:

$$
\frac{\text{apple} \sqsubseteq \text{fruit} \qquad \text{pie} \sqsubseteq \text{dessert}}{\text{fruit} \to \text{pie} \;\sqsubseteq\; \text{apple} \to \text{dessert}}
$$

A `fruit → pie` function can be used wherever an `apple → dessert` function is expected.

# Connections

- [[Subtyping]]: variance describes how subtyping extends to compound types
- [[Typing Rule]]: the function rule is a subtyping rule in inference-rule form
- [[Parametric Polymorphism]]: generics are where variance matters in practice

# Sources

- [[Programming Languages (HMC CS131)]]

# Maps

![[Map.base#Maps]]
