#!/usr/bin/python3
import random
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class Minesweeper:
    def __init__(self, width=10, height=10, mines=10):
        self.width = width
        self.height = height
        self.mines = set(random.sample(range(width * height), mines))
        self.field = [[' ' for _ in range(width)] for _ in range(height)]
        self.revealed = [[False for _ in range(width)] for _ in range(height)]
        self.flagged = [[False for _ in range(width)] for _ in range(height)]
        self.mines_count = mines

    def print_board(self, reveal=False):
        clear_screen()
        print('  ' + ' '.join(str(i) for i in range(self.width)))
        for y in range(self.height):
            print(y, end=' ')
            for x in range(self.width):
                if reveal or self.revealed[y][x]:
                    if (y * self.width + x) in self.mines:
                        print('*', end=' ')
                    else:
                        count = self.count_mines_nearby(x, y)
                        print(count if count > 0 else ' ', end=' ')
                elif self.flagged[y][x]:
                    print('F', end=' ')
                else:
                    print('.', end=' ')
            print()
        print(f"Mines remaining: {self.mines_count}")

    def count_mines_nearby(self, x, y):
        count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if (ny * self.width + nx) in self.mines:
                        count += 1
        return count

    def reveal(self, x, y):
        if (y * self.width + x) in self.mines:
            return False
        if self.revealed[y][x] or self.flagged[y][x]:
            return True
        self.revealed[y][x] = True
        if self.count_mines_nearby(x, y) == 0:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.width and 0 <= ny < self.height and not self.revealed[ny][nx]:
                        self.reveal(nx, ny)
        return True

    def flag(self, x, y):
        if not self.revealed[y][x]:
            if self.flagged[y][x]:
                self.flagged[y][x] = False
                self.mines_count += 1
            else:
                self.flagged[y][x] = True
                self.mines_count -= 1

    def check_win(self):
        for y in range(self.height):
            for x in range(self.width):
                if not self.revealed[y][x] and (y * self.width + x) not in self.mines:
                    return False
        return True

    def play(self):
        while True:
            self.print_board()
            try:
                action = input("Enter 'r' to reveal or 'f' to flag, followed by coordinates (e.g., r 3 4): ").split()
                if len(action) != 3 or action[0] not in ('r', 'f'):
                    print("Invalid input. Use 'r' to reveal or 'f' to flag, followed by x and y coordinates.")
                    continue
                cmd, x, y = action[0], int(action[1]), int(action[2])
                if x < 0 or x >= self.width or y < 0 or y >= self.height:
                    print("Coordinates out of bounds. Try again.")
                    continue

                if cmd == 'r':
                    if not self.reveal(x, y):
                        self.print_board(reveal=True)
                        print("Game Over! You hit a mine.")
                        break
                elif cmd == 'f':
                    self.flag(x, y)

                if self.check_win():
                    self.print_board(reveal=True)
                    print("Congratulations! You've cleared the minefield.")
                    break

            except ValueError:
                print("Invalid input. Please enter valid coordinates.")

if __name__ == "__main__":
    game = Minesweeper()
    game.play()