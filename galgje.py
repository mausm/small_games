#my very first small project, would definitely do it differently now

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
    print("\n This letter does not occur in the word")
    letters_already_guessed.append(user_input)
    return letters_already_guessed


def return_the_usermenu(wrong_guess_counter, letters_already_guessed): #takes in an integer and the list of letters already guessed

    print("\n", ",".join(letters_start))
    print("you have {} guesses left".format(maximum_guess - wrong_guess_counter))
    print("wrong guesses: {}".format("".join(letters_already_guessed)))
    user_input = input("Select a letter to guess: ")
    return user_input


def user_input_check(input_2): # returns true if the input is incorrect, so it raises an error
    if len(input_2) == 1 and input_2.isalpha():
        return False
    else:
        return True

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
    
    print(" /n Congratulations, you won!")
else:
    print("Sorry, you lost")
