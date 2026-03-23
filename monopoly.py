import random
from tabnanny import verbose
from typing import List, Tuple

class Monopoly:
    def __init__(self, verbose: bool = False):
        self._verbose = verbose

        # Standard UK Monopoly Chance cards
        self._chance_cards: List[str] = [
            "Advance to GO (Collect £200)", # Move to 0
            "Advance to Trafalgar Square", # Move to 24
            "Advance to Pall Mall", # Move to 11
            "Advance to Mayfair", # Move to 39
            "Advance to the nearest Utility", # Move to 12 or 28
            "Advance to the nearest Railroad", # Move to 5, 15, 25, or 35
            "Advance to the nearest Railroad", # Move to 5, 15, 25, or 35
            "Bank pays you dividend of £50",
            "Get out of Jail Free",
            "Go back 3 spaces", # Move back 3 spaces
            "Go to Jail, do not pass GO, do not collect £200", # Move to 10
            "Make general repairs on all your property (£25 per house, £100 per hotel)",
            "Pay poor tax of £15",
            "Take a trip to Marylebone Station", # Move to 15
            "Take a walk to Fleet Street", # Move to 23
            "You have been elected Chairman of the Board, pay each player £50",
        ]

        self._community_chest_cards: List[str] = [
            "Advance to GO (Collect £200)", # Move to 0
            "Bank error in your favour, collect £200",
            "Doctor's fees, pay £50",
            "From sale of stock you get £50",
            "Get out of Jail Free",
            "Go to Jail, do not pass GO, do not collect £200", # move to 10
            "Holiday fund matures, receive £100",
            "Income tax refund, collect £20",
            "It is your birthday, collect £10 from each player",
            "Life insurance matures, collect £100",
            "Pay hospital fees of £100",
            "Pay school fees of £50",
            "Receive £25 consultancy fee",
            "You are assessed for street repairs (£40 per house, £115 per hotel)",
            "You have won second prize in a beauty contest, collect £10",
            "You inherit £100",
        ]

        self._monopoly_squares: List[Tuple[int, str]] = [
            (0, "GO"),
            (1, "Old Kent Road"),
            (2, "Community Chest"), # draw community chest card
            (3, "Whitechapel Road"),
            (4, "Income Tax"),
            (5, "King's Cross Station"),
            (6, "The Angel, Islington"),
            (7, "Chance"), # draw chance card
            (8, "Euston Road"),
            (9, "Pentonville Road"),
            (10, "Jail / Just Visiting"),
            (11, "Pall Mall"),
            (12, "Electric Company"),
            (13, "Whitehall"),
            (14, "Northumberland Avenue"),
            (15, "Marylebone Station"),
            (16, "Bow Street"),
            (17, "Community Chest"), # draw community chest card
            (18, "Marlborough Street"),
            (19, "Vine Street"),
            (20, "Free Parking"),
            (21, "Strand"),
            (22, "Chance"), # draw chance card
            (23, "Fleet Street"),
            (24, "Trafalgar Square"),
            (25, "Fenchurch Street Station"),
            (26, "Leicester Square"),
            (27, "Coventry Street"),
            (28, "Water Works"),
            (29, "Piccadilly"),
            (30, "Go To Jail"), # Move to 10
            (31, "Regent Street"),
            (32, "Oxford Street"),
            (33, "Community Chest"), # draw community chest card
            (34, "Bond Street"),
            (35, "Liverpool Street Station"),
            (36, "Chance"), # draw chance card
            (37, "Park Lane"),
            (38, "Super Tax"),
            (39, "Mayfair")
        ]

    def _log(self, message: str):
        if self._verbose:
            print(message)

    def _reset_game(self):
        # Shuffle the chance and community chest decks
        self._shuffle_decks()

        # Deck and board indices
        self._chance_index = 0
        self._community_chest_index = 0
        self._board_index = 0  # Start at GO

        # dice roll history
        self._dice_rolls: List[Tuple[int, int]] = []

        # Track the board position history (starting at GO)
        self._board_positions: List[int] = [0]
        self._log(f"Starting on {self._monopoly_squares[0][1]} (Square 0)")


    def _shuffle_decks(self):
        random.shuffle(self._chance_cards)
        random.shuffle(self._community_chest_cards)

    def _draw_chance_card(self) -> str:
        card = self._chance_cards[self._chance_index]
        self._chance_index += 1

        # Loop back to start when deck is exhausted
        if self._chance_index >= len(self._chance_cards):
            self._chance_index = 0

        self._log(f"Chance Card: {card}")

        return card

    def _draw_community_chest_card(self) -> str:
        card = self._community_chest_cards[self._community_chest_index]
        self._community_chest_index += 1

        # Loop back to start when deck is exhausted
        if self._community_chest_index >= len(self._community_chest_cards):
            self._community_chest_index = 0

        self._log(f"Community Chest Card: {card}")

        return card

    def _move_player(self, steps: int, position: int | None = None):
        if position is not None:
            if not 0 <= position < 40:
                raise ValueError(f"Position must be between 0 and 39, got {position}")
            self._board_index = position
        else:
            self._board_index = (self._board_index + steps) % 40
        
        self._board_positions.append(self._board_index)
        self._log(f"Moved to {self._current_square()[1]} (Square {self._board_index})")
    
    def _roll_dice(self) -> Tuple[int, int, int]:
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)

        self._log(f"Rolled dice: {die1 + die2} ({die1} and {die2})")
        # Store the roll
        self._dice_rolls.append((die1, die2))

        return die1, die2, die1 + die2
        

    def _current_square(self) -> Tuple[int, str]:
        return self._monopoly_squares[self._board_index]

    def _process_current_square(self):
        square_index, _ = self._current_square()
        if square_index in {2,17,33}:  # Community Chest
            # Draw a community chest card
            card = self._draw_community_chest_card()
            
            if card == "Go to Jail, do not pass GO, do not collect £200":
                self._move_player(0, position=10)  # Move to Jail
            elif card == "Advance to GO (Collect £200)":
                self._move_player(0, position=0)  # Move to GO   
        elif square_index in {7,22,36}:  # Chance
            # Draw a chance card
            card = self._draw_chance_card()
            
            if card == "Go to Jail, do not pass GO, do not collect £200":
                self._move_player(0, position=10)  # Move to Jail
            elif card == "Advance to GO (Collect £200)":
                self._move_player(0, position=0)  # Move to GO
            elif card == "Advance to Trafalgar Square":
                self._move_player(0, position=24)  # Move to Trafalgar Square    
            elif card == "Advance to Pall Mall":
                self._move_player(0, position=11)  # Move to Pall Mall
            elif card == "Advance to Mayfair":
                self._move_player(0, position=39)  # Move to Mayfair
            elif card == "Advance to the nearest Utility":
                if self._board_index < 12 or self._board_index >= 28:
                    self._move_player(0, position=12)  # Move to Electric Company
                else:
                    self._move_player(0, position=28)  # Move to Water Works
            elif card == "Advance to the nearest Railroad":
                if self._board_index < 5 or self._board_index >= 35:
                    self._move_player(0, position=5)  # Move to King's Cross Station
                elif self._board_index < 15:
                    self._move_player(0, position=15)  # Move to Marylebone Station
                elif self._board_index < 25:
                    self._move_player(0, position=25)  # Move to Fenchurch Street Station
                else:
                    self._move_player(0, position=35)  # Move to Liverpool Street Station
            elif card == "Go back 3 spaces":
                self._move_player(-3)  # Move back 3 spaces
                self._process_current_square()  # Process the new square after moving back
            elif card == "Take a trip to Marylebone Station":
                self._move_player(0, position=15)  # Move to Marylebone Station    
            elif card == "Take a walk to Fleet Street":
                self._move_player(0, position=23)  # Move to Fleet Street
        elif square_index == 30:  # Go To Jail
            self._log("Go To Jail! Moving to Jail square.")
            self._move_player(0, position=10)  # Move to Jail

    def play_game(self, turns: int) -> Tuple[List[int], List[Tuple[int, int]]]:
        # reset the game state
        self._reset_game()
        for _ in range(turns):
            _, _, dice_total = self._roll_dice()
            self._move_player(dice_total)
            self._process_current_square()
        return self._board_positions, self._dice_rolls
            
def main():
    game = Monopoly()
    board_positions, dice_rolls = game.play_game(turns=20)

if __name__ == "__main__":
    main()
