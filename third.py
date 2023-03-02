# from kivy.app import App
# from kivy.graphics import Color, Line
# from kivy.uix.widget import Widget
# import math

# class TriangleWidget(Widget):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
        
#         with self.canvas:
#             # Set color to black with a line width of 2
#             Color(0, 0, 0, mode='rgba', group='triangle')
            
#             # Draw a triangle using lines only
#             self.line1 = Line(points=[0, 0, 0, 0], group='triangle')
#             self.line2 = Line(points=[0, 0, 0, 0], group='triangle')
#             self.line3 = Line(points=[0, 0, 0, 0], group='triangle')
#             self.update_triangle()
#             self.bind(size=self.update_triangle)
    
#     def rotate_point(self, x, y, cx, cy, angleInDegrees):
#         angleInRadians = angleInDegrees * (math.pi / 180)
#         cosTheta = math.cos(angleInRadians)
#         sinTheta = math.sin(angleInRadians)
#         X = (int)(cosTheta * (x - cx) - sinTheta * (y - cy) + cx)
#         Y = (int) (sinTheta * (x - cy) +cosTheta * (y - cy) + cy)
#         return (X, Y)
    
#     def update_triangle(self, *args):
#         height = min(self.width, self.height) / 2
#         base_width = 0.25 * height
#         x1 = (self.width - base_width) / 2
#         x2 = x1 + base_width
#         x3 = x1 + base_width / 2
#         y1 = (self.height - height) / 2
#         y2 = y1
#         y3 = y1 + height
#         x3 = self.width/2
#         y3 = self.height/2 

#         x1, y1 = self.rotate_point(x1, y1, x3, y3, 20)
#         x2, y2 = self.rotate_point(x2, y2, x3, y3, 20)
#         self.line1.points = [x1, y1, x2, y2]
#         self.line2.points = [x2, y2, x3, y3]
#         self.line3.points = [x3, y3, x1, y1]
#         self.canvas.before.clear()
#         with self.canvas.before:
#             Color(1, 0, 0, mode='rgba', group='triangle')
#             Line(points=self.line1.points, width=2, group='triangle')
#             Line(points=self.line2.points, width=2, group='triangle')
#             Line(points=self.line3.points, width=2, group='triangle')

#         # x1, y2 = self.rotate_point(x1, y1, x3, y3, 45)
#         # print(val)

# class TriangleApp(App):
#     def build(self):
#         return TriangleWidget()


# if __name__ == '__main__':
#     TriangleApp().run()

from math import cos, sin, pi, dist, sqrt
from kivy.app import App
from kivy.graphics import Color, Triangle, Line, Ellipse, Mesh
from kivy.uix.widget import Widget
import random
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window

