from collections import defaultdict, UserDict
from functools import reduce
from operator import xor


def process_magma_output(bstdout):
    """ Reconstructs a set based on magma's output. """
    stdout = bstdout.decode("utf-8")
    magout = stdout.rstrip("\r\n").split("\n")
    lines = [l[:-1] if l[-1] == "\\" else l for l in magout]
    magset = "".join(lines)
    strsets = magset[1:-1].split("},")
    sets = set()
    for strset in strsets[:-1]:
        sets.add(frozenset(eval(strset + "}")))
    sets.add(frozenset(eval(strsets[-1])))
    return sets


class hashdict(UserDict):
    """ A class useful to realise an immutable, hashable dictionary.
        Note that immutability is not enforced.
    """
    def __init__(self, dictionary):
        super().__init__(dictionary)

    def __hash__(self):
        return reduce(xor, (hash(k) ^ hash(frozenset(v)) for k, v in self.data.items()))

    def __eq__(self, other):
        if isinstance(other, hashdict):
            return self.data == other.data
        else:
            raise NotImplemented

