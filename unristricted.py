import os

class Game:
    def __init__(self):
        self.board_size = 10
        self.board = {}  # (row, col) -> 'X' or 'O'
        self.current_player = 'X'
        
    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def get_position(self, num: int) -> tuple[int, int]:
        """Convert a number to (row, col) position."""
        return divmod(num, self.board_size)
    
    def print_board(self):
        """Prints the current state of the board."""
        self.clear_screen()
        print("=== 10x10 (5-IN-A-ROW) ===")
        print(f"Player: {self.current_player}\n")
        
        for row in range(self.board_size):
            line = ""
            for col in range(self.board_size):
                if (row, col) in self.board:
                    line += f" {self.board[(row, col)]} "
                else:
                    pos = row * self.board_size + col
                    line += f"{pos:>3}"
            print(line)
        print()
    
    def is_valid_move(self, row: int, col: int) -> bool:
        """Check if move is within 3 Manhattan distance of any existing piece."""
        if not self.board:
            return True  # First move can be anywhere
        
        for existing_row, existing_col in self.board:
            if abs(row - existing_row) + abs(col - existing_col) <= 3:
                return True
        return False
    
    def place_piece(self, position: int) -> tuple[bool, str]:
        """Attempt to place a piece at the given position number."""
        if not (0 <= position < self.board_size ** 2):
            return False, "Invalid position"
        
        row, col = self.get_position(position)
        
        if (row, col) in self.board:
            return False, "Position already occupied"
        
        if not self.is_valid_move(row, col):
            return False, "Move too far from existing pieces"
        
        self.board[(row, col)] = self.current_player
        
        if self.check_win(row, col):
            return True, f"{self.current_player} wins!"
        
        # Swap players
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        return True, f"{self.current_player}'s turn"
    
    def check_win(self, row: int, col: int) -> bool:
        """Check whether the current move results in 5 in a row."""
        player = self.board[(row, col)]
        directions = [
            (0, 1),   # Horizontal
            (1, 0),   # Vertical
            (1, 1),   # Diagonal down-right
            (1, -1),  # Diagonal down-left
        ]
        
        for dr, dc in directions:
            count = 1
            for sign in [1, -1]:
                for i in range(1, 5):
                    r = row + sign * dr * i
                    c = col + sign * dc * i
                    if (r, c) in self.board and self.board[(r, c)] == player:
                        count += 1
                    else:
                        break
            if count >= 5:
                return True
        return False
    
    def run_game(self):
        """Main game loop."""
        print("Welcome to 10x10!")
        print("Goal: Get 5 in a row.")
        print("Enter position numbers (0–99) to play.")
        input("Press Enter to start...")
        
        while True:
            self.print_board()
            
            if not self.board:
                print("First move: place anywhere.")
            else:
                print("Next move: must be within 3 spaces of an existing piece.")
            
            try:
                position = int(input(f"{self.current_player}'s move (0–99): "))
                success, message = self.place_piece(position)
                print(f"Result: {message}")
                
                if "wins" in message:
                    self.print_board()
                    print("Game Over!")
                    break
            
            except ValueError:
                print("Invalid input. Please enter a number.")
                input("Press Enter to continue...")
            except KeyboardInterrupt:
                print("\nGame interrupted. Thanks for playing!")
                break

if __name__ == "__main__":
    game = Game()
    game.run_game()