import random

user_name = None
board_size = 5
user_board = []
computer_board = []

def generate_board(size):
    board = []
    for i in range(1, (size*size) + 1):
        board.append(i)    
    random.shuffle(board)
    return board

def print_board(board, size, player):
    cell_width = 4 
    horizontal_line = "+" + ("-" * cell_width + "+") * size 

    print(f"\n==================== {player}'s Board ====================\n")

    for i in range(size):
        print(horizontal_line) 
        row = "|"
        for j in range(size):
            value = board[i * size + j]
            row += f"{value:^{cell_width}}" + "|" 
        print(row)  
    print(horizontal_line)  
   
def generate_bingo(lines):
    bingo = "BINGO"
    return bingo[:lines]

def check_bingo(board, board_size):
    line_count = 0

    # Check rows for Bingo
    for i in range(board_size):
        same = True  # Assume the row has all 'X'
        for j in range(board_size):
            if board[i * board_size + j] != "X":
                same = False
                break
        if same:
            line_count += 1

    # Check columns for Bingo
    for i in range(board_size):
        same = True  # Assume the column has all 'X'
        for j in range(board_size):
            if board[j * board_size + i] != "X":
                same = False
                break
        if same:
            line_count += 1

    # Check main diagonal (top-left to bottom-right)
    same = True  # Assume the diagonal has all 'X'
    for i in range(board_size):
        if board[i * board_size + i] != "X":
            same = False
            break
    if same:
        line_count += 1

    # Check anti-diagonal (top-right to bottom-left)
    same = True  # Assume the diagonal has all 'X'
    for i in range(board_size):
        if board[i * board_size + (board_size - 1 - i)] != "X":
            same = False
            break
    if same:
        line_count += 1

    return line_count

def save_game(user_name, user_board, computer_board, numbers_left, board_size):
    with open(f"{user_name}_bingo_save.txt", "w") as save_file:
        # Write user name and board size
        save_file.write(f"{user_name}\n")
        save_file.write(f"{board_size}\n")

        # Write user board
        save_file.write("User Board:\n")
        for i in range(board_size):
            # Convert integers to strings before joining
            save_file.write(" ".join(map(str, user_board[i * board_size:(i + 1) * board_size])) + "\n")

        # Write computer board
        save_file.write("Computer Board:\n")
        for i in range(board_size):
            # Convert integers to strings before joining
            save_file.write(" ".join(map(str, computer_board[i * board_size:(i + 1) * board_size])) + "\n")

        # Write remaining numbers
        save_file.write("Numbers Left:\n")
        save_file.write(" ".join(map(str, numbers_left)) + "\n")

    print(f"Game saved for {user_name}!")


def load_game(user_name):
    try:
        with open(f"{user_name}_bingo_save.txt", "r") as save_file:
            # Read the user's name and board size
            user_name_from_file = save_file.readline().strip()
            board_size = int(save_file.readline().strip())

            # Read user board
            save_file.readline()  # Skip the "User Board:" line
            user_board = []
            for _ in range(board_size):
                row = save_file.readline().strip().split()
                user_board.extend(row)  # Flatten the board rows into a single list

            # Read computer board
            save_file.readline()  # Skip the "Computer Board:" line
            computer_board = []
            for _ in range(board_size):
                row = save_file.readline().strip().split()
                computer_board.extend(row)  # Flatten the board rows into a single list

            # Read numbers left
            save_file.readline()  # Skip the "Numbers Left:" line
            numbers_left = list(map(int, save_file.readline().strip().split()))

            print(f"Game loaded for {user_name_from_file}!")

            # Convert "X" values to strings and numbers to integers
            user_board = [int(x) if x != "X" else "X" for x in user_board]
            computer_board = [int(x) if x != "X" else "X" for x in computer_board]

            # Return the data as a dictionary, with proper types
            return {
                    "user_name": user_name_from_file,
                    "user_board": user_board,
                    "computer_board": computer_board,
                    "numbers_left": numbers_left,
                    "board_size": board_size
            }

    except FileNotFoundError:
        print(f"No saved game found for {user_name}. Starting a new game.")
        return None


