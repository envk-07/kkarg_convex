#!/usr/bin/env -S python3 -B
from convex import Point, Segment, Polygon
from tk_drawer import TkDrawer
from r2point import R2Point
from convex import Void


def void_draw(self, tk):
    pass


def point_draw(self, tk):
    tk.draw_point(self.p)


def segment_draw(self, tk):
    tk.draw_line(self.p, self.q)


def polygon_draw(self, tk):
    for n in range(self.points.size()):
        tk.draw_line(self.points.last(), self.points.first())
        self.points.push_last(self.points.pop_first())


# Подключаем методы рисования к классам фигур
setattr(Void, 'draw', void_draw)
setattr(Point, 'draw', point_draw)
setattr(Segment, 'draw', segment_draw)
setattr(Polygon, 'draw', polygon_draw)

# Ввод отрезка в консоли
print("Введите координаты отрезка:")
ta = R2Point()
tb = R2Point()
print(f"Отрезок задан: ({ta.x}, {ta.y}) – ({tb.x}, {tb.y})")

# Создаём фигуру с заданным отрезком
f = Void(ta, tb)

# Открываем окно
tk = TkDrawer()
tk.clean()
tk.draw_line(ta, tb, color="red", width=3)
tk.draw_neighborhood(ta, tb)
tk.root.update()

print("\nТеперь вводите координаты точек:")
try:
    while True:
        p = R2Point()          # ввод точки в консоли
        f = f.add(p)           # добавляем в оболочку
        tk.clean()             # очищаем окно
        tk.draw_line(ta, tb, color="red", width=3)
        tk.draw_neighborhood(ta, tb)
        f.draw(tk)             # рисуем оболочку
        tk.root.update()       # обновляем окно
        print(f"S = {f.area():.3f}, P = {f.perimeter():.3f}, "
              f"Рёбер в окрестности = {f.neighborhood_edges_count()}\n")
except (EOFError, KeyboardInterrupt):
    print("\nStop")
    tk.close()
