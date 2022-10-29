from src.domain.domain import *
import random


class Repository:
    def __init__(self):
        self.player_board = Board()
        self.computer_board = Board()
        self.player_planes_list = []
        self.computer_planes_list = generate_planes()

    def add_plane(self, plane, board):
        """
        adds a plane to the specified board
        :param plane: the plane to be added
        :param board: the board to which the plane is added. If the board is the player's, it also adds it to the player
        planes list
        """
        self.player_planes_list.append(plane)
        for cell in plane.cells_occupied:
            board.player_board_matrix[cell[0]][cell[1]] = 1
        board.player_board_matrix[plane.cockpit_coordinates[0]][plane.cockpit_coordinates[1]] += 1

    def remove_plane(self, plane_to_remove, board):
        """
        removes a plane from the specified planes list
        :param plane_to_remove: the plane to be removed
        :param board: the board from which the plane is. the plane will be removed from the board's plane list, not the
        board itself
        """
        if board == "player_board":
            for i in range(len(self.player_planes_list)):
                if self.player_planes_list[i] == plane_to_remove:
                    del self.player_planes_list[i]
                    break
        else:
            for i in range(len(self.computer_planes_list)):
                if self.computer_planes_list[i] == plane_to_remove:
                    del self.computer_planes_list[i]
                    break


def generate_planes():
    """
    the function generates a list of 3 valid planes
    :return: the list of generated planes
    """
    planes_list = []
    occupied_cells = []
    while len(planes_list) < 3:
        orientation = random.randint(0, 1)
        if orientation == 0:
            cockpit_coordinates = (random.randint(2, 7), random.randint(0, 9))
            if cockpit_coordinates in occupied_cells:
                while cockpit_coordinates[0] == cockpit_coordinates[1] and cockpit_coordinates in occupied_cells:
                    cockpit_coordinates = (random.randint(2, 7), random.randint(0, 9))
            if cockpit_coordinates[1] > 6:
                tail_coordinates = (cockpit_coordinates[0], cockpit_coordinates[1] - 3)
            elif cockpit_coordinates[1] < 3:
                tail_coordinates = (cockpit_coordinates[0], cockpit_coordinates[1] + 3)
            else:
                sign = random.choice(["+", "-"])
                if sign == "+":
                    tail_coordinates = (cockpit_coordinates[0], cockpit_coordinates[1] + 3)
                else:
                    tail_coordinates = (cockpit_coordinates[0], cockpit_coordinates[1] - 3)
        else:
            cockpit_coordinates = (random.randint(0, 9), random.randint(2, 7))
            if cockpit_coordinates[0] == cockpit_coordinates[1] or cockpit_coordinates in occupied_cells:
                while cockpit_coordinates[0] == cockpit_coordinates[1] and cockpit_coordinates in occupied_cells:
                    cockpit_coordinates = (random.randint(0, 9), random.randint(2, 7))
            if cockpit_coordinates[0] > 6:
                tail_coordinates = (cockpit_coordinates[0] - 3, cockpit_coordinates[1])
            elif cockpit_coordinates[0] < 3:
                tail_coordinates = (cockpit_coordinates[0] + 3, cockpit_coordinates[1])
            else:
                sign = random.choice(["+", "-"])
                if sign == "+":
                    tail_coordinates = (cockpit_coordinates[0] + 3, cockpit_coordinates[1])
                else:
                    tail_coordinates = (cockpit_coordinates[0] - 3, cockpit_coordinates[1])
        plane = Plane(cockpit_coordinates, tail_coordinates)
        cell_already_occupied = False
        for cell in plane.cells_occupied:
            if cell in occupied_cells:
                cell_already_occupied = True
        if not cell_already_occupied:
            planes_list.append(plane)
            for cell in plane.cells_occupied:
                occupied_cells.append(cell)
    return planes_list
