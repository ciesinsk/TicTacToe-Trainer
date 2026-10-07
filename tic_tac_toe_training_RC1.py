"""Tic-Tac-Toe: Gewinne nach genau einem Fehler des Gegners üben.

Start: python tic_tac_toe_training.py
Benötigt nur die Python-Standardbibliothek (Tkinter).
"""

import random
import tkinter as tk
from functools import lru_cache
from tkinter import ttk


LINES = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
)
EMPTY = "." * 9


def result(board):
    """1 = X gewonnen, -1 = O gewonnen, 0 = remis, None = offen."""
    for a, b, c in LINES:
        if board[a] != "." and board[a] == board[b] == board[c]:
            return 1 if board[a] == "X" else -1
    return 0 if "." not in board else None


def moves(board, symbol):
    return [(i, board[:i] + symbol + board[i + 1:])
            for i, cell in enumerate(board) if cell == "."]


@lru_cache(maxsize=None)
def value(board, turn):
    """Spieltheoretischer Wert aus Sicht von X bei optimalem Spiel."""
    done = result(board)
    if done is not None:
        return done
    scores = [value(next_board, "O" if turn == "X" else "X")
              for _, next_board in moves(board, turn)]
    return max(scores) if turn == "X" else min(scores)


@lru_cache(maxsize=None)
def score(board, turn):
    """Wie value, aber X gewinnt möglichst früh und O hält möglichst lange dagegen.

    Bei eigenem erzwungenem Sieg versucht O ebenfalls, möglichst früh zu gewinnen.
    """
    done = result(board)
    if done is not None:
        return done * (10 - (9 - board.count(".")))
    scores = [score(next_board, "O" if turn == "X" else "X")
              for _, next_board in moves(board, turn)]
    return max(scores) if turn == "X" else min(scores)


def best_x_moves(board):
    best = score(board, "X")
    return [i for i, next_board in moves(board, "X")
            if score(next_board, "O") == best]


def immediate_x_win(board):
    """Kann X mit genau einem Zug eine Reihe vollenden?"""
    return any(result(next_board) == 1 for _, next_board in moves(board, "X"))


def choose_o_move(board, make_mistake=False, rng=None, challenging=False):
    """O spielt optimal; einmal darf O einen erzwingbaren X-Sieg zulassen.

    Im anspruchsvollen Modus lassen wir keine sofortige Gewinnreihe für X zu.
    Gibt es keinen solchen Fehler, wartet O auf eine spätere Gelegenheit.
    """
    rng = rng or random
    choices = moves(board, "O")
    if make_mistake and value(board, "O") == 0:
        mistakes = [(i, b) for i, b in choices
                    if value(b, "X") == 1
                    and (not challenging or not immediate_x_win(b))]
        if mistakes:
            if challenging:
                hardest = min(score(b, "X") for _, b in mistakes)
                mistakes = [(i, b) for i, b in mistakes
                            if score(b, "X") == hardest]
            return (*rng.choice(mistakes), True)
    best = min(score(b, "X") for _, b in choices)
    optimal = [(i, b) for i, b in choices if score(b, "X") == best]
    i, b = rng.choice(optimal)
    return i, b, False


@lru_cache(maxsize=1)
def late_puzzles():
    """Stellungen nach einem späteren, nicht sofort verlierenden O-Zug."""
    puzzles = set()
    visited = set()

    def collect(board, turn, o_turns):
        key = board, turn
        if key in visited or result(board) is not None:
            return
        visited.add(key)
        if turn == "O":
            if o_turns >= 1 and value(board, "O") == 0:
                puzzles.update(next_board for _, next_board in moves(board, "O")
                               if value(next_board, "X") == 1
                               and not immediate_x_win(next_board))
            for _, next_board in moves(board, "O"):
                if value(next_board, "X") == 0:
                    collect(next_board, "X", o_turns + 1)
        else:
            for _, next_board in moves(board, "X"):
                if value(next_board, "O") == 0:
                    collect(next_board, "O", o_turns)

    for opening in (0, 1, 4):
        collect(EMPTY[:opening] + "X" + EMPTY[opening + 1:], "O", 0)
    return tuple(sorted(puzzles))


