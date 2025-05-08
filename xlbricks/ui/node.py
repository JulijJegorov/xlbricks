
class Node(object):

    def __init__(self, name, parent=None):
        self._name = name
        self._parent = parent
        self._children = []
        self._value = None
        if parent is not None:
            parent.add_child(self)

    def add_child(self, child):
        self._children.append(child)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def child(self, row):
        return self._children[row]

    def child_count(self):
        return len(self._children)

    def parent(self):
        return self._parent

    def row(self):
        if self._parent is not None:
            return self._parent._children.index(self)

    def data(self, column):
        if column is 0:
            return self.name
        elif column is 1:
            return self.value

    def set_data(self, column, value):
        if column is 0:
            self.name = value
        if column is 1:
            self.value = value

