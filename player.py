from dataclasses import dataclass
import logging


logging.basicConfig(level=logging.INFO, format='%(message)s')


@dataclass
class Player:
    """
    A class of presentation a Player
        Args:
            name (str): Player`s Name.
            real_lifes (int): The number of player`s lifes in this game.
            max_lifes(int): The number of all lifes, which player can get.
            maze_lifes (int): The number of all lifesin this maze.
            _real_position (tuple): Player`s coordinates in this maze at this moment.
            _pre_position(tuple): Player`s previous coordinates in this  maze.
            has_key (int): Information about whether the Player has a key
    """

    name: str
    real_lifes: int = 5
    max_lifes: int = 5
    maze_lifes: int = 2
    _real_position: tuple[int, int] = (0, 3)
    _pre_position: tuple[int, int] = (0, 3)
    has_key: bool = False
    life_position: tuple = ((6, 2), (4, 0))

    @property
    def pre_position(self):
        return self._pre_position

    @pre_position.setter
    def pre_position(self, value: tuple):
        self._pre_position = value

    @property
    def real_position(self):
        return self._real_position

    @real_position.setter
    def real_position(self, value: tuple):
        self._real_position = value

    def get_info(self) -> None:
        """Show information about the Player"""
        logging.info(
            f"Name: {self.name}, Position: {self.real_position}, Previous position: {self.pre_position}"
            f"Player has lifes: {self.real_lifes}, All lifes in the maze: {self.maze_lifes},"
            f"{'Player has key' if self.has_key else 'Player has not key'}, ")

    def get_player_info(self) -> dict:
        """Return information about the Player for saving."""
        return {
            'name': self.name,
            'real_lifes': self.real_lifes,
            'maze_lifes': self.maze_lifes,
            'real_position': self._real_position,
            'pre_position': self._pre_position,
            'has_key': self.has_key,
        }

    def set_player_info(self, player_info_dict: dict) -> None:
        """Set information about the Player for loading."""
        self.name = player_info_dict.get('name')
        self.real_lifes = player_info_dict.get('real_lifes')
        self.maze_lifes = player_info_dict.get('maze_lifes')
        self._real_position = tuple(player_info_dict.get('real_position'))
        self._pre_position = tuple(player_info_dict.get('pre_position'))
        self.has_key = player_info_dict.get('has_key')

    def take_life(self) -> bool:
        """Add life to Player.  Displays information about take one more life in the Maze."""
        if self.maze_lifes == 0:
            logging.info(f"Player {self.name} doesn`t take one life. Try another command.")
            return False
        if self.real_lifes < self.max_lifes:
            if self._real_position in self.life_position:
                self.maze_lifes -= 1
                self.real_lifes += 1
                logging.info(f"Player {self.name} takes one life. The quantity of life is: {self.real_lifes}")
                return True
            else:
                logging.info(f"Player {self.name} is not in the cell with life point. Now wait your move")
                return False
        else:
            logging.info(f"Player {self.name} has maximum lifes. Now wait your move")
            return False

    def is_dead(self) -> bool:
        """Check, is Player dead"""
        if self.real_lifes <= 0:
            return True
        return False

    def get_key(self) -> None:
        self.has_key = True

    def take_damage(self, damage_type) -> None:
        """Displays information about does Player take damage."""
        self.real_lifes -= 1
        logging.info(f"{self.name} received damage from {damage_type}. Lifes left: {self.real_lifes}")

    def make_damage(self, enemy) -> None:
        """Displays information about did Player make damage to another Player"""
        self.real_lifes -= 1
        logging.info(f'Player {self.name} attacked {enemy} with a sword and his lifes are {self.real_lifes}')


if __name__ == "__main__":
    pass
