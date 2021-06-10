import scoping
class VeryScoped(scoping.scoping): pass
del scoping

a = 2
with VeryScoped():
    assert(2 == a)
    a = 3
    b = 'BB'
    VeryScoped.keep('b')
    assert(3 == a)
assert(2 == a)
assert('BB' == b)
