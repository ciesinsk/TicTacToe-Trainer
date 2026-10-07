"""Tic-Tac-Toe Trainer

Start: python tic_tac_toe_training.py
Tkinter; für den README-Viewer zusätzlich: pip install -r requirements.txt
"""

import random
import tkinter as tk
import webbrowser
from functools import lru_cache
from pathlib import Path
from tkinter import messagebox, ttk


LINES = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
)
EMPTY = "." * 9


def render_readme(content):
    """Erzeugt HTML im Speicher; die README bleibt die einzige Quelldatei."""
    import markdown

    body = markdown.markdown(content, extensions=["tables", "fenced_code"])
    return """<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
body { font-family: sans-serif; font-size: 14px; color: #202020;
       background-color: white; margin: 20px; }
h1 { font-size: 26px; } h2 { font-size: 20px; }
p, li { line-height: 1.5; }
table { border-collapse: collapse; width: 100%; }
th, td { border: 1px solid #cccccc; padding: 8px; text-align: left; }
th { background-color: #eeeeee; }
pre { background-color: #f3f3f3; padding: 12px; }
code { font-family: monospace; }
a { color: #1559a6; }
</style></head><body>""" + body + "</body></html>"


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


def other(symbol):
    return "O" if symbol == "X" else "X"


def sign(symbol):
    return 1 if symbol == "X" else -1


def best_moves(board, symbol):
    best = max(sign(symbol) * score(next_board, other(symbol))
               for _, next_board in moves(board, symbol))
    return [i for i, next_board in moves(board, symbol)
            if sign(symbol) * score(next_board, other(symbol)) == best]


def immediate_win(board, symbol):
    """Kann symbol mit genau einem Zug eine Reihe vollenden?"""
    return any(result(next_board) == sign(symbol)
               for _, next_board in moves(board, symbol))


def choose_computer_move(board, symbol, make_mistake=False, rng=None,
                         challenging=False):
    """Computer spielt optimal, außer bei höchstens einem entscheidenden Fehler."""
    rng = rng or random
    player = other(symbol)
    choices = moves(board, symbol)
    if make_mistake and value(board, symbol) == 0:
        mistakes = [(i, b) for i, b in choices
                    if value(b, player) == sign(player)
                    and (not challenging or not immediate_win(b, player))]
        if mistakes:
            if challenging:
                hardest = max(sign(symbol) * score(b, player)
                              for _, b in mistakes)
                mistakes = [(i, b) for i, b in mistakes
                            if sign(symbol) * score(b, player) == hardest]
            return (*rng.choice(mistakes), True)
    best = max(sign(symbol) * score(b, player) for _, b in choices)
    optimal = [(i, b) for i, b in choices
               if sign(symbol) * score(b, player) == best]
    threats = {i for i, b in moves(board, player)
               if result(b) == sign(player)}
    blocking = [(i, b) for i, b in optimal if i in threats]
    if blocking:
        optimal = blocking
    # In bereits verlorenen Stellungen möglichst viele Drohungen abwehren.
    fewest_threats = min(sum(result(next_board) == sign(player)
                             for _, next_board in moves(b, player))
                         for _, b in optimal)
    optimal = [(i, b) for i, b in optimal
               if sum(result(next_board) == sign(player)
                      for _, next_board in moves(b, player)) == fewest_threats]
    i, b = rng.choice(optimal)
    return i, b, False


@lru_cache(maxsize=2)
def late_puzzles(player):
    """Stellungen nach einem späteren Fehler des jeweiligen Computers."""
    computer = other(player)
    puzzles = set()
    visited = set()

    def collect(board, turn):
        key = board, turn
        if key in visited or result(board) is not None:
            return
        visited.add(key)
        if turn == computer and board.count(computer) >= (1 if computer == "O" else 2):
            if value(board, computer) == 0:
                puzzles.update(next_board for _, next_board in moves(board, computer)
                               if value(next_board, player) == sign(player)
                               and not immediate_win(next_board, player))
        for _, next_board in moves(board, turn):
            if value(next_board, other(turn)) == 0:
                collect(next_board, other(turn))

    collect(EMPTY, "X")
    return tuple(sorted(puzzles))


