from src.services.services import *
import random


class AI:
    def __init__(self, repository):
        self.computer_board = repository.computer_board
        self.services = Services(repository)

    def random_move(self):
        """
        the function generates a random cell which was not hit before
        :return: the coordinates of the cell chosen
        """
        target_coordinates = (random.randrange(self.computer_board.height), random.randrange(self.computer_board.width))
        while self.computer_board.tracking_board_matrix[target_coordinates[0]][target_coordinates[1]] != 0:
            target_coordinates = (random.randrange(self.computer_board.height),
                                  random.randrange(self.computer_board.width))
        return target_coordinates

    @staticmethod
    def go_left(coordinates):
        return coordinates[0], coordinates[1] - 1

    @staticmethod
    def go_right(coordinates):
        return coordinates[0], coordinates[1] + 1

    @staticmethod
    def go_up(coordinates):
        return coordinates[0] - 1, coordinates[1]

    @staticmethod
    def go_down(coordinates):
        return coordinates[0] + 1, coordinates[1]

    def valid_coordinates(self, coordinates):
        """
        checks if the given coordinates are on the board
        :param coordinates: the coordinates to be tested
        """
        return coordinates[0] in range(self.computer_board.height) and coordinates[1] in \
               range(self.computer_board.width)

    def found_plane(self, hit_coordinates, direction):
        """
        :param hit_coordinates: the coordinates of a cell with a plane on it
        :param direction: the direction in which the function calculates the adjacent cell
        :return: the coordinates of the adjacent cell
        """
        if direction == "left":
            if self.valid_coordinates(self.go_left(hit_coordinates)):
                return self.go_left(hit_coordinates)
        elif direction == "right":
            if self.valid_coordinates(self.go_right(hit_coordinates)):
                return self.go_right(hit_coordinates)
        elif direction == "up":
            if self.valid_coordinates(self.go_up(hit_coordinates)):
                return self.go_up(hit_coordinates)
        elif direction == "down":
            if self.valid_coordinates(self.go_down(hit_coordinates)):
                return self.go_down(hit_coordinates)
        return None

    def pattern(self):
        """
        the function does a random move and if it hits something, it tries to hit a random adjacent cell until it misses
        :return:
        """
        first_move = self.services.computer_round(self.random_move())
        if type(first_move) != tuple:
            if first_move < 0:
                return
            elif first_move == 2:
                self.pattern()
        else:
            directions = ["left", "right", "up", "down"]
            random_direction = random.choice(directions)
            next_move = self.services.computer_round(self.found_plane(first_move, random_direction))
            while type(next_move) == tuple:
                hit_coordinates = next_move
                random_direction = random.choice(directions)
                next_move = self.services.computer_round(self.found_plane(hit_coordinates, random_direction))
            if next_move < 0:
                return
            elif next_move == 2:
                self.pattern()
