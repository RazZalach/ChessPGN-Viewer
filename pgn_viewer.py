import tkinter as tk
from tkinter import filedialog, messagebox
import chess
import chess.pgn
from PIL import Image, ImageTk
import os

class ChessApp:
    def __init__(self, root, games):
        self.root = root
        self.games = games
        self.current_game_index = 0
        self.current_game = self.games[self.current_game_index]
        self.board = chess.Board()
        self.moves = list(self.current_game.mainline_moves())
        self.current_move_index = 0
        self.result = self.current_game.headers["Result"]

        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.pack()

        self.piece_images = self.load_piece_images()

        self.draw_board()

        self.next_button = tk.Button(root, text="הבא", command=self.next_move)
        self.next_button.pack(side=tk.RIGHT, padx=10, pady=10)

        self.prev_button = tk.Button(root, text="אחורה", command=self.prev_move)
        self.prev_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.next_game_button = tk.Button(root, text="משחק הבא", command=self.next_game)
        self.next_game_button.pack(side=tk.BOTTOM, pady=10)
        self.next_game_button.config(state=tk.DISABLED)  # Initially disabled

        # Set up key bindings
        root.bind("<Right>", self.handle_right_arrow)
        root.bind("<Left>", self.handle_left_arrow)

    def load_piece_images(self):
        pieces = ['p', 'r', 'n', 'b', 'q', 'k']
        piece_images = {}
        colors = ['w', 'b']  
        script_dir = os.path.dirname(__file__) 
        image_dir = os.path.join(script_dir, 'pieces')
        for color in colors:
            for piece in pieces:
                image_path = os.path.join(image_dir, f"{color}_{piece}.png")
                image = Image.open(image_path)
                image = image.resize((50, 50))
                piece_images[color + piece] = ImageTk.PhotoImage(image)
        return piece_images

    def draw_board(self):
        self.canvas.delete("all")
        colors = ["#f0d9b5", "#b58863"]
        for row in range(8):
            for col in range(8):
                color = colors[(row + col) % 2]
                self.canvas.create_rectangle(col*50, row*50, (col+1)*50, (row+1)*50, fill=color)
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                x = (square % 8) * 50
                y = (7 - square // 8) * 50
                piece_color = 'w' if piece.color == chess.WHITE else 'b'
                piece_key = piece_color + piece.symbol().lower()
                self.canvas.create_image(x, y, anchor=tk.NW, image=self.piece_images[piece_key])

    def next_move(self):
        if self.current_move_index < len(self.moves):
            self.board.push(self.moves[self.current_move_index])
            self.current_move_index += 1
            self.draw_board()

            if self.current_move_index == len(self.moves):
                self.check_result()
                if self.current_game_index < len(self.games) - 1:
                    self.next_game_button.config(state=tk.NORMAL)  # Enable the next game button

    def prev_move(self):
        if self.current_move_index > 0:
            self.board.pop()
            self.current_move_index -= 1
            self.draw_board()

    def check_result(self):
        if self.result == "1-0":
            messagebox.showinfo("תוצאה", "לבן ניצח")
        elif self.result == "0-1":
            messagebox.showinfo("תוצאה", "שחור ניצח")
        elif self.result == "1/2-1/2":
            messagebox.showinfo("תוצאה", "תיקו")

    def next_game(self):
        if self.current_game_index < len(self.games) - 1:
            self.current_game_index += 1
            self.current_game = self.games[self.current_game_index]
            self.board = chess.Board()
            self.moves = list(self.current_game.mainline_moves())
            self.current_move_index = 0
            self.result = self.current_game.headers["Result"]
            self.draw_board()
            self.next_game_button.config(state=tk.DISABLED)  # Disable until game ends

    # Keyboard event handlers
    def handle_right_arrow(self, event):
        self.next_move()

    def handle_left_arrow(self, event):
        self.prev_move()

def open_pgn_file(root, welcome_label, select_button):
    pgn_file = filedialog.askopenfilename(title="בחר קובץ PGN", filetypes=[("PGN files", "*.pgn")])
    if pgn_file:
        try:
            games = []
            with open(pgn_file) as pgn:
                while True:
                    game = chess.pgn.read_game(pgn)
                    if game is None:
                        break
                    games.append(game)
            welcome_label.pack_forget()
            select_button.pack_forget()
            ChessApp(root, games)
        except Exception as e:
            messagebox.showerror("שגיאה", f"לא הצליח לטעון את הקובץ: {e}")

def start_app():
    root = tk.Tk()
    root.title("Chess PGN Viewer")

    welcome_label = tk.Label(root, text="ברוך הבא!", font=("Helvetica", 16))
    welcome_label.pack(pady=10)

    select_button = tk.Button(root, text="בחר קובץ PGN", command=lambda: open_pgn_file(root, welcome_label, select_button))
    select_button.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    start_app()
