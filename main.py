import monopoly
from tqdm import tqdm
from collections import Counter
import random


def main():
    games = 1000000
    all_games_board_history = []

    for _ in tqdm(range(games), desc="Playing games"):
        turns = random.randint(100, 200)  # Random turns per game

        game = monopoly.Monopoly(verbose=False)
        board_history, _ = game.play_game(turns)

        all_games_board_history.append(board_history)

    # Flatten all board positions
    all_positions = [
        pos for game_history in all_games_board_history for pos in game_history
    ]

    # Count occurrences
    counts = Counter(all_positions)

    # Most common square
    most_common_square, count = counts.most_common(1)[0]

    print(f"\nMost common square: {most_common_square}")
    print(f"Visits: {count:,}")

    print("\nTop 10 squares:")
    for square, cnt in counts.most_common(10):
        print(f"Square {square}: {cnt:,}")


if __name__ == "__main__":
    main()