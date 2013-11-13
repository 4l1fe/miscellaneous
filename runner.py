import io
from timeit import Timer


def file_test():
    f = open('some.txt', 'w+')
    f.write('lalala')
    f.seek(0)
    out = f.read()
    f.close()

def stringio_test():
    sio = io.StringIO()
    sio.write('lalala')
    sio.seek(0)
    out = sio.read()
    sio.close()


print(Timer('file_test()', 'from __main__ import file_test').timeit(number=1000))
print(Timer('stringio_test()', 'from __main__ import io, stringio_test').timeit(number=1000))


# 2.2147124966231084
# 0.012935039292414352