from scoping import scoping
#scoping.preserving = 1
#scoping.test = scoping.test_all_except_builtin
scoping.debugging = True
import torch
a = 2
t = torch.ones(1000,1000).cuda()
print(torch.cuda.memory_allocated())
print(dir())
print('[[[[[[[')
bbb = 5
with scoping(locals(),'bbb','ccc'):
    bbb = ccc = 99
    a = 3
    print(a)
    t *= 10
    print(t.mean())
    t = torch.ones(1000,1000).cuda()
    t *= -5
    print(t.mean())
    print(torch.cuda.memory_allocated())
    zzz = torch.ones(1000,1000).cuda()
    print(torch.cuda.memory_allocated())
    qqq = torch.ones(1000,500).cuda()
    print(torch.cuda.memory_allocated())
    scoping.keep('qqq')#(qqq)
    qqq = ()
    dddd = 99999
    scoping.keep('dddd')#(dddd)
    ggg = 54321
    with scoping(locals()):
        print('<<<<<<')
        eee = 123
        fff = 456
        ggg = 12345
        ggg2 = 5555
        ggg1 = 5555
        print('id(ggg1)',id(ggg1))
        print('id(ggg2)',id(ggg2))
        #id(ggg1) == id(ggg2) in script mode
        scoping.keep('fff','ggg','ggg1','ggg2')#(fff,ggg,ggg1,ggg2)
        del ggg1
        ggg11 = 5555
        print(id(ggg11))
        ggg2 = 3333
        dddd = 987654321
        print(dir())
        print('>>>>>>')
    print(dir())
    assert('eee' not in locals())
    assert('ggg1' not in locals())
    assert('ggg11' not in locals())
    #assert('ggg2' not in locals())
    assert('ggg2' in locals())
    assert(fff == 456)
    #assert(ggg == 54321)
    assert(ggg == 12345)
    assert(dddd == 99999)
    print(']]]]]]]')

print(dir())
assert('fff' not in locals())
assert('ggg' not in locals())
assert(dddd == 99999)
assert(bbb == ccc == 99)
assert(a == 2)
print(a,bbb,ccc,dddd)
print(torch.cuda.memory_allocated())
print(t.mean())
del t
print(torch.cuda.memory_allocated())

