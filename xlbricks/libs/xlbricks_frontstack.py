"""
    Author: julij.jegorov
    Date: 15/02/2026
    Description: Singleton stack of XLBricksFront instances; tracks bricks by alias/UUID.
"""

from xlbricks.libs.xlbricks_front import XLBricksFront

class Singleton(object):
    """ Singleton base class """

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance


class XLBricksFrontStack(Singleton):

    front_stack = dict()

    def __contains__(self, item):
        return item in self.front_stack

    def __setitem__(self, key, value):
        self.front_stack[key] = value

    def __getitem__(self, item):
        return self.front_stack.get(item, None)

    def __delitem__(self, item):
        del self.front_stack[item]

    def clear(self):
        self.front_stack.clear()

    def to_dict(self):
        res_dict = dict()
        for key, bricks_front in self.front_stack.items():
            res_dict[key] = bricks_front.xlbricks.to_dict()
        return res_dict


def add_bricks_to_front_stack(bricks: XLBricksFront):
    container_name = bricks.bricks_name
    if container_name in XLBricksFrontStack():
        bricks.counter = XLBricksFrontStack()[container_name].counter + 1
    XLBricksFrontStack()[container_name] = bricks


def delete_bricks_from_front_stack(bricks: XLBricksFront):
    if not bricks.persist and bricks.bricks_name in XLBricksFrontStack():
        del XLBricksFrontStack()[bricks.bricks_name]
