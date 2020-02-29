def exercise(iterable):
    for item in iterable:
        pass

def unzip(pairs):
    a=[pair[0] for pair in pairs]
    b=[pair[1] for pair in pairs]
    return a,b
def prj(stuff,n):
    for item in stuff:
        yield( item[n] )
wrap = lambda fn_name : lambda obj : getattr( obj, fn_name )
lmap = lambda *a,**b : list(map(*a,**b))
lzip = lambda *a,**b : list(zip(*a,**b))
lprj = lambda *a,**b : list(prj(*a,**b))

