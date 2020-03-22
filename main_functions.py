import numpy as np
import nltk
import tqdm
import re

nltk.download('brown')
nltk.download('wordnet')
nltk.download('reuters')
nltk.download('names')
nltk.download('webtext')

from nltk.corpus import wordnet as wn
from nltk.corpus import brown
from nltk.corpus import reuters
from nltk.corpus import names
from nltk.corpus import webtext

from nltk.corpus import words
import itertools

# Right now this just works with 5x5, there's no reason you can't change it though, 
# Just need to spend the time to actually make that work

# Global
MATCH_DICT = {}

sgridsize = [5,5]
grid = np.full(gridsize, fill_value='.', dtype=str)

#word_list = list(brown.words())
#word_list = list(wn.words()) + list(words.words())
#word_list = list( set( list(reuters.words()) + list(brown.words() + list(names.words()) + list(webtext.words())) ))
word_list = list( set( list(reuters.words()) + list(brown.words()) ))
word_list = [x.upper() for x in word_list if x.isalnum()]

word_limits = gridsize
word_list = list(filter(lambda x: (len(x) >= word_limits[0]) and (len(x) <= word_limits[0]), word_list))

word_list.extend(starting_words)
word_list = list(set(word_list))


MATCH_DICT = {}

def word_options(grid, column=None, row=None):
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
        MATCH_DICT[match_str] = options
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
    
def add_valid_entries(grid, row=False, column=False, amount=1):
    # So let's try the smallest two options, figure out which are valid grids
    if row and column:
        return Exception('Only one of row or column may be set')
    elif (not row) and (not column):
        return Exception('One of row or column must be set')
    
    try:
        row_lengths, col_lengths = check_grid(grid)
    except:
        return None
    
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

def generate_list(length=50):
    while True:
        grid = np.full(gridsize, fill_value='.', dtype=str)
        starting_words = [random.choice(word_list), random.choice(word_list)]
        print(time.asctime())
        print('{} - {}'.format(starting_words[0], starting_words[1]))
        
        grid[0] = list(starting_words[0])
        # TODO: I forget if this is row or column size, check
        grid[gridsize[0] - 1] = list(starting_words[1])

        valid_grids_col = add_valid_entries(grid, column=True, amount=3)
        
        if valid_grids_col is None:
            continue
        
        final_grids = []
        for tgrid in valid_grids_col:
            res = add_valid_entries(tgrid, row=True, amount=3)
            if res:
                final_grids.extend(res)
            else:
                pass
        if len(final_grids) > 0:
            print('Success!')
            all_grids.extend(final_grids)
            print(len(all_grids))
        if len(all_grids) >= length:
            break
    return all_grids
