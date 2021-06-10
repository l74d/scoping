from scoping import scoping
#scoping.debugging = True
#scoping.settle(globals())
#a = 2
#with scoping(locals()):
#    assert(2 == a)
#    a = 3
#    b = 'BB'
#    scoping.keep('b')
#    assert(3 == a)
#assert(2 == a)
#assert('BB' == b)

A = 1

def test ():
    a = 10
    a = 20
    #import pdb; pdb.set_trace()
    with scoping():
        #import pdb; pdb.set_trace()
        assert(20 == a)
        a = 3
        b = 'BB'
        A = 5
        scoping.keep('b')
        assert(3 == a)
    assert('A' not in locals())
    #import pdb; pdb.set_trace()
    assert(20 == a)
    assert('BB' == b)

test()
