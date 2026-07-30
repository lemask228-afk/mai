from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
import math


board = [" " for _ in range(9)]

PLAYER = "X"
ROBOT = "O"


def winner(b):
    wins = [
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    ]

    for a,b1,c in wins:
        if b[a] == b[b1] == b[c] != " ":
            return b[a]

    if " " not in b:
        return "Draw"

    return None


def minimax(b, max_player):

    r = winner(b)

    if r == ROBOT:
        return 1
    if r == PLAYER:
        return -1
    if r == "Draw":
        return 0

    if max_player:
        best = -999

        for i in range(9):
            if b[i] == " ":
                b[i] = ROBOT
                best = max(best, minimax(b, False))
                b[i] = " "

        return best

    else:
        best = 999

        for i in range(9):
            if b[i] == " ":
                b[i] = PLAYER
                best = min(best, minimax(b, True))
                b[i] = " "

        return best


def robot_play():

    best = -999
    move = 0

    for i in range(9):
        if board[i] == " ":
            board[i] = ROBOT
            score = minimax(board, False)
            board[i] = " "

            if score > best:
                best = score
                move = i

    board[move] = ROBOT
    return move



class TicTacToe(App):

    def build(self):

        self.buttons = []

        layout = BoxLayout(
            orientation="vertical"
        )

        self.label = Label(
            text="You: X   Robot: O",
            font_size=25
        )

        layout.add_widget(self.label)


        grid = GridLayout(
            cols=3
        )

        for i in range(9):

            b = Button(
                font_size=50
            )

            b.bind(
                on_press=lambda x, i=i:self.play(i)
            )

            self.buttons.append(b)
            grid.add_widget(b)


        layout.add_widget(grid)


        reset = Button(
            text="Restart",
            size_hint_y=.2
        )

        reset.bind(
            on_press=self.reset
        )

        layout.add_widget(reset)

        return layout


    def play(self,index):

        if board[index] == " ":

            board[index]="X"
            self.buttons[index].text="X"


            if self.check():
                return


            move=robot_play()

            self.buttons[move].text="O"


            self.check()


    def check(self):

        r=winner(board)

        if r:

            Popup(
                title="Game",
                content=Label(text=r+" wins"),
                size_hint=(.6,.3)
            ).open()

            self.reset(None)

            return True


        return False


    def reset(self,button):

        for i in range(9):
            board[i]=" "
            self.buttons[i].text=""


TicTacToe().run()
