import sys

def run_statement(statement):
    print('In: {}'.format(statement))
    print('Out: {}'.format(eval(statement)))

def test_big_integer_refcount():
    """This is a test to know the 'minimum' refcount for an integer."""
    run_statement('sys.getrefcount(1234567)')

def test_small_integers():
    '''This is a test to look at how small integers are stored and shared.'''
    #small = range(-10,3) + range(253,258)              # OK for 2.7 KO for 3.5
    small = list(range(-10,3)) + list(range(253,260))   # OK for both
    small = range(-10,260)                             # Show for range. 2.7 behaviour should be investigated

    # Slightly different behavior in 2.7 (intobject.c) or 3.5 (longobject.c)
    unit = (id(1)-id(0))
    print('Address offset between 0 and 1: {}'.format(unit)) # Should be OK on both but more common in 3.5
    format_string = '{:3} {:20} {:8} {:8} {:6}'
    print(format_string.format('Val', 'Address', 'NAO*', 'RefCount', 'Size'))
    for t in ((v, id(v), (id(v) - id(0)) / unit, sys.getrefcount(v), sys.getsizeof(v)) for v in small):
        print(format_string.format(*t))
    print('NAO: Normalized address offset')
    print('In 3.5 NAO are aligned but in 2.7 numbers do not seem aligned')


def test_big_integers():
    '''This is a test to know if big integers (that are dynamically allocated) are always shared.'''
    run_statement('[id(i) for i in [1000,1000,500*2]]')
    print('They are not as the location of the last item is different from the first two.\n')

    run_statement('[sys.getrefcount(i) for i in [1000,1000,500*2]]')
    print('The interpreter shared the first two but the third one was a new allocation.')


if __name__ == '__main__':
    separator = '-' * 45
    funcs = [test_big_integer_refcount, test_small_integers, test_big_integers]
    for f in funcs:
        print(separator)
        print('Running: ' + f.__name__)
        print(separator)
        print(f.__doc__)
        f()
        print(separator + '\n')
