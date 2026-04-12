import tkinter as tk
import random

# --- Game configuration ---
BOARD_SIZE = 10          # 10x10 board
CELL_SIZE = 60           # pixels per cell
BOARD_PIXELS = BOARD_SIZE * CELL_SIZE

# Snakes and ladders: start -> end
LADDERS = {
    4: 14,
    9: 31,
    17: 74,
    21: 42,
    28: 84,
    51: 67,
    72: 91
}

SNAKES = {
    26: 5,
    39: 3,
    48: 10,
    56: 37,
    62: 18,
    88: 24,
    97: 78
}

PLAYERS = [
    {"name": "Player 1", "color": "#ff5555"},
    {"name": "Player 2", "color": "#5555ff"},
]


class SnakeLadderGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake & Ladder")

        # Game state
        self.current_player_index = 0
        self.positions = [1 for _ in PLAYERS]  # both players start at 1
        self.tokens = [None for _ in PLAYERS]
        self.game_over = False

        # --- UI layout ---
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(padx=10, pady=10)

        # Canvas for board
        self.canvas = tk.Canvas(
            self.main_frame,
            width=BOARD_PIXELS,
            height=BOARD_PIXELS,
            bg="white"
        )
        self.canvas.grid(row=0, column=0, rowspan=4)

        # Right-side controls
        self.info_frame = tk.Frame(self.main_frame)
        self.info_frame.grid(row=0, column=1, sticky="n", padx=15)

        self.label_turn = tk.Label(
            self.info_frame,
            text="Turn: Player 1",
            font=("Arial", 14, "bold")
        )
        self.label_turn.pack(pady=5)

        self.label_roll = tk.Label(
            self.info_frame,
            text="Roll: -",
            font=("Arial", 12)
        )
        self.label_roll.pack(pady=5)

        self.label_pos = tk.Label(
            self.info_frame,
            text="P1: 1 | P2: 1",
            font=("Arial", 12)
        )
        self.label_pos.pack(pady=5)

        self.label_msg = tk.Label(
            self.info_frame,
            text="Click 'Roll Dice' to start!",
            wraplength=180,
            justify="left",
            font=("Arial", 10)
        )
        self.label_msg.pack(pady=10)

        self.btn_roll = tk.Button(
            self.info_frame,
            text="Roll Dice",
            font=("Arial", 12, "bold"),
            width=12,
            command=self.roll_dice
        )
        self.btn_roll.pack(pady=5)

        self.btn_new = tk.Button(
            self.info_frame,
            text="New Game",
            font=("Arial", 10),
            width=12,
            command=self.new_game
        )
        self.btn_new.pack(pady=5)

        # Draw everything
        self.draw_board()
        self.init_tokens()

    # --- Board drawing and coordinates ---

    def draw_board(self):
        # Draw grid cells with alternating colors and numbers
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                x1 = col * CELL_SIZE
                y1 = row * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE

                # Checkerboard background
                if (row + col) % 2 == 0:
                    fill = "#f0e4d7"
                else:
                    fill = "#e0c8a0"

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline="black")

                # Compute board number for this (row, col)
                num = self.coords_to_position(row, col)
                self.canvas.create_text(
                    x1 + 5,
                    y1 + 5,
                    text=str(num),
                    anchor="nw",
                    font=("Arial", 8, "bold")
                )

        # Optionally highlight snake/ladder starts
        for start, end in LADDERS.items():
            x, y = self.position_to_center(start)
            self.canvas.create_oval(
                x - 8, y - 8, x + 8, y + 8,
                outline="#228b22",
                width=2
            )

        for start, end in SNAKES.items():
            x, y = self.position_to_center(start)
            self.canvas.create_oval(
                x - 8, y - 8, x + 8, y + 8,
                outline="#b22222",
                width=2
            )

    def coords_to_position(self, row, col):
        """
        Convert canvas row,col (from top-left) to board position 1..100
        using a serpentine pattern.
        """
        # Row 0 is top visually but represents 10th row (91-100)
        row_from_bottom = BOARD_SIZE - 1 - row  # 0 at bottom
        base = row_from_bottom * BOARD_SIZE

        if row_from_bottom % 2 == 0:
            # left to right
            pos = base + col + 1
        else:
            # right to left
            pos = base + (BOARD_SIZE - col)
        return pos

    def position_to_center(self, pos):
        """
        Convert board position 1..100 to canvas center (x, y).
        """
        pos -= 1
        row_from_bottom = pos // BOARD_SIZE
        col_in_row = pos % BOARD_SIZE

        if row_from_bottom % 2 == 0:
            col = col_in_row
        else:
            col = (BOARD_SIZE - 1) - col_in_row

        row = (BOARD_SIZE - 1) - row_from_bottom

        x = col * CELL_SIZE + CELL_SIZE / 2
        y = row * CELL_SIZE + CELL_SIZE / 2
        return x, y

    def init_tokens(self):
        # Draw player tokens at starting position
        for i, player in enumerate(PLAYERS):
            x, y = self.position_to_center(self.positions[i])
            # Offset tokens slightly so they don't overlap exactly
            offset = -10 if i == 0 else 10
            token = self.canvas.create_oval(
                x - 12 + offset,
                y - 12,
                x + 12 + offset,
                y + 12,
                fill=player["color"],
                outline="black",
                width=2
            )
            self.tokens[i] = token

    def move_token(self, player_index):
        x, y = self.position_to_center(self.positions[player_index])
        offset = -10 if player_index == 0 else 10
        self.canvas.coords(
            self.tokens[player_index],
            x - 12 + offset,
            y - 12,
            x + 12 + offset,
            y + 12
        )

    # --- Game logic ---

    def roll_dice(self):
        if self.game_over:
            self.label_msg.config(text="Game over. Click 'New Game' to play again.")
            return

        player = PLAYERS[self.current_player_index]
        roll = random.randint(1, 6)
        self.label_roll.config(text=f"Roll: {roll}")

        old_pos = self.positions[self.current_player_index]
        tentative = old_pos + roll

        msg_parts = [f"{player['name']} rolled a {roll}. "]

        if tentative > 100:
            msg_parts.append("Needs exact roll to reach 100, so stays in place.")
            # No movement
        else:
            new_pos = tentative
            # Check ladders
            if new_pos in LADDERS:
                dest = LADDERS[new_pos]
                msg_parts.append(f"Hit a ladder! Climb from {new_pos} to {dest}. ")
                new_pos = dest
            # Check snakes
            elif new_pos in SNAKES:
                dest = SNAKES[new_pos]
                msg_parts.append(f"Oops, a snake! Slide from {new_pos} to {dest}. ")
                new_pos = dest

            self.positions[self.current_player_index] = new_pos
            self.move_token(self.current_player_index)

        # Update positions label
        self.label_pos.config(
            text=f"P1: {self.positions[0]} | P2: {self.positions[1]}"
        )

        # Check win
        if self.positions[self.current_player_index] == 100:
            self.game_over = True
            msg_parts.append(f"{player['name']} wins! 🎉")
            self.label_msg.config(text="".join(msg_parts))
            self.label_turn.config(text="Game Over")
            return

        # Switch turn
        self.current_player_index = 1 - self.current_player_index
        next_player = PLAYERS[self.current_player_index]
        msg_parts.append(f"Now it's {next_player['name']}'s turn.")
        self.label_msg.config(text="".join(msg_parts))
        self.label_turn.config(text=f"Turn: {next_player['name']}")

    def new_game(self):
        self.game_over = False
        self.current_player_index = 0
        self.positions = [1 for _ in PLAYERS]

        for i in range(len(PLAYERS)):
            self.move_token(i)

        self.label_turn.config(text="Turn: Player 1")
        self.label_roll.config(text="Roll: -")
        self.label_pos.config(text="P1: 1 | P2: 1")
        self.label_msg.config(text="New game started. Click 'Roll Dice'!")


def main():
    root = tk.Tk()
    game = SnakeLadderGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
