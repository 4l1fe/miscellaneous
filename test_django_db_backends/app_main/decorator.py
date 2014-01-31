def skip(is_skiped):

    def decorator(func):
        if is_skiped:
            return func
        else:
            return func

    return decorator


@skip(True)
def some():
    print('ololaskdada')


@skip(False)
def some2():
    print('aazxzzxczxc')

some()
some2()