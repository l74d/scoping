# Probably the best way to simulate block scopes in Python.

This is a package, as it says on the tin, to emulate block scoping in Python, 
the lack of which being a clever design choice yet sometimes a trouble.

In addition to readability and code organization 
(where your mileage may vary),
block scoping in particular helps to have variables garbage collected as soon as possible, which is useful for situations where variables may refer to expensive resources (e.g. GPU arrays).

 This package is designed to be as easy to use as possible, with the least mental burden on the user,
 whilst the implementation being necessarily confusing and cryptic due to the tricks used.

## Usage

 Other than installing from PyPI the usual way,
you can also directly download scoping.py to where your main script is to use the package.

To start a scoped block (where the variables created in the block is to be deleted after the block) use
```python
    with scoping():
        #scoped code here........
```

Within a block, you can selectively let a variable leak through to the outer scope (as in the traditional behavior in Python) by passing the name (as a string) to

    scoping.keep()

If you are only after using the library, 
just consider scoping and scoping.keep as 
some kind of quasi-keywords rather than real classes/objects.

See 
```python
from scoping import scoping
a = 2
with scoping():
    assert(2 == a)
    a = 3
    b = 4
    scoping.keep('b')
    assert(3 == a)
assert(2 == a)
assert(4 == b)
```

In the rare case that you would like to reserve the word "scoping" for other uses, the class can be renamed arbitrarily using the following trick:

```python
import scoping
class VeryScoped(scoping.scoping): pass
del scoping
```

Then the names "VeryScoped" and "VeryScoped.keep" can be used instead,
whereas the name "scoping" can be put to other uses at will.

Blocks can be nested, as well as used in functions (unlike prior art),
at the price of relying on some CPython specific feature.

## Motivation/Prior Art

See https://github.com/bskinn/tempvars with a similar idea but not the intended use for general programming, as well as a more mentally demanding interface (IMHO).

## Compatibility

Tested with python 3.6/7/8/9 under Linux

