import numpy as np
import nltk
import re
from nltk.corpus import wordnet as wn

starting_words = ['TRUMP', 'PENCE']
gridsize = [5,5]
grid = np.full(gridsize, fill_value='.', dtype=str)

word_list = list(wn.words())
word_list = [x.upper() for x in word_list]

word_list.extend(starting_words)
word_list = list(set(word_list))

# Change this so that it can be in other positions other than 0 and 4
grid[0] = list(starting_words[0])
# TODO: I forget if this is row or column size, check
grid[gridsize[0] - 1] = list(starting_words[1])


# So we're going to check that there's some possible solution at least vertically for everything
# This should be extended to an arbitrary function to see if we can use it to iterate through

option_length = {}

# Getting length of possible options vertically. 
for x in range(0, gridsize[0]):
    match_str = '^'+''.join(grid[:,x])+'$'
    regex = re.compile(match_str)
    options = len(list(filter(regex.match, word_list)))
    option_length[x] = options

#Start iterating for the option with the least 
key_min = min(option_length.keys(), key=(lambda k: option_length[k]))

# Get possibile answers for a row or column
def word_options(grid, column=None, row=None):
    if row and column:
        return Exception('Can only set one of row or column')
    elif row is not None:
        match_str = '^'+''.join(grid[row,:])+'$'
    elif column is not None:
        match_str = '^'+''.join(grid[:,column])+'$'
    else:
        return Exception('Must set one of row or column')
    regex = re.compile(match_str)
    options = list(filter(regex.match, word_list))
    #TODO: Remove words that have special characters
    return options

def check_grid(grid, verbose=False, boolean=False):
    row_lengths = {}
    for row in range(0, grid.shape[0]):
        rl = len(word_options(grid, row=row))
        if rl == 1:
            pass
        elif  rl > 0:
            row_lengths[row] = rl
        else:
            if verbose:
                print('Failed on Row {}'.format(row))
            return False
    col_lengths = {}
    for col in range(0, grid.shape[0]):
        cl = len(word_options(grid, column=col))
        if cl == 1:
            pass
        elif  cl > 0:
            col_lengths[col] = cl
        else:
            if verbose:
                print('Failed on Column {}'.format(col))
            return False
    if boolean:
        return True
    else:
        return row_lengths, col_lengths

import tqdm

def add_valid_cols(grid):
    row_lengths, col_lengths = check_grid(grid)

    # So let's try the smallest two options, figure out which are valid grids
    key_min = min(col_lengths.keys(), key=(lambda k: col_lengths[k]))
    del col_lengths[key_min]
    key_second = min(col_lengths.keys(), key=(lambda k: col_lengths[k]))

    short_col_options = word_options(grid, column=key_min)
    second_shortest_col_options = word_options(grid, column=key_second)

    valid_grids = []
    for word in short_col_options:
        for word2 in second_shortest_col_options:
            new_grid = grid.copy()
            new_grid[:, key_min] = list(word)
            new_grid[:, key_second] = list(word2)
            #print(new_grid)
            if check_grid(new_grid, boolean=True):
                valid_grids.append(new_grid)
                
    return valid_grids


#####
#
# TODO : This really needs to account for the fact that you can't always add 2 at once
#
##### 

def add_valid_rows(grid):
    row_lengths, col_lengths = check_grid(grid)

    # So let's try the smallest two options, figure out which are valid grids

    try:
        key_min = min(row_lengths.keys(), key=(lambda k: row_lengths[k]))
        del row_lengths[key_min]
        key_second = min(row_lengths.keys(), key=(lambda k: row_lengths[k]))
    except:
        return None

    short_row_options = word_options(grid, row=key_min)
    second_shortest_row_options = word_options(grid, row=key_second)

    valid_grids = []
    for word in short_row_options:
        for word2 in second_shortest_row_options:
            new_grid = grid.copy()
            new_grid[key_min, :] = list(word)
            new_grid[key_second, :] = list(word2)
            #print(new_grid)
            if check_grid(new_grid, boolean=True):
                valid_grids.append(new_grid)
                
    return valid_grids

valid_grids_col = add_valid_cols(grid)
valid_grids_rows = []
for v_grid in tqdm.tqdm(valid_grids_col):
    res = add_valid_rows(v_grid)
    if res:
        valid_grids_rows.extend(res)
    else:
        pass