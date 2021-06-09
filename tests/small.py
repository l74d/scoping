
from scoping import scoping
a = 2
with scoping(locals()):
    assert(2 == a)
    a = 3
    b = 'BB'
    scoping.keep('b')
    assert(3 == a)
assert(2 == a)
assert('BB' == b)
