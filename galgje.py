"""
Ik moet nog een try except functie invoegen
zodat de gebruikers alleen losse letters kunnen invoegen
nu crasht die waarschijnlijk
"""


class wrong_input_value(ValueError): #raises an error if a user inputs something different than a single letter
    pass


word_to_guess = input("Enter the word that the other user has to guess: ") #The word that the other has to guess
word_to_guess = word_to_guess.strip().lower() #remove any capitalized letters
letters_start = list("_" * len(word_to_guess)) #startvalue of letters you know

maximum_guess = 8  # set this to limit the amount of guesses
wrong_guess_counter = 0
letters_already_guessed = []



def create_a_list_from_guessword(word_to_guess_2):  #makes it easier to take the positionvalues
    return [item for item in remove_formatting(word_to_guess_2)]


def remove_formatting(user_string):  # returns everything to lowercase without spaces
    user_string_clean = user_string.strip().lower()
    return user_string_clean


def letter_check(user_input): #returns true if the user guessed correctly
    if user_input in create_a_list_from_guessword(word_to_guess):
        return True


def position_check(user_input): #checks in which places the user letter occurs
    position_answer = []
    pos = 0
    for i in create_a_list_from_guessword(word_to_guess): #uses the global variable word_to_guess
        if user_input == i:
            position_answer.append(pos)
        pos += 1
    return position_answer


def letters_you_know(user_input): #adds the correct guesses to the line with the "_"s
    for i in position_check(user_input):
        letters_start[i] = word_to_guess[i]
    return letters_start


def guess_counter(wrong_guess_counter): #should be an integer
    wrong_guess_counter += 1
    guesses_left = maximum_guess - wrong_guess_counter
    print("you have made {} wrong guesses, {} guesses left".format(wrong_guess_counter,guesses_left))
    return wrong_guess_counter


def wrong_guess(user_input):
    print("")
    print("This letter does not occur in the word")
    letters_already_guessed.append(user_input)
    return letters_already_guessed


def return_the_usermenu(wrong_guess_counter, letters_already_guessed): #takes in an integer and the list of letters already guessed
    print("")
    print("".join(letters_start))
    current_count = maximum_guess - wrong_guess_counter
    print("you have {} guesses left".format(current_count))
    letters_already_guessed_2 = ""
    letters_already_guessed_2 = "".join(letters_already_guessed)
    print("letters you already guessed: {}".format(letters_already_guessed_2))
    user_input = input("Select a letter to guess: ")
    return user_input


def user_input_check(input_2): # returns true if the input is incorrect, so it raises an error
    len_check = len(input_2) == 1
    letter_check_2 = input_2.isalpha()
    if len_check and letter_check_2:
        output1 = False
    else:
        output1 = True
    return output1

#def sanitizing_user_input(user_input):
#    try:
#
#    except:
#       print("you tried to enter an invalid input")


while (''.join(letters_start)) != word_to_guess and wrong_guess_counter < maximum_guess:
    try:
        input_var = return_the_usermenu(wrong_guess_counter, letters_already_guessed)
        if user_input_check(input_var):
            raise wrong_input_value("You gave an incorrect input, please try again")
        elif letter_check(input_var):
            letters_start = letters_you_know(input_var)
        else:
            letters_already_guessed = wrong_guess(input_var)
            wrong_guess_counter = guess_counter(wrong_guess_counter)
    except wrong_input_value:
        print("You have given an incorrect input, please try again")
        continue

#when you come out of the while loop, you have either won or lost
if word_to_guess == "".join(letters_start):
    print("")
    print("congratulations, you won!")
else:
    print("sorry, you lost")

#print(''.join(letters_start))