class Trainer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tic-Tac-Toe: Training")
        self.resizable(False, False)
        self.board = EMPTY
        self.computer_turns = 0
        self.mistake_used = False
        self.pending = False
        self.pending_job = None
        self.hint_shown = False
        self.readme_window = None
        self.player = tk.StringVar(value="X")
        self.mode = tk.StringVar(value="Früh: bei erster Gelegenheit")
        self.status = tk.StringVar()
        self.details = tk.StringVar()

        frame = ttk.Frame(self, padding=16)
        frame.grid()
        ttk.Label(frame, text="Übe gegen einen perfekten Gegner oder nutze einen Fehler aus.").grid(
            row=0, column=0, columnspan=3, sticky="w")
        ttk.Label(frame, text="Du spielst:").grid(row=1, column=0, sticky="w", pady=(10, 4))
        role = ttk.Combobox(frame, state="readonly", textvariable=self.player, width=5,
                            values=("X", "O"))
        role.grid(row=1, column=1, columnspan=2, sticky="w", pady=(10, 4))
        role.bind("<<ComboboxSelected>>", lambda _: self.new_game())
        ttk.Label(frame, text="Modus:").grid(row=2, column=0, sticky="w", pady=(4, 8))
        menu = ttk.Combobox(frame, state="readonly", textvariable=self.mode, width=36,
                            values=("Perfekter Gegner (kein Fehler)",
                                    "Früh: bei erster Gelegenheit", "Später: kein Sofortgewinn",
                                    "Späte Trainingsstellung laden"))
        menu.grid(row=2, column=1, columnspan=2, sticky="w", pady=(4, 8))
        menu.bind("<<ComboboxSelected>>", lambda _: self.new_game())

        self.cells = []
        for i in range(9):
            r, c = divmod(i, 3)
            button = tk.Button(frame, width=5, height=2, font=("Arial", 22, "bold"),
                               command=lambda j=i: self.play(j))
            button.grid(row=r + 3, column=c, padx=3, pady=3)
            self.cells.append(button)

        controls = ttk.Frame(frame)
        controls.grid(row=6, column=0, columnspan=3, pady=(10, 0))
        ttk.Button(controls, text="Zug prüfen / Tipp", command=self.hint).pack(side="left", padx=3)
        ttk.Button(controls, text="Neue Runde", command=self.new_game).pack(side="left", padx=3)
        ttk.Button(controls, text="README / Hilfe", command=self.show_readme).pack(side="left", padx=3)
        ttk.Label(frame, textvariable=self.status, wraplength=340).grid(
            row=7, column=0, columnspan=3, sticky="w", pady=(12, 3))
        ttk.Label(frame, textvariable=self.details, wraplength=340).grid(
            row=8, column=0, columnspan=3, sticky="w")
        self.new_game()

    def show_readme(self):
        """Öffnet die lokale README in einem eigenen, schreibgeschützten Fenster."""
        if self.readme_window is not None and self.readme_window.winfo_exists():
            self.readme_window.deiconify()
            self.readme_window.lift()
            self.readme_window.focus_set()
            return

        readme_path = Path(__file__).resolve().with_name("README.md")
        try:
            content = readme_path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            messagebox.showerror(
                "README nicht verfügbar",
                f"Die README konnte nicht gelesen werden:\n{readme_path}\n\n{exc}",
                parent=self)
            return

        try:
            from tkinterweb import HtmlFrame
            html = render_readme(content)
        except ImportError:
            messagebox.showerror(
                "README-Viewer nicht installiert",
                "Für die formatierte Anzeige werden Markdown und TkinterWeb benötigt.\n\n"
                "Installiere sie mit:\npython -m pip install -r requirements.txt",
                parent=self)
            return

        window = tk.Toplevel(self)
        self.readme_window = window
        window.title("Tic-Tac-Toe: README / Hilfe")
        window.geometry("760x560")
        window.minsize(420, 300)
        window.transient(self)
        window.rowconfigure(0, weight=1)
        window.columnconfigure(0, weight=1)

        try:
            viewer = HtmlFrame(window, messages_enabled=False, javascript_enabled=False,
                               on_link_click=webbrowser.open)
            viewer.grid(row=0, column=0, sticky="nsew", padx=12, pady=(12, 0))
            viewer.load_html(html, base_url=readme_path.as_uri())
        except tk.TclError as exc:
            window.destroy()
            self.readme_window = None
            messagebox.showerror("README-Viewer nicht verfügbar", str(exc), parent=self)
            return
        ttk.Button(window, text="Schließen", command=window.destroy).grid(
            row=1, column=0, pady=12)
        window.bind("<Escape>", lambda _: window.destroy())
        viewer.focus_set()

    def new_game(self):
        if self.pending_job is not None:
            self.after_cancel(self.pending_job)
            self.pending_job = None
        self.board = EMPTY
        self.computer_turns = 0
        self.mistake_used = False
        self.pending = False
        self.hint_shown = False
        player = self.player.get()
        computer = other(player)
        self.status.set("Du bist dran: Wähle deine Eröffnung." if player == "X"
                        else "X beginnt …")
        if self.mode.get() == "Perfekter Gegner (kein Fehler)":
            self.details.set(f"{computer} spielt durchgehend optimal. Bei fehlerfreiem Spiel endet die Partie remis.")
        else:
            self.details.set(f"{computer} macht höchstens einen entscheidenden Fehler und spielt sonst optimal. "
                             "Im späteren Modus kann die passende Gelegenheit ausbleiben.")
        if self.mode.get() == "Späte Trainingsstellung laden":
            self.board = random.choice(late_puzzles(player))
            self.computer_turns = self.board.count(computer)
            self.mistake_used = True
            self.status.set(f"{computer} hat einen späteren Fehler gemacht. Finde den Gewinnweg!")
            self.details.set(f"Es gibt keinen sofortigen Gewinnzug. {computer} verteidigt sich ab jetzt optimal.")
        elif player == "O":
            self.pending = True
            self.pending_job = self.after(250, self.opponent)
        self.refresh()

    def refresh(self):
        for i, button in enumerate(self.cells):
            button.configure(text="" if self.board[i] == "." else self.board[i],
                             state=("normal" if self.board[i] == "." and
                                    (self.board.count("X") == self.board.count("O"))
                                    == (self.player.get() == "X") and
                                    not self.pending and result(self.board) is None
                                    else "disabled"),
                             bg="#dcfce7" if self.hint_shown and i in best_moves(self.board, self.player.get())
                             and not self.pending and result(self.board) is None
                             else "SystemButtonFace")

    def play(self, i):
        player = self.player.get()
        computer = other(player)
        if (self.pending or self.board[i] != "." or result(self.board) is not None
                or (self.board.count("X") == self.board.count("O")) != (player == "X")):
            return
        before = sign(player) * value(self.board, player)
        self.board = self.board[:i] + player + self.board[i + 1:]
        after = sign(player) * value(self.board, computer)
        self.hint_shown = False
        self.details.set("")
        if result(self.board) is not None:
            self.finish()
            return
        if after < before:
            self.status.set(f"Dieser Zug hat deine Stellung verschlechtert. {computer} antwortet optimal …")
        else:
            self.status.set(f"{computer} ist am Zug …")
        self.pending = True
        self.refresh()
        self.pending_job = self.after(250, self.opponent)

    def opponent(self):
        self.pending_job = None
        computer = other(self.player.get())
        self.computer_turns += 1
        mode = self.mode.get()
        challenging = mode in ("Später: kein Sofortgewinn", "Späte Trainingsstellung laden")
        target = (mode != "Perfekter Gegner (kein Fehler)"
                  and (not challenging or self.computer_turns >= (3 if computer == "X" else 2)))
        i, self.board, blunder = choose_computer_move(
            self.board, computer, make_mistake=target and not self.mistake_used,
            challenging=challenging)
        if blunder:
            self.mistake_used = True
        self.pending = False
        self.hint_shown = False
        self.status.set(f"{computer} hat Feld {i + 1} gewählt. Du bist dran.")
        self.details.set("Prüfe selbst, ob du jetzt einen Sieg erzwingen kannst."
                         if mode != "Perfekter Gegner (kein Fehler)"
                         else f"{computer} hat ohne absichtlichen Fehler gespielt.")
        if result(self.board) is not None:
            self.finish()
        else:
            self.refresh()

    def hint(self):
        if self.pending or result(self.board) is not None or self.board == EMPTY:
            return
        player = self.player.get()
        computer = other(player)
        assessment = sign(player) * value(self.board, player)
        name = {1: f"{player} kann gewinnen", 0: "Bei optimalem Spiel Remis",
                -1: f"{computer} kann gewinnen"}[assessment]
        good = best_moves(self.board, player)
        self.hint_shown = True
        self.status.set(name + ". Beste Züge: " + ", ".join(str(i + 1) for i in good) + ".")
        self.details.set("Grün markierte Felder bewahren den bestmöglichen Ausgang; "
                         f"{computer} verteidigt sich danach optimal.")
        self.refresh()

    def finish(self):
        outcome = result(self.board)
        self.status.set({1: "X gewinnt!", 0: "Remis.", -1: "O gewinnt."}[outcome])
        computer = other(self.player.get())
        note = (f"{computer} hat genau einen entscheidenden Fehler gemacht."
                if self.mistake_used else
                f"{computer} hat ohne entscheidenden Fehler gespielt.")
        self.details.set(note + " Starte eine neue Runde für eine andere Stellung.")
        self.refresh()


if __name__ == "__main__":
    Trainer().mainloop()
