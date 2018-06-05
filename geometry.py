from math import sqrt
from numbers import Number


class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __getitem__(self, item):
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        elif item > 1:
            raise IndexError
        raise TypeError


    def __add__(self, other):
        return self.__class__(self.x + other[0], self.y + other[1])

    def __sub__(self, other):
        return self.__class__(self.x - other[0], self.y - other[1])

    def __mul__(self, other):
        if isinstance(other, Number):
            return self.__class__(self.x * other, self.y * other)
        else:
            return self.__class__(self.x * other[0], self.y * other[1])

    def __truediv__(self, other):
        if isinstance(other, Number):
            return self.__class__(self.x / other, self.y / other)
        else:
            return self.__class__(self.x / other[0], self.y / other[1])

    def __abs__(self):
        return sqrt(self.x ** 2 + self.y ** 2)

    def __len__(self):
        return 2

class Point(Vector2):
    def __init__(self, x, y):
        super().__init__(x, y)


class Size(Vector2):
    def __init__(self, w, h):
        super().__init__(w, h)
        self.w = w
        self.h = h

    @property
    def w(self):
        return self.x

    @w.setter
    def w(self, value):
        self.x = value

    @property
    def h(self):
        return self.y

    @h.setter
    def h(self, value):
        self.y = value

    @property
    def width(self):
        return self.x

    @width.setter
    def width(self, value):
        self.x = value

    @property
    def height(self):
        return self.y

    @height.setter
    def height(self, value):
        self.y = value


class Rect:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def __getitem__(self, item):
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        elif item == 2:
            return self.w
        elif item == 3:
            return self.h
        raise IndexError

    def __contains__(self, item):
        return self.contains_point(item)

    @property
    def width(self):
        return self.x

    @width.setter
    def width(self, value):
        self.x = value

    @property
    def height(self):
        return self.y

    @height.setter
    def height(self, value):
        self.y = value

    @property
    def origin(self):
        return Point(self.x, self.y)

    @origin.setter
    def origin(self, value):
        self.x = value[0]
        self.y = value[1]

    @property
    def size(self):
        return Size(self.w, self.h)

    @size.setter
    def size(self, value):
        self.w = value[0]
        self.h = value[1]

    @property
    def min_x(self):
        return min(self.x, self.x + self.w)

    @property
    def max_x(self):
        return max(self.x, self.x + self.w)

    @property
    def min_y(self):
        return min(self.y, self.y + self.h)

    @property
    def max_y(self):
        return max(self.y, self.y + self.h)

    def center(self, p=None):
        if p:
            self.x = p[0] - self.w / 2
            self.y = p[1] - self.h / 2
        else:
            return Point(self.x + self.w / 2, self.x + self.h / 2)

    def contains_point(self, p):
        if self.x < p[0]:
            if self.x + self.w > p[0]:
                if self.y < p[1]:
                    if self.y + self.w > p[1]:
                        return True
        return False

    def contains_rect(self, other_rect):
        return self.contains_point((other_rect[0], other_rect[1])) and self.contains_point(
            (other_rect[0] + other_rect[2], other_rect[1] + other_rect[3]))

    def intersects(self, other_rect):
        return (other_rect[0] + other_rect[2] >= self.x and other_rect[0] <= self.x + self.w) and \
               (other_rect[1] + other_rect[3] >= self.y and other_rect[1] <= self.y + self.h)

    def intersection(self, other_rect):  # TODO make robust n test n stuff
        return Rect(max(self.x, other_rect[0]),
                    max(self.y, other_rect[1]),
                    min(self.x + self.w, other_rect[0] + other_rect[2]),
                    min(self.y + self.h, other_rect[1] + other_rect[3]))

    def union(self, other_rect):  # TODO make robust
        return Rect(min(self.x, other_rect[0]),
                    min(self.y, other_rect[1]),
                    max(self.x + self.w, other_rect[0] + other_rect[2]),
                    max(self.y + self.h, other_rect[1] + other_rect[3]))

    def translate(self, x, y):
        self.x += x
        self.y += y

    def inset(self, top, left, bottom=None, right=None):  # TODO check its the same as pythonista
        if not bottom:
            bottom = top
        if not right:
            right = left
        self.x -= left
        self.w += left + right
        self.y -= top
        self.h += top + bottom
