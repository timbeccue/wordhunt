import random
import statistics 
from collections import Counter

# Load wordhunt boards from file
real_boards = []
with open('wordhunt_boards.txt', 'r') as file:
    for line in file:
        real_boards.append(line.strip())

# generate weights
def compute_letter_frequencies(word_list):
    letter_counts = Counter(char for word in word_list for char in word)
    sorted_letter_counts = dict(sorted(letter_counts.items()))
    # Normalize
    total_letters = sum(len(word) for word in word_list)
    for key in sorted_letter_counts:
        sorted_letter_counts[key] /= total_letters
    return sorted_letter_counts

def get_index_letter_frequencies(word_list, index):
    letter_counts = Counter(word[index] for word in word_list)
    for char in 'abcdefghijklmnopqrstuvwxyz':
        if char not in letter_counts:
            letter_counts[char] = 0
    sorted_letter_counts = dict(sorted(letter_counts.items()))
    # Normalize
    # total_letters = sum(len(word) for word in word_list)
    # for key in sorted_letter_counts:
    #     sorted_letter_counts[key] /= total_letters
    return sorted_letter_counts

def generate_weighted_string(n, char_weights):
    characters, weights = zip(*char_weights.items())
    board = ''.join(random.choices(characters, weights=weights, k=n))
    return board

gamepigeon_weights = compute_letter_frequencies(real_boards)