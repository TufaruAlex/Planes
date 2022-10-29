from src.repository.repository import *


class Services:
    def __init__(self, repository):
        self.repository = repository
    # getters for the matrices

    def get_player_board_matrix(self):
        return self.repository.player_board.player_board_matrix

    def get_player_tracking_matrix(self):
        return self.repository.player_board.tracking_board_matrix

    def get_computer_board_matrix(self):
        return self.repository.computer_board.player_board_matrix

    def get_computer_tracking_matrix(self):
        return self.repository.computer_board.tracking_board_matrix

    def place_plane(self, cockpit_coordinates, tail_coordinates):
        """
        the function checks if the plane is valid and if so, it adds it to the board
        :param cockpit_coordinates: the cockpit coordinates from the player input
        :param tail_coordinates: the tail coordinates from the player input
        """
        if cockpit_coordinates[0] != tail_coordinates[0] and cockpit_coordinates[1] != tail_coordinates[1]:
            raise PlaneError("Invalid coordinates")
        if cockpit_coordinates[0] == tail_coordinates[0]:
            if abs(cockpit_coordinates[1] - tail_coordinates[1]) != 3:
                raise PlaneError("Plane length must be 4 cells")
        else:
            if abs(cockpit_coordinates[0] - tail_coordinates[0]) != 3:
                raise PlaneError("Plane length must be 4 cells")
        plane_to_place = Plane(cockpit_coordinates, tail_coordinates)
        for cell in plane_to_place.cells_occupied:
            if self.get_player_board_matrix()[cell[0]][cell[1]] != 0:
                raise PlaneError("Planes cannot overlap")
            if cell[0] not in range(0, 10) or cell[1] not in range(0, 10):
                raise PlaneError("Plane is out of bounds")
        self.repository.add_plane(plane_to_place, self.repository.player_board)

    def place_computer_planes(self):
        """
        the function places the planes generated on the board
        """
        for plane in self.repository.computer_planes_list:
            self.repository.add_plane(plane, self.repository.computer_board)

    def player_round(self, target_coordinates):
        """
        the function checks for the state of the cell shot by the player and returns a certain value for each case
            -1 if the cell is empty
            1 if the cell has a part of the plane other than the cockpit
            2 if the cell has the cockpit of a ship
        then it updates the board accordingly
        :param target_coordinates: the coordinates of the cell targeted by the player
        :return:
        """
        if self.get_player_tracking_matrix()[target_coordinates[0]][target_coordinates[1]] != 0:
            raise BoardError("Target already hit. Try again")
        if self.get_computer_board_matrix()[target_coordinates[0]][target_coordinates[1]] == 0:
            self.get_player_tracking_matrix()[target_coordinates[0]][target_coordinates[1]] = -1
            return -1
        elif self.get_computer_board_matrix()[target_coordinates[0]][target_coordinates[1]] == 1:
            self.get_player_tracking_matrix()[target_coordinates[0]][target_coordinates[1]] = 1
            return 1
        else:
            for plane in self.repository.computer_planes_list:
                if plane.cockpit_coordinates == target_coordinates:
                    for cell in plane.cells_occupied:
                        self.get_player_tracking_matrix()[cell[0]][cell[1]] = 1
                    self.repository.remove_plane(plane, "computer_board")
            return 2

    def computer_round(self, target_coordinates):
        """
        the function checks for the state of the cell shot by the player and returns a certain value for each case:
            -1 if the cell is empty
            the coordinates of the cell if it has a part of the plane other than the cockpit
            2 if the cell has the cockpit of a ship
        then it updates the board accordingly
        :param target_coordinates:
        :return:
        """
        if self.get_player_board_matrix()[target_coordinates[0]][target_coordinates[1]] == 0:
            self.get_computer_tracking_matrix()[target_coordinates[0]][target_coordinates[1]] = -1
            self.get_player_board_matrix()[target_coordinates[0]][target_coordinates[1]] = -1
            return -1
        elif self.get_player_board_matrix()[target_coordinates[0]][target_coordinates[1]] == 1:
            self.get_computer_tracking_matrix()[target_coordinates[0]][target_coordinates[1]] = 1
            self.get_player_board_matrix()[target_coordinates[0]][target_coordinates[1]] = -2
            return target_coordinates
        else:
            for plane in self.repository.player_planes_list:
                if plane.cockpit_coordinates == target_coordinates:
                    for cell in plane.cells_occupied:
                        self.get_computer_tracking_matrix()[cell[0]][cell[1]] = 1
                        self.get_player_board_matrix()[cell[0]][cell[1]] = -2
                    self.repository.remove_plane(plane, "player_board")
            return 2

    def end_game(self):
        """
        the function checks if any of the players has any ships left. If one of them doesn't have any ships left it
        returns the winner
        :return: None if both players have at least one ship left and the name of the winner if the other player
        doesn't have any ships left
        """
        if not self.repository.player_planes_list:
            winner = "computer"
            return winner
        elif not self.repository.computer_planes_list:
            winner = "player"
            return winner
        else:
            return None
