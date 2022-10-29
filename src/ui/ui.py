from src.services.ai import *
import random


class UI:
    def __init__(self):
        self.repository = Repository()
        self.services = Services(self.repository)
        self.ai = AI(self.repository)

    def start(self):
        print("1. Play game")
        print("2. Exit game")
        user_input = input("Enter option: ")
        if user_input == '1':
            self.game()
        elif user_input == '2':
            self.exit_game()
        else:
            print("Invalid option")

    def game(self):
        planes_placed = 0
        while planes_placed < 3:
            print(self.repository.player_board.create_player_board())
            cockpit_coordinates = input("Enter the coordinates of the cockpit(Example: B4, A10): ")
            tail_coordinates = input("Enter the coordinates of the tail(Example: B4, A10): ")
            cockpit_coordinates = self.string_to_coordinates(cockpit_coordinates)
            tail_coordinates = self.string_to_coordinates(tail_coordinates)
            if cockpit_coordinates is None or \
                    tail_coordinates is None:
                print("Invalid coordinates. Try again")
            try:
                self.services.place_plane(cockpit_coordinates, tail_coordinates)
                planes_placed += 1
            except PlaneError as pe:
                print(str(pe))
        self.services.place_computer_planes()
        who_goes_first = random.randint(0, 1)
        if who_goes_first == 0:
            while winner := self.services.end_game() is None:
                print(self.repository.player_board.create_player_board())
                print(self.repository.computer_board.create_player_board())
                print("Computer turn...")
                self.ai.pattern()
                print("Player turn...")
                target_coordinates = input("Enter the coordinates of your attack: ")
                target_coordinates = self.string_to_coordinates(target_coordinates)
                while target_coordinates is None:
                    print("Invalid input. Try again")
                    target_coordinates = input("Enter the coordinates of your attack: ")
                    target_coordinates = self.string_to_coordinates(target_coordinates)
                try:
                    result = self.services.player_round(target_coordinates)
                    print(self.repository.player_board.create_player_board())
                    print(self.repository.computer_board.create_player_board())
                    if result == -1:
                        print("Miss!")
                    elif result == 1:
                        print("Hit!")
                    else:
                        print("Head!")
                except BoardError as be:
                    print(str(be))
                    target_coordinates = input("Enter the coordinates of your attack: ")
                    target_coordinates = self.string_to_coordinates(target_coordinates)
                    while target_coordinates is None:
                        print("Invalid input. Try again")
                        target_coordinates = input("Enter the coordinates of your attack: ")
                        target_coordinates = self.string_to_coordinates(target_coordinates)
            if winner == "computer":
                print("Computer wins!")
            elif winner == "player":
                print("Player wins!")

        else:
            while winner := self.services.end_game() is None:
                print(self.repository.player_board.create_player_board())
                print(self.repository.computer_board.create_player_board())
                print("Player turn...")
                target_coordinates = input("Enter the coordinates of your attack: ")
                target_coordinates = self.string_to_coordinates(target_coordinates)
                while target_coordinates is None:
                    print("Invalid input. Try again")
                    target_coordinates = input("Enter the coordinates of your attack: ")
                    target_coordinates = self.string_to_coordinates(target_coordinates)
                try:
                    result = self.services.player_round(target_coordinates)
                    print(self.repository.player_board.create_player_board())
                    print(self.repository.computer_board.create_player_board())
                    if result == -1:
                        print("Miss!")
                    elif result == 1:
                        print("Hit!")
                    else:
                        print("Head!")
                except BoardError as be:
                    print(str(be))
                    target_coordinates = input("Enter the coordinates of your attack: ")
                    target_coordinates = self.string_to_coordinates(target_coordinates)
                    while target_coordinates is None:
                        print("Invalid input. Try again")
                        target_coordinates = input("Enter the coordinates of your attack: ")
                        target_coordinates = self.string_to_coordinates(target_coordinates)
                print("Computer turn...")
                self.ai.pattern()
            if winner == "computer":
                print("Computer wins!")
            elif winner == "player":
                print("Player wins!")

    @staticmethod
    def exit_game():
        return

    @staticmethod
    def string_to_coordinates(string_to_convert):
        letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        string_to_convert = string_to_convert.strip()
        letter = string_to_convert[0].upper()
        number = string_to_convert[1:].strip()
        try:
            number = int(number)
        except ValueError as ve:
            print(str(ve))
        if letter not in letters:
            return None
        if number not in range(1, 11):
            return None
        y = number - 1
        x = ""
        for i in range(len(letters)):
            if letters[i] == letter:
                x = i
                break
        return x, y


ui = UI()
ui.start()
