from collections import Counter
from collections import defaultdict
import pyfiglet
from trie import valid_dict

class Board:
    def __init__(self, letters, trie_dict=valid_dict):

        self.grid_size = int(len(letters) ** 0.5)
        if self.grid_size ** 2 != len(letters):
            print("!! The letters don't form a square grid. Lenght: ", len(letters))

        self.letters = letters
        self.all_words_trie = trie_dict
        self.valid_words = set() 

    def __str__(self): 
        return self._format_board(self.letters)
    
    @staticmethod
    def _format_board(letters):
        dim = int(len(letters) ** 0.5)
        if dim ** 2 != len(letters):
            print(f"Board with length {len(letters)} is not a square.")
            return
        board_string = ''
        for i in range(0, len(letters), dim):
            row = '  '.join(letters[i:i+dim])
            board_string += f"{row}\n"
        return board_string.upper()
    
    @staticmethod
    def _get_board_dimensions(letters):
        dim = int(len(letters) ** 0.5)
        if dim ** 2 != len(letters):
            raise ValueError(f"Board with length {len(letters)} is not a square.")
        return dim

    @staticmethod
    def print_board(letters, font="ntgreek"):
        n = Board._get_board_dimensions(letters)
        grid_string = Board._format_board(letters)
        # print(pyfiglet.figlet_format(grid_string, font=font))
        print(Board._format_board(letters))
                
    def get_letter_neighbors(self):
        """ return a dict of dicts, where dict[c1][c2] gives the number of times char c2 appeared next to c1"""
        alpha = "abcdefghijklmnopqrstuvwxyz"
        letter_neighbors = {char: {char: 0 for char in alpha} for char in alpha}
        for index, char in enumerate(self.letters):
            neighbors_indices = self._get_neighbors_from_char_index(index)
            for i in neighbors_indices:
                letter_neighbors[char][self.letters[i]] += 1
        return letter_neighbors

    def _to_1d_index(self, row, col):
        return (self.grid_size * row) + col


    def _get_neighbors_from_char_index(self, index):
        neighbor_indices = []

        # convert index to 0-indexed row/col
        i, j = divmod(index, self.grid_size)

        # Directions: NSEW + diagonals
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1),    # NSEW
                      (-1, -1), (-1, 1), (1, -1), (1, 1)]  # Diagonals

        for di, dj in directions:
            ni, nj = i + di, j + dj
            # check boundaries
            if 0 <= ni < self.grid_size and 0 <= nj < self.grid_size:
                neighbor_indices.append(self._to_1d_index(ni, nj))

        return neighbor_indices


    def _get_unused_neighbors(self, index, used):
        return [n for n in self._get_neighbors_from_char_index(index) if not used[n]]
        

    def _find_all_valid_words(self):

        def dfs(fragment, prev_char_index, used):
            if len(fragment) >= 3 and self.all_words_trie.search(fragment):
                self.valid_words.add(fragment)
            if not self.all_words_trie.starts_with(fragment):
                return 
            unused_neighbors = self._get_unused_neighbors(prev_char_index, used)
            for char_index in unused_neighbors:
                new_fragment = fragment + self.letters[char_index]
                updated_used_list = used[:]
                updated_used_list[char_index] = 1
                dfs(new_fragment, char_index, updated_used_list)

        # array tracking whether a letter index has been used or not
        used = [0 for char in self.letters]

        # search for wards starting with each character
        for index, char in enumerate(self.letters):
            updated_used = used[:]
            updated_used[index] = 1
            dfs(char, index, updated_used)

        
    def print_valid_words(self):
        if len(self.valid_words) == 0:
            self._find_all_valid_words()
        sorted_strings = sorted(self.valid_words, key=lambda s: (-len(s), s))

        grouped = defaultdict(list)
        for word in self.valid_words:
            grouped[len(word)].append(word)
        
        # Sort by length in descending order and convert to list of lists
        result = [grouped[length] for length in sorted(grouped.keys(), reverse=True)]
      
        # Output the result
        for group in result:
            print(group)
            
        # print(sorted_strings)


    def print_word_lengths(self):
        if len(self.valid_words) == 0:
            self._find_all_valid_words()
        length_counts = Counter(len(word) for word in self.valid_words)
        # Sort by length in descending order
        for length, count in sorted(length_counts.items(), key=lambda x: x[0], reverse=True):
            print(f"Words with {length} characters: {count}")
    

    def print_word_scores(self):
        if len(self.valid_words) == 0:
            self._find_all_valid_words()
        def points(length):
            if length == 3: 
                return 100
            elif length == 4: return 400
            elif length == 5: return 800
            else: return 200 + (400 * (length - 3))
        length_counts = Counter(len(word) for word in self.valid_words)
        # Sort by length in descending order
        for length, count in sorted(length_counts.items(), key=lambda x: x[0], reverse=True):
            print(f"{points(length)}: {count}")
        
    
    def get(self, row, col):
        """ get letter at the 1-indexed row and column """
        if row < 1 or row > 4 or col < 1 or col > 4:
            return -1
        index = (4 * (row - 1)) + (col - 1)
        return self.letters[index]


