#BSD 3-Clause License

#Copyright (c) 2021, l74d
#All rights reserved.

#Redistribution and use in source and binary forms, with or without
#modification, are permitted provided that the following conditions are met:

#1. Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.

#2. Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.

#3. Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.

#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
#FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import inspect
import ctypes

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
    @classmethod
    def settle(c, scope):
        c1 = type(c.__name__, c.__bases__, dict(c.__dict__))
        c1.module_globals = scope
        k = c.__name__
        scope[k] = c1
        if c.debugging:
            assert(c1.module_globals is inspect.stack()[1][0].f_globals)
            import sys; print('SELF0',k,id(c),id(c1),file=sys.stderr)

    def __init__(self, *args, preserving = None, whitelisting = None):
        if whitelisting is None: whitelisting = self.whitelisting
        if len(args)>0 and type(args[0]) == dict:
            self.scope = args[0]
            args = args[1:]
            if self.debugging:
                assert(self.scope is inspect.stack()[1][0].f_locals)
        else:
            self.scope = inspect.stack()[1][0].f_locals
            
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
        if preserving is not None:
            self.preserving = preserving
        assert self.preserving in [0,1,2]
        if self.preserving < 2:
            self.shadowed = {}

        if hasattr(c,'module_globals'):
            if self.debugging:
                assert(c.module_globals is inspect.stack()[1][0].f_globals)
            self.scope_of_class = c.module_globals
                #self.scope #globals() #wrong globals().
        else:
            self.scope_of_class = inspect.stack()[1][0].f_globals
        for k in list(self.scope.keys()):
            if k == c.__name__:
                self.scope_of_class = self.scope
                pass
            elif self.test(k,self.scope[k]):
                if self.preserving < 2:
                    self.shadowed[k] = self.scope[k]
                    if self.debugging: import sys; print('SHADOW',k,file=sys.stderr)
                if 0 == self.preserving:
                    self.scope.pop(k)
                    if self.debugging: import sys; print('POP',k,file=sys.stderr)

        k = c.__name__
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
        self.scope_of_class[k] = c1
        if self.debugging:
            import sys; print('SELF',k,id(c),id(c1),file=sys.stderr)
    def __enter__(self):
        pass
    def __exit__(self, exc_type, exc_val, exc_tb):
        #if self.debugging:
        assert(self.scope is inspect.stack()[1][0].f_locals)
            #implicitly activates something necessary
        self.scope = inspect.stack()[1][0].f_locals
        frame = inspect.stack()[1][0]
        #import pdb; pdb.set_trace()
        assert(self.preserving in [0,1,2])
        c = self.__class__
        c1 = self.scope_of_class[c.__name__]
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
                    if self.debugging:
                        import sys
                        print('POP',k,id(self.scope),file=sys.stderr)
            u = { k:self.shadowed[k] for k in self.shadowed if k not in c1._kept }
            self.scope.update(u)
            if self.debugging:
                import sys;
                print('UNSHADOW',*u.keys(),file=sys.stderr)
        del c1._kept
        self.scope_of_class[c.__name__] = c
        if self.debugging:
            import sys;
            print('RESTORE SELF',c.__name__,file=sys.stderr)

        #https://pydev.blogspot.com/2014/02/changing-locals-of-frame-frameflocals.html
        #https://stackoverflow.com/questions/34650744/modify-existing-variable-in-locals-or-frame-f-locals
        #https://www.python.org/dev/peps/pep-0558/
        ctypes.pythonapi.PyFrame_LocalsToFast(
            ctypes.py_object(frame), ctypes.c_int(1))

        return False

if False:
    r = 1
    with scoping(locals()):
        r = 5
        print(r)
    print(r)
     
