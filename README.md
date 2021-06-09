# Scoping
Probably the best way to create Python block scopes.

## Usage

Simply download scoping.py to use the package

    from scoping import scoping
    a = 2
    with scoping(locals()):
        assert(2 == a)
        a = 3
        b = 4
        scoping.keep('b')
        assert(3 == a)
    assert(2 == a)
    assert(4 == b)



## Motivation/Prior Art

See https://github.com/bskinn/tempvars

## Compatibility

Tested with python 3.6/7/8/9 under Linux

