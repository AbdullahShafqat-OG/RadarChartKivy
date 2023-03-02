import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from random import randint
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.uix.widget import Widget
from enum import Enum
from kivy.lang import Builder

from player import Player
from compass_directions import CompassDirection

class WhiteBackgroundImage(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Create a new Canvas with a white background
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)

        # Update the size and position of the white Rectangle when the Image is resized or repositioned
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size



class MyApp(App):
    first_turn = True

    board_grid = [[0 for j in range(16)] for i in range(9)]
    board_grid_rain = [[0 for j in range(16)] for i in range(9)]
    board_grid_gui_u = [BoxLayout(orientation="vertical") for _ in range(16)]

    phases_gui = BoxLayout(orientation='horizontal', size_hint=(1, 0.3))

    def build(self):
        # Initialize players
        self.players = []
        for i in range(0, 6):
            name = f"Player {i+1}"
            player = Player(name)
            player.wind_direction = CompassDirection(i)
            self.players.append(player)
        
        # Initialize UI
        self.root = BoxLayout(orientation='vertical')
        self.current_player_index = 0
        self.current_player_label = Label(text=self.players[self.current_player_index].name, size_hint=(1, 0.1))
        self.current_phase = 1
        self.current_phase_label = Label(text=f'Phase {self.players[self.current_player_index].current_phase}', 
                                         color=[1, 0, 0], size_hint=(1, 0.1))
        self.rolling_info_label = Label(text="Helpful Text", color=[0, 1, 0], size_hint=(1, 0.1))
        self.rolled_number_label = Label(text="What you rolled", color=[1, 1, 0], size_hint=(1, 0.1))
        self.board = WhiteBackgroundImage(source="board.png")

        header_grid = BoxLayout(orientation="horizontal")
        for i in range(0, 16):
            header_grid.add_widget(Button(text=CompassDirection(i).name, size_hint=(1, 0.2)))
        for i in range(0, len(self.board_grid_gui_u)):
            for j in range(0, 9):
                self.board_grid_gui_u[i].add_widget(Button())

        self.random_rain_generator()
        self.phase1_gui()

        self.root.add_widget(self.current_player_label)
        self.root.add_widget(self.current_phase_label)
        self.root.add_widget(self.rolling_info_label)
        self.root.add_widget(self.board)
        self.root.add_widget(header_grid)
        parent = BoxLayout(orientation="horizontal")
        for box_layout in self.board_grid_gui_u:
            parent.add_widget(box_layout)
        self.root.add_widget(parent)
        self.root.add_widget(self.rolled_number_label)
        self.root.add_widget(self.phases_gui)

        return self.root

    def random_rain_generator(self):
        for i in range(0, len(self.board_grid_gui_u)):
            value = randint(-1, len(self.board_grid_gui_u[0].children) - 2)
            if value < 0: continue
            print(value)
            self.board_grid_gui_u[i].children[value].background_color = (0, 0, 1, 1)
            self.board_grid_gui_u[i].children[value+1].background_color = (1, 0, 0, 1)

            self.board_grid_rain[value][i] = 1

    def select_wind_direction(self, instance):
        # Update current player's score
        current_player = self.players[self.current_player_index]

        # Update current player label
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self.current_player_label.text = self.players[self.current_player_index].name

    def phase1_gui(self):
        print("PHASE 1")
        self.enter_phase()
        self.phases_gui.clear_widgets()

        btn1 = Button(text="Last Player Left")
        btn1.bind(on_press=self.phase1_btn)

        btn2 = Button(text="Last Player Direction")
        btn2.bind(on_press=self.phase1_btn)

        btn3 = Button(text="Last Player Right")
        btn3.bind(on_press=self.phase1_btn)

        btn4 = Button(text="Select a Card")

        self.phases_gui.add_widget(btn1)
        self.phases_gui.add_widget(btn2)
        self.phases_gui.add_widget(btn3)
        self.phases_gui.add_widget(btn4)

        self.update_wind_directions(btn1, btn2, btn3)

    def update_wind_directions(self, btn1, btn2, btn3):
        current_player = self.players[self.current_player_index]

        next_direction = current_player.wind_direction.next()
        prev_direction = current_player.wind_direction.prev()
            
        print(prev_direction, current_player.wind_direction,next_direction)

        # Update dice button text
        btn1.text = f"{current_player.wind_direction.name}"
        if not self.first_turn:
            btn2.text = f"{prev_direction.name}"
            btn3.text = f"{next_direction.name}"
        else:
            self.first_turn = False
            btn2.text = f"{current_player.wind_direction.name}"
            btn3.text = f"{current_player.wind_direction.name}"

    def phase1_btn(self, instance):
        current_player = self.players[self.current_player_index]
        next_player = self.players[(self.current_player_index + 1) % len(self.players)]

        direction = getattr(CompassDirection, instance.text)

        current_player.wind_direction = direction
        next_player.wind_direction = current_player.wind_direction

        current_player.row = 0
        current_player.col = direction.value
        
        self.update_board_grid(current_player.row, current_player.col)

        for row in self.board_grid:
            print(row)

        self.exit_phase()
        self.phase2_gui()

    def update_board_grid(self, row, col):
        self.board_grid[row][col] = self.current_player_index + 1
        self.board_grid_gui_u[col].children[row].text = f"{self.current_player_index + 1}"
        
    def phase2_gui(self):
        print("PHASE 2")
        self.enter_phase()
        self.phases_gui.clear_widgets()

        info_txt = "Roll at least 8 to reach dam"
        current_player = self.players[self.current_player_index]
        for row in self.board_grid_rain:
            print(row)
        for i in range(0, len(self.board_grid_rain[current_player.col])):
            if self.board_grid_rain[current_player.col][i] == 1:
                print("KJDFKJF", i)
                value = (8 - i) + 1
                info_txt = f"Roll at least {value} to continue turn"
                break
        
        self.rolling_info_label.text = info_txt

        btn1 = Button(text="Roll Green Die")
        btn1.bind(on_press=self.roll_green_die_phase2)

        self.phases_gui.add_widget(btn1)

    def phase3_gui(self):
        print("PHASE 3")
        self.enter_phase()
        self.phases_gui.clear_widgets()

        btn1 = Button(text="Roll Blue Die")
        btn1.bind(on_press=self.roll_die)
        btn2 = Button(text="Roll Red Die")
        btn2.bind(on_press=self.roll_die)

        self.phases_gui.add_widget(btn1)
        self.phases_gui.add_widget(btn2)

    def phase4_gui(self):
        print("PHASE 4")
        self.enter_phase()
        self.phases_gui.clear_widgets()

        btn1 = Button(text="Roll Green Die")
        btn1.bind(on_press=self.roll_green_die_phase4)

        self.phases_gui.add_widget(btn1)

    def roll_green_die_phase2(self, instance):
        #print(randint(1, 6))
        self.rolled_number_label.text = f"Green Die: {randint(1, 6)}"

        self.exit_phase()
        self.phase3_gui()

    def roll_green_die_phase4(self, instance):
        # print(randint(1, 6))
        self.rolled_number_label.text = f"Green Die: {randint(1, 6)}"

        self.exit_phase()
        self.phase1_gui()

    def roll_die(self, instance):
        # print(randint(1, 6))
        self.rolled_number_label.text = f"{instance.text}: {randint(1, 6)}"
        self.phases_gui.remove_widget(instance)

        if len(self.phases_gui.children) <= 0:
            self.exit_phase()
            self.phase4_gui()

    def enter_phase(self):
        current_player = self.players[self.current_player_index]
        print("phase", current_player.current_phase)
        self.current_phase_label.text = f"Phase {current_player.current_phase}"
        self.current_player_label.text = self.players[self.current_player_index].name

    def exit_phase(self):
        current_player = self.players[self.current_player_index]
        current_player.current_phase += 1
        if current_player.current_phase > 4:
            current_player.current_phase = 1
            self.current_player_index = (self.current_player_index + 1) % len(self.players)

if __name__ == '__main__':
    MyApp().run()
