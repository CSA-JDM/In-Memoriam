# Jacob Meadows
# 4th Period, Computer Programming
# April 16th, 2018
"""
This will be taking place over the next few weeks, with minor reviews put in place at the end of each week.
You will also have to show me progress each week on the program.
You are welcome to use research, but I will not be able to answer very specific questions
(this is a review, I can't reteach you things you should already know).
I need a proposal from you in regards what you want to do with Python.
This will need to cover everything we have done this year (from simple printing to loops to classes and reading/writing
files).
Of course a common one is simple games, but ones that are useful in everyday life would be great too
(maybe terminal programs to reserve airplanes or rental cars, inventory/cash register, etc).
This proposal must be completed BEFORE class on Wednesday.
You can ask me ideas for what to do, you can ask each other as well.
Look online for ideas as well.
Proposal should be professional, slide show with examples.
Must be an in depth description of what you want to do, why, what it will do, and how it is a useful program.
It will also need a time line of what you will have done and when.
"""
import Canvas_Objects
import Game_Sequences
import turtle
import time
import random
import mp3play


class App:
    def __init__(self):
        # Root Initialization
        self.root = turtle._Root()
        self.root.config(width=1280, height=720)
        self.root.bind("<Escape>", lambda args: self.root.destroy())
        self.root.title("In Memoriam")

        # Canvas Initialization
        self.canvas = turtle.Canvas(self.root)
        self.canvas.config(width=1280, height=720, background="white")
        self.canvas.place(x=0, y=0)

        # Audio Initialization
        sayo_nara = Audio(self.root, r"..\Final-Project\Sayo-nara.mp3")
        sayo_nara.play(loop=True)

        # Item Dictionaries
        self.buttons = {}
        self.text_boxes = {}
        self.text_inputs = {}

        # Time Text Box Initialization
        current_time = time.localtime()
        self.text_boxes["time_text_box"] = Canvas_Objects.TextBox(
            self.canvas, x=1140, y=650, length=140, height=65,
            text=f"  {current_time[3]}:{current_time[4]}:{current_time[5]}\n"
                 f"{current_time[1]}/{current_time[2]}/{current_time[0]}"
        )

        # Main Sequence
        self.menu()
        self.time_update()
        self.root.mainloop()

    def time_update(self):
        current_time = list(time.localtime()[:6])
        if len(str(current_time[3])) < 2:
            current_time[3] = "0" + str(current_time[3])
        if len(str(current_time[4])) < 2:
            current_time[4] = "0" + str(current_time[4])
        if len(str(current_time[5])) < 2:
            current_time[5] = "0" + str(current_time[5])
        if len(str(current_time[1])) < 2:
            current_time[1] = "0" + str(current_time[1])
            if len(str(current_time[2])) < 2:
                current_time[2] = "0" + str(current_time[2])
        self.text_boxes["time_text_box"].update(
            text=f"  {current_time[3]}:{current_time[4]}:{current_time[5]}\n"
                 f"{current_time[1]}/{current_time[2]}/{current_time[0]}"
        )
        self.root.after(1, self.time_update)

    def menu(self):
        self.clear_all()
        self.text_boxes["title_text_box"] = Canvas_Objects.TextBox(self.canvas, x=10, y=10, text="In Memoriam",
                                                                   font=("Times New Roman", 30, "bold"))
        self.buttons["new_game_button"] = Canvas_Objects.Button(self.canvas, x=10, y=110, length=130, height=35,
                                                                text="New Game", command=self.username)
        self.buttons["load_game_button"] = Canvas_Objects.Button(self.canvas, x=10, y=185, length=135, height=35,
                                                                 text="Load Game", command=None)
        self.buttons["quit_button"] = Canvas_Objects.Button(self.canvas, x=10, y=260, length=60, height=35, text="Quit",
                                                            command=lambda event: self.root.destroy())

    def username(self, *args):
        self.clear_all()
        self.text_boxes["title_text_box"] = Canvas_Objects.TextBox(self.canvas, x=10, y=30, text="Username:",
                                                                   font=("Times New Roman", 20, "normal"))
        self.text_inputs["username_text_input"] = Canvas_Objects.TextInput(
            self.canvas, x=145, y=30, length=500, height=35,
            command=lambda event: [self.main_sequence(),
                                   setattr(self.text_inputs["username_text_input"], "active", False)])
        self.buttons["back_button"] = Canvas_Objects.Button(self.canvas, x=10, y=680, length=65, height=35, text="Back",
                                                            command=lambda event: [
                                                                self.menu(), setattr(
                                                                    self.text_inputs["username_text_input"], "active",
                                                                    False)])
        self.buttons["load_game_button"].update(x=920, y=680)
        self.buttons["quit_button"].update(x=1065, y=680)

    def main_sequence(self):
        self.clear_all()
        self.main_user_input = Game_Sequences.MainSequence(self.canvas, 10, 10,
                                                           self.text_inputs['username_text_input'].text,
                                                           self.buttons)
        self.buttons["load_game_button"].update()
        self.buttons["quit_button"].update()

    def clear_all(self):
        self.canvas.delete("all")
        self.canvas.unbind("<Motion>")
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind_all("<Key>")
        self.canvas.unbind_all("<Return>")

    def save(self):
        pass


