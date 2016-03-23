import numpy
import _lipsmin
import adolc

def function(file, tape_tag, q, x, y):
    """
    evaluate the function f(x) recorded on tape with index tape_tag
    """
    assert type(tape_tag) == int
    assert type(q) == float
    ts = adolc.tapestats(tape_tag)
    N = ts['NUM_INDEPENDENTS']
    M = ts['NUM_DEPENDENTS']
    x = numpy.ascontiguousarray(x, dtype=float)
    assert numpy.size(x) == N
    assert numpy.ndim(x) == 1
    y = numpy.zeros(M, dtype=float)
    _lipsmin.LiPsMin(tape_tag, q, N, x, y)