def main():
    print("Welcome to the game of Bingo!")

    global user_name
    if user_name is None:
        print("Enter your name: ")
        user_name = input()    
        game_data = load_game(user_name)
    else:
        game_data = None
    
    if game_data:
        print("Do you want to continue the game? (Y/N)")
        continue_game = input().upper()
        if continue_game == "Y":
            user_board = game_data["user_board"]
            computer_board = game_data["computer_board"]
            numbers_left = game_data["numbers_left"]
            board_size = game_data["board_size"]
        else:
            print("Starting a new game...")
            print("Enter 5 to play 5x5 and 7 to play 7x7")
            board_size = int(input())
            user_board = generate_board(board_size)
            computer_board = generate_board(board_size)
            numbers_left = [i for i in range(1, board_size * board_size + 1)]   
    else:
        print("Enter 5 to play 5x5 and 7 to play 7x7")
        board_size = int(input())
        user_board = generate_board(board_size)
        computer_board = generate_board(board_size)
        numbers_left = [i for i in range(1, board_size * board_size + 1)]
    
    
    print_board(user_board, board_size, user_name)
    print_board(computer_board, board_size, "Computer")

    game_over = False
    winner = ""
    
    
    while not game_over:
        user_input = 0
        
        
        while True:
            
            if user_input == "p" or user_input == "P":
                print("Game Paused.")
                print("1) Continue")
                print("2) Save and Exit")
                
                user_choice = input()
            
                if user_choice == "1":
                    user_input = 0
                elif user_choice == "2":
                    save_game(user_name, user_board, computer_board, numbers_left, board_size)
                    exit()
                
                    
            
            elif user_input in user_board:
                numbers_left.remove(user_input)
                user_input_index = user_board.index(user_input)
                computer_input_index = computer_board.index(user_input)
                user_board[user_input_index] = "X"
                computer_board[computer_input_index] = "X"
                print_board(user_board, board_size, user_name)
                print_board(computer_board, board_size, "Computer")
                
                user_line_count = check_bingo(user_board, board_size)
                computer_line_count = check_bingo(computer_board, board_size)
                
                print(f"User Bingo: {generate_bingo(user_line_count)}")
                print(f"Computer Bingo: {generate_bingo(computer_line_count)}")


                if user_line_count == 5 and computer_line_count == 5:
                    winner = "Tie"
                    game_over = True
                elif user_line_count == 5 or generate_bingo(user_line_count) == "BINGO":
                    winner = user_name
                    game_over = True
                elif computer_line_count == 5 or generate_bingo(computer_line_count) == "BINGO":
                    winner = "Computer"
                    game_over = True
                save_game(user_name, user_board, computer_board, numbers_left, board_size)
                break
            else:
                if user_input == 0:
                    try:
                        user_input = input("Enter a number or 'p' to pause: ")
                        if not user_input == "p"  :
                            user_input = int(user_input)
                        else:
                            user_input = 'p'
                    except ValueError:
                        print("Invalid input. Please enter a number")
                        user_input = 0
                        continue
                else:
                    print("Invalid Number. Please enter a different number")
                    try:
                        user_input = input("Enter a number or 'p' to pause: ")
                        if not user_input == "p":
                            user_input = int(user_input)
                        else:
                            user_input = 'p'
                    except ValueError:
                        print("Invalid input. Please enter a number")
                        user_input = 0
                        continue
                
        if not game_over:
            random_number = random.choice(numbers_left)
            if random_number in computer_board:
                numbers_left.remove(random_number)
                user_input_index = user_board.index(random_number)
                computer_input_index = computer_board.index(random_number)
                user_board[user_input_index] = "X"
                computer_board[computer_input_index] = "X"
                print_board(user_board, board_size, user_name)
                print_board(computer_board, board_size, "Computer")
    
                user_line_count = check_bingo(user_board, board_size)
                computer_line_count = check_bingo(computer_board, board_size)
    
                print(f"User Bingo: {generate_bingo(user_line_count)}")
                print(f"Computer Bingo: {generate_bingo(computer_line_count)}")
                
                if user_line_count == 5 and computer_line_count == 5:
                    winner = "Tie"
                    game_over = True
                elif user_line_count == 5:
                    winner = user_name
                    game_over = True
                elif computer_line_count == 5:
                    winner = "Computer"
                    game_over = True
                save_game(user_name, user_board, computer_board, numbers_left, board_size)
                
               
             
    
    print("Game Over! The winner is: ", winner)
    
    
    print("Do you want to play again? (Y/N)")
    play_again = input().upper()
    if play_again == "Y":
        main()
    else:
        print("Thank you for playing Bingo!")
        exit()
            
        
        
        
    
    
    
    



main()
 
    


    



