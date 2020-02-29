import importlib 
from collections import OrderedDict
from argparse import ArgumentParser
import r20.tools.func as func

def superparser(mip):
    parents = dictionize_mip(mip).values()
    parents = filter(None,parents)
    return parser4mip4parents(
        mip=mip,
        parents=parents
    )

##########################################################################
def subparser4mip(mip):
    """fn(a.b) -> the subparser mod(a/b/config/parser.py).parser

    The [config/parser.py] file is a nice out of the way place to define
    the options useful for [a.b] if [a.b] is directly imported (and for
    [a.b.X[.Y]] if [a.b.X[.Y]] wishes to aquire the options.

    We say the returned parser is a *sub*parser because it is intended to
    belong to a list of parsers that will be the parents of a main parser.
    """
    try:
        return importlib.import_module( '%s.__config.parser' % mip ).subparser
    except ModuleNotFoundError:
        return None

def parser4mip4parents(mip,parents):
    """fn('a.b.c', <parsers> ) -> a properly configured parser for a.b

    Typically the list <parsers> will be a list of subparsers including
    the subparser of mip 'a.b.c' itself, and possibly includin those of
    the parent mips 'a.b' and 'a'.
    """
    return ArgumentParser(
        prog='python -m %s' % mip,
        parents=parents
    )

def parser4mip(mip):
    """fn(<mip>) -> parser4mip4parents(<mip>,[subparser4mip(<mip>))] )

    A convenience function for when no parent parsers are desired.
    """
    return parser4mip4parents(
        mip=mip,
        parents=[subparser4mip(mip)]
    )








def parent4mip(mip):
    return '.'.join(mip.split('.')[:-1])

def parentS4mip(mip):
    if mip: return [mip] + parentS4mip( parent4mip(mip) )
    else: return []
def dictionize_mip(mip):
    # Note: not all values will be parsers. Some may be None.
    mips=parentS4mip(mip)
    subparsers = map(subparser4mip, mips )
    return OrderedDict(list(zip(mips,subparsers)))

def parent_parsers(mip):
    return list( filter(None,dictionize_mip(mip).values()))


def dump_parsers_of_mip(mip):
    form = lambda item : '%s ==> %s\n'  % item
    show = lambda item : print(form(item))
    row = map(show, dictionize_mip(mip).items())
    func.exercise(row)

