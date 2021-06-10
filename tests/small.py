from scoping import scoping
#scoping.settle(globals())

a = 2
with scoping():
    assert(2 == a)
    a = 3
    b = 'BB'
    scoping.keep('b')
    assert(3 == a)
assert(2 == a)
assert('BB' == b)
