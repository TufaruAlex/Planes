import texttable


class PlaneError(Exception):
    pass


class BoardError(Exception):
    pass


class Plane:
    def __init__(self, cockpit_coordinates, tail_coordinates):
        """
        class for plane object
        :param cockpit_coordinates: tuple with the cockpit's coordinates
        :param tail_coordinates: tuple with the tail's coordinates
        """
        self.cockpit_coordinates = cockpit_coordinates
        self.tail_coordinates = tail_coordinates
        self.cells_occupied = []
        if cockpit_coordinates[0] == tail_coordinates[0]:
            if cockpit_coordinates[1] < tail_coordinates[1]:
                x = cockpit_coordinates[0]
                for y in range(cockpit_coordinates[1], tail_coordinates[1] + 1):
                    self.cells_occupied.append((x, y))
                x = cockpit_coordinates[0]
                for y in range(tail_coordinates[1], cockpit_coordinates[1] + 1):
                    self.cells_occupied.append((x, y))
                for i in range(1, 3):
                    wing_coordinate1 = (cockpit_coordinates[0] + i, cockpit_coordinates[1] + 1)
                    wing_coordinate2 = (cockpit_coordinates[0] - i, cockpit_coordinates[1] + 1)
                    self.cells_occupied.append(wing_coordinate1)
                    self.cells_occupied.append(wing_coordinate2)
                tailplane_coordinate1 = (tail_coordinates[0] + 1, tail_coordinates[1])
                tailplane_coordinate2 = (tail_coordinates[0] - 1, tail_coordinates[1])
                self.cells_occupied.append(tailplane_coordinate1)
                self.cells_occupied.append(tailplane_coordinate2)
            else:
                x = cockpit_coordinates[0]
                for y in range(tail_coordinates[1], cockpit_coordinates[1] + 1):
                    self.cells_occupied.append((x, y))
                for i in range(1, 3):
                    wing_coordinate1 = (cockpit_coordinates[0] + i, cockpit_coordinates[1] - 1)
                    wing_coordinate2 = (cockpit_coordinates[0] - i, cockpit_coordinates[1] - 1)
                    self.cells_occupied.append(wing_coordinate1)
                    self.cells_occupied.append(wing_coordinate2)
                tailplane_coordinate1 = (tail_coordinates[0] + 1, tail_coordinates[1])
                tailplane_coordinate2 = (tail_coordinates[0] - 1, tail_coordinates[1])
                self.cells_occupied.append(tailplane_coordinate1)
                self.cells_occupied.append(tailplane_coordinate2)
        else:
            if cockpit_coordinates[0] < tail_coordinates[0]:
                y = cockpit_coordinates[1]
                for x in range(cockpit_coordinates[0], tail_coordinates[0] + 1):
                    self.cells_occupied.append((x, y))
                for i in range(1, 3):
                    wing_coordinate1 = (cockpit_coordinates[0] + 1, cockpit_coordinates[1] + i)
                    wing_coordinate2 = (cockpit_coordinates[0] + 1, cockpit_coordinates[1] - i)
                    self.cells_occupied.append(wing_coordinate1)
                    self.cells_occupied.append(wing_coordinate2)
                tailplane_coordinate1 = (tail_coordinates[0], tail_coordinates[1] + 1)
                tailplane_coordinate2 = (tail_coordinates[0], tail_coordinates[1] - 1)
                self.cells_occupied.append(tailplane_coordinate1)
                self.cells_occupied.append(tailplane_coordinate2)
            else:
                y = cockpit_coordinates[1]
                for x in range(tail_coordinates[0], cockpit_coordinates[0] + 1):
                    self.cells_occupied.append((x, y))
                for i in range(1, 3):
                    wing_coordinate1 = (cockpit_coordinates[0] - 1, cockpit_coordinates[1] + i)
                    wing_coordinate2 = (cockpit_coordinates[0] - 1, cockpit_coordinates[1] - i)
                    self.cells_occupied.append(wing_coordinate1)
                    self.cells_occupied.append(wing_coordinate2)
                tailplane_coordinate1 = (tail_coordinates[0], tail_coordinates[1] + 1)
                tailplane_coordinate2 = (tail_coordinates[0], tail_coordinates[1] - 1)
                self.cells_occupied.append(tailplane_coordinate1)
                self.cells_occupied.append(tailplane_coordinate2)

    def __eq__(self, other):
        return self.cockpit_coordinates == other.cockpit_coordinates and self.tail_coordinates == other.tail_coordinates


class Board:
    def __init__(self, height=10, width=10):
        """
        class for board object
        :param height: the height of the board
        :param width: the width of the board
        """
        if height < 5 or width < 5:
            raise BoardError("The board is too small")
        self.height = height
        self.width = width
        self.player_board_matrix = [[0 for i in range(height)] for j in range(width)]
        self.tracking_board_matrix = [[0 for i in range(height)] for j in range(width)]

    def create_player_board(self):
        """
        turns the player board matrix into a texttable object
        :return: the texttable object
        """
        player_board = texttable.Texttable()
        aux = [""]
        for x in range(1, self.width + 1):
            aux += [x]
        player_board.add_row(aux)
        for i in range(self.height):
            aux = [chr(ord('A') + i)]
            for j in range(self.width):
                if self.player_board_matrix[i][j] == 0:
                    aux += [""]
                elif self.player_board_matrix[i][j] == 1:
                    aux += ["[]"]
                elif self.player_board_matrix[i][j] == 2:
                    aux += [""]
                    if j < 9:
                        if self.player_board_matrix[i][j + 1] != 0:
                            aux[-1] = "<"
                    if j > 0:
                        if self.player_board_matrix[i][j - 1] != 0:
                            aux[-1] = ">"
                    if i < 9:
                        if self.player_board_matrix[i + 1][j] != 0:
                            aux[-1] = "^"
                    if i > 0:
                        if self.player_board_matrix[i - 1][j] != 0:
                            aux[-1] = "v"
                elif self.player_board_matrix[i][j] == -1:
                    aux += ["X"]
                elif self.player_board_matrix[i][j] == -2:
                    aux += ["[X]"]
            player_board.add_row(aux)
        return player_board.draw()

    def create_tracking_board(self):
        """
        turns the tracking board matrix into a texttable object
        :return:
        """
        tracking_board = texttable.Texttable()
        aux = [""]
        for x in range(1, self.width + 1):
            aux += [x]
        tracking_board.add_row(aux)
        for i in range(self.height):
            aux = [chr(ord('A') + i)]
            for j in range(self.width):
                if self.tracking_board_matrix[i][j] == 0:
                    aux += [""]
                elif self.tracking_board_matrix[i][j] > 0:
                    aux += ["X"]
                elif self.tracking_board_matrix[i][j] == -1:
                    aux += ["O"]
            tracking_board.add_row(aux)
        return tracking_board.draw()
