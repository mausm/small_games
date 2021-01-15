import sys

import numpy as np

def random_bin_array(K, N):
    arr = np.zeros(N)
    arr[:K] = 1
    np.random.shuffle(arr)
    return arr


def create_matrix(array1d, col, row):
    twod_matrix = np.reshape(array1d, (row, col))
    return twod_matrix

def get_xy_user(rmax,ymax):
    while True:
        xy_val = input("Please given an column and a row value separated with a comma like: x,y ")
        xy_val = xy_val.split(",")
        try:
            if 0 > int(xy_val[0]) > rmax or 0 > int(xy_val[1]) > ymax:
                continue
            xy_val = [int(xy_val[0]), int(xy_val[1])]
            return xy_val
        except (ValueError, IndexError):
            if input("please try again, or press q to quit") == "q":
                return "quit"


class Board:
    def __init__(self, x, y):
        self.bom = np.empty(x*y)  # 1: voor bom 0: voor geen
        self.bomrondom = np.empty((x, y))  # hoeveel bommen er naast zijn
        self.leeg = np.empty((x, y))  # 1 als er of een bom / bommen rondom  zijn 0 als het helemaal leeg is
        self.checked = np.zeros((x,y))
        self.pcview = np.zeros((x,y))

    def insert_bombs(self, bombs, x, y):
        random_bin_array(bombs, x * y)
        arr = np.zeros(x * y)
        arr[:bombs] = 1
        np.random.shuffle(arr)
        self.bom = self.transform_matrix(arr, x, y)
        return self.bom

    @staticmethod
    def transform_matrix(array1d, col, row):
        twod_matrix = np.reshape(array1d, (row, col))
        return twod_matrix


    def create_bombmap_old(self, bom, x, y):
        for i in range(bom.shape[0]):
            for j in range(bom.shape[1]):
                check_list = [[i-1,j-1], [i-1,j],[i-1,j+1],[i,j-1],[i, j+1], [i+1,j-1], [i+1,j],[i+1,j+1]]
                check_list = [pos for pos in check_list if 0 <= pos[0] < x and 0 <= pos[1] < y]
                bom_val = 0
                for a,b in check_list:

                    bom_val += bom[a,b]
                if self.bom[i,j] == 0:
                    self.bomrondom[i,j] = bom_val
                else:
                    self.bomrondom[i,j] = 0

    def create_bombmap(self, bom):
        # with some simple matrix adding up we can create the totals for all 8 directions.
        # example for the neighbors on te left, all cases with 2 have a neighbor left
        # 0101 =>  00101 + 01010 = 01111
        # 1100 =>  01100 + 11000 = 12100
        # 0011 =>  00011 + 00110 = 00121
        # 1010 =>  01010 + 10100 = 11110
        # this works extremely fast for larger boards!
        x,y = bom.shape[0], bom.shape[1]
        bommap = np.zeros((x,y))
        bommap = bommap + np.vstack((bom[1:,:], np.zeros(x))) + np.vstack((np.zeros(x),bom[:-1,:]))
        #up= bom[1:,:] #down = bom[:-1,:] #left = bom[:,1:] #right = bom[:,:-1]
        bommap = bommap +  np.hstack((bom[:,1:], np.zeros((y,1)))) + np.hstack((np.zeros((y,1)), bom[:,:-1]))
        # rightup = bom[1:,:-1] # rightdown = bom[:-1,:-1]
        tempdiag = np.pad(bom[1:,:-1], ((0,1),(1,0)), 'constant' ) + np.pad(bom[:-1,1:], ((1,0),(0,1)), 'constant' )
        tempdiag2 = np.pad(bom[1:,1:], ((0,1),(0,1)), 'constant' ) + np.pad(bom[:-1,:-1], ((1,0),(1,0)), 'constant' )
        self.bomrondom = tempdiag + tempdiag2 + bommap

    def create_leegmap(self, bom, bommap):
        """
        for i in range(bommap.shape[0]):
            for j in range(bommap.shape[1]):
                if bom[i,j] == 1 or bommap[i,j] > 0:
                    self.leeg[i,j] = 1
                else:
                    self.leeg[i,j] = 0
        """
        # quick numpy way:
        self.leeg = np.where(bom + bommap == 0, 0, 1)


    def check_surrounding(self, x, y):
        fields_to_check = set()
        fields_to_check.add((x,y))
        self.checked[x, y] = 1
        while True:
            x,y = fields_to_check.pop()
            if self.leeg[x,y] == 0:
                check_list = {(x - 1, y), (x, y - 1), (x, y + 1),  (x + 1, y)}
                check_list = {pos for pos in check_list if 0 <= pos[0] < self.checked.shape[0] and 0 <= pos[1] < self.checked.shape[1]}

                for positions in check_list.difference(fields_to_check):
                    if self.leeg[positions] == 0 and self.checked[positions] == 0:
                        fields_to_check.add(positions)
                    self.checked[positions] = 1

            if len(fields_to_check) == 0:
                #adds all the diagonal fields where a checked field is next to it.
                # for each field which is unchecked, but is diagional to a checked empty field it should add it to checked

                checkmap = np.where(self.bomrondom == 0, 1, 0) * self.checked
                checkmap = np.logical_not(self.bom) * checkmap

                #checkmap = np.vstack((self.checked[1:, :], np.zeros(self.checked.shape[0]))) + np.vstack((np.zeros(self.checked.shape[0]), self.checked[:-1, :]))
                # = checkmap + np.hstack((self.checked[:, 1:], np.zeros((self.checked.shape[1], 1)))) + np.hstack((np.zeros((self.checked.shape[1], 1)), self.checked[:, :-1]))
                tempdiag = np.pad(checkmap[1:, :-1], ((0, 1), (1, 0)), 'constant') + np.pad(checkmap[:-1, 1:], ((1, 0), (0, 1)),
                                                                                       'constant')
                tempdiag = tempdiag + np.pad(checkmap[1:, 1:], ((0, 1), (0, 1)), 'constant') + np.pad(checkmap[:-1, :-1], ((1, 0), (1, 0)),
                                                                                       'constant')


                checked = (tempdiag == 1) * np.where(self.bom == 0, 1,0) * (self.checked == 0)
                self.checked = self.checked - checked + self.checked

                break

    def convert_to_pc_view(self):

        #NOT DONE YET!
        check_view = self.checked
        rondom_view = np.where(self.bomrondom > 0, self.bomrondom, 1)
        combined = np.add(check_view, rondom_view)
        updown = np.add(combined[1:,:], combined[0:-1,:])
        leftright =  np.add(combined[1:,:], combined[0:-1,:])
        np.stack(updown[0,:], updown)
        np.stack(leftright[:,0], leftright)


