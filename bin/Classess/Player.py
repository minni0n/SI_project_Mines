# WINDOW_X = 533 + 1200
# WINDOW_Y = 950
# FRAME_WIDTH = 533
# FRAME_HEIGHT = 533
#
# # Size of small image
# IMAGE_SIZE = 50

from resources.Globals import *


class Player(object):
    def __init__(self):
        self.x_start = 5
        self.y_start = 5
        self.current_x = self.x_start
        self.current_y = self.y_start
        self.step = IMAGE_SIZE + self.x_start
        self.current_array_x = 0
        self.current_array_y = 0
        self.direction = "east"
        self.directions = ["north", "east", "south", "west"]
        self.arrow_north_image = None
        self.arrow_south_image = None
        self.arrow_west_image = None
        self.arrow_east_image = None
        self.image_canvas_id = None

    def MovingRight(self):
        if self.current_x + self.step < FRAME_WIDTH:
            self.current_x += self.step
            self.current_array_x += 1

    def MovingLeft(self):
        if self.current_x - self.step >= self.x_start:
            self.current_x -= self.step
            self.current_array_x -= 1

    def MovingUp(self):
        if self.current_y - self.step >= self.y_start:
            self.current_y -= self.step
            self.current_array_y -= 1

    def MovingDown(self):
        if self.current_y + self.step < FRAME_HEIGHT:
            self.current_y += self.step
            self.current_array_y += 1

    def Moving(self):
        if self.direction == "north":
            self.MovingUp()
        if self.direction == "south":
            self.MovingDown()
        if self.direction == "west":
            self.MovingLeft()
        if self.direction == "east":
            self.MovingRight()
