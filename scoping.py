class scoping(object):
    #compose tests to whitelist some variables?
    def test_math_style_0(k):
        import re
        return bool(re.fullmatch('[a-z][A-Z0-9]*',k))
    def test_math_style_1(k,v):
        import re
        return bool(
            re.fullmatch('[a-z][A-Z0-9]*|[A-Z][0-9]*',k)
            and type(v).__name__ not in ['function','module'])
    def test_all(k,v):
        return True
    def test_all_except_builtin(k,v):
        return k[:2] != '__'
    test = test_all_except_builtin
    debugging = False
    preserving = 1
    whitelisting = True
    def interpret_test_arguments(*args):
        if len(args) == 1 and type(args[0]) == type(lambda _:_):
            return args[0]
        elif args:
            return (lambda x: x in args)
    #_kept = set(()) #not needed at the outmost level
    #def keep(*vs):  _kept.update(map(id,vs)) #has no way to reference current class!
    def __init__(self, scope, *args, preserving = None, whitelisting = None):
        if whitelisting is None: whitelisting = self.whitelisting
        import inspect
        c = self.__class__
        f0 = c.interpret_test_arguments(*args)
        #g0 = self.test #binds first argument as self!
        g0 = c.test
        g1 = ( lambda k, v: g0(k) ) \
            if 1 == len(inspect.getfullargspec(g0).args) \
            else g0
        if f0 is None:
            self.test = g1
        else:
            f1 = ( lambda k, v: f0(k) ) \
                if 1 == len(inspect.getfullargspec(f0).args) \
                else f0
            self.test = (lambda k,v: g1(k,v) and not f1(k,v)) if whitelisting else f1
        #import pdb; pdb.set_trace()
        self.scope = scope
        if preserving is not None:
            self.preserving = preserving
        assert self.preserving in [0,1,2]
        if self.preserving < 2:
            self.shadowed = {}
        for k in list(self.scope.keys()):
            if k == c.__name__:
                #always pop-push with new classes regardless of test
                #if self.test(k,self.scope[k]):
                    #self.shadowed[k] = c
                c1 = type(c.__name__, c.__bases__, dict(c.__dict__))
                    #c.__dict__ can't be deep-copied #TypeError: cannot pickle 'getset_descriptor' object
                #c1._kept = set(())
                #c1.keep = lambda *vs: c1._kept.update(map(id,vs))
                #c1._kept = {}
                #c1.keep = lambda *vs: c1._kept.update({id(v):(print('idv',id(v)),v)[1] for v in vs})
                #get reference to c1 by closure.
                #object could be del'ed after being kept.
                #object kept in dict not released......
                #TODO: get object created time/frame?
                #      patch __del__?
                c1._kept = set(())
                c1.keep = lambda *ks: c1._kept.update(ks)
                self.scope[k] = c1
                if self.debugging: import sys; print('SELF',k,file=sys.stderr)
            elif self.test(k,self.scope[k]):
                if self.preserving < 2:
                    self.shadowed[k] = self.scope[k]
                    if self.debugging: import sys; print('SHADOW',k,file=sys.stderr)
                if 0 == self.preserving:
                    self.scope.pop(k)
                    if self.debugging: import sys; print('POP',k,file=sys.stderr)
    def __enter__(self):
        pass
    def __exit__(self, exc_type, exc_val, exc_tb):
        assert(self.preserving in [0,1,2])
        c = self.__class__
        c1 = self.scope[c.__name__]
        if self.preserving < 2:
            for k in list(self.scope.keys()):
                if self.test(k,self.scope[k]) and not (
                    k in c1._kept #guaranteed to be unique but could the id change?
                    #id(self.scope[k]) in c1._kept #guaranteed to be unique but could the id change?
                    # key of kept variables is not accessible
                    #self.scope[k] in c1.kept #Check only the value?
                    #k in c1.kept[k] and self.scope[k] is c1.kept[k]
                    #check only the key? 
                    ):
                    self.scope.pop(k)
                    if self.debugging: import sys; print('POP',k,file=sys.stderr)
            u = { k:self.shadowed[k] for k in self.shadowed if k not in c1._kept }
            self.scope.update(u)
            if self.debugging: import sys; print('UNSHADOW',*u.keys(),file=sys.stderr)
        del c1._kept
        self.scope[c.__name__] = c
        if self.debugging: import sys; print('RESTORE SELF',c.__name__,file=sys.stderr)
        return False

if False:
    r = 1
    with scoping(locals()):
        r = 5
        print(r)
    print(r)
     
