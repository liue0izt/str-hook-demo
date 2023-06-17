# -*- coding: utf-8 -*-
def test():
    s = "stack"
    o = "overflow"
    return s + o

if __name__ == '__main__':
    print("-----" * 5 + "TEST" + "-----" * 5)

    from hook import fh_hook

    fh_hook.apply_hook()
    print(test())
