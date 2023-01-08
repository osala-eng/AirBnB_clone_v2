#!/bin/python3

class Test:
    '''Class desc'''

    __att = 'att'
    __mnm__ = 'mnm'
    file = None

    def __init__(self) -> None:
        '''Init meth'''
        name = 'name'

    def some(self) -> None:
        '''Rand meth'''
        print('some')

    @property
    def att(self) -> str:
        '''Att getter'''
        return self.__att

    @att.setter
    def att(self, name) -> None:
        '''Att setter'''
        self.__att = name


if __name__ == '__main__':
    meth = [func for func in dir(Test) if callable(
        getattr(Test, func)) and not func.startswith('__')]

    for m in meth:
        f = getattr(Test, m)
        print(f.__doc__)