class RadarChartWidget(Widget):
    triangles = []
    polygons = []
    polygon_vertices = []
    test = "null"
    speed = 0.5
    indices = [0, 1, 2, 3]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sides = 16  # Number of sides in the chart
        self.data = []
        self.color = (0, 0, 1, 0.7)  # Color of the chart
        self.update_chart()
        self.bind(size=self.update_chart)

        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)

    def update_chart(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(*self.color)

            center_x = self.width / 2
            center_y = self.height / 2
            radius = min(self.width, self.height) / 2 * 0.9
            angles = [(i + (0.5 * 7)) * 2 * pi / self.sides for i in range(self.sides)]
            # print(angles)
            vertices = [(center_x + radius * cos(angle), center_y + radius * sin(angle))
                        for angle in angles]
            # print(vertices[0])
            self.polygon_vertices = []
            for i in range(self.sides):
                p1 = vertices[i]
                p2 = vertices[(i + 1) % self.sides]
                p3 = (center_x, center_y)
                self.p3 = (center_x, center_y)
                # Triangle(points=[p1[0], p1[1], p2[0], p2[1], p3[0], p3[1]])
                # drawing the outer triangle
                Line(points=[p1[0], p1[1], p2[0], p2[1]], width=2, group='triangle')
                Line(points=[p2[0], p2[1], p3[0], p3[1]], width=2, group='triangle')
                Line(points=[p1[0], p1[1], p3[0], p3[1]], width=2, group='triangle')
                
                # adding to the list of triangles
                self.triangles.append([(p1[0], p1[1]), (p2[0], p2[1]), (p3[0], p3[1])])

                # drawing the circle
                x_mid = (p1[0] + p2[0]) / 2
                y_mid = (p1[1] + p2[1]) / 2
                radius = min(self.width, self.height) / 50
                self.circle = Ellipse(pos=(x_mid - radius, y_mid - radius), size=(2 * radius, 2 * radius))

                # drawing the middle lines
                points_1 = self.evenly_spaced_points((p1[0], p1[1]), (p3[0], p3[1]), 9)
                points_2 = self.evenly_spaced_points((p2[0], p2[1]), (p3[0], p3[1]), 9)
                # print(points_1[0])
                for j in range(0, len(points_1)):
                    # print(points_1[j][0])
                    Line(points=[points_1[j], points_2[j]], width=2, group='triangle')

                polygon_vertices = []
                for j in range(0, len(points_1)-1):
                    mesh_vertices = [*points_1[j], 1, 1, *points_1[j+1], 1, 1, *points_2[j+1], 1, 1, *points_2[j], 1, 1]
                    polygon_vertices.append(mesh_vertices)
                    # print(mesh_vertices)
                    self.polygons.append([points_1[j], points_1[j+1], points_2[j+1], points_2[j]])
                    # r, g, b = random.random(), random.random(), random.random()
                    # Color(r, g, b, 0.5)
                    # Mesh(vertices=polygon_vertices[j], indices=self.indices, mode="triangle_fan")
                self.polygon_vertices.append(polygon_vertices)
                # v = [*points_1[2], 1, 1, *points_1[3], 1, 1, *points_2[3], 1, 1, *points_2[2], 1, 1]
                # self.polygons.append([points_1[2], points_1[3], points_2[3], points_2[2]])
                # indices = [0, 1, 2, 3]
                # Mesh(vertices=v, indices=indices, mode="triangle_fan")
                r, g, b = random.random(), random.random(), random.random()
                Color(r, g, b, 0.5)

            print(len(self.polygon_vertices))
            Mesh(vertices=self.polygon_vertices[0][7], indices=self.indices, mode="triangle_fan")

    def evenly_spaced_points(self, start, end, n):
        """
        Returns a list of n evenly spaced points between the start and end points on a line.
        """
        # Calculate the distance between the start and end points.
        dx = (end[0] - start[0])
        dy = (end[1] - start[1])
        dist = ((dx ** 2) + (dy ** 2)) ** 0.5
        
        # Calculate the step size between each point.
        step = dist / (n - 1)
        
        # Calculate the x and y increments for each point.
        x_inc = (dx / dist) * step
        y_inc = (dy / dist) * step
        
        # Create a list of n evenly spaced points.
        points = [(start[0] + i * x_inc, start[1] + i * y_inc) for i in range(n)]
        
        return points

    def is_point_inside_triangle(self, pt, v1, v2, v3):
        """
        Determine if a point is inside a triangle defined by three vertices.
        Arguments:
            pt: tuple (x, y) representing the coordinates of the point to check
            v1, v2, v3: tuples (x, y) representing the coordinates of the vertices of the triangle
        Returns:
            True if the point is inside the triangle, False otherwise.
        """
        def sign(p1, p2, p3):
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

        d1 = sign(pt, v1, v2)
        d2 = sign(pt, v2, v3)
        d3 = sign(pt, v3, v1)

        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

        return not (has_neg and has_pos)

    def is_point_inside_polygon(self, point, polygon):
        """
        Check if a point is inside a 4-sided polygon.

        Parameters:
            point (tuple): The (x, y) coordinates of the point.
            polygon (list): A list of 4 tuples representing the (x, y) coordinates of the vertices of the polygon.

        Returns:
            bool: True if the point is inside the polygon, False otherwise.
        """
        x, y = point
        polygon = list(polygon)  # make a copy of the polygon vertices

        # Check if point is outside the polygon bounding box
        min_x = min(vertex[0] for vertex in polygon)
        max_x = max(vertex[0] for vertex in polygon)
        min_y = min(vertex[1] for vertex in polygon)
        max_y = max(vertex[1] for vertex in polygon)
        if x < min_x or x > max_x or y < min_y or y > max_y:
            return False

        # Check if point is inside the polygon
        inside = False
        p1x, p1y = polygon[0]
        for i in range(1, len(polygon) + 1):
            p2x, p2y = polygon[i % len(polygon)]
            if y > min(p1y, p2y) and y <= max(p1y, p2y) and x <= max(p1x, p2x) and p1y != p2y:
                x_intercept = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                if p1x == p2x or x <= x_intercept:
                    inside = not inside
            p1x, p1y = p2x, p2y

        return inside

    def move_to_center(self, dt):
        x, y = self.circle.pos
        dx = (self.p3[0] - x - 10)
        dy = (self.p3[1] - y - 10)
        magnitude = sqrt(dx ** 2 + dy ** 2)
        if magnitude > 0:
            dx /= magnitude
            dy /= magnitude
        dx *= self.speed
        dy *= self.speed
        self.circle.pos = (x + dx, y + dy)

        c = (x + dx + 10, y + dy + 10)
        self.test = self.is_point_inside_polygon(c, self.polygons[-1])
        # if (self.test): Clock.unschedule(self.move_to_center)

    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        x, y = self.circle.pos

        if text == 'a':
            dx = -10
            dy = 0
        elif text == 'd':
            dx = 10
            dy = 0
        else:
            return False
        
        if text == 'o':
            Clock.schedule_interval(self.move_to_center, 1.0/60.0)

        self.circle.pos = (x + dx, y + dy)

class MyLabel(Label):
    def __init__(self, data, **kwargs):
        super().__init__(**kwargs)
        self.counter = 0
        self.size_hint = (1, 0.1)
        Clock.schedule_interval(self.update_text, 1/60)
        self.data = data

    def update_text(self, dt):
        self.counter += 1
        self.text = str(self.data.test)

class RadarChartApp(App):
    def build(self):
        box = BoxLayout(orientation="vertical")
        
        game = RadarChartWidget()

        self.label = MyLabel(game)
        box.add_widget(self.label)

        box.add_widget(game)
        Clock.schedule_interval(game.move_to_center, 1.0/60.0)
        
        return box


if __name__ == '__main__':
    RadarChartApp().run()

