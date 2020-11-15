"""
Created on Sun Nov  1 17:28:20 2020

@author: petrs
"""

import random
import string
import cProfile

# A function to search for a word in the square
# Uses for loops to iterate over all items in the square
def search(square, wordlist, longest_word, found_words, min_word_len):
    # iterate over each column and row in the square
    methods_list = get_method_list()
    for i in range(len(square)):
        for j in range(len(square)):
            # search from this collagens
            search_from_coord(square, wordlist, longest_word, i, j, methods_list, found_words, min_word_len)    
    return None

# Function starts from the coordinates and moves one square by one using each method
# If the word it found is in the dictionary, it will update the list of found words
def search_from_coord(square, wordlist, longest_word, i, j, methods_list, found_words, min_word_len):
    # iterate using each method
    for elem in methods_list:
        # create a temporary storage
        temp = []
        # start moving in the relevant direction
        coord = [i,j]
        empty = ""
        while is_valid_coord(square, coord) == True:
            temp.append(square[coord[0]][coord[1]])
            # I do not want one letter words
            if len(temp) > 1:    
                if word_guessed_ver2(empty.join(temp), wordlist) == True:
                    update_found_list(empty.join(temp), found_words, i, j, elem, min_word_len)
            coord = move(coord, elem)

# If the word found in the square is in the dictionary, update the list
# The function also remembers the coordinates and which the word starts and the moveset.
# This is useful in further stages where I need to remove the found words and replace them with zeros
def update_found_list (my_word, found_words, i, j, method, min_word_len):
    if len(my_word) < min_word_len:
        return
    if my_word in found_words:
        found_words[my_word].append([i, j, method])
    else:
        found_words[my_word] = [[i, j, method]]

# A function to tell me if a guessed word is in the dictionary
def word_guessed_ver2 (temp_word, wordlist):
    if temp_word in wordlist:
        return True
    else:
        return False

# Function to load a dictionary from a file. Note that I am exporting it as both dictionary and a list,
# because for some actions, dictionary seemed faster and vice versa when runnig the programme in a loop.
def loadWords(language):
    WORDLIST_FILENAME = select_dictionary(language)
    inFile = open(WORDLIST_FILENAME, 'r', encoding = "utf8")
    line = inFile.read()
    wordlist = line.split()
    wordlist_dict = {}
    wordlist_list = []
    for item in wordlist:
        wordlist_dict[item] = None
        wordlist_list.append(item)
    return wordlist_dict, wordlist_list

# Function to select the relevant dictionary file
# NOTE: The dictionary must contain words separated by spaces
def select_dictionary(language):
    if language == "e":
        return "words.txt"
    if language == "e+":
        return "words_alpha.txt"
    if language == "c":
        return "czech-updated.txt"
    
# A simple function to determine length of the longest word in a dictionary
def find_longest(wordlist):
    temp = 0
    for item in wordlist:
        if len(item) > temp:
            temp = len(item)
    return temp

# Function to generate a blank square. When "r" is selected as a method (this is only for testing),
# random chars are filled in and when "z", only zeros are added.
def gen_square(delka, method):
    t1 = []
    for i in range(delka):
        temp = []
        for i in range(delka):
            if method == "r":
                temp.append(random.choice(string.ascii_lowercase))
            if method == "z":
                temp.append(0)
        t1.append(temp)
    return(t1)

# Function to print the square
# TBD how to add numbers to each axis, because this will break if square is bigger than 10
def print_square(square):
    temp = len(square)
    for q in range(temp*2 + 1):
        print("_", end="")
    print("")
    
    for i in range(temp):
        for j in range(temp):
            if type(square[i][j]) is int:
                print("|", end="")
                print(square[i][j], end="")
            else:
                print("|", end="")
                print(square[i][j].capitalize(), end="")
        print("|", end="")
        print("")
    for q in range(temp*2 + 1):
        print("‾", end="")
    print("")
    return 0

# Fuction to randomly select a word. The word must not be longer that the size of the square and shorter than size specified by the user.
def pick_rand_word(wordlist_list, max_len, min_len):
    while True:
        temp = random.choice(wordlist_list) 
        if len(temp) <= max_len and len(temp) >= min_len:
            return temp

# Function to select a random coordinate at which the application will attempt to place the selected word.
def pick_rand_coord(max_len):
    return [random.randint(0,max_len - 1), random.randint(0,max_len - 1)]

# Funaction to get us a randomly sorted list of methods for insertion
def get_rand_method_list():
    methods_list = ["w", "e", "n", "s", "nw", "ne", "sw", "se"]
    random.shuffle(methods_list)
    return methods_list

