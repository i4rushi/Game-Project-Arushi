"""
Author: Arushi Gupta, gupt1077@purdue.edu
Assignment: 12.1 - Battleship
Date: 11/27/2023

Description:
    This program allows the user to play the game Battleship, see instructions, see a sample map, and keeps track of a hall of fame.
"""

import random

def make_grid():
    grid = [['~' for _ in range(12)] for _ in range(10)]
    ships = {'M': 5, 'B': 4, 'D': 3, 'S': 3, 'P': 2}

    for ship, size in ships.items():
        place_ship(grid, ship, size)

    return grid

def is_valid_position(grid, row, col, size, orientation):
    if orientation == 'horizontal':
        return all(grid[row][col + i] == '~' for i in range(size))
    else:  # vertical
        return all(grid[row + i][col] == '~' for i in range(size))

def place_ship(grid, ship, size):
    while True:
        orientation = random.choice(['horizontal', 'vertical'])
        if orientation == 'horizontal':
            row = random.randint(0, 9)
            col = random.randint(0, 11 - size)
        else:  # vertical
            row = random.randint(0, 9 - size)
            col = random.randint(0, 11)

        if is_valid_position(grid, row, col, size, orientation):
            for i in range(size):
                if orientation == 'horizontal':
                    grid[row][col + i] = ship
                else:
                    grid[row + i][col] = ship
            break

class BattleshipGame:
    def __init__(self):
        self.grid_size = 10
        self.grid = make_grid()  # Use make_grid to generate a randomized grid
        self.ships = {'P': 2, 'S': 3, 'D': 4, 'M': 5, 'B': 3}
        self.ship_names = {
            'P': 'Patrol Ship',
            'S': 'Stealth Ship',
            'D': 'Destroyer',
            'M': 'Mothership',
            'B': 'Battleship'
        }
        self.ship_hits = {ship: 0 for ship in self.ships}
        self.hits = 0
        self.shots = 0
        self.hit_positions = set()

    def print_grid(self):
        header = "\n   " + "  ".join([chr(c) for c in range(ord("A"), ord("L") + 1)])
        print(header)

        for i, row in enumerate(self.grid):
            #display_row = [str(cell) for cell in row]
            display_row = ['~' if cell in 'MBDSP' else cell for cell in row]
            row_str = "  ".join(display_row)
            print(f"{i}  {row_str}")

    def guess(self, row, col):
        position = (row, col)
        if position in self.hit_positions:
            print("\nYou've already targeted that location")
        elif self.grid[row][col] == '~': 
            print('\nmiss')
            self.grid[row][col] = 'o'
        elif self.grid[row][col] in self.ships:
            print("\nIT'S A HIT!")
            ship_type = self.grid[row][col]
            self.hits += 1
            self.hit_positions.add(position)
            self.grid[row][col] = 'x'
            if not any(ship_type in row for row in self.grid):
                print(f"The enemy's {self.ship_names[ship_type]} has been destroyed.")

        else:
            print("\nYou've already hit this location")
        
        self.shots += 1
        if self.hits == sum(self.ships.values()):
            print("\nYou've destroyed the enemy fleet!\nHumanity has been saved from the threat of AI.\n\nFor now ...\n")
            return True
        return False

        
    def get_accuracy(self):
        if self.shots == 0:
            return 0.0
        return self.hits / self.shots

def play_battleship(hall_of_fame):
    game = BattleshipGame()
    
    while True:
        game.print_grid()
        user_input = input('\nWhere should we target next (q to quit)? ')

        if user_input.lower() == 'q':
            break

        while len(user_input) != 2 or not user_input[0].isdigit() or not user_input[1].isalpha():
            if user_input.lower() == 'q':
                return 
            elif(len(user_input) != 2):
               print('Please enter exactly two characters.')
            elif (not user_input[0].isdigit() or not user_input[1].isalpha()): 
                print('Please enter a location in the form "6G".')
            user_input = input('\nWhere should we target next (q to quit)? ')
            continue

        try:
            guess_row = int(user_input[:-1])
            guess_col = ord(user_input[-1].upper()) - ord('A')
        except (ValueError, IndexError):
            continue

        if 0 <= guess_row < game.grid_size and 0 <= guess_col < len(game.grid[0]):
            if game.guess(guess_row, guess_col):
                accuracy = game.get_accuracy()
                print(f"Congratulations, you have achieved a targeting accuracy of\n{accuracy:.2%} and earned a spot in the Hall of Fame.")
                player_name = input("Enter your name: ")
                new_record = (accuracy, player_name)
                hall_of_fame.append(new_record)
                hall_of_fame.sort(key=lambda x: x[0], reverse=True)
                save_hall_of_fame(hall_of_fame)
                display_hall_of_fame(hall_of_fame)

                break