# Base values in case something goes wrong with the user input
row,col = 10,10
bombs = 20

while True:
    try:
        print("let's set up the board!")
        row = int(input("Please select the amount of rows: "))
        col = int(input("Please select the amount of columns: "))
        bombs = int(input("Please select the amount of bombs: "))
    except ValueError:
        if input("if you want to exit, press q or else try again: only use numbers") == 'q':
            break
    break

bord = Board(row, col)
bord.insert_bombs(bombs, row,col)
bord.create_bombmap(bord.bom)
bord.create_leegmap(bord.bom, bord.bomrondom)
print("Let's start")


user_input = get_xy_user(row,col)
if user_input == "quit":
    sys.exit()
else:
    x = user_input[0]
    y = user_input[1]
bord.check_surrounding(x,y)

while True:

    user_input = get_xy_user(x, y)
    if user_input == "quit":
        break
    else:
        x = user_input[0]
        y = user_input[1]

    if bord.bom[x,y] == 1:
        print(bord.bom)
        if input("Helaas, je hebt een bom geraakt, opnieuw proberen druk 'r'") == "r":
            bord = bord(row,col)
        else:
            break

    bord.check_surrounding(x,y)
    print(bord.checked)

    if np.sum(bord.checked) == row * col:
        print("You have won!!")
                if input("play again? press 'a': ") == "a":
            bord = bord(row,col)
        else:
            break
            


