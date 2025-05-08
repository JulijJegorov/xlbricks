"""
    Author: julij
    Date: 02/10/2022
    Description: 
"""

import uuid


class XLBricksFront(object):

    def __init__(self, alias, xlbricks, persist=True):
        self.counter = 0
        self.alias = alias
        self.xlbricks = xlbricks
        self.persist = persist
        self.uuid = str(uuid.uuid1())

    @property
    def bricks_name(self):
        return self.alias if self.persist else self.uuid

    @property
    def bricks_full_name(self):
        return '%s:%s' % (self.bricks_name, self.counter)


