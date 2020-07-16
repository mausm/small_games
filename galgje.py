#my very first small project, would definitely do it differently now

class Wrong_input_value(ValueError): #raises an error if a user inputs something different than a single letter
    pass


while True:
    word_to_guess = input("Enter the word that the other user has to guess: ") #The word that the other has to guess
    if word_to_guess.isalpha():
        break
    else:
        print("Please use valid characters only")

word_to_guess = word_to_guess.strip().lower() #remove any capitalized letters
letters_start = list("_" * len(word_to_guess)) #startvalue of letters you know

MAXIMUM_GUESS = 8  # set this to limit the amount of guesses
wrong_guess_counter = 0
letters_already_guessed = []


def create_a_list_from_guessword(word):  #makes it easier to take the positionvalues
    word = word.strip().lower()
    return list(word)


def position_check(user_input, word_to_guess): #checks in which places the user letter occurs
    position_answer = []
    pos = 0
    for i in create_a_list_from_guessword(word_to_guess): #uses the global variable word_to_guess
        if user_input == i:
            position_answer.append(pos)
        pos += 1
    return position_answer


def letters_you_know(user_input, word_to_guess): #adds the correct guesses to the line with the "_"s
    for i in position_check(user_input, word_to_guess):
        letters_start[i] = word_to_guess[i]
    return letters_start


def guess_counter(wrong_guess_counter): #should be an integer
    guesses_left = MAXIMUM_GUESS - wrong_guess_counter
    print("you have made {} wrong guesses, {} guesses left".format(wrong_guess_counter,guesses_left))


def return_the_usermenu(wrong_guess_counter, letters_already_guessed): #takes in an integer and the list of letters already guessed
    print("\n", ",".join(letters_start))
    print("you have {} guesses left".format(MAXIMUM_GUESS - wrong_guess_counter))
    print("wrong guesses: {}".format("".join(letters_already_guessed)))
    user_input = input("Select a letter to guess: ")
    return user_input.lower()


def user_input_check(input):
    return len(input) != 1 or not input.isalpha()


while (''.join(letters_start)) != word_to_guess and wrong_guess_counter < MAXIMUM_GUESS:
    try:
        input_var = return_the_usermenu(wrong_guess_counter, letters_already_guessed)
        if user_input_check(input_var):
            raise Wrong_input_value("You gave an incorrect input, please try again")
        elif input_var in create_a_list_from_guessword(word_to_guess):
            letters_start = letters_you_know(input_var, word_to_guess)
        else:
            print("\n"  "This letter does not occur in the word")
            letters_already_guessed.append(input_var)
            wrong_guess_counter += 1
            guess_counter(wrong_guess_counter)
    except Wrong_input_value:
        print("You have given an incorrect input, please try again")
        continue

#when you come out of the while loop, you have either won or lost
if word_to_guess == "".join(letters_start):
    print(" \nCongratulations, you won!")
else:
    print(" \nSorry, you loose :(")
