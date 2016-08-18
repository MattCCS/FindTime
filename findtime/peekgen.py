
def peekgen(gen):
    for e in gen:
        peek = yield e
        if peek is not None:
            yield
            yield peek
