from deq import Deq
from r2point import R2Point


class Figure:
    """ Абстрактная фигура """

    def perimeter(self):
        return 0.0

    def area(self):
        return 0.0

    def neighborhood_edges_count(self):
        return 0


class Void(Figure):
    """ "Hульугольник" """

    def __init__(self, ta, tb):
        self.ta, self.tb = ta, tb

    def add(self, p):
        return Point(p, self.ta, self.tb)


class Point(Figure):
    """ "Одноугольник" """

    def __init__(self, p, ta, tb):
        self.p = p
        self.ta, self.tb = ta, tb

    def add(self, q):
        return self if self.p == q else Segment(self.p, q, self.ta, self.tb)


class Segment(Figure):
    """ "Двуугольник" """

    def __init__(self, p, q, ta, tb):
        self.p, self.q = p, q
        self.ta, self.tb = ta, tb
        self._edge_count = self._check_edge(p, q)

    def _check_edge(self, u, v):
        d1 = u.dist_to_segment(self.ta, self.tb)
        d2 = v.dist_to_segment(self.ta, self.tb)
        return 1 if (d1 < 1.0 and d2 < 1.0) else 0

    def neighborhood_edges_count(self):
        return self._edge_count

    def perimeter(self):
        return 2.0 * self.p.dist(self.q)

    def add(self, r):
        if R2Point.is_triangle(self.p, self.q, r):
            return Polygon(self.p, self.q, r, self.ta, self.tb)
        elif r.is_inside(self.p, self.q):
            return self
        elif self.p.is_inside(r, self.q):
            return Segment(r, self.q, self.ta, self.tb)
        else:
            return Segment(self.p, r, self.ta, self.tb)


class Polygon(Figure):
    """ Многоугольник """

    def __init__(self, a, b, c, ta, tb):
        self.points = Deq()
        self.ta, self.tb = ta, tb
        self.points.push_first(b)
        if b.is_light(a, c):
            self.points.push_first(a)
            self.points.push_last(c)
        else:
            self.points.push_last(a)
            self.points.push_first(c)
        self._perimeter = a.dist(b) + b.dist(c) + c.dist(a)
        self._area = abs(R2Point.area(a, b, c))

        self._edge_count = 0
        if self._is_edge_valid(a, b):
            self._edge_count += 1
        if self._is_edge_valid(b, c):
            self._edge_count += 1
        if self._is_edge_valid(c, a):
            self._edge_count += 1

    def perimeter(self):
        return self._perimeter

    def area(self):
        return self._area

    def neighborhood_edges_count(self):
        return self._edge_count

    def _is_edge_valid(self, u, v):
        d1 = u.dist_to_segment(self.ta, self.tb)
        d2 = v.dist_to_segment(self.ta, self.tb)
        return d1 < 1.0 and d2 < 1.0

    # добавление новой точки
    def add(self, t):

        # поиск освещённого ребра
        for n in range(self.points.size()):
            if t.is_light(self.points.last(), self.points.first()):
                break
            self.points.push_last(self.points.pop_first())

        # хотя бы одно освещённое ребро есть
        if t.is_light(self.points.last(), self.points.first()):

            # учёт удаления ребра, соединяющего конец и начало дека
            if self._is_edge_valid(self.points.last(), self.points.first()):
                self._edge_count -= 1
            self._perimeter -= self.points.first().dist(self.points.last())
            self._area += abs(R2Point.area(t,
                                           self.points.last(),
                                           self.points.first()))

            # удаление освещённых рёбер из начала дека
            p = self.points.pop_first()
            while t.is_light(p, self.points.first()):
                if self._is_edge_valid(p, self.points.first()):
                    self._edge_count -= 1
                self._perimeter -= p.dist(self.points.first())
                self._area += abs(R2Point.area(t, p, self.points.first()))
                p = self.points.pop_first()
            self.points.push_first(p)

            # удаление освещённых рёбер из конца дека
            p = self.points.pop_last()
            while t.is_light(self.points.last(), p):
                if self._is_edge_valid(self.points.last(), p):
                    self._edge_count -= 1
                self._perimeter -= p.dist(self.points.last())
                self._area += abs(R2Point.area(t, p, self.points.last()))
                p = self.points.pop_last()
            self.points.push_last(p)

            # добавление двух новых рёбер
            if self._is_edge_valid(t, self.points.first()):
                self._edge_count += 1
            if self._is_edge_valid(self.points.last(), t):
                self._edge_count += 1
            self._perimeter += t.dist(self.points.first()) + \
                t.dist(self.points.last())
            self.points.push_first(t)

        return self


if __name__ == "__main__":
    f = Figure()
    print(type(f), f.__dict__)
    f = f.add(R2Point(0.0, 0.0))
    print(type(f), f.__dict__)
    f = f.add(R2Point(1.0, 0.0))
    print(type(f), f.__dict__)
    f = f.add(R2Point(0.0, 1.0))
    print(type(f), f.__dict__)
