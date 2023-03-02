from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Rectangle, Line

from kivy.core.window import Window
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty, ListProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.uix.slider import Slider

from wind_directions import wind_directions

class WhiteBackgroundImage(Image):
    velocity_x = 0
    velocity_y = 0.2

    color = ListProperty([1, 0, 0, 1])
    trail_width = 3
    trail_color = [0, 0, 0, 0.5]
    max_trail_length = 10

    last_x, last_y = 0, 0

    wind_value = 0.2

    offset_x = 1
    offset_y = 1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)

        self.trail = []

        # Create a new Canvas with a white background
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)
            Color(1, 0, 0)
            self.circle = Ellipse(pos=(0, 0), size=(20, 20))

            self.circle2 = Ellipse(pos=(0, 0), size=(20, 20))
            print(self.get_position_from_dic("SE"))
            self.circle2.pos = self.get_position_from_dic("SSE")

            self.circle3 = Ellipse(pos=(0, 0), size=(20, 20))
            self.circle4 = Ellipse(pos=(0, 0), size=(20, 20))

            # self.canvas.add(Color(*self.color))

        # Update the size and position of the white Rectangle when the Image is resized or repositioned
        self.bind(pos=self.update_rect, size=self.update_rect)

    def get_position_from_dic(self, direction):
        value = wind_directions[direction]
        w, h = self.size
        x, y = self.circle.size
        offsetX = x
        offsetY = y
        if value[0] != 0: offsetX = x - w/value[0]
        if value[1] != 0: offsetY = y - h/value[1]

        self.circle.pos = (0.5 * w - 25 + offsetX, 0.5 * h - 25 + offsetY)
        return (0.5 * w - 25 + offsetX, 0.5 * h - 25 + offsetY)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

        self.get_position_from_dic("NW")
        # self.get_circle_pos()

    def update_offset_x(self, instance, slider_value):
        self.offset_x = slider_value
        # print(self.offset_x)

        self.get_circle_pos()

    def update_offset_y(self, instance, slider_value):
        self.offset_y = slider_value
        # print(self.offset_y)

        self.get_circle_pos()

    def get_circle_pos(self):
        w, h = self.size
        x, y = self.circle.size
        offsetX = x
        offsetY = y
        if self.offset_x != 0: offsetX = x - w/self.offset_x
        if self.offset_y != 0: offsetY = y - h/self.offset_y

        # offsetX = x
        # offsetY = y - h/-2.6041666666666714
        self.circle.pos = (0.5 * w - 25 + offsetX, 0.5 * h - 25 + offsetY)
        print(0.5 * w - 25 + offsetX, 0.5 * h - 25 + offsetY)
        return (0.5 * w - 25 + offsetX, 0.5 * h - 25 + offsetY)
    
    def update(self, dt):
        # self.move()
        pass

    def move(self):
        # self.circle.pos = Vector(self.velocity_x, self.velocity_y) + self.circle.pos
        
        new_pos = Vector(self.velocity_x + self.wind_value, self.velocity_y) + self.circle.pos
        x, y = self.circle.size
        if len(self.trail) > self.max_trail_length:
            self.canvas.remove(self.trail.pop(0))
        self.trail.append(Line(points=[new_pos[0]+x/2, new_pos[1]+y/2, self.circle.pos[0]+x/2, self.circle.pos[1]+y/2],
                                width=self.trail_width, cap='round', joint='round', close=False, dash_length=0,
                                dash_offset=0, dash_inline=False, dash_round=False, dash_cap='none',
                                dash_join='miter', dash_precision=10, dash_width=1.0,
                                dash_scale=1.0, dash_phase=0.0, color=(1, 1, 0)))
        
        for i in range(0, len(self.trail)):
            self.canvas.add(self.trail[i])

        self.circle.pos = new_pos

    def on_touch_down(self, touch, *args):
        self.last_x = touch.x
    
    def on_touch_up(self, touch, *args):
        self.velocity_x = 0
    
    def on_touch_move(self, touch):
        delta_x = touch.x - self.last_x
        delta_y = touch.y - self.last_y
        if (abs(delta_x) > 1):
            self.velocity_x = delta_x
        else:
            self.velocity_x = 0
        # print(delta_x, delta_y)
        self.last_x = touch.x
        self.last_y = touch.y

    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        if text == 'a':
            self.velocity_x = -1
            self.circle.pos = Vector(self.velocity_x, self.velocity_y) + self.circle.pos
            self.velocity_x = 0
        if text == 'd':
            self.velocity_x = 1
            self.circle.pos = Vector(self.velocity_x, self.velocity_y) + self.circle.pos
            self.velocity_x = 0
        if text == 'q':
            print("x", self.offset_x)
            print("y", self.offset_y)

class MyKivyApp(App):
    def build(self):
        game = WhiteBackgroundImage(source="board.png")
        Clock.schedule_interval(game.update, 1.0/60.0)

        sx = Slider(min=-100, max=100, value=0, size_hint=(1, 0.1))
        sx.bind(value=game.update_offset_x)
        sy = Slider(min=-100, max=100, value=0, size_hint=(1, 0.1))
        sy.bind(value=game.update_offset_y)

        box = BoxLayout(orientation="vertical")
        box.add_widget(sx)
        box.add_widget(sy)
        box.add_widget(game)
        
        
        return box

    def on_enter(instance, value):
        print('User pressed enter in', value.text)

if __name__ == '__main__':
    MyKivyApp().run()