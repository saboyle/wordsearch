# https://codereview.stackexchange.com/questions/92649/word-search-generator
import numpy as np
import json
import random
import string

LETTERS = set(string.ascii_lowercase)
EMPTY = '.'

HARD_DIRECTIONS = dict(up=(-1,0), down=(1,0), left=(0,-1), right=(0,1),
                  upleft=(-1,-1), upright=(-1,1), downleft=(1,-1),
                  downright=(1,1))

MEDIUM_DIRECTIONS = dict(up=(-1,0), down=(1,0), left=(0,-1), right=(0,1))

EASY_DIRECTIONS = dict(down=(1,0), right=(0,1))

DIRECTIONS = EASY_DIRECTIONS

class WordSearch:
    """A word search puzzle.

    Arguments to the constructor:

    size        Width and height (assumed square puzzles).
    word_list   List of words to use (default: None).
    directions  Iterable of names of allowed directions (default: all eight).
    density     Stop generating when this density is reached (default: .7).

    """
    def __init__(self, word_list, size, directions, title, difficulty="", density=.7):

        self.title = title
        self.difficulty = difficulty
        self.word_list = word_list
        
        width = size
        height = size
        
        # Check arguments and load word list.
        max_len = min(width, height)
        random.shuffle(word_list)

        # Initially empty grid and list of words.
        self.grid = [[EMPTY] * width for _ in range(height)]
        self.words = []

        # Generate puzzle by adding words from word_list until either
        # the word list is exhausted or the target density is reached.
        filled_cells = 0
        target_cells = width * height * density
        
        for word in word_list:
            # List of candidate positions as tuples (i, j, d) where
            # (i, j) is the coordinate of the first letter and d is
            # the direction.
            candidates = []
            for d in directions:
                di, dj = directions[d]
                for i in range(max(0, 0 - len(word) * di),
                               min(height, height - len(word) * di)):
                    for j in range(max(0, 0 - len(word) * dj),
                                   min(width, width - len(word) * dj)):
                        for k, letter in enumerate(word):
                            g = self.grid[i + k * di][j + k * dj]
                            if g != letter and g != EMPTY:
                                break
                        else:
                            candidates.append((i, j, d))
            if candidates:
                i, j, d = random.choice(candidates)
                di, dj = directions[d]
                for k, letter in enumerate(word):
                    if self.grid[i + k * di][j + k * dj] == EMPTY:
                        filled_cells += 1
                        self.grid[i + k * di][j + k * dj] = letter
                self.words.append((word, i, j, d))
                if filled_cells >= target_cells:
                    break
                    
        # Fill in the puzzle replacing all empty cells with randomly generated letters
        random_letters = lambda n: ''.join([random.choice(string.ascii_lowercase) for i in range(n)])
        self.puzzle = self.grid.copy()
        for (i, row) in enumerate(self.grid):
            for (j, cell) in enumerate(row):
                if (self.grid[i][j] == EMPTY):
                    self.puzzle[i][j] = list(random_letters(size * size)).pop()
                    
    def to_html(self):
        # Table format
        wordlist = self.word_list
        arr = np.array(self.puzzle)

        html = [f"<H1>{self.title}: ({self.difficulty})</H1><P>"]
        
        html.append (f"<table>")
        rows, columns = arr.shape
        for i in range(rows):
            html.append(f"<tr>")
            for j in range(columns):
                val = arr[i, j]
                html.append(f"<td>{val}</td>")
            html.append(f"</tr>")
        html.append("</table>")
        html.append (f"<H2>Wordlist</H2>")
        html.append ("<Table>")
        for i in range(10):
            html.append(f"<tr><td>{i+1}</td><td width=125px style=\"text-align:left\">{wordlist[i]}</td><td>{i+11}</td><td width=125px style=\"text-align:left\">{wordlist[i+10]}</td></tr>")
        html.append ("</Table>")
        
        strHtml = "".join(html)
        with open(f"{self.difficulty}.html", "w") as f:
            f.write(strHtml)
        
        return strHtml
        
def make_wordsearch_pack(wordlist, title):   
    ws_easy = WordSearch(wordlist, 15, EASY_DIRECTIONS, title, "Easy")
    ws_medium = WordSearch(wordlist, 15, MEDIUM_DIRECTIONS, title, "Medium")
    ws_hard = WordSearch(wordlist, 20, HARD_DIRECTIONS, title, "Hard")
    
    pack = [ws_easy, ws_medium, ws_hard]
    
    for p in pack:
        p.to_html()
        
    with open("answers.txt", "w") as f:
            f.write("Notes / Answers.\n=======================================\n")
            f.write("Answers shown as word, row, column (starting at 0) and direction.\n\n")
            f.write("Easy puzzle has words vertical and horizontal (left to right, top to bottom).\n\n")
            f.write("Medium puzzle has words vertical and horizontal (forwards and backwards vertical and horizontal).\n\n")
            f.write("Difficult puzzle has words vertical, horizontal and diagonal (forwards and backwards).\n\n")

            f.write("Easy\n")
            f.write(json.dumps(ws_easy.words))
            f.write("\n\nMedium\n")
            f.write(json.dumps(ws_medium.words))
            f.write("\n\nDifficult\n")
            f.write(json.dumps(ws_hard.words))
        
    
    