# Funaction to get us a list of methods for insertion, which is not sorted
def get_method_list():
    methods_list = ["w", "e", "n", "s", "nw", "ne", "sw", "se"]
    return methods_list

# Function to check whether a word fits into a square at the given coordinates and using a specified method
def check_fit(word, square, coord, method):
    for i in range(len(word) - 1):
        coord = move(coord, method)
    return is_valid_coord(square, coord)

#  Function to check whether a given coordinate is valid, taking into account the number 
def is_valid_coord(square, coord):
    max_coord = len(square) - 1
    if coord[0] < 0 or coord[1] < 0 or coord[0] > max_coord or coord[1] > max_coord:
        return False
    else:
        return True

# Function to attempt to place a word at given coordinates, using all available methods
def attemp_place(square, rand_word, rand_coord, words_inserted):
    # Get a randomly sorted list of methods
    # print("Trying to place a word", rand_word, "at the coordinates", rand_coord)
    methods_list = get_rand_method_list()
    # try insert the word using each method
    for elem in methods_list:
        # check if the word fits
        word_fit = check_fit(rand_word, square, rand_coord[:], elem)
        # if it fits - place it into the square
        conflict_free = None
        if word_fit == True:    
            conflict_free = check_conflict(square, rand_word, rand_coord[:], elem)
        if conflict_free == True:
            place_word_into_square(rand_word, square, rand_coord[:], elem)
            # and place it in a list of found words
            words_inserted.append(rand_word)
            # and return, because we do not want to attempt inserting it again
            return
    # if nothing is found, return anyway
    return

#  Function to actually place a word into a square using the given method
def place_word_into_square(rand_word, square, rand_coord, elem):
    # iterate over each element in a word
    for item in rand_word:
        # insert the relevant item from 
        square[rand_coord[0]][rand_coord[1]] = item
        # move the coordinates using appropriate method
        move(rand_coord, elem)
    return

# Check whether the word fits in the relevant directions.
# I am checking whether the square to which it is to be placed is zero or contains the same letter.
# This prevents the already inserted words from being over-written.
def check_conflict(square, rand_word, rand_coord, method):
    for elem in rand_word:
        if square[rand_coord[0]][rand_coord[1]] == 0:
            move(rand_coord, method)
            continue
        elif elem == square[rand_coord[0]][rand_coord[1]]:
            move(rand_coord, method)
            continue
        else:
            return False       
    return True
    
# Function to fill-in empty square with words. 
# These are randomly chosen as well as coordinates at which they are to be placed.
def fill_in_square(wordlist_list, square, words_inserted, min_word_len):
    max_len = len(square)
    rand_word = pick_rand_word(wordlist_list, max_len, min_word_len)
    # print("Random word selected: ", rand_word)
    rand_coord = pick_rand_coord(max_len)
    # print("Random coordinates selected: ", rand_coord)
    attemp_place(square, rand_word, rand_coord, words_inserted)
    return 0

# Function to ask the user for a size of dictionary
def get_select_size():
    while True:
        square_size = input("Please enter a size of a square (higher than 1): ")
        try: 
            square_size = int(square_size)
            if square_size > 0:
                break
            else:
                print("Incorrect input. Please try again and select between 1 and 26!")
        except ValueError:
            print(square_size, "is not an integer.")   
    return square_size

# Ask the user to insert a minimum length of a word to be accepted, in particular if it wants to avoid two or three letter words
def get_min_word_len(square_len):
    while True:
        min_word_len = input("Please enter a minimum length of a word (higher than 1 and lower than size of the square): ")
        try: 
            min_word_len = int(min_word_len)
            if min_word_len > 0 and min_word_len <= square_len:
                break
            else:
                print("Incorrect input. Please try again and select between 1 and", square_len, "!")
        except ValueError:
            print(min_word_len, "is not an integer.")   
    return min_word_len

# After all words are placed, replace the remaining chars with random chars.
def sanitize_square(square):
    temp = len(square)
    for i in range(temp):
        for j in range(temp):
            if square[i][j] == 0:
                square[i][j] = random.choice(string.ascii_lowercase)

