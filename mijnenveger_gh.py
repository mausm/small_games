import numpy as np

# use numpy 2d arrays for speed!

from random import randint

# these numbers can be edited, max is around 700 * 700

#NEW PLAN
# use the numpy arrays to get the bombs on random locations
# transform the numpy arrays to 2d matrices
# use indexing with np.where to count the amount of bombs around a location (check if index is valid/not out of bounds)
# use the leeg array for all positions which do not have a number or bomb. (so we just need one measure to open all empty fields)
# use a deque to add all fields around clicked position and add them to deque. 
# for each field remove the checked field and make leeg pos '1' and add the surrounding empty fields to deque

LENGTE = 10
BREEDTE = 10
MIJNEN = 20
BOMMEN = 10

def random_bin_array(K, N):
    arr = np.zeros(N)
    arr[:K] = 1
    np.random.shuffle(arr)
    return arr

def create_matrix(array1d, col, row):
    twod_matrix = np.reshape(array1d, (row, col))
    return twod_matrix

Veld = Board(LENGTE, BREEDTE)
Veld.insert_bombs(BOMMEN, LENGTE,BREEDTE)

class Board:
    def __init__(self, x, y):
       
        self.bom = [] # 1: voor bom 0: voor geen 
        self.bomrondom = np.empty((x,y) # hoeveel bommen er naast zijn
        self.leeg = np.empty((x,y)) # 1 als er of een bom / bommen rondom  zijn 0 als het helemaal leeg is
      
    def insert_bombs(self, bombs, x, y):
        random_bin_array(bombs, x*y
        arr = np.zeros(x*y 
        arr[:bombs] = 1
        np.random.shuffle(arr)
        return self.bombs
                       
    def transform_matrix(array1d, col, row):
        twod_matrix = np.reshape(array1d, (row, col))
        return twod_matrix

                       
                       
class out_of_range(Exception):
    pass

class Veld:
    def __init__(self, punten):
        self.punten = punten

    def __getitem__(self, item): #item moet een nummer zijn
        return self.punten[item]

    def coordinaten_naar_item(self, x , y):
        if x < 1 or x > LENGTE:
            return False
        elif y < 1 or y > BREEDTE:
            return False
        else:
            a = (x - 1) * BREEDTE + y - 1
            return self.punten[a]

    def __setitem__(self, a, value):
        self.punten[a] = value

    def check_around(self, x, y):
        punt_boven = self.coordinaten_naar_item(x - 1, y)
        punt_onder = self.coordinaten_naar_item(x + 1, y)
        punt_links = self.coordinaten_naar_item(x, y - 1)
        punt_rechts = self.coordinaten_naar_item(x, y + 1)
        return [punt_boven, punt_onder, punt_links, punt_rechts]

    def check_around_full_8(self, x, y):
        punt_rechtsboven = self.coordinaten_naar_item(x - 1, y + 1)
        punt_linksboven = self.coordinaten_naar_item(x - 1, y - 1)
        punt_linksonder = self.coordinaten_naar_item(x + 1, y - 1)
        punt_rechtsonder = self.coordinaten_naar_item(x + 1, y + 1)
        list_to_return = [punt_rechtsboven, punt_linksboven, punt_linksonder, punt_rechtsonder]
        for item in self.check_around(x, y):
            list_to_return.append(item)
        return list_to_return


    def check_next_list(self, x, y):
        a = self.coordinaten_naar_item(x, y)

        to_check_list = []

        if a.status == 0 and a.som == 0:
            while True:
                # first run we have to check the first item, otherwise the len() check in the end triggers the end of the code
                if len(to_check_list) == 0:
                    surrounding = self.check_around(x,y)
                    a.check()
                # this block below adds all the surrounding elements to the list and checks() the original numbers
                else:
                    surrounding = []
                    for item in to_check_list:
                        item.check()
                        for item2 in self.check_around(item.x,item.y):
                            surrounding.append(item2)

                # this block adds the items in the surrounding list to the tochecklist according to the checks
                for punt in surrounding:
                    if punt == False:
                        continue
                    elif punt.status == 0 and punt.som == 0 and punt.checked == 0:

                        to_check_list.append(punt)

                # this is the list with the old numbers and the new unchecked numbers
                # the code adds the all the surrounding elements of the current list that are checked
                # this part is sort of double of the above, but this also removes any double entries
                # also this code only checks the original numbers, so that the next loop contains the
                # new numbers, this keeps the list size smaller

                current_list = len(to_check_list)
                for item in to_check_list[0:current_list-1]:
                    if item == False:
                        continue
                    x = item.x
                    y = item.y
                    for item in self.check_around(x, y):
                        if item == False:
                            continue

                        elif item.checked == 0 and item.som == 0 and item.status == 0 and item not in to_check_list:
                            to_check_list.append(item)


                # remove all the numbers that have been checked before in the current list, before the code runs again
                to_check_list = [item for item in to_check_list if item.checked == 0 or item == False]


                # it doesnt stop until there are no more numbers to check
                if len(to_check_list) < 1:
                    return False

        elif a == False:
            return False

class Punt:
    def __init__(self, x, y):
        self.status = 0 # 0 geen bom, 1, bom
        self.checked = 0 # 0 is niet bekeken 1 is bekeken
        self.x = x
        self.y = y
        self.som = 0

    def __repr__(self):
        return "{},{},{},{},{}".format(self.x,self.y, self.status, self.checked, self.som)

    def __str__(self):
        return "{},{},{},{},{}".format(self.x, self.y, self.status, self.checked, self.som)

    def check(self):
        if self.status == 1:
            return False
        else:
            self.checked = 1
            return True

    def user_view(self):
        if self.checked == 1:
            return self.som
        elif self.checked == 0:
            for item in Mijnenveger.check_around(self.x, self.y):
                if item == False:
                    continue
                elif item.checked == 1 and item.som == 0 and not item.status == 1:
                    return self.som
            else:
                return "-"

        else:
            return "-"

    def computer_view(self):
        if self.status == 1:
            return self.status
        elif self.som != 0:
            return self.som
        else:
            return "-"


def create_number_map():
    number_map = []
    for i in range(1, LENGTE + 1):
        for j in range(1, BREEDTE + 1):
            number_map.append(Punt(i, j))
    return number_map


def insert_mine_numbers(list, main_object):
    for item in list:
        if item.status == 1:
            for item2 in main_object.check_around_full_8(item.x,item.y):
                if item2 == False:
                    continue
                item2.som  = item2.som + 1



                       
                       
Puntlijst = create_number_map() # creates a list of punt objects according to the size of the board

Mijnenveger = Veld(Puntlijst) # you can change this name

Mijnenveger.punten = insert_mines(MIJNEN, Mijnenveger.punten)

insert_mine_numbers(Mijnenveger.punten, Mijnenveger)



def computer_view():
    printwaarde = "\n"
    for i in range(1,LENGTE+1):
        for j in range(1,BREEDTE+1):
            printwaarde = printwaarde + str(Mijnenveger.coordinaten_naar_item(i,j).computer_view()) + " "

        printwaarde = printwaarde + "\n"

    print(printwaarde)


def user_viewpoint():
    printwaarde = "\n"
    for i in range(1, LENGTE + 1):
        for j in range(1, BREEDTE + 1):
            printwaarde = printwaarde + str(Mijnenveger.coordinaten_naar_item(i, j).user_view()) + " "

        printwaarde = printwaarde + "\n"

    print(printwaarde)

# IF you want to check where the mines are, unccoment the computerview
computer_view()
#user_viewpoint()




while True:
    total_checked, total_mines = 0,0
    user_viewpoint()
    try:
        x = int(input("Welke rij van boven? "))
        y = int(input("Welke kolom? "))
        if x > LENGTE or y > BREEDTE:
            raise out_of_range
        elif x < 1 or y < 1:
            raise out_of_range
    except out_of_range:
        print("de waarde moeten binnen 1 en {} en 1 en {} liggen".format(LENGTE, BREEDTE))
        continue

    except ValueError:
        print("Alleen hele nummers aub")
        pass

    if Mijnenveger.coordinaten_naar_item(x,y).check() == False:
        print("Helaas, je hebt een bom geraakt")
        break
    else:
        Mijnenveger.check_next_list(x,y)

    # sometimes the insert mine function inserts one to many mines, so I can't check against MINES
    for i in Mijnenveger.punten:
        if i.checked == 1:
            total_checked += 1
        elif i.status == 1:
            total_mines += 1


    if len(Mijnenveger.punten) - total_checked <= total_mines:
        print("Gefeliciteerd, je hebt gewonnen")
        break


