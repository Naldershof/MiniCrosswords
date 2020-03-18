import numpy as np
import nltk
import re
from nltk.corpus import wordnet as wn
import tqdm
import itertools

# Right now this just works with 5x5, there's no reason you can't change it though, 
# it's just not super optimized just yet

# Global
MATCH_DICT = {}

starting_words = ['TRUMP', 'PENCE']
gridsize = [5,5]
grid = np.full(gridsize, fill_value='.', dtype=str)

word_list = list(brown.words()) + list(words.words())
word_list = [x.upper() for x in word_list]

word_limits = gridsize
word_list = list(filter(lambda x: (len(x) >= word_limits[0]) and (len(x) <= word_limits[0]), word_list))

word_list.extend(starting_words)
word_list = list(set(word_list))

grid[0] = list(starting_words[0])
grid[gridsize[0] - 1] = list(starting_words[1])

MATCH_DICT = {}

def word_options(grid, column=None, row=None):
    # For a given row or column get the possible options
    if row and column:
        return Exception('Can only set one of row or column')
    elif row is not None:
        match_str = '^'+''.join(grid[row,:])+'$'
    elif column is not None:
        match_str = '^'+''.join(grid[:,column])+'$'
    else:
        return Exception('Must set one of row or column')
    
    global MATCH_DICT
    
    if match_str in MATCH_DICT.keys():
        options = MATCH_DICT[match_str]
    else:
        regex = re.compile(match_str)
        options = list(filter(regex.match, word_list))
        #TODO: Remove words that have special characters
        match_dict[match_str] = options
    return options

def check_grid(grid, verbose=False, boolean=False):
    # Check that each unfilled row or column has at least one valid way it can be filled in
    # Or if it's a full grid check to make sure that it's only full of valid words
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
    
def add_valid_entries(grid, row=False, column=False, amount=1):
    # So let's try the smallest two options, figure out which are valid grids
    if row and column:
        return Exception('Only one of row or column may be set')
    elif (not row) and (not column):
        return Exception('One of row or column must be set')
    
    row_lengths, col_lengths = check_grid(grid)
    
    if row:
        lengths = row_lengths
    if column:
        lengths = col_lengths
        
    keys = sorted(lengths, key=lengths.get)[0:amount]
    
    if len(lengths) < amount:
        return None
    
    suggestion_lists = []
    for num in keys:
        if row:
            suggestion_lists.append(word_options(grid, row=num))
        if column:
            suggestion_lists.append(word_options(grid, column=num))
    
    if amount == 1:
        product_list = list(itertools.product(suggestion_lists[0], repeat=1))
    elif amount > 1:
        product_list = list(itertools.product(*suggestion_lists))
    else: 
        return Exception('Incorrect amount parameter')
    
    #print(product_list)
    valid_grids = []
    for entry in product_list:
        new_grid = grid.copy()
        for index, col in enumerate(keys):
            if row:
                new_grid[col, :] = list(entry[index])
            if column:
                new_grid[:, col] = list(entry[index])
        if check_grid(new_grid, boolean=True):
            valid_grids.append(new_grid)
                
    return valid_grids

valid_grids_col = add_valid_entries(grid, column=True, amount=3)
final_grids = []
for tgrid in tqdm.tqdm(valid_grids_col):
    res = add_valid_entries(tgrid, row=True, amount=3)
    if res:
        final_grids.extend(res)
    else:
        pass