# Function to ask the user to select a word.
# Refuses input which does not contain alphanumeric chars (including special Czech chars).
# Also checks against the wordlist and refuses words which are not valid
def get_player_guess(wordlist):
    while True:
        player_guess = input("Please select a word: ").lower()
        is_alpha = True
        for elem in player_guess:
            if elem not in string.ascii_lowercase and elem not in ["ě", "š", "č", "ř", "ž", "ý", "á", "í", "é", "ú", "ů", "ť", "ď", "ň", "ó"]:
                is_alpha = False    
        if is_alpha == True:
            if player_guess not in wordlist:
                print("The word you selected is not valid.")
            else:
                break
        else:
            print("Incorrect input. Please try again!")
    return player_guess

# A function asking the user to select the language. Just Czech and English now
def get_select_language():
    while True:
        language = input("Please select language. \"E\" for English, \"C\" for Czech: ")
        if (language == "E" or language == "C" or language == "e" or language == "c"):
            break
        else:
            print("Incorrect input. Please try again!")
    return language

# Function to check whether the word guessed by the user is in the list of words found by the search algorithm
def check_if_found(square, player_guess, found_words):
    if player_guess in found_words:
        return True
    else:
        return False

# Function to remove the found word
# I replace it with char "0", because int broke some other functions
def remove_found_word(square, search_outcome, delka):
    for i in range(delka):
        square[search_outcome[0]][search_outcome[1] + i] = "0"

# Function determines individual movesets
def moveset(method):
    if method == "w":
        return[0,-1]
    elif method == "e":
        return[0,1]
    elif method == "n":
        return[-1,0]
    elif method == "s":
        return[1,0]
    elif method == "nw":
        return[-1,-1]
    elif method == "ne":
        return[-1,1]
    elif method == "sw":
        return[1,-1]
    elif method == "se":
        return[1,1]

# Function to move in the square always by one step using the relevant moveset
def move(coord, method):
    move_set = moveset(method)
    coord[0], coord[1] = coord[0] + move_set[0], coord[1] + move_set[1]
    return coord

# Function to remove a word from the square in it was guessed correctly.
# Since we have stored where the relevant word is found as well as direction
# in which it is places, it is not necessary to search for it again.
def remove_found_word_v2(square, player_guess, found_words):
    starting_coordinates = [found_words[player_guess][0][0], found_words[player_guess][0][1]]
    direction = found_words[player_guess][0][2]
    for i in range(len(player_guess)):
        square[starting_coordinates[0]][starting_coordinates[1]] = "0"
        move(starting_coordinates, direction)
    return True 

# Function to create a list of all words.
# TBD the efficiency of lists / dictionaries for various functions here.
def create_dict_list(wordlist):
    temp = []
    for key, value in wordlist.items():
        temp.append(key)
    return temp

#  The main game function which calls other functions.
def game(hint = False, square = None, lang = None, square_size = None, min_word_len = None, testing_mode = False):
    # Select language of the dictionary
    if lang == None:
        lang = get_select_language()
    # Load the wordlist
    wordlist, wordlist_list = loadWords(lang)
    # Ask user for a size of the dictionary
    if square == None:
        if square_size == None:
            square_size = get_select_size()
        square = gen_square(square_size, "z")
    words_inserted = []
    if min_word_len == None:
        min_word_len = get_min_word_len(len(square))
    # I selected that the number of words to be attempted shall be 5 x length of the square.
    # TBD where the square usually gets filled-in so that no new words can be inserted
    for i in range(5*len(square)):    
        fill_in_square(wordlist_list, square, words_inserted, min_word_len)
    sanitize_square(square)
    longest_word = find_longest(wordlist)
    found_words = {}
    search(square, wordlist, longest_word, found_words, min_word_len)
    # For some testing purposes, I do not want to move to the guessing phase
    if testing_mode == True:
        return len(found_words)
    print_square(square)
    # This shows you the words found the the search() function.
    # Note that it will find more words than inserted, because some additional words 
    # might have been created in other directions.
    if hint == True:
        print("Words found: ", sorted(found_words))
    while len(found_words) > 0:
         player_guess = get_player_guess(wordlist)
         search_outcome = check_if_found(square, player_guess, found_words)
         if search_outcome == True:
             print("You found a word", player_guess)
             remove_found_word_v2(square, player_guess, found_words)
             # I need to make the search again. If one word is removed from the list, 
             # it might affect other words using the same letters.
             found_words = {}
             search(square, wordlist, longest_word, found_words, min_word_len)
             print_square(square)
             # print("Words  inserted: ", sorted(words_inserted))
             if hint == True:
                 print("Words found: ", sorted(found_words))
         else:
            print("Wrong guess")
    return 0 

# Insert game(True) to get hints showing you the words found by the algorithm. 
# This is also great for testing.
game()
