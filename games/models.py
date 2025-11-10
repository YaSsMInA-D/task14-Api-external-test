from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    # Player choices - matches task requirement
    PLAYER_1 = '1'
    PLAYER_2 = '2'
    PLAYER_CHOICES = [
        (PLAYER_1, 'Player 1'),
        (PLAYER_2, 'Player 2'),
    ]
    
    # Game states - simplified as per task requirement
    STATUS_ACTIVE = 'active'
    STATUS_WON = 'won'
    STATUS_TIE = 'tie'
    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Active'),
        (STATUS_WON, 'Won'),
        (STATUS_TIE, 'Tie'),
    ]
    
    room_name = models.CharField(max_length=100, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='games_owned')
    
    # Board: 9-character string representing 3x3 grid
    # Use 'X' for player 1, 'O' for player 2, ' ' for empty
    board = models.CharField(max_length=9, default=' ' * 9)
    
    # Track whose turn it is (player 1 or 2)
    active_player = models.CharField(
        max_length=1, 
        choices=PLAYER_CHOICES, 
        default=PLAYER_1
    )
    
    # Game state as per task requirement
    game_state = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default=STATUS_ACTIVE
    )
    
    # Store who won (only relevant when game_state='won')
    winner = models.CharField(
        max_length=1, 
        choices=PLAYER_CHOICES, 
        blank=True, 
        null=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.room_name} - {self.get_game_state_display()}"
    
    # Helper methods for board manipulation
    def get_board_as_list(self):
        """Convert board string to 3x3 list for easy access"""
        return [list(self.board[i:i+3]) for i in range(0, 9, 3)]
    
    def set_board_from_list(self, board_list):
        """Convert 3x3 list back to board string"""
        self.board = ''.join(''.join(row) for row in board_list)
    
    def make_move(self, position, player_symbol):
        """Make a move at the given position (0-8)"""
        if self.board[position] == ' ':
            board_list = list(self.board)
            board_list[position] = player_symbol
            self.board = ''.join(board_list)
            return True
        return False
    
    def check_winner(self):
        """Check if there's a winner or tie"""
        board = self.board
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]              # diagonals
        ]
        
        for combo in winning_combinations:
            if (board[combo[0]] != ' ' and 
                board[combo[0]] == board[combo[1]] == board[combo[2]]):
                return board[combo[0]]  # Returns 'X' or 'O'
        
        if ' ' not in board:
            return 'tie'
        
        return None