"""command line menu-driven application that allows a user to display,
sort and update, as needed a List of U.S states containing the state capital,
overall state population, and state flower"""

import json
import sys
import matplotlib.pyplot as plt
from PIL import Image

# Opening JSON file
f = open('states.json', )

# returns JSON object as a dictionary
data = json.load(f)


def goodbye():
    """Print out goodbye message and exit app"""
    print("\nHave a good day. Goodbye!")
    f.close()
    sys.exit()


def print_state(state):
    """Method to print out details about state"""
    print("state: " + state["state"],
          "\nCapital: " + state["capital"],
          "\nPopulation: ", state["population"],
          "\nFlower: " + state["flower"] + "\n")


def validate_state_input(state):
    """Method to validate user enters a valid state"""
    has_abbrev = any(x["abbrev"] == state.lower() for x in data)
    has_name = any(x["state"] == state.lower() for x in data)

    while not state or (not has_abbrev and not has_name):
        state = input("Please enter a valid U.S. State: ")
        has_abbrev = any(x["abbrev"] == state.lower() for x in data)
        has_name = any(x["state"] == state.lower() for x in data)

    return state.lower()


def sort_states():
    """Method to sort state in alphabetical order and display to user"""
    print("Here are the U.S. States in alphabetical order: \n")

    data.sort(key=lambda x: x["state"])
    for i in data:
        print_state(i)


def search_for_state():
    """Method to display state information based on user input"""
    state = input("What state would you like to look up? \n"
                  "Enter state by full name or abbreviation: ")
    state = validate_state_input(state)
    correct_state = next((x for x in data if state in (x["state"], x["abbrev"])), None)

    print_state(correct_state)
    image = Image.open(r'state_flowers/' + correct_state["abbrev"] + '.jpg')

    image.show()


def highest_population():
    """Method that gets top 5 states with highest population and displays graph"""
    data.sort(key=lambda x: x["population"], reverse=True)
    top_5 = data[:5]

    plt.figure()

    states = []
    population = []
    for i in top_5:
        states.append(i["state"])
        population.append(i["population"])

    plt.bar(states, population)

    plt.ylabel('Population')
    plt.xlabel('States')
    plt.title('Top 5 Highest Population States')
    plt.show()


def update_state_population():
    """Method to update a states population based on user's choice"""
    state = input("Which state\'s population would you like to update? \n"
                  "Enter state by full name or abbreviation: ")
    state = validate_state_input(state)

    population = input("Whats the new population? ")
    while not population or not population.isnumeric():
        population = input("Please enter a valid number for the population: ")

    for i in data:
        if state in (i["state"], i["abbrev"]):
            i["population"] = int(population)
            print("Here is the updated state: \n")
            print_state(i)


def user_menu():
    """Method to display menu to user and gets input of what they want to do"""
    print("Welcome to Jackie\'s U.S. states display shop.\n"
          "Select one of the following options: \n\n"
          "a. Display all U.S. states in alphabetical order. \n"
          "b. Search for specific state and display the appropriate information. \n"
          "c. Provide a bar graph of the top 5 populated states. \n"
          "d. Update state population for specific state."
          "e. Exit the program.")

    option = input("\nWhat would you like to do? \n"
                   "Enter \'a\' through \'d\' or to exit program enter \'e\': ")

    valid_inputs = ['a', 'b', 'c', 'd', 'e']

    while not option or option not in valid_inputs:
        option = input("\nOops, you may have accidentally entered an invalid entry. \n"
                       "Please only enter \'a\' through \'d\' or to exit program enter \'e\': ")

    option = option.lower()
    user_options(option)


def user_options(option):
    """Method that takes user to desired option"""
    if option == 'e':
        goodbye()

    if option == 'a':
        sort_states()

    if option == 'b':
        search_for_state()

    if option == 'c':
        highest_population()

    if option == 'd':
        update_state_population()

    go_again = input("Would you like to make another choice? \n"
                     "Enter \'y\' for yes and \'n\' for no: ")

    while not go_again or not go_again.isalpha() or go_again.lower() not in ('y', 'n'):
        go_again = input("Please enter \'y\' for yes and \'n\' for no: ")

    if go_again.lower() == 'y':
        user_menu()
    else:
        goodbye()


user_menu()
