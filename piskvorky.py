import random

class Grid:
    _MAX = 3

    def __init__(self):
        self.grid = [[" " for _ in range(self._MAX)] for _ in range(self._MAX)]

    def show(self):
        print("\n")
        print("   " + "   ".join(map(str, range(self._MAX))))
        line = "  " + "-" * (4 * self._MAX - 1)
        print(line)
        for r in range(self._MAX):
            row_label = chr(r + ord("a"))
            row = " | ".join(self.grid[r])
            print(f"{row_label}| {row} |")
            print(line)
        print()

    def is_full(self):
        return all(self.grid[r][c] != " " for r in range(self._MAX) for c in range(self._MAX))

    def is_winner(self, mark):
        # řádky
        for row in self.grid:
            if all(cell == mark for cell in row):
                return True
        # sloupce
        for column in range(self._MAX):
            if all(self.grid[r][column] == mark for r in range(self._MAX)):
                return True
        # diagonály
        if all(self.grid[i][i] == mark for i in range(self._MAX)):
            return True
        if all(self.grid[i][self._MAX - 1 - i] == mark for i in range(self._MAX)):
            return True
        return False

    def is_free(self, r, c):
        return self.grid[r][c] == " "

    def set_move(self, r, c, mark):
        self.grid[r][c] = mark

class Player:
    def __init__(self, mark):
        self.mark = mark

    def do_move(self, grid):
        while True:
            try:
                move = input("Zadej řádek a sloupec: ")
                if move in ("q", "Q"):
                    return False
                r = ord(move[0]) - ord("a")
                c = int(move[1])
            except (IndexError, ValueError):
                print("Chybně zadaný tah, musí být ve tvaru rs, například b1.")
                continue

            if 0 <= r < grid._MAX and 0 <= c < grid._MAX and grid.is_free(r, c):
                grid.set_move(r, c, self.mark)
                break
            else:
                print("Neplatný tah, zkus znovu.")
        return True

class Computer:
    def __init__(self, mark, opponent):
        self.mark = mark
        self.opponent = opponent

    def do_move(self, grid):
        # 1. pokus vyhrát
        for r, c in self.free_cells(grid):
            grid.set_move(r, c, self.mark)
            if grid.is_winner(self.mark):
                #print(f"Počítač táhne na {chr(r + ord("a"))}{c} (výhra)")
                return True
            grid.set_move(r, c, " ")

        # 2. zablokuj hráče
        for r, c in self.free_cells(grid):
            grid.set_move(r, c, self.opponent)
            if grid.is_winner(self.opponent):
                grid.set_move(r, c, self.mark)
                #print(f"Počítač táhne na {chr(r + ord("a"))}{c} (blokuje)")
                return True
            grid.set_move(r, c, " ")

        # 3. jinak náhodně
        r, c = random.choice(self.free_cells(grid))
        grid.set_move(r, c, self.mark)
        #print(f"Počítač táhne na {chr(r + ord("a"))}{c} (náhodně)")
        return True

    def free_cells(self, grid: Grid):
        return [(r, c) for r in range(grid._MAX) for c in range(grid._MAX) if grid.is_free(r, c)]

class Game:
    def __init__(self):
        self.grid = Grid()
        self.player = Player("X")
        self.computer = Computer("O", "X")
        self.current = self.player  # člověk začíná

    def run(self):
        while True:
            self.grid.show()
            if not self.current.do_move(self.grid):
                break

            if self.grid.is_winner(self.current.mark):
                self.grid.show()
                print(f"Vyhrál {self.current.mark}!")
                break
            if self.grid.is_full():
                self.grid.show()
                print("Remíza!")
                break

            # střídání hráčů
            if self.current == self.player:
                self.current = self.computer
            else:
                self.current = self.player

if __name__ == "__main__":
    game = Game()
    game.run()
