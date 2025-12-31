import random
import discord
import string
from discord.ui import View, Button

# --- UTILS ---

def generate_random_number():
    """Generates a random number between 1 and 100"""
    return random.randint(1, 100)

def help_command():
    """Returns a list of available commands for the help message"""
    help_commands = {
        "!get_help": "Returns all available commands",
        "!give_role @user @rank": "Gives role to selected user",
        "!random_number": "Generate random number from 1 to 100",
        "!generate_password": "Program generates password and checks its strength",
        "!tictactoe": "Play PvP Tic Tac Toe",
        "!tictactoeAI": "Play vs AI Bot",
        "!clear (amount of messages to clear)": "Clears messages about amount(default: 50)"
    }

    help_text = ""
    for command, description in help_commands.items():
        help_text += f"**{command}**: {description}\n"
    return help_text

class PasswordGenerator:
    def __init__(self):
        self.basic_chars = string.ascii_lowercase
        self.capital_chars = string.ascii_uppercase
        self.numbers = string.digits
        self.special_chars = "!@#$%^&*()_-+={[]};:'<,>.?/|"

    def generate(self, length: int, use_caps: bool, use_nums: bool, use_special: bool):
        pool = self.basic_chars
        if use_caps: pool += self.capital_chars
        if use_nums: pool += self.numbers
        if use_special: pool += self.special_chars

        password = "".join(random.choice(pool) for _ in range(length))
        
        # Strength calculation logic
        score = 0
        if length >= 12: score += 1
        if use_caps: score += 1
        if use_nums: score += 1
        if use_special: score += 1
        
        strength = "Weak"
        if score == 4: strength = "Strong"
        elif score == 3: strength = "Medium"
        
        return password, strength

# --- TIC TAC TOE CORE ---

class TicTacToeButton(Button):
    def __init__(self, x, y):
        # Set initial style as secondary (gray/empty)
        super().__init__(style=discord.ButtonStyle.secondary, label="\u200b", row=y)
        self.x = x
        self.y = y

    async def callback(self, interaction: discord.Interaction):
        view = self.view
        
        # Determine if it's AI or PvP mode
        if isinstance(view, TicTacToeAIView):
            # AI Mode checks
            if interaction.user != view.player_x:
                await interaction.response.send_message("This is not your game!", ephemeral=True)
                return
            if view.board[self.y][self.x] != 0:
                return 
            
            await view.process_player_move(self, interaction)

        elif isinstance(view, TicTacToeView):
            # PvP Mode checks
            state = view.board[self.y][self.x]
            if state != 0:
                return

            current_player = view.player_x if view.current_turn == view.X else view.player_o
            
            # Allow player O to join if the slot is empty
            if view.player_o is None and interaction.user != view.player_x:
                view.player_o = interaction.user
                current_player = view.player_o

            if interaction.user != current_player:
                await interaction.response.send_message("To nie Twoja tura!", ephemeral=True)
                return

            await view.process_move(self, interaction)

class TicTacToeView(View):
    X = -1
    O = 1

    def __init__(self, author):
        super().__init__()
        self.player_x = author
        self.player_o = None
        self.current_turn = self.X
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.game_over = False # Fixed naming collision (changed from is_finished)

        # Create the 3x3 grid of buttons
        for y in range(3):
            for x in range(3):
                self.add_item(TicTacToeButton(x, y))

    def disable_all_buttons(self):
        for child in self.children:
            child.disabled = True

    async def process_move(self, button, interaction: discord.Interaction):
        # Process the visual and logical move
        if self.current_turn == self.X:
            button.style = discord.ButtonStyle.success
            button.label = "X"
            self.board[button.y][button.x] = self.X
            self.current_turn = self.O
            content = f"Turn: O ({self.player_o.mention if self.player_o else 'waiting...'})"
        else:
            button.style = discord.ButtonStyle.danger
            button.label = "O"
            self.board[button.y][button.x] = self.O
            self.current_turn = self.X
            content = f"Turn: X ({self.player_x.mention})"
        
        button.disabled = True

        # Check for game end conditions
        winner = self.check_winner()
        if winner is not None:
            self.game_over = True
            self.disable_all_buttons()
            content = f"Winner: {'X' if winner == self.X else 'O'}!"
            self.stop()
        elif self.is_full():
            self.game_over = True
            self.disable_all_buttons()
            content = "It's a Tie!"
            self.stop()

        await interaction.response.edit_message(content=content, view=self)

    def check_winner(self):
        # Check rows, columns and diagonals for 3 in a row
        for row in self.board:
            if abs(sum(row)) == 3: return row[0]
        for col in range(3):
            if abs(self.board[0][col] + self.board[1][col] + self.board[2][col]) == 3: return self.board[0][col]
        diag1 = self.board[0][0] + self.board[1][1] + self.board[2][2]
        diag2 = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if abs(diag1) == 3 or abs(diag2) == 3: return self.board[1][1]
        return None

    def is_full(self):
        return all(all(cell != 0 for cell in row) for row in self.board)

class TicTacToeAIView(TicTacToeView):
    def __init__(self, author):
        super().__init__(author)
        self.player_o = "AI Bot"

    async def process_player_move(self, button, interaction: discord.Interaction):
        # Handle player action
        button.style = discord.ButtonStyle.success
        button.label = "X"
        button.disabled = True 
        self.board[button.y][button.x] = self.X
        
        # Verify if player won or tie
        winner = self.check_winner()
        if winner == self.X or self.is_full():
            self.game_over = True
            self.disable_all_buttons()
            content = f"Winner: {self.player_x.mention}!" if winner == self.X else "It's a Tie!"
            await interaction.response.edit_message(content=content, view=self)
            self.stop()
            return

        # Trigger AI move automatically
        await self.process_ai_move(interaction)
    
    async def process_ai_move(self, interaction: discord.Interaction):
        # AI decision making
        move = self.get_best_move()
        if move:
            y, x = move
            self.board[y][x] = self.O
            for child in self.children:
                if isinstance(child, TicTacToeButton) and child.x == x and child.y == y:
                    child.style = discord.ButtonStyle.danger
                    child.label = "O"
                    child.disabled = True
                    break
        
        # Verify if AI won or tie
        winner = self.check_winner()
        if winner == self.O or self.is_full():
            self.game_over = True
            self.disable_all_buttons()
            content = "Winner: AI Bot!" if winner == self.O else "It's a Tie!"
            self.stop()
        else:
            content = f"Your turn: {self.player_x.mention}"

        await interaction.response.edit_message(content=content, view=self)

    def get_best_move(self):
        # Priority: 1. Win, 2. Block, 3. Center, 4. Random
        for player in [self.O, self.X]:
            for y in range(3):
                for x in range(3):
                    if self.board[y][x] == 0:
                        self.board[y][x] = player
                        if self.check_winner() == player:
                            self.board[y][x] = 0
                            return (y, x)
                        self.board[y][x] = 0
        if self.board[1][1] == 0: return (1, 1)
        available = [(y, x) for y in range(3) for x in range(3) if self.board[y][x] == 0]
        return random.choice(available) if available else None