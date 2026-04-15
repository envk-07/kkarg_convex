from tkinter import *
import math

# Размер окна
SIZE = 600
# Коэффициент гомотетии
SCALE = 50


def x(p):
    """ преобразование x-координаты """
    return SIZE / 2 + SCALE * p.x


def y(p):
    """ преобразование y-координаты """
    return SIZE / 2 - SCALE * p.y


class TkDrawer:
    """ Графический интерфейс для выпуклой оболочки """

    def __init__(self):
        self.root = Tk()
        self.root.title("Выпуклая оболочка")
        self.root.geometry(f"{SIZE + 5}x{SIZE + 5}")
        self.root.resizable(False, False)
        self.root.bind('<Control-c>', lambda e: self.close())
        self.canvas = Canvas(self.root, width=SIZE, height=SIZE)
        self.canvas.pack(padx=5, pady=5)

    def close(self):
        self.root.quit()

    def clean(self):
        """Стирает всё и рисует оси координат"""
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, SIZE, SIZE, fill="white")
        self.canvas.create_line(0, SIZE / 2, SIZE, SIZE / 2, fill="blue")
        self.canvas.create_line(SIZE / 2, 0, SIZE / 2, SIZE, fill="blue")
        self.root.update()

    def draw_point(self, p):
        self.canvas.create_oval(
            x(p) - 2, y(p) - 2, x(p) + 2, y(p) + 2,
            fill="black", outline="black"
        )
        self.root.update()

    def draw_line(self, p, q, color="black", width=2):
        self.canvas.create_line(
            x(p), y(p), x(q), y(q), fill=color, width=width)
        self.root.update()

    def draw_neighborhood(self, a, b):
        """Рисует 1-окрестность отрезка [a,b] в виде капсулы"""
        if a is None or b is None:
            return
        length = a.dist(b)
        radius = SCALE * 1.0   # 1 единица в пикселях
        if length < 1e-9:
            # Отрезок вырожден в точку — рисуем окружность радиуса 1
            cx, cy = x(a), y(a)
            self.canvas.create_oval(
                cx - radius, cy - radius,
                cx + radius, cy + radius,
                outline="green", width=2, dash=(4, 4)
            )
            return

        # Вектор отрезка
        dx = b.x - a.x
        dy = b.y - a.y
        len_scaled = math.hypot(dx, dy)
        # Единичный перпендикуляр
        nx = -dy / len_scaled
        ny = dx / len_scaled

        # Смещение на 1 единицу в пикселях
        offset_x = nx * radius
        offset_y = ny * radius

        # Концы параллельных линий
        x1_top, y1_top = x(a) + offset_x, y(a) + offset_y
        x2_top, y2_top = x(b) + offset_x, y(b) + offset_y
        x1_bot, y1_bot = x(a) - offset_x, y(a) - offset_y
        x2_bot, y2_bot = x(b) - offset_x, y(b) - offset_y

        # Рисуем две параллельные линии (пунктир)
        self.canvas.create_line(x1_top, y1_top, x2_top, y2_top,
                                fill="green", width=2, dash=(4, 4))
        self.canvas.create_line(x1_bot, y1_bot, x2_bot, y2_bot,
                                fill="green", width=2, dash=(4, 4))

        # Угол поворота отрезка (в градусах)
        angle = math.degrees(math.atan2(dy, dx))

        # Полукруг около точки a (левый, выпуклый наружу)
        self.canvas.create_arc(
            x(a) - radius, y(a) - radius,
            x(a) + radius, y(a) + radius,
            start=angle + 90, extent=180,
            style="arc", outline="green", width=2, dash=(4, 4)
        )

        # Полукруг около точки b (правый, выпуклый наружу)
        self.canvas.create_arc(
            x(b) - radius, y(b) - radius,
            x(b) + radius, y(b) + radius,
            start=angle - 90, extent=180,
            style="arc", outline="green", width=2, dash=(4, 4)
        )

        self.root.update()
