#!/usr/bin/env python3
import sys, os, json
# Check to make sure we are running the correct version of Python
assert sys.version_info >= (3,7), "This script requires at least Python 3.7"

# The game and item description files (in the same folder as this script)
game_file = 'zork.json'
item_file = 'items.json'
inventory = []



# Load the contents of the files into the game and items dictionaries. You can largely ignore this
# Sorry it's messy, I'm trying to account for any potential craziness with the file location
def load_files():
    try:
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        with open(os.path.join(__location__, game_file)) as json_file: game = json.load(json_file)
        with open(os.path.join(__location__, item_file)) as json_file: items = json.load(json_file)
        return (game,items)
    except:
        print("There was a problem reading either the game or item file.")
        os._exit(1)


def check_inventory(item):
    for i in inventory:
        if i == item:
            return True
        return False

def calculate_points(items):
    points = 0
    for i in inventory:
        if i in items:
            points += items[i]["points"]
    return points


def render(game,items,current,moves,points):
    c = game[current]
    print("\n\n{} Moves\t\t\t\t{} Points".format(moves, points))
    print("\n\nYou are in section " + c["name"])
    print(c["desc"])


    for item in c["items"]:
        if not check_inventory(item["item"]):
            print(item["desc"])


    for i in inventory:
        if i in items:
            if current in items[i]["exits"]:
                print(items[i]["exits"][current])
    


def get_input():
    response = input("\nWhat would you like to do? Or which direction would you like to walk?")
    response = response.upper().strip()
    return response



def update(game,items,current,response):
    if response == "INVENTORY":
        print("You are carrying:")
        if len(inventory) == 0:
            print("Nothing")
        else:
            for i in inventory:
                print(i.lower())
        return current

    c = game[current]
    for e in c["exits"]:   
        if response == e["exit"]:   #If the response == the Exit of the current location then return the current to the corresponding target
            return e["target"]

    for item in c["items"]:
        if response == "GET " + item["item"] and not check_inventory(item["item"]):
            print(item["take"])
            inventory.append(item["item"])
            return current

    for i in inventory:
        if i in items:
            for action in items[i]["actions"]:
                if response == action + " " + i:
                    print(items[i]["actions"][action])
                    return current


    if response[0:3] == "GET":
        print("You can't take that!")
    elif response in ["NW","NE","SW","SE","UP","DOWN"]:
        print("You can't go that way!")
    else:
        print("I don't understand what you are trying to do.")

    return current




# The main function for the game
def main():
    current = 'A1'  # The starting location
    end_game = 'E6'  # Any of the end-game locations
    moves = 0
    points = 0

    (game,items) = load_files()

   
    while True:  # Start of the never ending game loop
        render(game,items,current,moves,points)
        response = get_input()

        if response == "QUIT":
            break

        current = update(game,items,current,response)
        moves += 1
        points = calculate_points(items)

    print("You scored {} points in {} moves".format(points,moves))





# run the main function
if __name__ == '__main__':
    main()