def load_hall_of_fame():
    # Load hall of fame records from the file
    hall_of_fame = []

    try:
        with open("battleship_hof_short.txt", "r") as file:  # Update to your correct file name
            header = next(file)
            if "misses" not in header.lower() or "name" not in header.lower():
                print("Invalid file format. Missing 'misses' or 'name' in the header.")
                return hall_of_fame
            for line in file:
                misses, name = line.strip().split(',')
                hall_of_fame.append((float(misses), name))
    except FileNotFoundError:
        pass

    return hall_of_fame

def save_hall_of_fame(hall_of_fame):
    # Save hall of fame records to the file
    with open("battleship_hof_short.txt", "w") as file:
        file.write("Misses,Name\n")
        for record in hall_of_fame:
            file.write(f"{record[0]},{record[1]}\n")


def display_hall_of_fame(hall_of_fame):
    sorted_hall_of_fame = sorted(hall_of_fame, key=lambda x: x[0], reverse=True)

    print("\nHall of Fame:")
    print("+------+-------------+----------+")
    print("| Rank | Player Name | Accuracy |")
    print("+------+-------------+----------+")
    for i, record in enumerate(sorted_hall_of_fame, start=1):
        display_accuracy = record[0] * 100
        
        print(f"| {i:^5}| {record[1]:^11} | {display_accuracy:7.2f}% |") 
    print("+------+-------------+----------+")


def main():
    hall_of_fame = load_hall_of_fame()  # List to store hall of fame records

    print("\n                   ~ Welcome to Battleship! ~                   ")
    print('')
    print("ChatGPT has gone rogue and commandeered a space strike fleet.")
    print("It's on a mission to take over the world.  We've located the")
    print("stolen ships, but we need your superior intelligence to help")
    print("destroy them before it's too late.")

    while True:
        print("\nMenu:")
        print("  1 : Instructions")
        print("  2 : View Example Map")
        print("  3 : New Game")
        print("  4 : Hall of Fame")
        print("  5 : Quit")

        choice = input("What would you like to do? ")

        if choice == '1':
            # View Instructions
            print("\nInstructions:")
            print("\nShips are positioned at fixed locations in a 10-by-12 grid. The")
            print("rows of the grid are labeled 0 through 9, and the columns are")
            print('labeled A through L. Use menu option "2" to see an example.')
            print("Target the ships by entering the row and column of the location")
            print("you wish to shoot. A ship is destroyed when all of the spaces")
            print("it fills have been hit. Try to destroy the fleet with as few")
            print("shots as possible. The fleet consists of the following 5 ships:")
            print("")
            print("Size : Type")
            print("   5 : Mothership") 
            print("   4 : Battleship")         
            print("   3 : Destroyer")          
            print("   3 : Stealth Ship")                  
            print("   2 : Patrol Ship")

        elif choice == '2':
            grid = make_grid()
            header = "\n   " + "  ".join([chr(c) for c in range(ord("A"), ord("L") + 1)])
            print(header)

            for i, row in enumerate(grid):
                display_row = [str(cell) for cell in row]
                row_str = "  ".join(display_row)
                print(f"{i}  {row_str}")

        elif choice == '3':
            # Start a New Game
            accuracy = play_battleship(hall_of_fame)
            #display_hall_of_fame(hall_of_fame)

        elif choice == '4':
            # View Hall of Fame
            hall_of_fame = load_hall_of_fame()
            display_hall_of_fame(hall_of_fame)

        elif choice == '5':
            print("\nGoodbye")
            break

        else:
            print("\nInvalid selection.  Please choose a number from the menu.")


if __name__ == "__main__":
    main()
