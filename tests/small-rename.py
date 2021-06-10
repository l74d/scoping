import scoping
class VeryScoped(scoping.scoping): pass
del scoping

scoping = 2
with VeryScoped():
    assert(2 == scoping)
    scoping = 3
    keep = 'BB'
    VeryScoped.keep('keep')
    assert(3 == scoping)
assert(2 == scoping)
assert('BB' == keep)
