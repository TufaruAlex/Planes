from src.services.services import *
import unittest


class Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = Repository()
        self.services = Services(self.repository)

    def tearDown(self) -> None:
        pass

    def test_place_plane__valid_plane__place_successfully(self):
        self.services.place_plane((2, 3), (5, 3))
        self.assertEqual(self.repository.player_planes_list, [Plane((2, 3), (5, 3))])

    def test_place_computer_planes__valid_planes__place_successfully(self):
        self.services.place_computer_planes()
        self.assertEqual(len(self.repository.computer_planes_list), 3)

    def test_player_round__miss__update_tracking_board(self):
        self.services.player_round((3, 5))
        self.assertEqual(self.services.get_player_tracking_matrix()[3][5], -1)

    def test_player_round__hit__update_tracking_board(self):
        self.services.place_computer_planes()
        computer_plane = self.repository.computer_planes_list[1]
        coordinates = computer_plane.cells_occupied[1]
        self.services.player_round(coordinates)
        self.assertEqual(self.services.get_player_tracking_matrix()[coordinates[0]]
                         [coordinates[1]], 1)

    def test_player_round__head__update_tracking_board(self):
        self.services.place_computer_planes()
        computer_plane = self.repository.computer_planes_list[1]
        coordinates = computer_plane.cockpit_coordinates
        self.services.player_round(coordinates)
        for cell in computer_plane.cells_occupied:
            self.assertEqual(self.services.get_player_tracking_matrix()[cell[0]]
                             [cell[1]], 1)
        self.assertEqual(len(self.repository.computer_planes_list), 2)

    def test_computer_round__miss__update_tracking_board(self):
        self.services.computer_round((3, 5))
        self.assertEqual(self.services.get_computer_tracking_matrix()[3][5], -1)

    def test_computer_round__hit__update_tracking_board(self):
        self.services.place_plane((2, 3), (5, 3))
        self.services.computer_round((5, 3))
        self.assertEqual(self.services.get_computer_tracking_matrix()[5][3], 1)

    def test_computer_round__head__update_tracking_board(self):
        self.services.place_plane((2, 3), (5, 3))
        self.services.computer_round((2, 3))
        self.assertEqual(len(self.repository.player_planes_list), 0)
