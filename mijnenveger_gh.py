import collections

import numpy as np

# use numpy 2d arrays for speed!

from random import randint

# these numbers can be edited, max is around 700 * 700

# NEW PLAN
# use the numpy arrays to get the bombs on random locations DONE
# transform the numpy arrays to 2d matrices DONE
# use indexing with np.where to count the amount of bombs around a location (check if index is valid/not out of bounds) DONE
# use the leeg array for all positions which do not have a number or bomb. (so we just need one measure to open all empty fields) DONE
# use a deque to add all fields around clicked position and add them to deque. -> SET OPERATIONS WORKED BETTER - DONE
# for each field remove the checked field and make leeg pos '1' and add the surrounding empty fields to deque DONE

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



class Board:
    def __init__(self, x, y):
        self.bom = np.empty(x*y)  # 1: voor bom 0: voor geen
        self.bomrondom = np.empty((x, y))  # hoeveel bommen er naast zijn
        self.leeg = np.empty((x, y))  # 1 als er of een bom / bommen rondom  zijn 0 als het helemaal leeg is
        self.checked = np.zeros((x,y))

    def insert_bombs(self, bombs, x, y):
        random_bin_array(bombs, x * y)
        arr = np.zeros(x * y)
        arr[:bombs] = 1
        np.random.shuffle(arr)
        self.bom = self.transform_matrix(self, arr, x, y)
        return self.bom

    @staticmethod
    def transform_matrix(self, array1d, col, row):
        twod_matrix = np.reshape(array1d, (row, col))
        return twod_matrix


    def create_bombmap(self, bom, x, y):
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


    def create_leegmap(self, bom, bommap):
        for i in range(bommap.shape[0]):
            for j in range(bommap.shape[1]):
                if bom[i,j] == 1 or bommap[i,j] > 0:
                    self.leeg[i,j] = 1
                else:
                    self.leeg[i,j] = 0


    def check_surrounding(self, x, y):
        fields_to_check = set()
        #waiting_list = collections.deque
        current_check = 0
        fields_to_check.add((x,y))
        self.checked[x, y] = 1
        while True:
            x,y = fields_to_check.pop()
            if self.leeg[x,y] == 0: #and checked[x,y] == 0:
                check_list = {(x - 1, y), (x, y - 1), (x, y + 1),  (x + 1, y)}
                check_list = {pos for pos in check_list if 0 <= pos[0] < self.checked.shape[0] and 0 <= pos[1] < self.checked.shape[1]}

                for positions in check_list.difference(fields_to_check):
                    if self.leeg[positions] == 0 and self.checked[positions] == 0:
                        fields_to_check.add(positions)
                    self.checked[positions] = 1

            if len(fields_to_check) == 0:
                break


test = Board(100,100)
test.insert_bombs(50,100,100)
test.create_bombmap(test.bom, 10,10)

test.create_leegmap(test.bom, test.bomrondom)

test.check_surrounding(2,2)

print(test.bom, "\n")
print(test.leeg, "\n")
print(test.bomrondom, "\n")
print(test.checked)
