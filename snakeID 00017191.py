# <Ilyosov Abbos 00017191>
# <python snake game>

from tkinter import *
import random

# <Creating global variables for the snake game>
# <choosing the screen width>
snake__width = 800

# <choosing the height of the screen>
snake__height = 600

# <Snake Cell Size>
snake__size = 20

# <The variable responsible for the state of the game>
go__snake = True


# <Auxiliary function of the game>
def create_block():
    """ Creating food for the snake """
    global BLOCK
    posx = snake__size * random.randint(1, (snake__width - snake__size) / snake__size)
    posy = snake__size * random.randint(1, (snake__height - snake__size) / snake__size)
    BLOCK = c.create_oval(posx, posy,
                          posx + snake__size, posy + snake__size,
                          fill="red")


# <Scoring points>
class Score(object):

    # <the function of displaying glasses on the screen>
    def __init__(self):
        self.score = 0
        # <horizontally>
        self.x = 700
        # <vertically>
        self.y = 30
        c.create_text \
            (self.x, self.y, text=" Game score: {}".format(self.score), font="Arial 14",
                      fill="Red", tag="score", state='hidden')

    # <scoring function and display on the screen>
    def increment(self):
        c.delete("score")
        self.score += 1
        c.create_text\
            (self.x, self.y, text=" Game score: {}".format(self.score), font="Arial 14",
                      fill="Red", tag="score")

    # <the function of resetting points at the start of a new game>
    def reset(self):
        c.delete("score")
        self.score = 0


# <A function for controlling the gameplay>
def main():
    """ We simulate the gameplay """
    global go__snake
    if go__snake:
        s.move()

        # <We determine the coordinates of the head>
        head_coords = c.coords(s.segments[-1].instance)
        x1, y1, x2, y2 = head_coords

        # <collisions with the edges of the playing field>
        if x2 > snake__width or x1 < 0 or y1 < 0 or y2 > snake__height:
            go__snake = False

        # <Eating an apple>
        elif head_coords == c.coords(BLOCK):
            s.add_segment()
            c.delete(BLOCK)
            create_block()

        # <Eating a snake>
        else:
            for index in range(len(s.segments) - 1):
                if head_coords == c.coords(s.segments[index].instance):
                    go__snake = False

        # <the larger the number, the slower the speed and vice versa>
        root.after(70, main)


    # <Don't go__snake -> stop the game and output messages>
    else:
        set_state(restart_text, 'normal')
        set_state(game_over_text, 'normal')
        set_state(close_but, 'normal')



class Segment(object):
    """ Snake Segment """

    def __init__(self, x, y):
        self.instance = c.create_rectangle(x, y,
                                           x + snake__size, y + snake__size,
                                           fill="purple")


class Snake(object):
    """ Snake Class """

    def __init__(self, segments):
        self.segments = segments

        # <Snake movement options>
        self.mapping = {"Down": (0, 1), "Right": (1, 0),
                        "Up": (0, -1), "Left": (-1, 0)}

        # <initiate the direction of the snake's movement>
        self.vector = self.mapping["Right"]

    def move(self):
        """ Move the snake in the specified direction """
        for index in range(len(self.segments) - 1):
            segment = self.segments[index].instance
            x1, y1, x2, y2 = c.coords(self.segments[index + 1].instance)
            c.coords(segment, x1, y1, x2, y2)

        x1, y1, x2, y2 = c.coords(self.segments[-2].instance)
        c.coords(self.segments[-1].instance,
                 x1 + self.vector[0] * snake__size, y1 + self.vector[1] * snake__size,
                 x2 + self.vector[0] * snake__size, y2 + self.vector[1] * snake__size)

    def add_segment(self):
        """ Adding a snake segment """
        score.increment()
        last_seg = c.coords(self.segments[0].instance)
        x = last_seg[2] - snake__size
        y = last_seg[3] - snake__size
        self.segments.insert(0, Segment(x, y))

    def change_direction(self, event):
        """ Changing the direction of movement of the snake """
        if event.keysym in self.mapping:
            self.vector = self.mapping[event.keysym]

    # <Snake update function at the start of a new game>
    def reset_snake(self):
        for segment in self.segments:
            c.delete(segment.instance)


# <function for message output>
def set_state(item, state):
    c.itemconfigure(item, state=state)
    c.itemconfigure(BLOCK, state='hidden')


# <Function for pressing a button 'new game'>
def clicked(event):
    global go__snake
    s.reset_snake()
    go__snake = True
    c.delete(BLOCK)
    score.reset()
    c.itemconfigure(restart_text, state='hidden')
    c.itemconfigure(game_over_text, state='hidden')
    c.itemconfigure(close_but, state='hidden')
    start_game()


# <Function for starting the game>
def start_game():
    global s
    create_block()
    s = create_snake()

    # Reacting to keystrokes
    c.bind("<KeyPress>", s.change_direction)
    main()


# <Creating segments and a snake>
def create_snake():
    segments = [Segment(snake__size, snake__size),
                Segment(snake__size * 2, snake__size),
                Segment(snake__size * 3, snake__size)]
    return Snake(segments)


# <exiting the game>
def close_win(root):
    exit()



# <Setting up the main window>
root = Tk()
root.title("Snake / Ilyosov Abbos 00017191")



# Creating an instance of the Canvas class
c = Canvas(root, width=snake__width, height=snake__height, bg="#F5F5DC")
c.grid()

# <Capturing the focus to catch keystrokes>
c.focus_set()

# <Text of the game result>
game_over_text = c.create_text(snake__width / 2, snake__height / 2,
         text="Player you lost! :)",
         font='Arial 50', fill='red',
         state='hidden')

# <The text of the start of a new game after a loss>
restart_text = c.create_text(snake__width / 2, snake__height - snake__height / 3,
         font='Arial 30',
         fill='LimeGreen',
         text="Start a new game",
         state='hidden')

# <The text of the exit from the program after the loss>
close_but = c.create_text(snake__width / 2, snake__height - snake__height / 5,
        font='Arial 27',
        fill='OrangeRed',
        text="Exit :(",
        state='hidden')

# <Testing events when buttons are pressed>
c.tag_bind(restart_text, "<Button-1>", clicked)
c.tag_bind(close_but, "<Button-1>", close_win)

# <Counting points>
score = Score()

# <Starting the game>
start_game()

# <launching the window>
root.mainloop()