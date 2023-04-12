from dataclasses import dataclass, field
import logging
import random


logging.basicConfig(level=logging.INFO, format='%(message)s')


@dataclass
class Maze:
    """The class in which the maze is implemented
        Args:
            fire_cells (list): Locations where the fire is burned.
            key_location(tuple): Location of the key.
            key_exists(bool):Whether there is a key in the maze.
            golem_location (int): Location of the golem.
            safe_positions (int): Locations where fire can't burn.
            maze_structure (int): Structure of the maze.
    """
    fire_cells: list = field(default_factory=lambda: [])
    key_location: tuple = (2, 1)
    key_exists: bool = True
    golem_location: tuple = (7, 0)
    safe_positions: tuple = ((2, 1), (6, 2), (4, 0))
    maze_structure: list = field(default_factory=lambda: [
        [False, False, False, False, True, True, True, True],
        [False, False, True, False, False, True, False, False],
        [False, True, True, True, False, True, True, False],
        [True, True, False, True, True, True, False, False]
    ])

    def get_movable_positions(self):
        movable_positions = [
            (x, y) for y in range(4) for x in range(8)
            if self.maze_structure[y][x] and (x, y) not in self.safe_positions]
        return movable_positions

    def get_key_info(self) -> dict:
        """Get information about key in the maze for saving."""
        return {
            "key_location": self.key_location,
            "key_exists": self.key_exists
        }

    def set_key_info(self, key_location_info: dict) -> None:
        """Create information about the key for uploading."""
        self.key_location = tuple(key_location_info.get('key_location'))
        self.key_exists = key_location_info.get('key_exists')

    def check_key_location(self) -> tuple:
        """Check key location"""
        return self.key_location, self.key_exists

    def drop_key(self, player_position: tuple) -> None:
        """Drop the key in the cell when a player is died"""
        self.key_location = player_position
        self.key_exists = True

    def take_key(self) -> None:
        """Take key via player"""
        self.key_exists = False

    def get_random_fires(self) -> None:
        """Generating fire cell in the 4 random positions."""
        random_fires = random.sample(self.get_movable_positions(), 4)
        self.fire_cells = random_fires
        logging.info(f"There is the fire in the positions: {self.fire_cells}")

    def get_position_status(self, player_position, course: tuple) -> str:
        """Return player position when he made move."""
        x, y = player_position
        next_x, next_y = course
        if not (0 <= x + next_x < 8 and 0 <= y + next_y < 4):
            return "wrong_coordinates"
        if (x + next_x, y + next_y) == self.golem_location:
            return "golem"
        if self.maze_structure[y + next_y][x + next_x]:
            if (x + next_x, y + next_y) in self.fire_cells:
                return 'burned'
            return "life" if (x + next_x, y + next_y) in self.safe_positions[1:] else "success"
        else:
            return "wrong_coordinates"


if __name__ == "__main__":
    pass