class Character:
    def __init__(self, main_sequence, type_):
        self.main_sequence = main_sequence
        self.type = type_
        self.character_type = {
            "Player": {
                "Health": 100,
                "Mana": 20,
                "Items": self.main_sequence.inventory,
                "Agility": 5,
                "Attack": 5,
                "Defense": 5,
                "Luck": 2
            },
            "NPC": {},
            "Boss": {},
            "Enemy": {
                "Health": 100,
                "Mana": 10,
                "Items": None,
                "Agility": 5,
                "Attack": 5,
                "Defense": 5,
                "Luck": 2
            }
        }

        self.health = self.character_type[self.type]["Health"]
        self.mana = self.character_type[self.type]["Mana"]
        self.items = self.character_type[self.type]["Items"]
        self.agility = self.character_type[self.type]["Agility"]
        self.attack = self.character_type[self.type]["Attack"]
        self.defense = self.character_type[self.type]["Defense"]
        self.luck = self.character_type[self.type]["Luck"]


class Enemy(Character):
    def __init__(self, main_sequence, name):
        super().__init__(main_sequence, "Enemy")
        self.name = name
        self.text_boxes = {
            "name_text_box":
                Canvas_Objects.TextBox(self.main_sequence.canvas, x=10, y=10, length=445, height=35,
                                       text=f"Name: {self.name}"),
            "health_bar_text_box":
                Canvas_Objects.TextBox(self.main_sequence.canvas, x=10, y=60, length=445, height=35,
                                       text="Health:"),
            "mana_bar_text_box":
                Canvas_Objects.TextBox(self.main_sequence.canvas, x=465, y=60, length=445, height=35,
                                       text="Mana:")
        }

        self.health_bar = self.text_boxes["health_bar_text_box"].make_line(93, 77, 445, 77, fill="red")
        self.health_bar_meter = 352

        self.mana_bar = self.text_boxes["mana_bar_text_box"].make_line(535, 77, 900, 77, fill="blue")

    def enemy_game_over(self):
        for x in self.text_boxes:
            self.main_sequence.canvas.delete(self.text_boxes[x].text_item)
            self.main_sequence.canvas.delete(self.text_boxes[x].rect_item)
        self.main_sequence.canvas.delete(self.health_bar)
        self.main_sequence.canvas.delete(self.mana_bar)


class Audio:
    def __init__(self, root, file):
        self.root = root
        self.file = mp3play.load(file)
        self.loop = True

    def play(self, loop=None):
        if loop is not None:
            self.loop = loop
        self.file.play()
        if self.loop:
            self.root.after(157000, self.play)


if __name__ == "__main__":
    session = App()
    session.save()
