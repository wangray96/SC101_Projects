"""
File: breakoutgraphics.py
Name: Ray
-----------------------------
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman, 
and Jerry Liao

This program executes breakout game. If the user click the
mouse for the 1st time each round, the game starts. If the
ball falls to the ground, lives deducts one. The game will
end if there is no more lives or bricks.
"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import random

BRICK_SPACING = 5      # Space between bricks (in pixels). This space is used for horizontal and vertical spacing
BRICK_WIDTH = 40       # Width of a brick (in pixels)
BRICK_HEIGHT = 15      # Height of a brick (in pixels)
BRICK_ROWS = 10        # Number of rows of bricks
BRICK_COLS = 10        # Number of columns of bricks
BRICK_OFFSET = 50      # Vertical offset of the topmost brick from the window top (in pixels)
BALL_RADIUS = 10       # Radius of the ball (in pixels)
PADDLE_WIDTH = 75      # Width of the paddle (in pixels)
PADDLE_HEIGHT = 15     # Height of the paddle (in pixels)
PADDLE_OFFSET = 50     # Vertical offset of the paddle from the window bottom (in pixels)
INITIAL_Y_SPEED = 7    # Initial vertical speed for the ball
MAX_X_SPEED = 5        # Maximum initial horizontal speed for the ball


class BreakoutGraphics:
    def __init__(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH,
                 paddle_height=PADDLE_HEIGHT, paddle_offset=PADDLE_OFFSET,
                 brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS,
                 brick_width=BRICK_WIDTH, brick_height=BRICK_HEIGHT,
                 brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING,
                 title='Breakout'):

        # Create a graphical window, with some extra space
        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=window_width, height=window_height, title=title)

        # Create a paddle
        self.paddle = GRect(paddle_width, paddle_height)
        self.paddle.filled = True
        self.paddle_height = self.window.height - PADDLE_OFFSET
        self.window.add(self.paddle, (self.window.width - self.paddle.width) / 2, self.window.height - paddle_offset)

        # Center a filled ball in the graphical window
        self.ball = GOval(ball_radius * 2, ball_radius * 2)
        self.ball.filled = True
        self.original_x = self.window.width // 2 - ball_radius
        self.original_y = self.window.height // 2 - ball_radius
        self.window.add(self.ball, self.original_x, self.original_y)

        # Default initial velocity for the ball
        self.__dx = 0
        self.__dy = 0

        # Initialize our mouse listeners
        onmousemoved(self.paddle_moving)
        onmouseclicked(self.click)

        # Initialize variables
        self.count = 0
        self.brick_number = brick_rows * brick_cols
        self.starting = False

        # Draw bricks
        for i in range(brick_cols):
            for j in range(brick_rows):
                brick = GRect(brick_width, brick_height, x=(brick_width + brick_spacing) * i,
                              y=brick_offset + (brick_height + brick_spacing) * j)
                brick.filled = True
                if j // 2 == 0:
                    brick.fill_color = brick.color = 'red'
                elif j // 2 == 1:
                    brick.fill_color = brick.color = 'orange'
                elif j // 2 == 2:
                    brick.fill_color = brick.color = 'yellow'
                elif j // 2 == 3:
                    brick.fill_color = brick.color = 'green'
                else:
                    brick.fill_color = brick.color = 'blue'
                self.window.add(brick)

    def paddle_moving(self, mouse):
        """
        This function has the paddle move with its center following the mouse.
        :param mouse: the mouse event.
        :return: None
        """
        if self.paddle.width / 2 < mouse.x < self.window.width - self.paddle.width / 2:
            self.paddle.x = mouse.x - self.paddle.width / 2
        elif mouse.x < self.paddle.width / 2:  # To prevent the paddle from out-boarding the left side
            self.paddle.x = 0
        else:  # To prevent the paddle from out-boarding the right side
            self.paddle.x = self.window.width - self.paddle.width

    def click(self, event):
        """
        This function sets the velocity of the ball.
        :param event: the mouse event.
        :return: None
        """
        if not self.starting:
            self.starting = True
            self.__dx = random.randint(1, MAX_X_SPEED)
            self.__dy = INITIAL_Y_SPEED
            if random.random() > 0.5:
                self.__dx = -self.__dx

    def hit_ball_or_brick(self):
        """
        Detects whether the ball hits the paddle or any bricks.
        :return: None, This function uses return to end the loops.
        """
        for x in range(self.ball.x, self.ball.x+self.ball.width+1, self.ball.width):
            for y in range(self.ball.y, self.ball.y+self.ball.height+1, self.ball.height):
                maybe_object = self.window.get_object_at(x, y)
                if maybe_object is not None:
                    if maybe_object is self.paddle:
                        if self.__dy > 0:
                            self.__dy = -self.__dy
                    else:
                        self.window.remove(maybe_object)
                        self.__dy = -self.__dy
                        self.brick_number -= 1
                    return

    def restart(self):
        """
        This function resets the ball to its original position.
        :return: None
        """
        self.ball.x = self.original_x
        self.ball.y = self.original_y
        self.__dx = self.__dy = 0
        self.starting = False

    def get_dx(self):
        """
        Getter of dx.
        :return self.__dx: the value of private variable dx.
        """
        return self.__dx

    def get_dy(self):
        """
        Getter of dy.
        :return self.__dy: the value of private variable dy.
        """
        return self.__dy

    def set_dx(self, new_dx):
        """
        Setter function to update dx and bounce the ball.
        :param new_dx: the new dx value passed from the server side to the coder side.
        :return: None, this function does not return anything.
        """
        self.__dx = new_dx

    def set_dy(self, new_dy):
        """
        Setter function to update dy and bounce the ball.
        :param new_dy: the new dy value passed from the server side to the coder side.
        :return: None, this function does not return anything.
        """
        self.__dy = new_dy


