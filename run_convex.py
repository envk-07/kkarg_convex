#!/usr/bin/env -S python3 -B
from r2point import R2Point
from convex import Void

print("Введите координаты отрезка:")
ta = R2Point()
tb = R2Point()
f = Void(ta, tb)
try:
    while True:
        print("Теперь введите координаты точки:")
        f = f.add(R2Point())
        print(f"S = {f.area()}, P = {f.perimeter()}")
        print(f"Рёбер в окрестности: {f.neighborhood_edges_count()}")
        print()
except (EOFError, KeyboardInterrupt):
    print("\nStop")
