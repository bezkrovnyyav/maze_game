from dataclasses import dataclass, field
import sys
import json
import os
import logging

from maze import Maze
from player import Player


logging.basicConfig(level=logging.INFO, format='%(message)s')


@dataclass
class Game:
    """The class with game options
        Args:
            maze (Maze): Maze class instance.
            heroes (list): List of players
    """
    maze = Maze()
    players_list: list = field(default_factory=lambda: [])

    def download_game(self):
        """Download player`s data from json file"""
        if os.path.getsize("maze_game.json") == 0:
            logging.info("The file maze_game.json is empty. Start the game again")
            self.start_new_game()
        else:
            with open('maze_game.json', 'r') as file:
                player_data = json.load(file)
                for index, player in enumerate(player_data.get('players_dict')):
                    self.create_player(player.get('name'))
                    self.players_list[index].set_player_info(player)
                    self.players_list[index].get_info()
                self.maze.set_key_info(player_data.get("maze_dict"))

    def save_game(self):
        """Save player`s data to json file"""
        players_dict = []
        for player in self.players_list:
            players_dict.append(player.get_player_info())

        with open('maze_game.json', 'w') as file:
            data = {
                "players_dict": players_dict,
                "maze_dict": self.maze.get_key_info()
            }
            json.dump(data, file)
        logging.info("Data about players is saved")

    def start_new_game(self):
        """For starting new game"""
        logging.info("Enter the number of players: ")
        try:
            players_number = int(input())
            for _ in range(players_number):
                logging.info("Enter player`s name.")
                self.create_player(input())
            logging.info("New players are created.")
        except ValueError:
            logging.critical("The game is over. Please try start the game again.")
            sys.exit()
        logging.info("The game is started")

    def play_game(self):
        """Create commands of the game"""
        while True:
            if not os.path.isfile('maze_game.json'):
                self.start_new_game()
                break
            else:
                logging.info("There is a saved data about players. Do you want to download it?(y/n)")
            user_response = input()
            if user_response.strip().lower() == "y":
                self.download_game()
                logging.info("The game is started")
                break
            if user_response.strip().lower() == "n":
                self.start_new_game()
                break
            logging.info("Incorrect command is entered. Please enter y or n.")
        while True:
            if len(self.players_list) == 0:
                logging.info("All players are dead. The game is over.")
                break
            self.maze.get_random_fires()
            is_save = False
            for player in self.players_list:
                if player.is_dead():
                    logging.info(f"Player {player.name} died.")
                    self.delete_player(player)
                    continue
                logging.info(
                    f"Player {player.name} makes his move. Please type 'help' to see the list of commands\n")
                while True:
                    match input().strip().lower():
                        case "help":
                            logging.info('Enter "1" for changing position in the maze.\n'
                                         'Enter "2" for taking a life for your player.\n'
                                         'Enter "3" for attacking another player on position.\n'
                                         'Enter "4" for takith the key on position.\n'
                                         'Enter "5" to save the game.\n'
                                         'Enter "exit" if you want to leave the game.\n')
                        case "1":
                            self.move(player)
                            break
                        case "2":
                            if player.take_life():
                                break
                            logging.info(
                                f"Player {player.name} makes his move.")
                        case "3":
                            if self.make_damage(player):
                                break
                            logging.info(
                                f"Player {player.name} makes his move.")
                        case '4':
                            if self.maze.check_key_location() == (player._real_position, True):
                                player.get_key()
                                self.maze.take_key()
                                logging.info(f"Player {player.name} take the key")
                                break
                            else:
                                logging.info("There is no key here or someone has already taken it.")
                        case '5':
                            if is_save:
                                logging.info("The game will be saved after the moves of all players. Please don't use "
                                             "this command again.")
                            else:
                                is_save = True
                                logging.info("The game will be saved after the moves of all players.")
                            logging.info(f"Player {player.name} makes his move again.")
                        case 'exit':
                            logging.info('The game is over. Thank you for playing')
                            sys.exit()
                        case _:
                            logging.info("Incorect command. Try again or type 'help' to see the list of commands"
                                         )
            if is_save:
                self.save_game()

    def make_damage(self, player):
        """Make damage to another player"""
        players_list = []
        for player in self.players_list:
            if player != player and player._real_position == player._real_position:
                logging.info(f"Player {player.name} is in this cell.")
                players_list.append(player)
        if not players_list:
            logging.info("There is no player for attacking in this cell.")
            return False
        if len(players_list) == 1:
            player.make_damage(players_list[0].name)
            return True
        else:
            logging.info("Select the player for attacking:")
            for index, player in enumerate(players_list):
                logging.info(f"{index + 1}. {player.name}", extra={"terminator": ""})
            while True:
                choice = input()
                if not choice.isdigit() or int(choice) not in range(1, len(players_list) + 1):
                    logging.info("Invalid choice. Please enter the number of one of the player in the list.\n")
                else:
                    target_hero = players_list[int(choice) - 1]
                    player.make_damage(target_hero.name)
                    return True

    def move(self, player):
        """Represent commands of moving """
        logging.info("Enter command for moving. Enter 'help' to see  commands of moving.")
        while True:
            match input().strip().lower():
                case "help":
                    logging.info('Enter "r" to move your player to the right site of the maze.\n'
                                 'Enter "l" to move your player to the left site of the maze.\n'
                                 'Enter "u" to move your player to the top site of the maze.\n'
                                 'Enter "d" to move your player to the down site of the maze.\n')
                case "r":
                    next_x, next_y = (1, 0)
                    break
                case "l":
                    next_x, next_y = (-1, 0)
                    break
                case "u":
                    next_x, next_y = (0, -1)
                    break
                case 'd':
                    next_x, next_y = (0, 1)
                    break
                case _:
                    logging.info("Incorrect command. Please enter 'help' to see the list of commands")
        move_result = self.maze.get_position_status(player._real_position, (next_x, next_y))
        if move_result == "golem":
            if player.has_key:
                logging.info(f"Player {player.name} is the winer! Thanks for playing")
                sys.exit()
            else:
                logging.info(f"Player {player.name} is killed via a golem. The game is over.")
                self.delete_player(player)
        elif move_result == "wrong_coordinates":
            if player.is_dead():
                logging.info(f"Player {player.name} die.")
                self.delete_player(player)
            else:
                player.take_damage("wall")

        else:
            x, y = player._real_position
            player._real_position = x + next_x, y + next_y
            if player._real_position == player._pre_position:
                logging.info(f"Player {player.name} is scared.")
                self.delete_player(player)
                return None
            if player._real_position not in self.maze.safe_positions and (x, y) not in self.maze.safe_positions:
                player._pre_position = x, y
            logging.info(f"Player {player.name} go to position {player._real_position}.")
            if move_result == "life":
                logging.info(f"Player {player.name} is on the cell with lifes. Do you want to take a life?")
            if self.maze.check_key_location() == (player._real_position, True):
                logging.info(f"Player {player.name} is on the cell with key")
            for one_player in self.players_list:
                if one_player != player and one_player._real_position == player._real_position:
                    logging.info(f"Another player, {one_player.name}, is on this cell.")
            if move_result == "burned":
                if player.is_dead():
                    logging.info(f"Player {player.name} is died.")
                    self.delete_player(player)
                player.take_damage("fire")

    def create_player(self, name: str):
        """Create new player in list of players"""
        for player in self.players_list:
            if player.name == name.strip():
                logging.info(f"Player {player.name} was added befor this time.")
                break
        else:
            self.players_list.append(Player(name))
            logging.info(f"Player {name} is added andready to start the game.")

    def delete_player(self, player):
        """Delete the player from list of players"""
        if player.has_key:
            self.maze.drop_key(player._real_position)
            logging.info(f"Key dropped at {player._real_position}")
        self.players_list.remove(player)


if __name__ == "__main__":
    pass
