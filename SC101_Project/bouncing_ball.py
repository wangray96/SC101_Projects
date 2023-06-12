"""
File: bouncing_ball.py
Name: Sophia
-------------------------
This program simulates a bouncing ball at (START_X, START_Y)
that has VX as x velocity, vy as y velocity, and 1 as GRAVITY.
Each bounce reduces y velocity to REDUCE of itself.
The bouncing process starts when the mouse is clicked for the
first time, and it ends when the ball horizontally bounces out
of the window. The ball will move back to (START_X, START_Y)
at the end of each process. The bouncing process can only be
executed 3 times.
"""

from campy.graphics.gobjects import GOval
from campy.graphics.gwindow import GWindow
from campy.gui.events.timer import pause
from campy.gui.events.mouse import onmouseclicked

VX = 3
GRAVITY = 1
REDUCE = 0.9
DELAY = 10
SIZE = 20
START_X = 30
START_Y = 40

# Global Variables
window = GWindow(800, 500, title='bouncing_ball.py')
ball = GOval(SIZE, SIZE, x=START_X, y=START_Y)
is_first_click = True
process = 0


def main():
    """
    This program simulates the bouncing process of the ball
    when the user clicks the mouse for the first time. The
    bouncing process will be executed three times.
    """
    ball.filled = True
    window.add(ball)
    onmouseclicked(action)


def action(mouse):
    """
    This function starts the bouncing process if the mouse
    is clicked for the 1st time and the process is executed
    less than or equal three times.
    """
    global is_first_click, process
    if is_first_click is True:
        is_first_click = False
        process += 1
        if process <= 3:
            bouncing()


def bouncing():
    """
    This function stimulates the bouncing process of the ball.
    """
    global is_first_click
    vy = 0
    hit = 0  # Counting the times the ball hitting the ground.
    while True:
        if ball.x < window.width:
            ball.move(VX, vy)
            if ball.y + SIZE < window.height:
                hit = 0
            if ball.y + SIZE >= window.height:
                hit += 1
                if hit == 1:
                    vy = - vy * REDUCE  # Bouncing.
                else:  # The ball still hits the ground after bouncing.
                    dist = (ball.y + SIZE) - window.height
                    ball.move(0, -dist)
                    hit = 0
                    vy -= GRAVITY  # Offsetting the effect of hitting twice.
            vy += GRAVITY
            pause(DELAY)
        else:
            # The ball moves back to (START_X, START_Y).
            window.add(ball, x=START_X, y=START_Y)
            # Turning is_first_click into True to start the next round.
            is_first_click = True
            return is_first_click


if __name__ == "__main__":
    main()