class Trainer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tic-Tac-Toe: einen Fehler ausnutzen")
        self.resizable(False, False)
        self.board = EMPTY
        self.o_turns = 0
        self.mistake_used = False
        self.pending = False
        self.pending_job = None
        self.hint_shown = False
        self.mode = tk.StringVar(value="Beim ersten O-Zug")
        self.status = tk.StringVar()
        self.details = tk.StringVar()

        frame = ttk.Frame(self, padding=16)
        frame.grid()
        ttk.Label(frame, text="Du spielst X. Wähle eine Eröffnung oder eine spätere Aufgabe.").grid(
            row=0, column=0, columnspan=3, sticky="w")
        ttk.Label(frame, text="Fehler von O:").grid(row=1, column=0, sticky="w", pady=(10, 8))
        menu = ttk.Combobox(frame, state="readonly", textvariable=self.mode, width=36,
                            values=("Beim ersten O-Zug", "Später: kein Sofortgewinn für X",
                                    "Späte Trainingsstellung laden"))
        menu.grid(row=1, column=1, columnspan=2, sticky="w", pady=(10, 8))
        menu.bind("<<ComboboxSelected>>", lambda _: self.new_game())

        self.cells = []
        for i in range(9):
            r, c = divmod(i, 3)
            button = tk.Button(frame, width=5, height=2, font=("Arial", 22, "bold"),
                               command=lambda j=i: self.play(j))
            button.grid(row=r + 2, column=c, padx=3, pady=3)
            self.cells.append(button)

        controls = ttk.Frame(frame)
        controls.grid(row=5, column=0, columnspan=3, pady=(10, 0))
        ttk.Button(controls, text="Zug prüfen / Tipp", command=self.hint).pack(side="left", padx=3)
        ttk.Button(controls, text="Neue Runde", command=self.new_game).pack(side="left", padx=3)
        ttk.Label(frame, textvariable=self.status, wraplength=340).grid(
            row=6, column=0, columnspan=3, sticky="w", pady=(12, 3))
        ttk.Label(frame, textvariable=self.details, wraplength=340).grid(
            row=7, column=0, columnspan=3, sticky="w")
        self.new_game()

    def new_game(self):
        if self.pending_job is not None:
            self.after_cancel(self.pending_job)
            self.pending_job = None
        self.board = EMPTY
        self.o_turns = 0
        self.mistake_used = False
        self.pending = False
        self.hint_shown = False
        self.status.set("Du bist dran: Wähle deine Eröffnung.")
        self.details.set("O macht höchstens einen entscheidenden Fehler und spielt sonst optimal. "
                         "Im späteren Modus kann die passende Gelegenheit ausbleiben.")
        if self.mode.get() == "Späte Trainingsstellung laden":
            self.board = random.choice(late_puzzles())
            self.o_turns = self.board.count("O")
            self.mistake_used = True
            self.status.set("O hat einen späteren Fehler gemacht. Finde den Gewinnweg!")
            self.details.set("Es gibt keinen sofortigen Gewinnzug. O verteidigt sich ab jetzt optimal.")
        self.refresh()

    def refresh(self):
        for i, button in enumerate(self.cells):
            button.configure(text="" if self.board[i] == "." else self.board[i],
                             state=("normal" if self.board[i] == "." and
                                    not self.pending and result(self.board) is None
                                    else "disabled"),
                             bg="#dcfce7" if self.hint_shown and i in best_x_moves(self.board)
                             and not self.pending and result(self.board) is None
                             else "SystemButtonFace")

    def play(self, i):
        if self.pending or self.board[i] != "." or result(self.board) is not None:
            return
        if self.board == EMPTY and i not in (0, 1, 4):
            self.status.set("Für diese Übung beginne auf Feld 1, 2 oder 5.")
            return
        before = value(self.board, "X")
        self.board = self.board[:i] + "X" + self.board[i + 1:]
        after = value(self.board, "O")
        self.hint_shown = False
        self.details.set("")
        if result(self.board) is not None:
            self.finish()
            return
        if after < before:
            self.status.set("Dieser Zug hat deine Stellung verschlechtert. O antwortet optimal …")
        else:
            self.status.set("O ist am Zug …")
        self.pending = True
        self.refresh()
        self.pending_job = self.after(250, self.opponent)

    def opponent(self):
        self.pending_job = None
        self.o_turns += 1
        challenging = self.mode.get() != "Beim ersten O-Zug"
        target = not challenging or self.o_turns >= 2
        i, self.board, blunder = choose_o_move(
            self.board, make_mistake=target and not self.mistake_used,
            challenging=challenging)
        if blunder:
            self.mistake_used = True
        self.pending = False
        self.hint_shown = False
        self.status.set(f"O hat Feld {i + 1} gewählt. Du bist dran.")
        self.details.set("Prüfe selbst, ob du jetzt einen Sieg erzwingen kannst.")
        if result(self.board) is not None:
            self.finish()
        else:
            self.refresh()

    def hint(self):
        if self.pending or result(self.board) is not None or self.board == EMPTY:
            return
        assessment = value(self.board, "X")
        name = {1: "X kann gewinnen", 0: "Bei optimalem Spiel Remis",
                -1: "O kann gewinnen"}[assessment]
        good = best_x_moves(self.board)
        self.hint_shown = True
        self.status.set(name + ". Beste Züge: " + ", ".join(str(i + 1) for i in good) + ".")
        self.details.set("Grün markierte Felder bewahren den bestmöglichen Ausgang; "
                         "O verteidigt sich danach optimal.")
        self.refresh()

    def finish(self):
        outcome = result(self.board)
        self.status.set({1: "X gewinnt!", 0: "Remis.", -1: "O gewinnt."}[outcome])
        note = ("O hat genau einen entscheidenden Fehler gemacht."
                if self.mistake_used else
                "In dieser Runde gab es keinen entscheidenden O-Fehler.")
        self.details.set(note + " Starte eine neue Runde für eine andere Stellung.")
        self.refresh()


if __name__ == "__main__":
    Trainer().mainloop()
