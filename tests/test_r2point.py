from pytest import approx
from math import sqrt
from r2point import R2Point
from unittest.mock import patch


class TestR2Point:
    def test_r2point_input(self):
        coords = iter(["1", "2"])
        with patch('builtins.input', lambda _: next(coords)):
            assert R2Point() == R2Point(1.0, 2.0)

    def test_dist1(self):
        a = R2Point(1.0, 1.0)
        assert a.dist(R2Point(1.0, 1.0)) == approx(0.0)

    def test_dist2(self):
        a = R2Point(1.0, 1.0)
        assert a.dist(R2Point(1.0, 0.0)) == approx(1.0)

    def test_dist3(self):
        a = R2Point(1.0, 1.0)
        assert a.dist(R2Point(0.0, 0.0)) == approx(sqrt(2.0))

    def test_area1(self):
        a = R2Point(1.0, 1.0)
        assert R2Point.area(a, a, a) == approx(0.0)

    def test_area2(self):
        a, b, c = R2Point(0.0, 0.0), R2Point(1.0, 1.0), R2Point(2.0, 2.0)
        assert R2Point.area(a, b, c) == approx(0.0)

    def test_area3(self):
        a, b, c = R2Point(0.0, 0.0), R2Point(1.0, 0.0), R2Point(1.0, 1.0)
        assert R2Point.area(a, b, c) > 0.0

    def test_area4(self):
        a, b, c = R2Point(0.0, 0.0), R2Point(1.0, 0.0), R2Point(1.0, 1.0)
        assert R2Point.area(a, c, b) < 0.0

    def test_is_inside1(self):
        a, b = R2Point(0.0, 0.0), R2Point(2.0, 1.0)
        assert R2Point(1.0, 0.5).is_inside(a, b)

    def test_is_inside2(self):
        a, b = R2Point(0.0, 0.0), R2Point(2.0, 1.0)
        assert R2Point(1.0, 0.5).is_inside(b, a)

    def test_is_inside3(self):
        a, b = R2Point(0.0, 0.0), R2Point(2.0, 1.0)
        assert not R2Point(1.0, 1.5).is_inside(a, b)

    def test_is_light1(self):
        a, b = R2Point(0.0, 0.0), R2Point(1.0, 0.0)
        assert not R2Point(0.5, 0.0).is_light(a, b)

    def test_is_light2(self):
        a, b = R2Point(0.0, 0.0), R2Point(1.0, 0.0)
        assert R2Point(2.0, 0.0).is_light(a, b)

    def test_is_light3(self):
        a, b = R2Point(0.0, 0.0), R2Point(1.0, 0.0)
        assert not R2Point(0.5, 0.5).is_light(a, b)

    def test_is_light4(self):
        a, b = R2Point(0.0, 0.0), R2Point(1.0, 0.0)
        assert R2Point(0.5, -0.5).is_light(a, b)

    def test_eq1(self):
        assert R2Point(1.0, 1.0) != R2Point(2.0, 2.0)

    def test_eq2(self):
        assert R2Point(1.0, 1.0) != (1.0, 1.0)


# Новые тесты для dist_to_segment
class TestDistToSegment:

    def test_degenerate_segment(self):
        # Отрезок вырожден в точку (строка 33 в r2point.py)
        a = b = R2Point(0.0, 0.0)
        p = R2Point(1.0, 1.0)
        assert p.dist_to_segment(a, b) == approx(sqrt(2.0))

    def test_point_on_segment(self):
        a, b = R2Point(0.0, 0.0), R2Point(2.0, 0.0)
        p = R2Point(1.0, 0.0)
        assert p.dist_to_segment(a, b) == approx(0.0)

    def test_point_perpendicular(self):
        a, b = R2Point(0.0, 0.0), R2Point(2.0, 0.0)
        p = R2Point(1.0, 1.0)
        assert p.dist_to_segment(a, b) == approx(1.0)

    def test_point_beyond_a(self):
        a, b = R2Point(0.0, 0.0), R2Point(2.0, 0.0)
        p = R2Point(-1.0, 0.0)
        assert p.dist_to_segment(a, b) == approx(1.0)

    def test_point_beyond_b(self):
        a, b = R2Point(0.0, 0.0), R2Point(2.0, 0.0)
        p = R2Point(3.0, 0.0)
        assert p.dist_to_segment(a, b) == approx(1.0)

    def test_point_diagonal(self):
        a, b = R2Point(0.0, 0.0), R2Point(1.0, 1.0)
        p = R2Point(0.5, 0.5)
        assert p.dist_to_segment(a, b) == approx(0.0)
