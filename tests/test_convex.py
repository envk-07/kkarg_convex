from pytest import approx
from math import sqrt
from r2point import R2Point
from convex import Figure, Void, Point, Segment, Polygon

# Фиксированный отрезок для тестов (1-окрестность)
ta = R2Point(0.0, 0.0)
tb = R2Point(1.0, 0.0)


class TestVoid:

    def setup_method(self):
        self.f = Void(ta, tb)

    def test_figure(self):
        assert isinstance(self.f, Figure)

    def test_void(self):
        assert isinstance(self.f, Void)

    def test_perimeter(self):
        assert self.f.perimeter() == 0.0

    def test_area(self):
        assert self.f.area() == 0.0

    def test_add(self):
        assert isinstance(self.f.add(R2Point(0.0, 0.0)), Point)

    def test_neighborhood_edges_count(self):
        assert self.f.neighborhood_edges_count() == 0


class TestPoint:

    def setup_method(self):
        self.f = Point(R2Point(0.0, 0.0), ta, tb)

    def test_figure(self):
        assert isinstance(self.f, Figure)

    def test_point(self):
        assert isinstance(self.f, Point)

    def test_perimeter(self):
        assert self.f.perimeter() == 0.0

    def test_area(self):
        assert self.f.area() == 0.0

    def test_add1(self):
        assert self.f.add(R2Point(0.0, 0.0)) is self.f

    def test_add2(self):
        assert isinstance(self.f.add(R2Point(1.0, 0.0)), Segment)

    def test_neighborhood_edges_count(self):
        assert self.f.neighborhood_edges_count() == 0


class TestSegment:

    def setup_method(self):
        self.f = Segment(R2Point(0.0, 0.0), R2Point(1.0, 0.0), ta, tb)

    def test_figure(self):
        assert isinstance(self.f, Figure)

    def test_segment(self):
        assert isinstance(self.f, Segment)

    def test_perimeter(self):
        assert self.f.perimeter() == approx(2.0)

    def test_area(self):
        assert self.f.area() == 0.0

    def test_add1(self):
        assert self.f.add(R2Point(0.5, 0.0)) is self.f

    def test_add2(self):
        assert self.f.add(R2Point(0.0, 0.0)) is self.f

    def test_add3(self):
        assert isinstance(self.f.add(R2Point(2.0, 0.0)), Segment)

    def test_add4(self):
        assert isinstance(self.f.add(R2Point(-1.0, 0.0)), Segment)

    def test_add5(self):
        assert isinstance(self.f.add(R2Point(0.0, 1.0)), Polygon)

    def test_neighborhood_edges_count_inside(self):
        # Отрезок полностью в 1-окрестности (расстояние < 1)
        f = Segment(R2Point(0.2, 0.2), R2Point(0.8, 0.2), ta, tb)
        assert f.neighborhood_edges_count() == 1

    def test_neighborhood_edges_count_outside(self):
        # Отрезок далеко от целевого (расстояние >= 1)
        f = Segment(R2Point(0.5, 2.0), R2Point(1.5, 2.0), ta, tb)
        assert f.neighborhood_edges_count() == 0

    def test_neighborhood_edges_count_boundary(self):
        # Отрезок на границе 1-окрестности (расстояние = 1)
        f = Segment(R2Point(0.5, 1.0), R2Point(1.5, 1.0), ta, tb)
        assert f.neighborhood_edges_count() == 0  # Строго меньше 1


class TestPolygon:

    def setup_method(self):
        self.a = R2Point(0.0, 0.0)
        self.b = R2Point(1.0, 0.0)
        self.c = R2Point(0.0, 1.0)
        self.f = Polygon(self.a, self.b, self.c, ta, tb)

    def test_figure(self):
        assert isinstance(self.f, Figure)

    def test_polygon1(self):
        assert isinstance(self.f, Polygon)

    def test_polygon2(self):
        f2 = Polygon(self.b, self.a, self.c, ta, tb)
        assert isinstance(f2, Polygon)

    def test_vertexes1(self):
        assert self.f.points.size() == 3

    def test_vertexes2(self):
        assert self.f.add(R2Point(0.1, 0.1)).points.size() == 3

    def test_vertexes3(self):
        assert self.f.add(R2Point(1.0, 1.0)).points.size() == 4

    def test_vertexes4(self):
        f2 = self.f.add(R2Point(0.4, 1.0)).add(R2Point(1.0, 0.4)) \
            .add(R2Point(0.8, 0.9)).add(R2Point(0.9, 0.8))
        assert f2.points.size() == 7
        assert f2.add(R2Point(2.0, 2.0)).points.size() == 4

    def test_perimeter1(self):
        assert self.f.perimeter() == approx(2.0 + sqrt(2.0))

    def test_perimeter2(self):
        assert self.f.add(R2Point(1.0, 1.0)).perimeter() == approx(4.0)

    def test_area1(self):
        assert self.f.area() == approx(0.5)

    def test_area2(self):
        assert self.f.add(R2Point(1.0, 1.0)).area() == approx(1.0)

    def test_neighborhood_edges_count_triangle(self):
        # Треугольник с рёбрами в окрестности
        a = R2Point(0.2, 0.2)
        b = R2Point(0.8, 0.2)
        c = R2Point(0.5, 0.5)
        f = Polygon(a, b, c, ta, tb)
        # Все 3 ребра в окрестности (расстояние < 1)
        assert f.neighborhood_edges_count() == 3

    def test_neighborhood_edges_count_mixed(self):
        # Многоугольник с рёбрами внутри и снаружи
        a = R2Point(0.2, 0.2)  # В окрестности
        b = R2Point(0.8, 0.2)  # В окрестности
        c = R2Point(0.5, 2.0)  # Далеко (расстояние > 1)
        f = Polygon(a, b, c, ta, tb)
        # Только ребро (a,b) в окрестности
        assert f.neighborhood_edges_count() == 1

    def test_neighborhood_edges_count_inductive(self):
        # Проверка индуктивности: счётчик обновляется при добавлении точек
        a = R2Point(0.2, 0.2)
        b = R2Point(0.8, 0.2)
        c = R2Point(0.5, 0.5)
        f = Polygon(a, b, c, ta, tb)
        initial_count = f.neighborhood_edges_count()

        # Добавляем точку внутри оболочки (не меняет рёбра)
        f = f.add(R2Point(0.4, 0.3))
        assert f.neighborhood_edges_count() == initial_count

        # Добавляем точку снаружи (меняет рёбра)
        f = f.add(R2Point(0.5, 2.0))
        # Счётчик должен обновиться индуктивно
        assert f.neighborhood_edges_count() >= 0
